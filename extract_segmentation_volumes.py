"""
extract_segmentation_volumes.py

Extracts volumetric and intensity statistics from segmentation masks and 
corresponding MRI sequences (FLAIR, T1, T1CE, T2) for each patient.

"""

import os
import argparse
import pandas as pd
import nibabel as nib
import numpy as np

def calculate_image_stats(image_path, mask):
    """Calculate mean and standard deviation of image voxels within a mask."""
    if not os.path.exists(image_path):
        return None, None
    image = nib.load(image_path).get_fdata()
    masked_image = image[mask]
    return np.mean(masked_image), np.std(masked_image)

def process_segmentations(seg_dir, data_dir, output_dir):
    os.makedirs(output_dir, exist_ok=True)

    results = []

    for file_name in os.listdir(seg_dir):
        if not file_name.endswith(".nii.gz"):
            continue

        file_path = os.path.join(seg_dir, file_name)
        patient_id = "_".join(file_name.split("_")[0:2])

        # Define image paths
        modalities = {
            "flair": os.path.join(data_dir, patient_id, f"{patient_id}_brain_flair.nii.gz"),
            "t1": os.path.join(data_dir, patient_id, f"{patient_id}_brain_t1.nii.gz"),
            "t1ce": os.path.join(data_dir, patient_id, f"{patient_id}_brain_t1ce.nii.gz"),
            "t2": os.path.join(data_dir, patient_id, f"{patient_id}_brain_t2.nii.gz"),
        }

        if not all(os.path.exists(p) for p in modalities.values()):
            print(f"Skipping {patient_id}: missing MRI sequences.")
            continue

        seg_mask = nib.load(file_path).get_fdata()
        voxel_volume = np.prod(nib.load(file_path).header.get_zooms())

        for label_id in np.unique(seg_mask):
            if label_id == 0:
                continue

            label_mask = seg_mask == label_id
            num_voxels = np.sum(label_mask)
            volume = num_voxels * voxel_volume

            stats = {}
            for name, path in modalities.items():
                mean, std = calculate_image_stats(path, label_mask)
                stats[f"Image mean (brain_{name})"] = mean
                stats[f"Image stdev (brain_{name})"] = std

            results.append({
                "Patient ID": patient_id,
                "Label Id": label_id,
                "Label Name": f"Label {label_id}",
                "Number Of Voxels": num_voxels,
                "Volume (mm^3)": volume,
                **stats
            })

        print(f"Processed {file_name}")

    df = pd.DataFrame(results)
    output_csv = os.path.join(output_dir, "segmentation_data_output.csv")
    df.to_csv(output_csv, index=False)
    print(f"✅ Successfully completed. Data saved to {output_csv}")

def main():
    parser = argparse.ArgumentParser(description="Extract segmentation volumes and image statistics per label.")
    parser.add_argument("--seg_dir", required=True, help="Path to the segmentation NIfTI files.")
    parser.add_argument("--data_dir", required=True, help="Path to the patient imaging data directory.")
    parser.add_argument("--output_dir", required=True, help="Directory to save the output CSV file.")
    args = parser.parse_args()

    process_segmentations(args.seg_dir, args.data_dir, args.output_dir)

if __name__ == "__main__":
    main()
