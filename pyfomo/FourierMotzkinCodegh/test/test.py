#%%
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Sep 10 17:58:06 2018

@author: sadra
"""
import math
import sys
sys.path.append('..')

import numpy as np

from src.visualize_2D import visualize_2D
from src.main import fourier_motzkin_eliminate_single,project,convexhull
from src.polytope import translate

if True: # test 1   
    print("\n Test 1: Simple 2D Polytope")
    A=np.array([[1,1],[-1,-1],[-1,0]])    
    b=np.array([[0,-1,0]]).T  
    var_index= 0
    (A_new,b_new)=fourier_motzkin_eliminate_single(var_index,A,b,atol=10**-8)
    print("A_new=",A_new)
    print("b_new=",b_new)
    print("The inequalities cannot be proven correct")


if True:# test 2 
    print("\n Test 2: Simple 2D Polytope")
    A=np.array([[1,1,1],[1,1,-1],[1,-1,1],[-1,1,1],[-1,0,0], [0,-1,0], [0,0,-1]])    
    b=np.array([[-5,3,4,2,0,0,0]]).T  
    var_index= 0
    (A_new,b_new)=fourier_motzkin_eliminate_single(var_index,A,b,atol=10**-8)
    print("b_new=",b_new)
    print("A_new=",A_new)
    A = A_new
    b = np.array([[float(x) for x in b_new]]).T
    (A_new,b_new)=fourier_motzkin_eliminate_single(var_index,A,b,atol=10**-8)
    print("b_new=",b_new)
    print("A_new=",A_new)
    fmcont = True
    print(str(A_new[5]))
    for x in A_new:
        print(x)
        if math.isnan(x):
            fmcont = False
    print(fmcont)
    print()
    print()
    # print("\n Test 2: Simple 2D Polytope")
    # A=np.array(A_new)   
    # # b=np.array(b_new.flat(1)).T  
    # b=np.array(np.array(b_new).flatten()).T 
    # print(b) 
    # var_index= 0
    # (A_new,b_new)=fourier_motzkin_eliminate_single(var_index,A,b,atol=10**-8)
    # print("A_new=",A_new)
    # print("b_new=",end="")
    # print(list(b_new))
    
# if True: # test 3
#     print("\n\n\n Test 3: Projection")
#     G=np.array([[1,3],[-1,2]])
#     Pi=np.array([[ 1.,  0.],[0.,  1.],[-1., -0.],[-0., -1.]])
#     p1=translate(project(G,Pi,np.ones((4,1))),np.array([2,2]).reshape(2,1))
#     p1.show()
    
# if True: # test 4
#     print("\n\n\n Test 4: Another Projection")
#     G=np.array([[4,1],[-5,-1]])
#     Pi=np.array([[ 1.,  0.],[0.,  1.],[-1., -0.],[-0., -1.]])
#     p2=project(G,Pi,np.ones((4,1)))
#     p2.show()
    
# if True: # test 5
#     print("\n\n\n Test 5: Another Projection")
#     G=np.array([[1,0],[6,1]])
#     Pi=np.array([[ 1.,  0.],[0.,  1.],[-1., -0.],[-0., -1.]])
#     p3=translate(project(G,Pi,np.ones((4,1))),np.array([-5,0]).reshape(2,1))
#     p3.show()

# if True: # test 6
#     print("\n\n\n Test 5: Another Projection")
#     # G=np.array([[100,100],[6,8]])
#     G=np.array([[-1,-1],[6,8]])
#     Pi=np.array([[ 1.,  0.],[0.,  1.],[-1., -0.],[-0., -1.]])
#     p4=project(G,Pi,np.ones((4,1)))
#     p4.show()
    
# p=convexhull([p1,p2,p3,p4])
# p.show()

# visualize_2D([p,p1,p2,p3,p4])
print("program complete")
# %%
