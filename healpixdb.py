#!/usr/bin/python

import sys
import os
import psycopg2
import psycopg2.extras
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
import healpy as hp
username = sys.argv[1]
dbname = sys.argv[2]

def fits2healpix(cur,filename,dbname):
     NSIDE = 1
     NPIX = hp.nside2npix(NSIDE)
     #print type(cur)
     for pixel in range(0,NPIX):
         cur.execute("""INSERT INTO """ + dbname +""" (nside,npix,ipix,filename) 
         VALUES (%s,%s,%s,%s)""",(NSIDE,NPIX,pixel,filename))

conn = psycopg2.connect("dbname='postgres' user="+username+" host='localhost' password='dbpass'")
conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
cur = conn.cursor()
cur.execute("""CREATE DATABASE  """ + dbname)
conn = psycopg2.connect("dbname=" + dbname + " user=" + username + " host='localhost' password='dbpass'")
cur = conn.cursor()
cur.execute("""CREATE TABLE pixeldb (
    nside            int,
    npix             int,           
    ipix             int,           
    filename         varchar(80)         
)""")
print "table created!!"
fits2healpix(cur,"example.fits","pixeldb")
cur.execute("""SELECT * from pixeldb""")
rows = cur.fetchall()
for row in rows:
 print row
 

     