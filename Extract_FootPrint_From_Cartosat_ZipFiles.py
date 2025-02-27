import os
import shutil
import zipfile
import argparse

def copy_and_rename_files(zip_path, Sensor_ABR, Order_ID):
    """
    This function processes zip files in the specified directory, extracts specific files
    (.shp, .shx, .dbf, .prj), renames them, and saves them in the same directory.

    Args:
    zip_path (str): Path to the directory containing ZIP files.
    Sensor_ABR (str): Sensor ID (e.g., C3, C2E, C2F).
    Order_ID (str): Order ID for naming convention.
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
    Main function to parse command line arguments and call the copy_and_rename_files function.
    """
    # Set up argument parsing
    parser = argparse.ArgumentParser(description="Extract and rename specific files from zip archives in a directory.")
    
    # Command-line arguments
    parser.add_argument("zip_path", help="The path to the directory containing ZIP files.")
    parser.add_argument("Sensor_ABR", help="Sensor ID (e.g., C3, C2E, C2F).")
    parser.add_argument("Order_ID", help="Order ID to be used in file naming.")

    # Parse the command line arguments
    args = parser.parse_args()

    # Call the function with the provided arguments
    copy_and_rename_files(args.zip_path, args.Sensor_ABR, args.Order_ID)

if __name__ == "__main__":
    # Call the main function to execute the script
    main()
