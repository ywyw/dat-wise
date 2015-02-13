# dat-wise

A dat importer for the all-sky data release from WISE

Disclaimer: Work in progress

`columns.csv` has the metadata for the WISE data

Thanks to [Starlink](https://github.com/Starlink/starjava/blob/a3fb3f770ca7308784df21597377ed781d995ca8/ttools/src/resources/uk/ac/starlink/ttools/example/allwise-meta-full.txt) for parsing the column names!

# To run the demo, download the following:
[Docker image](https://github.com/pkafei/docker_scipy)

# Download an example FITS file here: 

```
curl http://lambda.gsfc.nasa.gov/data/map/dr4/ancillary/masks/wmap_temperature_analysis_mask_r9_7yr_v4.fits -o example.fits
```

# usage: username, databasename

```python
python healpixdb.py "Y" "tempdb"
```

# POSTGRES schema: `nside | npix | ipix | filename`
This should insert all the healpixels into a POSTGRES database of your naming and print them out.

# Demo for ra/dec to healpix geohash:

```python
import numpy
import healpy
m = numpy.arange(healpy.nside2npix(4))
healpy.mollview(m, nest=True, title="Mollview image NESTED")
nside = 4
(theta,phi) = radec2polar(60,-1.25)
ipix = polar2healpix(theta,phi,nside)
(binnum, remainder) = ipix2tuple(ipix,nside)
print tuple2hash(binnum,remainder)
bounds = healpy.boundaries(1,0,nest=True,step=1)
vectranspose = bounds.T
numpy.array(healpy.vec2ang(vectranspose))
map(polar2radec, numpy.array(healpy.vec2ang(vectranspose)).T)
```

For a bbox query of npix = 12 resolution:

```python
simplequery(ramin,decmin,ramax,decmax)
```

For a query returning minimum resolution healpix:

```python
fullquerywrap(ramin,decmin,ramax,decmax,nsidemin)
```

## WIP

-- hashing for queries
-- reverse functions
-- display resolution along with ipix
-- latlong vs radec
-- settle ring vs nest

