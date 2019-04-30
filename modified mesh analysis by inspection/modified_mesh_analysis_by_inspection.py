import numpy as np

'''
Electronic Circuit is
┌ R1 ┬ R2 ┬ R3 ┐
│    R4    R5   R6
└ V1 ┴────┴ V2 ┘
 -  +      -  +
with following values:
'''
R1 = 5
R2 = 10
R3 = 3
R4 = 7
R5 = 4
R6 = 1
V1 = 1
V2 = 3

'''
Mesh 1: V1-R1-R4 Loop
Mesh 2: R4-R2-R5 Loop
Mesh 3: V2-R5-R3-R6 Loop

Mesh Currents (all clockwise)
I1 for Mesh 1
I2 for Mesh 2
I3 for Mesh 3
'''

# Modified Mesh Analysis By Inspection
a = np.array([[R1 + R4, -R4, 0],[-R4, R2 + R4 + R5, -R5], [0, -R5, R3 + R5 + R6]])
b = np.array([-V1, 0 , -V2])
print("A:\n", a, "\n")
print("b:\n", b, "\n")

# Solve System
x = np.linalg.solve(a,b)
print("x:\n", x)
