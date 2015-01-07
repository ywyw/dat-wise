#!/usr/bin/python

import healpy
import math
import fitsio
import numpy

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
    healpixring = polar2healpix(theta,phi,nside)
    return healpy.ring2nest(nside,healpixring)
    
def healpix2radec(ipix,nside):
    (theta,phi) = healpy.pix2ang(nside,ipix)
    return polar2radec(theta,phi)    
    
# hex(binnum) concat hex(remainder): eg: 0123456789ab+0123456789abcdef: (10,15) -> af
# next: how to find the right healpix for a given resolution with a hash
def hash2tuple():
    # write the reverse function

def tuple2ipix(binnum,remainder,nside):
    # write the reverse function
    
# function for finding the resolution of

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
    
# this is an algorithm that computes with absolute certainty if healpix and a
# rectangular bbox intersect, using some clever geometric reasoning
def bboxpixintersect(ramin,decmin,ramax,decmax,ipix,nside):
    # if bbox corner in pixel return true
    for i in (ramin,ramax):
        for j in (decmin,decmax):
            if (radec2healpix(i,j,nside) == ipix):
                print "bbox corner in pixel",i,j,ipix
                return True
    # if center in bbox return true
    if (centerinbbox(ramin,decmin,ramax,decmax,ipix,nside)):
        print "center in bbox"
        return True
    # next test healpix corners
    corners = bboxcorners(ipix,nside)
    corners = map(radec2latlong, corners)
    for corner in corners:
        (ra,dec) = corner
        if (ptinsidebbox(ramin,decmin,ramax,decmax,ra,dec)):
            print "corner in bbox"
            return True
    # calculate diagonals for more tricky intersect
    # corners in cw order, starting from the top, so vert (0,2) and horiz (1,3)
    if (bboxintersectline(ramin,decmin,ramax,decmax,(corners[0],corners[2]))):
        print "complex intersect"
        return True
    if (bboxintersectline(ramin,decmin,ramax,decmax,(corners[1],corners[3]))):
        print "complex intersect"
        return True
    return False
    
def radec2latlong(radecpair):
    (ra,dec) = radecpair
    if (ra > 180):
        ra = ra - 360
    return (ra,dec)

def latlon2radec(latlonpair):
    (lat, lon) = latlonpair
    if (lon < 0):
        lon = lon + 360
    return (lat, lon)
    
def bboxintersectline(ramin,decmin,ramax,decmax,line):
    # test to see if two line segments intersect on each edge of bbox
    bboxedges = [((ramin,decmin),(ramin,decmax)),((ramin,decmin),(ramax,decmin)),
    ((ramax,decmax),(ramax,decmin)),((ramax,decmax),(ramin,decmax))]
    for edge in bboxedges:
        if lineintersectline(edge,line):
            return True
    return False

# expects each line to be a tuple of tuples: (p1,p2) -> where p1 is (x1,y1), p2 is (x2,y2)
# if intersecting, x,y that solves both eqns, parametrize by x = x1 + t * (x2 - x1), 0 <= t <= 1

def lineintersectline(line1,line2):
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
    
# simple query function: draw bbox, default min resolution, return set intersecting
# example of a tricky query now working: simplequery(-65,5,90,15) -> [0,3,4,5,7]
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
    
# recursive function that selects healpix of finer resolutions until minimum
# fullquerywrap(-65,5,90,15,2)
def fullquerywrap(ramin,decmin,ramax,decmax,nsidemin):
    intersecting = simplequery(ramin,decmin,ramax,decmax) # start with 12 pixels, nside =1
    dividenomore = []
    # for each pixel put in list intersecting or dividenomore
    for pixel in intersecting:
        corners = bboxcorners(pixel,1)
        if (healpixinsidebbox(ramin,decmin,ramax,decmax,corners)):
            intersecting.remove(pixel)
            dividenomore.append(ipix)
    print intersecting
    print dividenomore
    return fullquery(ramin,decmin,ramax,decmax,nsidemin,1,intersecting,dividenomore)
    
# meat of the recursion, we need to specify what resolution each ipix has
# fullquerywrap(-65,5,90,15,2)
# expect nsidemin = 2: [0, 12, 17, 18, 19, 20, 23, 29]
# expect nsidemin = 4: [0, 1, 2, 48, 49, 50, 71, 72, 73, 74, 75, 76, 77, 78, 80, 83, 91, 92, 94, 95, 117, 119, 69, 70, 89, 90]
def fullquery(ramin,decmin,ramax,decmax,nsidemin,nsidecur,intersecting,dividenomore):
    print intersecting
    print dividenomore
    print nsidecur
    if (nsidecur == nsidemin):
        return intersecting + dividenomore
    else:
        nsidecur *= 2
        # for every pixel in intersecting, divide into 4 and test each one
        addon = []
        todelete = []
        for pixel in intersecting:
            print "intersecting: ",intersecting
            pixelchildren = getchildrennest(pixel,nsidecur)
            for child in pixelchildren:
                print "parent pixel #", pixel, " child #", child
                if healpixinsidebbox(ramin,decmin,ramax,decmax,bboxcorners(child,nsidecur)):
                    print "this will not divide further"
                    dividenomore.append(child)
                else:
                    if bboxpixintersect(ramin,decmin,ramax,decmax,child,nsidecur):
                        print "adding child", child
                        print "corners for child are:", map(radec2latlong,bboxcorners(child,nsidecur))
                        addon.append(child)
            print "going to remove ", pixel
            todelete.append(pixel)
        intersecting = intersecting + addon
        for pixel in todelete:
            intersecting.remove(pixel)
        return fullquery(ramin,decmin,ramax,decmax,nsidemin,nsidecur,intersecting,dividenomore)


# assumes the notation is ring, not nested
def getchildren(ipix,nside):
    ipixnest = healpy.ring2nest(ipix,nside)
    # regardless of resolution the next children are always the same: 4 * ipix + 0,1,2,3
    children = [ipixnest*4, ipixnest*4+1, ipixnest*4+2, ipixnest*4+3]
    return children
    
# assumes the notation is nested
def getchildrennest(ipix,nside):
    children = [ipix*4, ipix*4+1, ipix*4+2, ipix*4+3]
    return children