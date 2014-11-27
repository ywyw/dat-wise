#!/usr/bin/python

import healpy
import math
import fitsio

def cart2polar(x,y,z):
    return (healpy.vec2ang(x,y,z))

def polar2cart(theta,phi):
    return (healpy.ang2vec(theta,phi))

# healpy.get_neighbors() for 4 nn, get_all for 8

def radec2polar(ra,dec):
    theta = (90-dec)*math.pi/180
    phi = ra*math.pi/180 
    return (theta,phi)
    
def polar2radec(theta,phi):
    ra = phi*180/math.pi
    dec = 90-theta*180/math.pi
    return (ra,dec)

def polar2healpix(theta,phi,nside):
    ipix = healpy.ang2pix(nside,theta,phi)
    return ipix

def ipix2tuple(pixelring,nside):
    ipixnest = healpy.ring2nest(nside,pixelring)
    npix = healpy.nside2npix(nside)
    return (ipixnest / (npix/12) ,ipixnest % (npix/12))

def tuple2hash(binnum,remainder):
    return str(hex(binnum)[2:])+str(hex(remainder)[2:])
    
# hex(binnum) concat hex(remainder): eg: 0123456789ab+0123456789abcdef: (10,15) -> af
# next: how to find the right healpix for a given resolution with a hash
def hash2tuple():
    # write the reverse function

def tuple2ipix(binnum,remainder,nside):
    # write the reverse function

# checking if a query is "valid" # note: can handle wraparound later
def isvalidbboxquery(ramin,decmin,ramax,decmax):
    if not (0 <= ramin <=360) or not (0 <= ramin <=360):
        return False
    if not (-90 <= decmin <= 90) or not (-90 <= decmax <= 90):
        return False
    if (ramin > ramax or decmin > decmax):
        return False
    return True
    
# find all the corners of the healpix bounding box, npix = 12
def bboxcorners(ramin,decmin,ramax,decmax):
    bounds = healpy.boundaries(1,0,nest=True,step=1)
    vectranspose = bounds.T
    result = map(polar2radec, numpy.array(healpy.vec2ang(vectranspose))[0],numpy.array(healpy.vec2ang(vectranspose))[1])
    return result

def query(ramin,decmin,ramax,decmax):
    if (isvalidbboxquery(ramin,decmin,ramax,decmax)):
        print "valid bbox query"
        corners = bboxcorners(ramin,decmin,ramax,decmax)
        print corners.join("_")
    else:
        print "not a valid bbox"

# healpix completely contained in bbox, don't divide further
def insidebbox(ramin,decmin,ramax,decmax,corners):
    for corner in corners:
        if (ramin <= corner.ra <= ramax and decmin <= corner.dec <= decmax):
            return True
        else:
            return False
            

def bboxpixintersect(ramin,decmin,ramax,decmax,ipix,nside):
    # if bbox corner in pixel return true    
    # calculate midlines
    # if bbox intersect midlines return true
    return False