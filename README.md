# DataPort-Examples
A collection of examples of how to use Pecan Street Inc. Data.

https://dataport.pecanstreet.org/

## Requirements
- Python 3
- A DataPort account

## Installation / Setup
### Python Modules
The requirements.txt file has the Python modules needed for these examples.
If you are using pip then issue the command:

`pip3 install -r requirements.txt`

### Database Credentials
If you have direct database access, you'll need to enter the connection parameters and authentication credentials
into the config/config.txt file. You can find the necessary info at https://dataport.pecanstreet.org/access . 

### Flat File Download
If you are a university free account, the data can be found on this page:
https://dataport.pecanstreet.org/academic
In particular the flat_file/read_csv.py example uses the `Austin 15-min (22.4 MB)` download.

## Examples
The examples directory has subdirectories containing Python 3 scripts for reading the csv
flat files downloaded from the DataPort portal as well as loading data by connecting to the 
DataPort Postgres database directly. 

### examples/flat_file
The flat_file directory has an example that uses the flat csv files downloaded from the DataPort portal.
To run this example, download the 15 minute Austin bundle, then untar and unzip its contents into the flat_file
directory. You'll need the `metadata.csv` file and the `15minute_data_austin.csv` to be in the same directory as 
the `read_csv.py` file.

At the top of the file there's a constant set to limit the size of the dataset that is read.

`LIMIT = 10000`

This is there because the dataset is quite large, and can take a long time to load, but this will limit 
time covered to a few months. Change it to `LIMIT = None` to read the entire dataset.

To run the example execute from the `examples/flat_file` directory:

`python3 read_csv.py`

### examples/database
The database directory has an example of reading the metadata and data directly from the Postgres database.
The `eclipse.py` script reads and plots solar panel generation over a few days surrounding the August 17, 2017 
solar eclipse. 

Be sure you configured your database connection parameters and credentials as outlined above.

To run this example execute from the `examples/database` directory:

`python3 eclipse.py`

## Dataport CSV to HDF Conversion
The kind folks at the NILMTK [repo](https://github.com/nilmtk/nilmtk) have contributed a converter for our Dataport CSV data to HDF. You can find the converter 
[here](https://github.com/nilmtk/nilmtk/tree/master/nilmtk/dataset_converters/dataport). 

## Contribute:
We're happy to take contributions! Submit a pull request to this repo!
