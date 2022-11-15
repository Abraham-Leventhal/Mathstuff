### This script defines the function, create_fib2D, which generates
### a matrix starting from the center and spiralling outwards. Each
### element is the sum of all adjacent elements that are currently in
### the matrix (the 8 entries surrounding the element). Starts at 0.

### Define the matrix-size and the direction of the spiral as the first
### and second arguments in create_fib2D(). Meant to work with n-by-n matrices
### for odd n.

### I made this for fun, I am sure this code could be vastly improved.
### Also, my machine seems to be unable to store the values for large versions
### of the matrix (somewhere after size = 101)

### I may modify in the future to allow for different initial values.

import numpy as np
import pandas as pd
import os
os.chdir('/Users/avileventhal/PycharmProjects/DataScience/Playground/')

## Create sub-functions

# Given heading from last step, and location in matrix, decide
# current heading
def decide_heading(ind,visited,heading):

    if heading == 'right' and (ind[0]-1,ind[1]) not in visited:
            return 'up'
    if heading == 'right' and (ind[0]-1,ind[1]) in visited:
            return 'right'

    if heading == 'left' and (ind[0]+1,ind[1]) not in visited:
            return 'down'
    if heading == 'left' and (ind[0]+1,ind[1]) in visited:
            return 'left'

    if heading == 'up' and (ind[0],ind[1]-1) not in visited:
            return 'left'
    if heading == 'up' and (ind[0],ind[1]-1) in visited:
            return 'up'

    if heading == 'down' and (ind[0],ind[1]+1) not in visited:
            return 'right'
    if heading == 'down' and (ind[0],ind[1]+1) in visited:
            return 'down'

# Given current heading and location in matrix, decide next location
# to fill
def next_index(ind,heading):
    if heading == 'right':
        return (ind[0],ind[1]+1)
    if heading == 'left':
        return (ind[0], ind[1]-1)
    if heading == 'up':
        return (ind[0]-1, ind[1])
    if heading == 'down':
        return (ind[0]+1, ind[1])

# Given next location to fill, grab indices of all cells that will be used to fill
# (we have to drop improper indices that are generated for edge-cells)
def get_adjacent_indices(i, j, size):
    all_adj = [(i-1,j),(i-1, j-1),(i,j-1),(i+1,j-1),
            (i+1,j),(i+1,j+1),(i,j+1),(i-1,j+1)]
    # drop improper indices
    valid_adj = [tup for tup in all_adj if tup[0] in range(0,size) and tup[1] in range(0,size)]
    return(valid_adj)

## Create matrix function: outputs the matrix as a dataframe, and the full series as a list
def create_fib2D(size,heading):
    # Initially the matrix is all-zero, our starting-index is the center
    base = np.zeros((size, size))
    center = int(np.ceil(size / 2) - 1)
    visited = [(center, center)]
    ind = (center,center)
    fib2D = [0]
    count = 0
    while count < size**2 - 1:
        # Special case for first step: don't re-evaluate the heading
        if count==0:
            ind = next_index(ind, heading)
            base[ind[0], ind[1]] = 1
            visited.append(ind)
            fib2D.append(base[ind[0], ind[1]])
            count = count + 1
        # Afterwards, reevaluate the heading for each step
        else:
            heading = decide_heading(ind, visited, heading)
            ind = next_index(ind, heading)
            adj_ind = get_adjacent_indices(ind[0], ind[1], size)
            base[ind[0], ind[1]] = np.sum([base[i] for i in adj_ind])
            visited.append(ind)
            fib2D.append(base[ind[0], ind[1]])
            count=count+1
    df = pd.DataFrame(base)
    for col in df.columns:
        df[col] = df[col].astype(int)
    return df, fib2D

df, fib2D = create_fib2D(<INSERT SIZE: WARNING IT GETS BIG FAST>,<INSERT DIRECTION OF SPIRAL>)

## The log of the proportion of the series over its index position is quite neat,
## the quotient series bounces around between ~1 and ~2, hitting 2 less and less frequently
## since the sequence only ~doubles after turning a corner
fib2D_quot_index = [np.log(x / y) for x, y in zip(fib2D, list(range(1,len(fib2D))))]
fib2D_quot = [fib2D[i]/fib2D[i-1] for i in range(2,len(fib2D))]
