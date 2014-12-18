#!/usr/bin/python

import healpy
import math
import fitsio

def cart2polar(x,y,z):
    return (healpy.vec2ang(x,y,z))

def polar2cart(theta,phi):
    return (healpy.ang2vec(theta,phi))

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

# ra/dec to healpix one function
def radec2healpix(ra,dec,nside):
    (theta,phi) = radec2polar(ra,dec)
    return polar2healpix(theta,phi,nside)
    
def healpix2radec(ipix,nside):
    (theta,phi) = healpy.pix2ang(nside,ipix)
    return polar2radec(theta,phi)    
    
# hex(binnum) concat hex(remainder): eg: 0123456789ab+0123456789abcdef: (10,15) -> af
# next: how to find the right healpix for a given resolution with a hash
def hash2tuple():
    # write the reverse function

def tuple2ipix(binnum,remainder,nside):
    # write the reverse function

# checking if a query is "valid" # note: can handle wraparound later
def isvalidbboxquery(ramin,decmin,ramax,decmax):
    if not (-180 <= ramin <= 180) or not (-180 <= ramax <= 180):
        return False
    if not (-90 <= decmin <= 90) or not (-90 <= decmax <= 90):
        return False
    if (ramin > ramax or decmin > decmax):
        return False
    return True
    
# find all the corners of the healpix, tuples of (ra,dec)
def bboxcorners(ipix,nside):
    bounds = healpy.boundaries(nside,ipix,nest=True,step=1)
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
def healpixinsidebbox(ramin,decmin,ramax,decmax,corners):
    for corner in corners:
        #print corner
        if (ramin <= corner[0] <= ramax and decmin <= corner[1] <= decmax):
            return True
        else:
            return False
            
# test if the center of healpix is in a bbox
def centerinbbox(ramin,decmin,ramax,decmax,ipix,nside):
    (racenter,deccenter) = healpix2radec(ipix,nside)
    if (ramin <= racenter <= ramax and decmin <= deccenter <= decmax):
        return True
    return False
    
    
def bboxpixintersect(ramin,decmin,ramax,decmax,ipix,nside):
    # if bbox corner in pixel return true
    for i in (ramin,ramax):
        for j in (decmin,decmax):
            if (radec2healpix(i,j,nside) == ipix):
                return True
    # if center in bbox return true
    if (centerinbbox(ramin,decmin,ramax,decmax,ipix,nside)):
        return True
    # next test healpix corners
    corners = bboxcorners(ipix,nside)
    for corner in corners:
        (ra,dec) = corner
        if (ra < 0):
            ra = ra + 360
        if (ptinsidebbox(ramin,decmin,ramax,decmax,ra,dec)):
            return True
    # calculate midlines for more tricky intersect
    # corners in ccw order? so lines are (0,2) and (1,3)
    # use library defined function to test intersect between line and bbox
    # if bbox intersect midlines return true
    return False
    
def ptinsidebbox(ramin,decmin,ramax,decmax,ra,dec):
    if (ramin <= ra <= ramax and decmin <= dec <= decmax):
        return True
    return False
    
# query function: draw bbox, default min resolution, return set intersecting
def simplequery(ramin,decmin,ramax,decmax,nside=1):
    intersecting = []
    pixels = healpy.nside2npix(nside)
    if (isvalidbboxquery(ramin,decmin,ramax,decmax)):
        print "valid bbox query"
    else:
        print "invalid query"
    for ipix in range(pixels):
        if (bboxpixintersect(ramin,decmin,ramax,decmax,ipix,nside)):
            intersecting.append(ipix)
    return intersecting