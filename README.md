# **NRSC_Bhoonidhi**

These scripts are designed to automate the process of creating basic metadata for Cartosat imagery downloaded from the Bhoonidhi portal. They also handle the extraction of image footprints from ZIP files and renaming the extracted files. Additionally, the repository includes scripts that convert the downloaded images into 8-bit format.....

## **Requirements**

This project requires the following Python libraries:

  **rasterio:** For reading and writing geospatial raster data.
  
  **GDAL:** For working with geospatial data formats, accessible through the osgeo package.
  
  **numpy:** For numerical computing.

Please refer to the requirements.txt file for the full list of dependencies.

### **Installation Instructions**

To install the required libraries, simply run the following command:

```pip install -r requirements.txt```

## **How to run the scripts**
**To get help on any script, use the following command:**

``` python MetaDataCSV_Footprints.py --help```

For example, to get help on the MetaDataCSV_Footprints.py script, run:

```python MetaDataCSV_Footprints.py --help```
  
## **Deatils of Scripts**

### MetaDataCSV_Footprints.py

Extracts metadata from a ZIP file containing BAND_META.txt and generates a CSV file with the metadata extracted from all ZIP files in the specified directory.

### Extract_FootPrint_From_Cartosat_ZipFiles.py

Processes ZIP files in the specified directory, extracts specific files (.shp, .shx, .dbf, .prj), renames them, and saves them in the same directory.

### Corrupted_ZipFile_Finder.py
Helps in finding corrupted ZIP files within a specified directory.

### internal_pyramid_layers.py

Builds overviews (pyramids) for the input TIFF file using block-wise processing. Compresses the overviews with LZW compression.

### internal_pyramid_layers_recursive.py

Builds overviews (pyramids) for the input TIFF files in a folder recursively using block-wise processing. Compresses the overviews with LZW compression.

### convert_to_8bit.py

Converts a multi-band/Panchromatic GeoTIFF image to 8-bit format.

### convert_to_8bit_recursive.py

Converts image files in a folder recursively to 8-bit format.

### Remove_4thband.py

Remove the 4th band from raster (.tif) files in a directory.

### find_files_by_extension_in_root.py

Find files by extension in a root directory



## **Acknowledgements**

If you use this repository or any part of the scripts in your work, please acknowledge the contributions. Attribution is appreciated.

## **Disclaimer**

This code is provided "as is" without any warranties or guarantees regarding its correctness. Use at your own risk.


