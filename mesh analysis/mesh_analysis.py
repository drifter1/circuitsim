import numpy as np

'''
Electronic Circuit is
┌─ R1 ┬ R2 ─┐
V1    R3    V2
└─────┴─────┘
with following values:
'''
V1 = 5
V2 = 2
R1 = 2000 # 2k Ohm
R2 = 2000 # 2k Ohm
R3 = 1000 # 1k Ohm

'''
1. Meshes
Mesh 1: V1-R1-R3 Loop
Mesh 2: R3-R2-V2 Loop

2. Mesh Currents (all clockwise)
I1 for Mesh 1
I2 for Mesh 2
'''

# 3. Apply KVL for all Meshes
# Mesh 1
# + V1 - R1·I1 - R3·(I1 - I2) = 0
# -(R1 + R3)·I1 + R3·I2 = - V1
I1_mesh1 = -(R1 + R3)
I2_mesh1 = R3
b_mesh1 = -V1

# Mesh 2
# + R3·(I1 - I2) - R2·I2 - V2 = 0
# + R3·I1 - (R3 + R2)·I2  = V2
I1_mesh2 = R3
I2_mesh2 = -(R3 + R2)
b_mesh2 = V2

# 4. Solve the Linear System
# -3000 I1 + 1000 I2 = -5
# +1000 I1 - 3000 I2 = 2
a = np.array([[I1_mesh1, I2_mesh1],[I1_mesh2, I2_mesh2]])
b = np.array([b_mesh1, b_mesh2])

# Solve System
x = np.linalg.solve(a,b)
print(x)

# 5. Solve for other Currents and Voltages
# The current that flows through R3 is
Ix = x[0] - x[1]
print("Ix = ", Ix)
# The voltage along R3 is
Vx = R3 * Ix
print("Vx = ", Vx)
