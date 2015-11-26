#!/usr/bin/env python3

"""
CS712 Final Project Submission
This module performs image contrast enhancement via histogram equalization
Example:
    $ python histogramEqualization.py -i <input_image> -o <output_image>
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
max_intensity = 255  # standard 8 bit grayscale max


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

    args = parser.parse_args()
    inputFile = args.inputFile
    outputFile = args.outputFile

    # Try to read the passed in image
    try:
        img = Image.open(inputFile)
    except IOError:
        print('Unable to open input file %s!' % inputFile)
        sys.exit()

    # Load image data into an 8 bit numpy array
    data = np.uint8(np.array(img))

    # Equalize histogram
    eqData = equalizeHistogram(data)
    hist, _ = np.histogram(eqData, bins=max_intensity+1)
    plotHistogram(hist, 'Output Histogram')

    # Write histogram equalized output to file
    img = Image.fromarray(eqData)
    img.save(outputFile)
        

# Histogram equalization
def equalizeHistogram(data):
    '''
    @param data : numpy 2d input array
    @return eqData : numpy 2d array - histogram equalized output
    '''
    eqData = np.zeros(data.shape, np.uint8)

    nPixels = data.shape[0] * data.shape[1]

    # First calculate the histogram of the input
    hist, _ = np.histogram(data, bins=max_intensity+1)
    assert hist.sum() / nPixels == 1, 'Unexpected input data format!'
    plotHistogram(hist, 'Input Histogram')
    
    # Store the transformation in s_k
    s_k = np.zeros(max_intensity + 1)
    for idx, _ in enumerate(s_k):
        s_k[idx] = max_intensity / nPixels * hist[:idx+1].sum()

    # Round the transformation to nearest integer
    s_k = np.rint(s_k)
    for idx, value in np.ndenumerate(s_k):
        if value > max_intensity:
            s_k[idx] = max_intensity

    plotHistogram(s_k, 's_k')

    for (x,y), value in np.ndenumerate(data):
        eqData[x,y] = s_k[value]

    return eqData

        
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
        histFile = title + '.svg'
        plt.savefig(histFile, format='svg', dpi=1200)
    except IOError:
        print('Unable to write histogram to file %s!' % histFile)
              
    #plt.show()
    
        
if __name__ == '__main__':
    main()
