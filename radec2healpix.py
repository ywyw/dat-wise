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
    # corners in cw order, starting from the top, so vert (0,2) and horiz (1,3)
    if (bboxintersectline(ramin,decmin,ramax,decmax,(corners[0],corners[2]))):
        return True
    if (bboxintersectline(ramin,decmin,ramax,decmax,(corners[1],corners[3]))):
        return True
    return False
    
def bboxintersectline(ramin,decmin,ramax,decmax,line):
    # test to see if two line segments intersect on each edge of bbox
    bboxedges = [((ramin,decmin),(ramin,decmax)),((ramin,decmin),(ramax,decmin)),
    ((ramax,decmax),(ramax,decmin)),((ramax,decmax),(ramin,decmax))]
    for edge in bboxedges:
        if lineintersectline(edge,line):
            return True
    return False

# expects each line to be a tuple of tuples:
# (p1,p2) -> where p1 is (x1,y1), p2 is (x2,y2)
# if intersecting, x,y that solves both eqns
# parametrize by x = x1 + t * (x2 - x1), 0 <= t <= 1

def lineintersectline(line1,line2):
    print "line 1:"
    print line1
    print "line 2:"
    print line2
    ((x1, y1), (x2, y2)) = line1
    ((x3, y3), (x4, y4)) = line2
    numerator1 = (x1 - x3) * (y4 - y3) - (y1 - y3) * (x4 - x3)
    numerator2 = (x1 - x3) * (y2 - y1) - (y1 - y3) * (x2 - x1)
    denominator = (y2 - y1) * (x4 - x3) - (x2 - x1) * (y4 - y3)
    # either parallel or collinear
    if (denominator == 0):
        # collinear if num is zero
        if (numerator1 == 0):
            # if either endpoint of the first line is within the second segment
            # we don't need to check both x,y since the segments are collinear
            if(x3 <= x1 <= x4 or x3 <= x2 <= x4):
                return True
            else:
                return False
        else:
            return False
    if (0 <= numerator1/denominator <= 1 and 0 <= numerator2/denominator <= 1):
        return True
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
        print "now testing pixel number:" + str(ipix)
        if (bboxpixintersect(ramin,decmin,ramax,decmax,ipix,nside)):
            intersecting.append(ipix)
    return intersecting
    
# example of a tricky query:
# simplequery(-65,5,90,15) -> [5,7]
# should also return 0,3,4