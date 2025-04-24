

## 🧠 Glioma Imaging Data Processing Toolkit

This repository contains a set of Python scripts designed to assist with preprocessing, analyzing, and extracting radiomics features from glioma imaging datasets. The tools are modular, general-purpose, and suitable for integration into AI research pipelines and clinical imaging projects.

---

### 📁 Project Structure

```
glioma-imaging-toolkit/
│
├── combine_csv_with_patient_ids.py
├── extract_segmentation_statistics.py
├── run_radiomics_extraction.py
├── README.md
├── requirements.txt 
└── example_data/
```

---

## 📜 Scripts Overview

### 1. `combine_csv_with_patient_ids.py`
**Purpose:**  
Combines multiple CSV files (e.g., one per patient) into a single Excel file, while tagging each row with a `PatientID` extracted from the filename.

**Usage:**
```bash
python combine_csv_with_patient_ids.py
```

By default, it looks for files named like `Patient_0001.csv`, `Patient_0002.csv`, etc., in the current directory and outputs an Excel file named `combined_output.xlsx`.

---

### 2. `extract_segmentation_statistics.py`
**Purpose:**  
Extracts statistical metrics from tumor segmentation masks and corresponding MRI sequences. Calculates voxel counts, volumes, and mean/std signal intensities per tumor label.

**Command-line usage:**
```bash
python extract_segmentation_statistics.py \
  --seg_dir ./segmentations \
  --data_dir ./patient_data \
  --output_dir ./results
```

**Parameters:**
- `--seg_dir`: Folder with `.nii.gz` segmentation masks
- `--data_dir`: Root folder of patient image data
- `--output_dir`: Destination for the output CSV

**Output:** A file named `segmentation_statistics.csv` in the output directory.

---

### 3. `run_radiomics_extraction.py`
**Purpose:**  
Batch-process patients using CaPTk's FeatureExtraction tool to generate radiomics features across different brain MRI modalities and tumor masks.

**Command-line usage:**
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

**Parameters:**
- `--captk_dir`: Path to your CaPTk installation
- `--params_file`: CSV config for CaPTk
- `--data_dir`: Imaging data directory (organized by PatientID & Timepoint)
- `--mask_dir`: Directory with segmentation mask files
- `--output_dir`: Where to store results
- `--start_id`, `--end_id`: Range of patient IDs
- `--timepoints`: Timepoints per patient (default: 6)

---

## ⚙️ Dependencies

Install required Python packages with:

```bash
pip install -r requirements.txt
```

Example `requirements.txt`:
```
pandas
nibabel
numpy
tqdm
scipy
```

> **Note:** `run_radiomics_extraction.py` requires a working installation of [CaPTk](https://www.cbica.upenn.edu/sbia/software/CaPTk/) and is OS-specific (typically Windows/Linux).

---

## 📂 Example Directory Structure

```
DataForFeTS/
└── PatientID_0001/
    └── Timepoint_1/
        ├── PatientID_0001_Timepoint_1_brain_t1c.nii.gz
        ├── PatientID_0001_Timepoint_1_brain_t1n.nii.gz
        ├── PatientID_0001_Timepoint_1_brain_t2w.nii.gz
        └── PatientID_0001_Timepoint_1_brain_t2f.nii.gz

labels/
└── PatientID_0001_Timepoint_1_seg_label_1.nii.gz
```

---

## 🧪 Contributing

Feel free to open issues or submit pull requests if you find bugs, have suggestions, or want to contribute new tools to this toolkit.

---

## 📄 License

This project is open-source and available under the MIT License.


