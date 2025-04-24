# 🧠 Glioma Imaging Data Processing Toolkit

This repository contains a collection of Python scripts designed to assist with preprocessing, segmentation, and radiomics analysis of glioma MRI datasets. The tools are general-purpose and modular, suitable for research pipelines involving AI, clinical analysis, and radiogenomics.

---

## 📁 Project Structure

```
glioma-imaging-toolkit/
│
├── run_fets_preprocessing.py           # Run FeTS preprocessing pipeline on raw data
├── extract_segmentation_volumes.py     # Extract tumor volumes and stats from segmentation labels
├── combine_csv_with_patient_ids.py     # Merge patient-level CSVs into one Excel file
├── extract_segmentation_statistics.py  # Analyze segmentation masks across modalities
├── run_radiomics_extraction.py         # Batch radiomics extraction using CaPTk
├── requirements.txt                    # Python package dependencies
├── README.md
└── example_data/                       # Optional test data or sample structure
```

---

## 📜 Script Overview

---

### 1. `run_fets_preprocessing.py`

**Purpose:**  
Automates preprocessing of multimodal brain MRIs using the official [FeTS pipeline](https://fets-ai.github.io/Front-End/process_data). It skull-strips, registers, and resamples MR images.

**Usage:**

```bash
python run_fets_preprocessing.py \
  --input_dir ./input \
  --output_dir ./output
```

**Arguments:**
- `--input_dir`: Folder containing raw MRI sequences (T1, T1CE, T2, FLAIR) per patient
- `--output_dir`: Folder to save preprocessed images
- `--patients` *(optional)*: List of patient folders to process (default: all)

> ⚠️ FeTS CLI or Docker setup is required. Follow the official docs:  
> https://fets-ai.github.io/Front-End/process_data

---

### 2. `extract_segmentation_volumes.py`

**Purpose:**  
Computes volume (mm³), voxel counts, and intensity statistics (mean, std) per tumor label using segmentation masks and co-registered MRI modalities (FLAIR, T1, T1CE, T2).

**Usage:**

```bash
python extract_segmentation_volumes.py \
  --seg_dir ./segmentations \
  --data_dir ./preprocessed_mri \
  --output_dir ./seg_volume_output
```

**Arguments:**
- `--seg_dir`: Directory with `.nii.gz` segmentation files
- `--data_dir`: Directory with patient MRI folders
- `--output_dir`: Output folder for saving CSV

**Output:**  
`segmentation_data_output.csv` in the output folder

---

### 3. `combine_csv_with_patient_ids.py`

**Purpose:**  
Merges multiple CSV files (e.g., one per patient) into a single Excel file, appending a `PatientID` from the filename.

**Usage:**

```bash
python combine_csv_with_patient_ids.py
```

**Behavior:**  
Looks for files like `Patient_0001.csv`, `Patient_0002.csv`, etc., in the current directory and outputs an Excel file named `combined_output.xlsx`.

---

### 4. `extract_segmentation_statistics.py`

**Purpose:**  
Extracts statistics for tumor segmentations across four modalities (T1C, T1N, T2F, T2W). For each label, it calculates volume and intensity-based features.

**Usage:**

```bash
python extract_segmentation_statistics.py \
  --seg_dir ./segmentations \
  --data_dir ./patient_data \
  --output_dir ./results
```

**Arguments:**
- `--seg_dir`: Folder with segmentation NIfTI files
- `--data_dir`: Folder with co-registered MRI modalities
- `--output_dir`: Folder to save the combined results

**Output:**  
`segmentation_statistics.csv` in the output folder

---

### 5. `run_radiomics_extraction.py`

**Purpose:**  
Batch-processing tool for running CaPTk’s `FeatureExtraction` on multimodal MRIs with tumor masks, generating radiomics feature tables per patient.

**Usage:**

```bash
python run_radiomics_extraction.py \
  --captk_dir /path/to/CaPTk \
  --params_file ./params.csv \
  --data_dir ./DataForFeTS \
  --mask_dir ./labels \
  --output_dir ./radiomics_output \
  --start_id 3 \
  --end_id 275
```

**Arguments:**
- `--captk_dir`: CaPTk installation path
- `--params_file`: Feature extraction parameters CSV
- `--data_dir`: Patient imaging data folder
- `--mask_dir`: Segmentation masks
- `--output_dir`: Output folder for features
- `--start_id`, `--end_id`: Patient ID range
- `--timepoints`: Number of timepoints (default: 6)

> ⚠️ Requires CaPTk (Windows/Linux only): https://www.cbica.upenn.edu/sbia/software/CaPTk/

---

## ⚙️ Dependencies

Install all required Python packages using:

```bash
pip install -r requirements.txt
```

**Example `requirements.txt`:**

```
pandas
nibabel
numpy
tqdm
scipy
SimpleITK
```

---

## 📂 Example Data Layout

```
DataForFeTS/
└── PatientID_0001/
    └── Timepoint_1/
        ├── PatientID_0001_Timepoint_1_brain_t1c.nii.gz
        ├── PatientID_0001_Timepoint_1_brain_t1n.nii.gz
        ├── PatientID_0001_Timepoint_1_brain_t2w.nii.gz
        └── PatientID_0001_Timepoint_1_brain_t2f.nii.gz

segmentations/
└── PatientID_0001_Timepoint_1_seg_label_1.nii.gz
```

---

## 🧪 Contributing

We welcome contributions! Feel free to open issues or submit pull requests for improvements, bug fixes, or new utilities.

---

## 📄 License

This project is licensed under the MIT License.

---
