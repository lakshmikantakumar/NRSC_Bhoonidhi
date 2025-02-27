import os
import warnings
import argparse
from osgeo import gdal

def convert_to_bigtiff(input_tif, output_tif):
    """
    Convert the input TIFF file to a BigTIFF format with DEFLATE compression.
    """
    options = ['COMPRESS=DEFLATE', 'BIGTIFF=YES']
    gdal.Translate(output_tif, input_tif, creationOptions=options)

def build_overviews(input_tif):
    """
    Build overviews (pyramids) for the input TIFF file using NEAREST resampling.
    Compresses the overviews with LZW compression.
    """
    gdal.SetConfigOption('COMPRESS_OVERVIEW', 'lzw')
    # gdal.SetConfigOption('PHOTOMETRIC_OVERVIEW', 'YCBCR')  # Uncomment if needed

    ds = gdal.Open(input_tif, gdal.GA_Update)
    if ds is not None:
        # Building overviews with scales 2, 4, 8, ..., 1024
        ds.BuildOverviews('NEAREST', [2, 4, 8, 16, 32, 64, 128, 256, 512, 1024])
        del ds  # Close dataset after processing

def process_single_tif_file(tif_file):
    """
    Process a single TIFF file: convert to BigTIFF and build overviews.
    """
    print(f"Processing {tif_file}...")
    output_file = os.path.splitext(tif_file)[0] + '_InterPyrd.tif'
    convert_to_bigtiff(tif_file, output_file)
    build_overviews(output_file)
    # os.remove(output_file)  # Uncomment to remove temporary processed file after building overviews

def main():
    """
    Main function to handle command-line arguments and initiate processing.
    """
    # Suppress FutureWarning about GDAL exceptions not being explicitly set
    warnings.filterwarnings("ignore", category=FutureWarning)

    # Create argument parser
    parser = argparse.ArgumentParser(description="Process a TIFF file: convert to BigTIFF and build overviews.")

    # Define the command-line argument for input TIFF file
    parser.add_argument('input_file', metavar='INPUT_FILE', type=str, 
                        help="Path to the input TIFF file to process")

    # Parse the command-line arguments
    args = parser.parse_args()

    # Check if the input file exists
    if not os.path.exists(args.input_file):
        print(f"Error: The file '{args.input_file}' does not exist.")
    else:
        # Process the provided TIFF file
        process_single_tif_file(args.input_file)
        print("Processing completed.")

if __name__ == "__main__":
    # Run the main function if this script is executed
    main()
