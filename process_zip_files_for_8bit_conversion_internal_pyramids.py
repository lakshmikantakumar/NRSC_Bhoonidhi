import zipfile
import os
import tempfile
import argparse
from find_files_by_extension_in_root import find_files_by_extension
from convert_to_8bit import convert_to_8bit
from internal_pyramid_layers import internal_pyramids

def process_zip_files(input_dir, output_dir, recursive=True):
    """
    Processes all ZIP files in the input directory (and subdirectories if recursive is True),
    extracts TIFF files, converts them to 8-bit, and generates internal pyramids for each.
    
    :param input_dir: Directory containing ZIP files to process.
    :param output_dir: Directory where processed TIFF files (8-bit and pyramids) are saved.
    :param recursive: Whether to search recursively for ZIP files in subdirectories.
    """
    # Find all ZIP files in the input directory (including subdirectories if recursive=True)
    zip_files = find_files_by_extension(input_dir, '.zip', recursive=recursive)
    
    for zip_file in zip_files:
        # Check if the ZIP file is corrupted using testzip()
        try:
            with zipfile.ZipFile(zip_file, 'r') as zip_ref:
                if zip_ref.testzip() is not None:
                    print(f"Warning: {zip_file} is corrupted, skipping it.")
                    continue  # Skip the corrupted ZIP file and move to the next one
        except zipfile.BadZipFile:
            print(f"Error: {zip_file} is not a valid ZIP file, skipping it.")
            continue  # Skip if the ZIP file is not valid
        
        # If the ZIP file is valid, process it
        print(f"Processing ZIP file: {zip_file}")
        
        # Extract all .tif files from the ZIP archive
        with zipfile.ZipFile(zip_file, 'r') as zip_ref:
            tif_files = [f for f in zip_ref.namelist() if f.endswith('.tif')]
            
            for tif_file in tif_files:
                print(f"  Processing TIFF file: {tif_file}")
                
                # Create a temporary directory to extract the current TIFF file
                with tempfile.TemporaryDirectory() as temp_dir:
                    zip_ref.extract(tif_file, temp_dir)
                    tif_path = os.path.join(temp_dir, tif_file)
                    
                    # 1. Convert the .tif file to 8-bit
                    # Construct the output file path: 'output_dir/ZIPName_TIFName_8bit.tif'
                    #zip_name = os.path.splitext(os.path.basename(zip_file))[0]  # Get the name of the ZIP file without extension              
                    #tif_name = os.path.splitext(tif_file)[0]  # Get the name of the TIFF file without extension
                    # Replace '/' with '_' in tif_file to ensure valid file names
                    tif_name = os.path.splitext(tif_file.replace('/', '_'))[0]  # Replace '/' with '_'
                    output_8bit = os.path.join(output_dir, f"{tif_name}_8bit.tif")
                    
                    # Ensure the output directory exists
                    os.makedirs(output_dir, exist_ok=True)
                    
                    
                    convert_to_8bit(tif_path, output_8bit)
                    #print(f"    Converted to 8-bit: {output_8bit}")
                    
                    # 2. Generate internal pyramids for the 8-bit TIFF file
                    internal_pyramids(output_8bit)
                    print(f"    Generated internal pyramids for: {output_8bit}")
                    
                    # 3. Delete the 8-bit file after pyramids are generated
                    os.remove(output_8bit)
                    #print(f"    Deleted 8-bit file: {output_8bit}")

def main():
    """
    Main function to handle command-line arguments and initiate processing of ZIP files.
    """
    # Setting up the command-line argument parser
    parser = argparse.ArgumentParser(description="Process ZIP files containing TIFF images.")
    
    # Add arguments for input and output directories
    parser.add_argument(
        'input_directory', 
        type=str, 
        help="The directory containing ZIP files to process."
    )
    parser.add_argument(
        'output_directory', 
        type=str, 
        help="The directory where processed TIFF files (8-bit and pyramids) will be saved."
    )
    
    # Add argument for recursive option
    parser.add_argument(
        '--recursive', 
        action='store_true', 
        default=True, 
        help="Whether to search recursively in subdirectories for ZIP files (default: True)."
    )
    
    # Parse the arguments
    args = parser.parse_args()
    
    # Ensure the output directory exists
    os.makedirs(args.output_directory, exist_ok=True)
    
    # Start processing the ZIP files
    process_zip_files(args.input_directory, args.output_directory, recursive=args.recursive)

if __name__ == "__main__":
    main()
