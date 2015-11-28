#!/usr/bin/env python3

"""
CS712 Final Project Submission
This module performs image contrast enhancement via histogram equalization
Example:
    $ python histogramEqualization.py -i <input_image> -o <output_image> -n <neighborhood_size>
"""

__author__ = 'Evan Hosseini'
__version__ = '1.0.0'

import sys
import argparse
import time
import numpy as np
import matplotlib.pyplot as plt
from PIL import Image

# Global parameters
max_intensity = 255   # standard 8 bit grayscale max
local_lower_limit = 3 # lower limit on local histogram

# Entry point
def main():
    # Construct an argument parser for cmd line interaction
    parser = argparse.ArgumentParser(description = 'This is an image contrast \
             enhancement script.  The software performs histogram equalization \
             to enhance contrast of a given image.')

    # Application version readback option
    parser.add_argument('-v', '--version', action='version',
                        version=__version__)

    # Input image file
    parser.add_argument('-i', '--input', dest='inputFile',
                        help='Input File Name', required=True)

    # Output image file
    parser.add_argument('-o', '--output', dest='outputFile',
                        help='Output File Name', required=False,
                        default='contrastEnhancedImage.jpg')

    # Local histogram neighborhood size, n
    parser.add_argument('-n', dest='n', help='Size of local neighborhood (nxn)',
                        type=int, required=False, default=0)

    args = parser.parse_args()
    inputFile = args.inputFile
    outputFile = args.outputFile
    n = args.n

    # Validate n w/ lower bound
    if n is not 0 and n < local_lower_limit:
        print('n parameter must be greater than %d!' % local_lower_limit - 1)
        sys.exit()

    # Try to read the passed in image
    try:
        img = Image.open(inputFile)
    except IOError:
        print('Unable to open input file %s!' % inputFile)
        sys.exit()

    # Generate a time stamp for performance monitoring
    t0 = time.time()

    # Load image data into an 8 bit numpy array
    data = np.uint8(np.array(img))

    # Equalize histogram

    # If n is set, we perform local equalization, otherwise global
    if n is not 0:
        eqData = localEq(data, n)
    else:
        eqData = globalEq(data)

    hist, _ = np.histogram(eqData, bins=max_intensity+1,
                           range=(0,max_intensity))

    # Generate end time stamp and report calculation time
    t1 = time.time()
    print('Processing complete in %3.2f seconds' % (t1 - t0))
    
    plotHistogram(hist, 'Output Histogram')

    # Write histogram equalized output to file
    img = Image.fromarray(eqData)
    img.save(outputFile)        

# Local Histogram equalization
def localEq(data, n):
    '''
    @param data    : numpy 2d input array
    @param n       : local histogram neighborhood size n in x and y
    @return eqData : numpy 2d array - local histogram equalized output
    '''
    eqData = np.zeros(data.shape, np.uint8)
    tmp = list()
    
    # Loop over each pixel in the image
    for (x,y), value in np.ndenumerate(data):

        # Collect the local neighborhood into tmp
        for i in range(0,n):
            s_x = x - int(n/2) + i
            for j in range(0,n):
                s_y = y - int(n/2) + j
                if s_x >= 0 and s_x < data.shape[0] and \
                   s_y >= 0 and s_y < data.shape[1]:
                    tmp.append(data[s_x][s_y])

        # Calculate the histogram transformation
        s_k = calcTransform(np.asarray(tmp))

        # Lookup the transformation for the given pixel
        eqData[x,y] = s_k[value]

        # Clear tmp for the next iteration
        tmp = []

    return eqData

# Histogram equalization
def globalEq(data):
    '''
    @param data    : numpy 2d input array
    @return eqData : numpy 2d array - histogram equalized output
    '''
    eqData = np.zeros(data.shape, np.uint8)

    # Calculate the histogram of the input for plotting
    hist, _ = np.histogram(data, bins=max_intensity+1,
                           range=(0,max_intensity))

    plotHistogram(hist, 'Input Histogram')
    
    # Store the transformation in s_k
    s_k = calcTransform(data)
    
    plotHistogram(s_k, 's_k')

    for (x,y), value in np.ndenumerate(data):
        eqData[x,y] = s_k[value]

    return eqData

# Transformation helper function
def calcTransform(data):
    '''
    @param data : numpy array
    @return s_k : numpy array of transformation coefficients
    '''
    nPixels = data.size

    # First calculate the histogram of the input
    hist, _ = np.histogram(data, bins=max_intensity+1,
                           range=(0,max_intensity))

    assert hist.sum() == nPixels, 'Unexpected input data format!'
    
    # Store the transformation in s_k
    s_k = np.zeros(max_intensity + 1)
    for idx, _ in enumerate(s_k):
        s_k[idx] = max_intensity / nPixels * hist[:idx+1].sum()

    # Round the transformation down to nearest integer
    s_k = np.floor(s_k)

    return s_k

# Histogram plotter
def plotHistogram(data, title):
    '''
    @param data : 1d histogram array
    @param title : string to place on plot title and file name
    '''
    plt.clf()
    plt.title(title)
    plt.xlabel('Intensity value')
    plt.ylabel('# of Occurances')
    plt.bar(range(len(data)), data, color='green')

    try:
        histFile = title + '.jpg'
        plt.savefig(histFile)
    except IOError:
        print('Unable to write histogram to file %s!' % histFile)
                      
if __name__ == '__main__':
    main()
