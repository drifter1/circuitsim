import numpy as np

'''
Electronic Circuit is
+ ┌─R1 ┬────┐
  V1   R2   I1 ↑
- └────┼────┘
       ⏚

with following values:
'''
R1 = 4
R2 = 2
V1 = 3
I1 = 2

'''
Node 0: Connecting V1-R2-I1 (node at the bottom)
Node 1: Connecting V1-R1    (upper left node)
Node 2: Connecting R1-R2-I1 (upper right node)
'''

# Modified Nodal Analysis
a = np.array([[1/R1, -1/R1, 1],[-1/R1, 1/R1 + 1/R2, 0],[1, 0, 0]])
b = np.array([0, 2, 3])
print("A:\n", a, "\n")
print("b:\n", b, "\n")

# Solve System
x = np.linalg.solve(a,b)
print("x:\n", x)
