import os
import csv
import zipfile
import shutil
import argparse

def extract_metadata_from_zip(zip_file):
    """
    Extract metadata from a ZIP file containing BAND_META.txt.

    Args:
    zip_file (str): Path to the zip file.

    Returns:
    dict: Metadata extracted from the BAND_META.txt file.
    """
    metadata = {}
    with zipfile.ZipFile(zip_file, 'r') as zip_ref:
        # Iterate through the files in the zip file
        for file_name in zip_ref.namelist():
            if file_name.endswith('BAND_META.txt'):
                # Open the metadata file and extract key-value pairs
                with zip_ref.open(file_name, 'r') as meta_file:
                    for line in meta_file:
                        line = line.decode('utf-8').strip()
                        key, value = line.split('=')
                        metadata[key.strip()] = value.strip()
    return metadata

def maincsv(zip_path, month_download, Order_ID):
    """
    Generate a CSV file with metadata extracted from all zip files in the specified directory.

    Args:
    zip_path (str): Path to the directory containing zip files.
    month_download (str): Month the data was downloaded.
    Order_ID (str): The Order ID to be included in the CSV.
    """
    folder_path = zip_path  # Directory containing the zip files
    csv_file_path = os.path.join(folder_path, '%s_metadata.csv' % Order_ID)  # Path to save the CSV file

    # Open CSV file for writing
    with open(csv_file_path, 'w', newline='') as csvfile:
        fieldnames = ['Zipfile', 'Order_ID', 'Month_Download', 'SatID', 'Sensor', 'ProductID', 'MapProjection', 'ZoneNumber', 'Datum', 'ProcessingLevel', 'DateOfPass', 'Resolution', 'SceneCenterLat', 'SceneCenterLon']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()

        # Process each zip file in the directory
        for zip_file in os.listdir(folder_path):
            if zip_file.endswith('.zip'):
                zip_file_path = os.path.join(folder_path, zip_file)
                metadata = extract_metadata_from_zip(zip_file_path)
                writer.writerow({
                    'Zipfile': zip_file,
                    'Order_ID': Order_ID,
                    'Month_Download': month_download,
                    'SatID': metadata.get('SatID', ''),
                    'Sensor': metadata.get('Sensor', ''),
                    'ProductID': metadata.get('ProductID', ''),
                    'MapProjection': metadata.get('MapProjection', ''),
                    'ZoneNumber': metadata.get('ZoneNumber', ''),
                    'Datum': metadata.get('Datum', ''),
                    'ProcessingLevel': metadata.get('ProcessingLevel'),
                    'DateOfPass': metadata.get('DateOfPass', ''),
                    'Resolution': metadata.get('InputResolutionAlong', ''),
                    'SceneCenterLat': metadata.get('SceneCenterLat', ''),
                    'SceneCenterLon': metadata.get('SceneCenterLon', '')
                })

def copy_and_rename_files(zip_path, Sensor_ABR, Order_ID):
    """
    Copy and rename specific files (.shp, .shx, .dbf, .prj) from zip files in the specified directory.

    Args:
    zip_path (str): Path to the directory containing zip files.
    Sensor_ABR (str): Sensor ID (e.g., C3, C2E, C2F).
    Order_ID (str): The Order ID used in the file naming.
    """
    # Get list of zip files in the specified directory
    zip_files = [file for file in os.listdir(zip_path) if file.endswith('.zip')]

    # Iterate over each zip file
    for zip_file in zip_files:
        # Open the zip file
        with zipfile.ZipFile(os.path.join(zip_path, zip_file), 'r') as zip_ref:
            # Extract .shp, .shx, .dbf, and .prj files from the zip file
            for file_info in zip_ref.infolist():
                # Extract only the files with the specified extensions
                if file_info.filename.endswith(('.shp', '.shx', '.dbf', '.prj')):
                    # Read the file contents
                    with zip_ref.open(file_info.filename) as file:
                        # Construct new file name by appending the zip file name
                        new_file_name = os.path.splitext(Sensor_ABR + '_' + str(Order_ID) + '_' + os.path.basename(file_info.filename))[0] + '_' + os.path.splitext(zip_file)[0] + os.path.splitext(file_info.filename)[1]

                        # Copy and rename the file contents
                        with open(os.path.join(zip_path, new_file_name), 'wb') as new_file:
                            shutil.copyfileobj(file, new_file)
                        print(f"Copied and renamed '{file_info.filename}' to '{new_file_name}'")

def main():
    """
    Main function to handle command-line arguments and execute the necessary functions.
    """
    # Set up argument parsing
    parser = argparse.ArgumentParser(description="Extract metadata and files from ZIP archives in a directory.")

    # Command-line arguments
    parser.add_argument("zip_path", help="The path to the directory containing ZIP files.")
    parser.add_argument("month_download", help="Month the data was downloaded (e.g., May-2024).")
    parser.add_argument("Order_ID", help="Order ID to be included in file and CSV naming.")
    parser.add_argument("Sensor_ABR", help="Sensor ID (e.g., C3, C2E, C2F).")

    # Parse the command-line arguments
    args = parser.parse_args()

    # Generate metadata CSV
    maincsv(args.zip_path, args.month_download, args.Order_ID)

    # Copy and rename files
    copy_and_rename_files(args.zip_path, args.Sensor_ABR, args.Order_ID)

if __name__ == "__main__":
    # Execute the main function
    main()
