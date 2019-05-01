import numpy as np

'''
Electronic Circuit is
  ┌───┬ R3 ┬───┐
↑ I1  R1   R2  I2 ↓
  └───┴─┬──┴───┘
        ⏚

with following values:
'''
R1 = 4
R2 = 10
R3 = 6
I1 = 1
I2 = 2

'''
Node 0: Connecting I1-R1-R2-I2 (node at the bottom)
Node A: Connecting I1-R1-R3    (upper left node)
Node B: Connecting I2-R2-R3    (upper right node)
'''

# Modified Nodal Analysis By Inspection
a = np.array([[1/R1 + 1/R3, -(1/R3)],[-(1/R3), 1/R2 + 1/R3]])
b = np.array([I1, -I2])
print("A:\n", a, "\n")
print("b:\n", b, "\n")

# Solve System
x = np.linalg.solve(a,b)
print("x:\n", x)
