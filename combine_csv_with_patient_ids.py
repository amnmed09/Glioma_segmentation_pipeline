import os
import pandas as pd
from tqdm import tqdm

def collect_csv_files(directory='.', prefix='Patient', extension='.csv'):
    """
    Collects and returns a sorted list of CSV files from the specified directory
    matching the given prefix and extension.
    """
    files = [file for file in os.listdir(directory)
             if file.startswith(prefix) and file.endswith(extension)]
    return sorted(files)

def process_csv_files(csv_files, directory='.'):
    """
    Reads each CSV file, adds a 'PatientID' column (extracted from filename),
    and returns a combined DataFrame.
    """
    dfs = []
    for file in tqdm(csv_files, desc="Processing CSV files", unit="file"):
        path = os.path.join(directory, file)
        try:
            df = pd.read_csv(path)
            patient_id = os.path.splitext(file)[0].split("_")[1]  # Extract PatientID from filename
            df.insert(0, "PatientID", patient_id)
            dfs.append(df)
        except Exception as e:
            print(f"Error processing {file}: {e}")
    return pd.concat(dfs, ignore_index=True) if dfs else pd.DataFrame()

def save_to_excel(dataframe, output_path="combined_output.xlsx", sheet_name="combined_data"):
    """
    Saves the provided DataFrame to an Excel file.
    """
    try:
        with pd.ExcelWriter(output_path) as writer:
            dataframe.to_excel(writer, index=False, sheet_name=sheet_name)
        print(f"Data successfully saved to {output_path}")
    except Exception as e:
        print(f"Failed to save Excel file: {e}")

def main():
    input_directory = '.'  # Change this to the path containing your CSV files
    output_file = 'combined_output.xlsx'

    csv_files = collect_csv_files(input_directory)
    if not csv_files:
        print("No matching CSV files found.")
        return

    combined_data = process_csv_files(csv_files, input_directory)
    if not combined_data.empty:
        save_to_excel(combined_data, output_path=output_file)
    else:
        print("No data to save.")

if __name__ == "__main__":
    main()
