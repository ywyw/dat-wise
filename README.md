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

## Breakdown of bounding box query cases:
All possible intersections of a rectangular query against a curved Healpix are as follows:

![Case one](https://cloud.githubusercontent.com/assets/7133238/6182724/dbb15d46-b2fe-11e4-9aa8-213ab5461dec.png "Healpix corner in bbox")

This case is handled by testing each Healpix corner and seeing if it's within range of the bounding box, which is easy

![Case two](https://cloud.githubusercontent.com/assets/7133238/6182725/dbb46130-b2fe-11e4-82d8-c10785cb1375.png "Bbox corner in healpix")

This case is done by the radec2healpix function, which tests each corner of the bbox and sees if it lands within the Healpix in question, also straightforward

![Case three](https://cloud.githubusercontent.com/assets/7133238/6182726/dbb63690-b2fe-11e4-8cc0-0f839f74c476.png "Bbox edge intersects diagonals of Healpix")

This is an edge case that took some consideration, when no corners of either fall within the other, this is a fairly fast and easy way to avoid complex math and dealing with curved Healpix edges

## WIP

- hashing for queries
- reverse functions
- latlong vs radec
- settle ring vs nest

