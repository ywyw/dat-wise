# dat-wise

A dat importer for the all-sky data release from WISE

Disclaimer: Work in progress

columns.csv has the metadata for the WISE data

Thanks to [Starlink](https://github.com/Starlink/starjava/blob/a3fb3f770ca7308784df21597377ed781d995ca8/ttools/src/resources/uk/ac/starlink/ttools/example/allwise-meta-full.txt) for parsing the column names!

# To run the demo, download the following:
[Docker image](https://github.com/pkafei/docker_scipy)

# Download an example FITS file here: 
curl http://lambda.gsfc.nasa.gov/data/map/dr4/ancillary/masks/wmap_temperature_analysis_mask_r9_7yr_v4.fits -o example.fits

# usage: username, databasename
python healpixdb.py "Y" "tempdb"

# POSTGRES schema: nside | npix | ipix | filename
This should insert all the healpixels into a POSTGRES database of your naming and print them out.

# Demo for ra/dec to healpix geohash:
import numpy <br>
import healpy <br>
m = numpy.arange(healpy.nside2npix(4)) <br>
healpy.mollview(m, nest=True, title="Mollview image NESTED") <br>
nside = 4 <br>
(theta,phi) = radec2polar(60,-1.25) <br>
ipix = polar2healpix(theta,phi,nside) <br>
(binnum, remainder) = ipix2tuple(ipix,nside) <br>
print tuple2hash(binnum,remainder)
bounds = healpy.boundaries(1,0,nest=True,step=1)
vectranspose = bounds.T
numpy.array(healpy.vec2ang(vectranspose))
map(polar2radec, numpy.array(healpy.vec2ang(vectranspose)).T)
