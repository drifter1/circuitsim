import numpy as np

'''
Electronic Circuit is
+ ┌─R1 ┬─R3─┐ +
  V1   R2   V2 
- └────┼────┘ -
       ⏚

with following values:
'''
R1 = 6
R2 = 3
R3 = 2
V1 = 5
V2 = 1

'''
Node 0: Connecting V1-R2-V2 (node at the bottom)
Node 1: Connecting V1-R1    (upper left node)
Node 2: Connecting R1-R2-R3 (upper middle node)
Node 3: Connecting R3-V2    (upper right node)
'''

# Modified Nodal Analysis
a = np.array(
       [[1/R1, -1/R1, 0, 1, 0],
       [-1/R1, 1/R1 + 1/R2 + 1/R3, -1/R3, 0, 0],
       [0, -1/R3, 1/R3, 0, 1],
       [1, 0, 0, 0, 0],
       [0, 0, 1, 0, 0]   
       ])
b = np.array([0, 0, 0, 5, 1])
print("A:\n", a, "\n")
print("b:\n", b, "\n")

# Solve System
x = np.linalg.solve(a,b)
print("x:\n", x)
