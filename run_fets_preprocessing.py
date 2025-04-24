"""
run_fets_preprocessing.py

This script provides a basic template to batch preprocess brain MRI data using the
FeTS (Federated Tumor Segmentation) pipeline.

FeTS documentation and official instructions:
🔗 https://fets-ai.github.io/Front-End/process_data

Make sure FeTS is correctly installed (via Docker or pip) and available in your system path.

"""
# Here is an example script

import os
import argparse
import subprocess

def preprocess_patient(input_dir, output_dir, patient_id):
    """
    Preprocess a single patient's data using FeTS.

    Args:
        input_dir (str): Path to input directory with patient subfolders
        output_dir (str): Path to output directory
        patient_id (str): Folder name for the patient (e.g., PatientID_0001)
    """
    patient_input_path = os.path.join(input_dir, patient_id)
    patient_output_path = os.path.join(output_dir, patient_id)

    if not os.path.isdir(patient_input_path):
        print(f"Skipping {patient_id}: input folder not found.")
        return

    os.makedirs(patient_output_path, exist_ok=True)

    print(f"Processing {patient_id}...")

    # Example: Use FeTS CLI or Docker command (adjust if needed)
    command = [
        "fets_preprocess",
        "--inputPath", patient_input_path,
        "--outputPath", patient_output_path
    ]

    try:
        subprocess.run(command, check=True)
    except subprocess.CalledProcessError as e:
        print(f"Error processing {patient_id}: {e}")

def main():
    parser = argparse.ArgumentParser(
        description="Batch preprocessing of brain MRI data using FeTS. "
                    "Refer to official documentation: https://fets-ai.github.io/Front-End/process_data"
    )
    parser.add_argument("--input_dir", required=True, help="Directory containing raw patient MRI folders.")
    parser.add_argument("--output_dir", required=True, help="Directory to save preprocessed data.")
    parser.add_argument("--patients", nargs='*', help="Optional list of patient folder names. If not set, all folders in input_dir will be used.")

    args = parser.parse_args()

    patient_ids = args.patients if args.patients else sorted(os.listdir(args.input_dir))

    for patient_id in patient_ids:
        preprocess_patient(args.input_dir, args.output_dir, patient_id)

    print("✅ Preprocessing complete.")

if __name__ == "__main__":
    main()
