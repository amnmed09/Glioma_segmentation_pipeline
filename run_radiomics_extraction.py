import os
import subprocess
import argparse

def build_image_paths(data_dir, patient_id_str, timepoint_str):
    """Construct paths to required imaging modalities."""
    return {
        "T1": os.path.join(data_dir, patient_id_str, timepoint_str, f"{patient_id_str}_{timepoint_str}_brain_t1c.nii.gz"),
        "T2": os.path.join(data_dir, patient_id_str, timepoint_str, f"{patient_id_str}_{timepoint_str}_brain_t1n.nii.gz"),
        "FL": os.path.join(data_dir, patient_id_str, timepoint_str, f"{patient_id_str}_{timepoint_str}_brain_t2w.nii.gz"),
        "T1CE": os.path.join(data_dir, patient_id_str, timepoint_str, f"{patient_id_str}_{timepoint_str}_brain_t2f.nii.gz"),
    }

def get_mask_files(mask_dir, patient_id_str, timepoint_str):
    """Finds segmentation masks for the given patient and timepoint."""
    return [
        os.path.join(mask_dir, f)
        for f in os.listdir(mask_dir)
        if f.startswith(f"{patient_id_str}_{timepoint_str}_") and f.endswith(".nii.gz")
    ]

def run_feature_extraction(CaPTk_dir, params_file, images, masks, output_csv, patient_id_str):
    """Run CaPTk's FeatureExtraction.exe with specified parameters."""
    command = [
        os.path.join(CaPTk_dir, "bin", "FeatureExtraction.exe"),
        "-p", params_file,
        "-n", patient_id_str,
        "-i", ",".join(images.values()),
        "-t", ",".join(images.keys()),
        "-m", ",".join(masks),
        "-r", "1",
        "-l", "TT",
        "-vc", "1",
        "-o", output_csv
    ]
    print("Running command:", " ".join(command))
    subprocess.run(command)

def main(args):
    os.makedirs(args.output_dir, exist_ok=True)

    for pid in range(args.start_id, args.end_id + 1):
        patient_id_str = f"{args.patient_prefix}{str(pid).zfill(4)}"

        for t in range(1, args.timepoints + 1):
            timepoint_str = f"Timepoint_{t}"
            output_csv = os.path.join(args.output_dir, f"output_{patient_id_str}_{timepoint_str}.csv")
            
            images = build_image_paths(args.data_dir, patient_id_str, timepoint_str)
            if not all(os.path.exists(img) for img in images.values()):
                print(f"Skipping {patient_id_str} {timepoint_str}: missing images.")
                continue

            masks = get_mask_files(args.mask_dir, patient_id_str, timepoint_str)
            if not masks:
                print(f"Skipping {patient_id_str} {timepoint_str}: no mask files found.")
                continue

            run_feature_extraction(args.captk_dir, args.params_file, images, masks, output_csv, patient_id_str)

    print("\n✅ Processing completed successfully.")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Batch CaPTk radiomics feature extraction tool.")
    parser.add_argument("--captk_dir", required=True, help="Path to CaPTk installation directory.")
    parser.add_argument("--params_file", required=True, help="Path to parameter CSV file.")
    parser.add_argument("--data_dir", required=True, help="Root directory containing patient imaging data.")
    parser.add_argument("--mask_dir", required=True, help="Directory containing segmentation mask files.")
    parser.add_argument("--output_dir", required=True, help="Directory to save output CSVs.")
    parser.add_argument("--patient_prefix", default="PatientID_", help="Prefix used for patient IDs.")
    parser.add_argument("--start_id", type=int, default=3, help="Start of patient ID range (inclusive).")
    parser.add_argument("--end_id", type=int, default=275, help="End of patient ID range (inclusive).")
    parser.add_argument("--timepoints", type=int, default=6, help="Number of timepoints per patient.")
    
    args = parser.parse_args()
    main(args)
