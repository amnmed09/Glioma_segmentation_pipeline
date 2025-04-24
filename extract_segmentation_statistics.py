import os
import argparse
import pandas as pd
import nibabel as nib
import numpy as np
import gzip
from scipy.ndimage import zoom

def is_valid_gzip(filepath):
    """Check if a file is a valid gzip file."""
    try:
        with gzip.open(filepath, 'r') as f:
            f.read(1)
        return True
    except OSError:
        return False

def calculate_image_stats(image_path, mask):
    """Load an image and compute mean and std of intensities within the mask."""
    if not os.path.exists(image_path):
        return None, None
    image = nib.load(image_path).get_fdata()
    
    # Resize mask if shape mismatch
    if mask.shape != image.shape:
        zoom_factors = [n / m for n, m in zip(image.shape, mask.shape)]
        mask = zoom(mask, zoom_factors, order=0)
    
    masked_image = image[mask]
    return np.mean(masked_image), np.std(masked_image)

def process_segmentation_files(seg_dir, data_dir, output_dir):
    """Process segmentation masks and extract image statistics."""
    os.makedirs(output_dir, exist_ok=True)
    results = []

    seg_files = sorted(f for f in os.listdir(seg_dir) if f.endswith(".nii.gz"))
    print(f"Found {len(seg_files)} segmentation files.")

    for file_name in seg_files:
        seg_path = os.path.join(seg_dir, file_name)

        if not is_valid_gzip(seg_path):
            print(f"Skipping invalid gzip file: {file_name}")
            continue

        # Extract patient info
        parts = file_name.split("_")
        patient_id = "_".join(parts[0:2])
        timepoint = "_".join(parts[2:4])
        base_name = f"{patient_id}_{timepoint}"

        # Image paths
        modalities = ["t1c", "t1n", "t2f", "t2w"]
        img_paths = {
            m: os.path.join(data_dir, patient_id, timepoint, f"{base_name}_brain_{m}.nii.gz")
            for m in modalities
        }

        if not all(os.path.exists(p) for p in img_paths.values()):
            print(f"Skipping {file_name}: missing modalities.")
            continue

        # Load segmentation mask
        seg_mask = nib.load(seg_path).get_fdata()
        voxel_volume = np.prod(nib.load(seg_path).header.get_zooms())
        unique_labels = np.unique(seg_mask)

        for label_id in unique_labels:
            if label_id == 0:
                continue
            label_mask = (seg_mask == label_id)
            num_voxels = np.sum(label_mask)
            volume = num_voxels * voxel_volume

            stats = {}
            for m in modalities:
                mean, std = calculate_image_stats(img_paths[m], label_mask)
                stats[f"Image mean (brain_{m})"] = mean
                stats[f"Image stdev (brain_{m})"] = std

            results.append({
                "Patient ID": patient_id,
                "Label Id": label_id,
                "Label Name": f"Label {label_id}",
                "Number Of Voxels": num_voxels,
                "Volume (mm^3)": volume,
                **stats
            })

        print(f"Processed {file_name}")

    # Save to CSV
    df = pd.DataFrame(results)
    output_file = os.path.join(output_dir, "segmentation_statistics.csv")
    df.to_csv(output_file, index=False)
    print(f"\n✅ Successfully completed. Results saved to: {output_file}")

def main():
    parser = argparse.ArgumentParser(description="Extract statistics from brain tumor segmentation masks and imaging modalities.")
    parser.add_argument("--seg_dir", required=True, help="Path to the directory containing segmentation files (.nii.gz).")
    parser.add_argument("--data_dir", required=True, help="Path to the root directory of patient imaging data.")
    parser.add_argument("--output_dir", required=True, help="Path to the output directory to save results.")
    args = parser.parse_args()

    process_segmentation_files(args.seg_dir, args.data_dir, args.output_dir)

if __name__ == "__main__":
    main()
