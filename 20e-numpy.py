"""
590PR Fall 2018
Assignment 4, on Numpy

I provided you both a small and two very large 3-D ndarrays of signed numbers.
Their dimensions are such that they are cubes.

For the small array, you can see the complete expected output results in the
Doctest below.

You are to complete the function that will search all sub-cubes of the
full ndarray, to find the sub-cube whose 'surface' has the largest sum.
Borrowing terminology from set theory, where a set is still an 'improper'
subset of itself, the full cube has to be checked as a possibility as
well as all possible smaller subcubes within it.

Additionally, it should be able to print the intermediate results for
each size of subcube, as shown in the example test output with size 5.
"""

import numpy as np

# create a class
class cell:
    def __init__(cell, sum=0, location=(0,0,0),width=0):
        cell.sum = sum
        cell.location = location
        cell.width = width


# find the subcube
def SUBCUBE(n,width,start=(0,0,0)):
    subcube= np.zeros((n,n,n), dtype=int)
    for i in range(width):
        for j in range(width):
            for k in range(width):
                subcube[start[0]+i][start[1]+j][start[2]+k]=1
                k=+1
            j=+1
        i=+1
    return subcube


# find the insidecube
def INSIDECUBE(n,width,start=(0,0,0)):
    insidecube= np.ones((n,n,n), dtype=int)
    for i in range(width):
        for j in range(width):
            for k in range(width):
                insidecube[start[0]+i][start[1]+j][start[2]+k]=0
                k=+1
            j=+1
        i=+1
    return insidecube

# create the starts
def STARTS(n,width):
    starts = []
    for i in range(n-width+1):
        for j in range(n - width + 1):
            for k in range(n - width + 1):
                start = (i,j,k)
                starts.append(start)
    return starts

def find_max_subcube(a: np.ndarray, show_intermediate_results=True) -> np.ndarray:


    """Given a cubical ndarray, search all subcubes (all proper and the improper one
    which is the whole thing), to find which one has the maximum sum of all cells
    in its outer layer. Since there are negative numbers in the values, there's no
    way to predict where it will be, and there's no theoretical advantage for
    largest subcubes vs medium ones.

    Note, to make the tests work on different OS platforms & hardware, all computed
    outputs are formatted to 2 decimal places. Also note that using the round() function
    on floats sometimes will not always produce the desired number of digits.
    So use string.format() instead, like shown in the test below.

    :param a: the whole array to search
    :param show_intermediate_results: whether to print results per subcube size
    :return: the subcube ndarray that had max sum

    >>> cube_size_5 = np.load(file='A4_cube_size_5.npy', allow_pickle=False, mmap_mode=None)
    >>> print('{:0.2f}'.format(cube_size_5[4,4,4]))
    -97.09
    >>> m = find_max_subcube(cube_size_5)  #doctest: +NORMALIZE_WHITESPACE
    searching cube of width 5
    checking all subcubes of width  1, of which     125 exist.  Highest sum    95.15 found at position (3, 4, 2)
    checking all subcubes of width  2, of which      64 exist.  Highest sum   355.41 found at position (1, 3, 3)
    checking all subcubes of width  3, of which      27 exist.  Highest sum   384.71 found at position (0, 0, 1)
    checking all subcubes of width  4, of which       8 exist.  Highest sum   503.98 found at position (0, 1, 1)
    checking all subcubes of width  5, of which       1 exist.  Highest sum   297.94 found at position (0, 0, 0)
    <BLANKLINE>
    Total number of subcubes checked: 225
    Highest sum found was 503.98 in a subcube of width 4 at position (0, 1, 1)
    >>> cube_size_60 = np.load(file='A4_cube_size_60.npy', allow_pickle=False, mmap_mode=None)
    >>> m = find_max_subcube(cube_size_60, show_intermediate_results=False)  #doctest: +NORMALIZE_WHITESPACE
    Total number of subcubes checked: 3348900
    Highest sum found was 29831.55 in a subcube of width 52 at position (0, 2, 3)
    """
    n = cube.shape[0]
    Maxcells = []
    for width in range(1,cube.shape[0]+1):
        maxcell =cell()
        for start in STARTS(n,width):
            resultcube = SUBCUBE(n, width, start) * cube
            insidestart = (start[0]+1,start[1]+1,start[2]+1)
            insidewidth = width-2
            insidecube = INSIDECUBE(n,insidewidth,insidestart)
            resultcube = resultcube*insidecube
            resultcell = cell(sum=resultcube.sum(), location=start, width=width)
            if resultcell.sum >= maxcell.sum:
                maxcell = resultcell
        Maxcells.append(maxcell)
        print("checking all subcubes of width  {width}, of which     {exist} exist.  Highest sum    {sum} found at position {position}".format(width=maxcell.width,
                                                                                                                                               exist=(n+1-width)**3,
                                                                                                                                               sum=round(maxcell.sum,2),
                                                                                                                                               position=maxcell.location))
    return Maxcells

if __name__ == '__main__':
    cube = np.load(file='A4_cube_size_5.npy', allow_pickle=False, mmap_mode=None)
    # cube = np.load(file='A4_cube_size_100.npy', allow_pickle=False, mmap_mode=None)

    n = cube.shape[0]
    texist = 0
    for i in range(1,n+1):
        texist += i**3
    sc = find_max_subcube(cube)
    tmaxcell=cell()
    for cell in sc:
        if cell.sum >= tmaxcell.sum:
            tmaxcell = cell
    print("Total number of subcubes checked: {texist}".format(texist=texist))
    print("Highest sum found was {sum}, in a subcube of width {width} at position {position}".format(sum=tmaxcell.sum,
                                                                                                     width = tmaxcell.width,
                                                                                                     position =tmaxcell.location))
