# coding=utf-8
import BasicCore
import os
import sys
import datetime
sys.setrecursionlimit(50000)



if __name__ == '__main__':
    BC = BasicCore.basic_core()
    # BC.run(1,1,1)
    n_x = 7
    n_h = 7
    n_y = 7
    layers_dims = (n_x, n_h, n_y)
    A,B = BC.two_layer_model(layers_dims)
    print(A)
    print(B)

    # from time import time

