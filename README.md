# local-histogram-equalization
CS712 Final Project
Evan Hosseini
Image processing application for contrast enhancement through local histogram equalization.

#Description:
This package contains my final project submission.

#Contents:
README.md - this file
histogramEqualization.py - Source python file for this project
light_bean.jpg - Heavily saturated input image for test
dark_bean.jpg - Heavily suppressed input image for test
test_pattern.jpg - Test image for the local histogram equalization
light_bean_eq.jpg - Result of applying global histogram equalization
dark_bean_eq.jpg - Result of applying global histogram equalization
test_pattern_local_n_3.jpg - Result of applying local histogram equalization
                             with a neighborhood of size 3
test_pattern_local_n_5.jpg - Result of applying local histogram equalization
                             with a neighborhood of size 5
test_pattern_local_n_25.jpg - Result of applying local histogram equalization
                              with a neighborhood of size 25

#Dependencies:
* Python3
  * Numpy
  * Matplotlib
  * Pillow

#Usage:
Execute the histogramEqualization.py script w/in a python environment.
Specify the input file by giving a -i command switch and optionally specify the
name of the output file with a -o switch.  To perform local histogram equalization
instead of global equalization, pass -n switch specifying the size of the neighborhood to use.
This parameter must be an odd number.  See below for examples on how the images
contained in this package were generated:

#####Global Equalization
evan@pc ~ $ ./histogramEqualization.py -i light_bean.jpg -o light_bean_eq.jpg

#####Local Equalization w/ neighborhood of size 3
evan@pc ~ $ ./histogramEqualization.py -i test_pattern.jpg -o test_pattern_local_n_3.jpg -n 3

#Notes:
The local histogram equalization may take a while.. Took about 10 minutes for me
with the test pattern image running on a quad core i7-3632QM.