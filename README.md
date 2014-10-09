# dat-wise

A dat importer for the all-sky data release from WISE

Disclaimer: Work in progress

columns.csv has the metadata for the WISE data

Thanks to [Starlink](https://github.com/Starlink/starjava/blob/a3fb3f770ca7308784df21597377ed781d995ca8/ttools/src/resources/uk/ac/starlink/ttools/example/allwise-meta-full.txt) for parsing the column names!

# Download an example FITS file here: 
curl http://lambda.gsfc.nasa.gov/data/map/dr4/ancillary/masks/wmap_temperature_analysis_mask_r9_7yr_v4.fits -o example.fits

# usage: username, databasename
python healpixdb.py "Y" "tempdb"

# POSTGRES schema: nside | npix | ipix | filename
This should insert all the healpixels into a POSTGRES database of your naming and print them out.
