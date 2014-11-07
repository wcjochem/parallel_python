#Circle Neighborhood using GDAL and PP
# Parallel Processing- dividing image with border zones, moving window across each piece then recombines
# Calculating the density over circles with radii from 1 to 20 miles
# Circular moving window is approximated using a regular-shaped octagon following Glasbey and Jones (1997)
#   and the average is calculated recursively.

# Reading data in subprocess

import os, sys, time, math, numpy, pp
import osgeo.gdal as gdal
from osgeo.gdalconst import *
  
  gdal.AllRegister()
startTime = time.time()


def image_process(startj, starti, rows, cols, offsetX, offsetY, pixelWidth, pixelHeight, originLat, originLon, miles):
  try:
  gdal
except:
  import osgeo.gdal 

#        print 'Rows: ', rows
#        print 'Cols: ', cols
#        print 'Startj: ', startj
#        print 'Starti: ', starti

fn = 'C:\\Users\\wcj\\Documents\\test\\pop_parallel\\file_0'
inImg = osgeo.gdal.Open(fn, osgeo.gdalconst.GA_ReadOnly)

if inImg is None:
  print 'Could not open file ' + fn
sys.exit(1)
band = inImg.GetRasterBand(1)
r = offsetX
p = int(round((1.414213562*(r+1)-1)/3.414213562))

windowSum = 0
count = 0
try:
  data = band.ReadAsArray(startj, starti, cols, rows).astype(numpy.int32) # read the subset block of data into memory
except:
  print 'Error reading image (subprocess): ' + str(starti) + ', ' + str(startj) + ', ' + str(cols) + ', ' + str(rows)
print sys.exc_info()
sys.exit(1)
outArray = numpy.zeros((rows - (2*offsetY), cols - (2*offsetX)), dtype=long) # output array removes overlapping regions

#f.write(str(startj) + ' ' + str(starti) + ' ' + str(rows) + ' ' + str(cols))

for i in range (offsetY, rows - offsetY): 
  # loop through all rows, start in from the edge of the grid by offset no. of cells
  for j in range (offsetX, cols - offsetX):  
  # loop through all columns, starting from the offset cell
  
  if j == offsetX: # and i == offsetY:  # first row and column location
  windowSum = 0 # reset the sum (no recursive calculation)
count = 0
for x in range((i - offsetX), (i + offsetX+1)): 
  # at each cell, loop through a square centered on i,j
  for y in range((j - offsetY), (j + offsetY+1)):
  if abs((x-i)+(y-j)) <= offsetX + p and abs((x-i)-(y-j)) <= offsetX + p:
  windowSum += data[x,y]
count += 1
##                                                        if j == offsetX and i == offsetY:
##                                                                f.write('windowSum: ' + str(windowSum) + ' ' + str(i) + ', ' + str(j) + '  \n')
##                                                        if j== offsetX and i ==offsetY:
##                                                                f.write(str(x) + ', ' + str(y) + '\n')
#print str(i) + ', ' + str(j) + ' - ' + str(x) + ',' + str(y) + ' ' + str(data[x,y])
#windowSum=-2

##                        elif j == offsetX and i > offsetY: # first column location in the rest of the image
##                                TL = TC = TR = BL = BC = BR = 0
##
##                                for k in range(-r,-p+1):
##                                        TR += data[i+k-1, j+r+p+k-1] #
##                                        TL += data[i+k-1, j-r-p-k-1]
##                                        if (i == offsetY + 1):
##                                                f.write(str(k) + ' ' + str(i+k-1) + ', ' + str(j+r+p+k-1) + '\n')
##                                                f.write(str(k) + ' ' + str(i+k-1) + ', ' + str(j-r-p-k-1) + '\n')
##
##                                for k in range(p, r+1):
##                                        BR += data[i+k-1, j+r+p-k-1] #
##                                        BL += data[i+k-1, j-r-p+k-1]
##                                        if (i == offsetY + 1):
##                                                f.write(str(k) + ' ' + str(i+k-1) + ', ' + str(j+r+p-k-1) + '\n')
##                                                f.write(str(k) + ' ' + str(i+k-1) + ', ' + str(j-r-p+k-1) + '\n')
##
##                                for k in range(-p+1, j+p):
##                                        BC += data[i+r, k]
##                                        TC += data[i-r, k]
##                                        if (i == offsetY + 1):
##                                                f.write(str(k) + ' ' + str(i+r) + ', ' + str(k) + '\n')
##                                                f.write(str(k) + ' ' + str(i-r) + ', ' + str(k) + '\n')
##
##                                windowSum = windowSum + BR + BL + BC - TR - TL - TC
##                                #windowSum = -1

else: # do recursively
  A = B = C = D = E = F = 0
try:
  try:
  for k in range(-r,-p+1):
  A += data[i+k-1, j+r+p+k] #j+r+p+k+1
D += data[i+k-1, j-r-p-k-1] #j-r-p-k-1
##                                                        if (j == offsetX + 1 and i == offsetY + 1) or (j == offsetX + 2 and i == offsetY + 1):
##                                                                f.write(str(k) + ' ' + str(i+k-1) + ', ' + str(j+r+p+k) + '\n')
##                                                                f.write(str(k) + ' ' + str(i+k-1) + ', ' + str(j-r-p-k-1) + '\n')
except:
  errorMsg = 'loop 1'
raise Exception
try:
  for k in range(-p+1,p): #(-p,p) adjusted for range inclusion
  B += data[i+k-1, j+r] # j+r
E += data[i+k-1, j-r-1] #i+k-1, j-r
##                                                        if (j == offsetX + 1 and i == offsetY + 1) or (j == offsetX + 2 and i == offsetY + 1):
##                                                                f.write(str(k) + ' ' + str(i+k-1) + ', ' + str(j+r) + '\n')
##                                                                f.write(str(k) + ' ' + str(i+k-1) + ', ' + str(j-r-1) + '\n')

except:
  errorMsg = 'loop 2'
raise Exception
try:
  for k in range(p,r+1):  
  C += data[i+k-1, j+r+p-k] # j+r+p-k
F += data[i+k-1, j-r-p+k-1]
##                                                        if (j == offsetX + 1 and i == offsetY + 1) or (j == offsetX + 2 and i == offsetY + 1):
##                                                                f.write(str(k) + ' ' + str(i+k-1) + ', ' + str(j+r+p-k) + '\n')
##                                                                f.write(str(k) + ' ' + str(i+k-1) + ', ' + str(j-r-p+k-1) + '\n')
except:
  errorMsg = 'loop 3'
raise Exception                                                
except:
  print 'Error in recursive sum at ' + str(i) + ', ' + str(j)
print 'Error in loop: ' + errorMsg
print 'r: ' + str(r)
print 'p: ' + str(p)
print 'k: ' + str(k)
print sys.exc_info()
sys.exit(1)

#print str(A) + ',' + str(B) + ',' + str(C) + ',' + str(D) + ',' + str(E) + ',' + str(F)
#f.write('before: ' + str(windowSum) + '\n')
windowSum = windowSum + (A + B + C - D - E - F)
##                                if i == offsetY:
##                                        f.write(str(A) + ',' + str(B) + ',' + str(C) + ',' + str(D) + ',' + str(E) + ',' + str(F) + '\n')
##                                        f.write('after: ' + str(windowSum) + ' ' + str(i) + ', ' + str(j) + '\n')
#if windowSum < 0: windowSum = 0
#print str(windowSum)
#if j == 20:
#sys.exit(1)

try:
  #print 'WindowSum: ' + str(windowSum)
  if windowSum < 0: windowSum = 0
outArray[i-offsetY,j-offsetX] = windowSum #/ (math.pi * miles**2)  # sum of all cells in 'circle' / area of circle in sq. miles

except:
  print 'Error at ' + str(i) + ', ' + str(j)      
print 'Sum = ' + str(sum)
print sys.exc_info()
sys.exit(1)

data = None
band = None
inImg = None
#f.close()
return outArray, startj+offsetX, starti+offsetY



# tuple of all parallel python servers to connect with
ppservers = ()
#ppservers = ("10.0.0.1",)

if len(sys.argv) > 1:
  ncpus = int(sys.argv[1])
# Creates jobserver with ncpus workers
job_server = pp.Server(ncpus, ppservers=ppservers)
else:
  # Creates jobserver with automatically detected number of workers
  job_server = pp.Server(ppservers=ppservers)

print "Starting pp with", job_server.get_ncpus(), "workers"

# open the file
#fn = 'L:\\Chris\\Reactors_Siting\\Pop\\version2\\lsusa08day'
#fn = 'P:\\demos\\pop_parallel\\file_0'
fn = 'C:\\Users\\wcj\\Documents\\test\\pop_parallel\\file_0'
#fn = 'P:\\demos\\pop_parallel\\pt_pop'
inImg = gdal.Open(fn, GA_ReadOnly)

if inImg is None:
  print 'Could not open file ' + fn
sys.exit(1)

# get image size        
cols = inImg.RasterXSize
rows = inImg.RasterYSize
bands = inImg.RasterCount
print 'Img: cols=' + str(cols) + ', rows=' + str(rows)

#band = inImg.GetRasterBand(1)

# get image properties
geotransform = inImg.GetGeoTransform()
originX = geotransform[0]
originY = geotransform[3]
pixelWidth = geotransform[1]
pixelHeight = geotransform[5]

originLat = originY + (pixelHeight / 2)
originLon = originX + (pixelWidth / 2)

# divide the image into subsets and send to PP jobs

for radius in range (1,2): # *** Change range for choice of radii ***
  print 'Radius: ' + str(radius)

miles = radius * 1609.344 # radius in meters -- pixel size in meters
offsetX = int(miles / pixelWidth) # convert the radius into the number of cells
offsetY = int(miles / (-1*pixelHeight))
print 'Pixel Width=' + str(pixelWidth) + ', Pixel Height=' + str(pixelHeight)
print 'Offset X:' + str(offsetX) + ' Y:' + str(offsetY)

jobs = []
#Read data by block - *** test different block sizes
xBlockSize = 400
yBlockSize = 400


for i in range(0, rows, yBlockSize): # starting at origin (upper-left)
  if i == 0:
  starti = 0
numRows =  yBlockSize + offsetY
else:
  starti = i - offsetY
if i + yBlockSize + offsetY < rows:
  numRows =  yBlockSize + (2*offsetY)
else:
  numRows = rows - starti

for j in range(0, cols, xBlockSize):
  if j == 0:
  startj = 0
numCols = xBlockSize + offsetX
else:
  startj = j - offsetX
if j + xBlockSize + offsetX < cols:
  numCols = xBlockSize + (2*offsetX)
else:
  numCols = cols - startj

try:
  print str(startj) + ', ' + str(starti) + ', ' + str(numCols) + ', ' + str(numRows)
# send to the job server: coordinates of the image process
jobs.append(job_server.submit(image_process, (startj, starti, numRows, numCols, offsetX, offsetY, pixelWidth, pixelHeight, originLat, originLon, miles,), (), ("math", "numpy", "osgeo.gdal", "osgeo.gdalconst",)))
data = None

except:
  print 'Error!'
print sys.exc_info()

#raw_input('Press a key ...')

# create output image
print ' ... creating output image'
#driver = inImg.GetDriver()
driver = gdal.GetDriverByName('HFA')
driver.Register()
#out_fn = 'C:\\Temp\\loop\\output2\\loop10_' + str(radius) + '.img'
out_fn = 'C:\\Users\\wcj\\Documents\\test\\ParallelPop\\loop10_' + str(radius) + '.img'
#outImg = driver.Create(out_fn, cols, rows, 1, GDT_Byte)
outImg = driver.Create(out_fn, cols, rows, 1, GDT_Int32)

if outImg is None:
  print 'Could not create output image ' + out_fn
sys.exit(1)

outBand = outImg.GetRasterBand(1)

# write output data

for job in jobs: # loop through returned PP tasks
  outData, j, i = job()
try:
  outBand.WriteArray(outData, j, i)
print '.... output ....'
print j, i
print outData.size
#print outData
outData = None
#break
except:
  print 'Error writing output image: ' + str(i) + ', ' + str(j)
print outData.size
print outData
print sys.exc_info()
sys.exit(1)

outBand.FlushCache()
stats = outBand.GetStatistics(0,1)

outImg.SetGeoTransform(inImg.GetGeoTransform())
outImg.SetProjection(inImg.GetProjection())
outImg = None

# clean up and finish
inImg = None
#data = None
#band = None
#outBand = None

job_server.print_stats()
endTime = time.time()
print 'Finished! ' + str(endTime - startTime)
