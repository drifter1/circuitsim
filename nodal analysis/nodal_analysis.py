import numpy as np

'''
Electronic Circuit is
+┌─ R1 ┬─────┬────┐
 V     R2    R3   I ↑
-└─────┴─────┴────┘
with following values:
'''
V = 140
I = 18
R1 = 20
R2 = 6
R3 = 5

'''
1/2. Identify and Assign Nodes
Node 0: Connecting V-R2-R3-I  (node at the bottom)
Node A: Connecting V-R1       (upper left node)
Node B: Connecting R1-R2-R3-I (upper right node)
'''

# 3. Apply KCL for Nodes A and B
# Node A
# simple case with VA = V
VA_nodeA = 1
VB_nodeA = 0
b_nodeA = V

# Node B
# (VB-VA)/20 + VB/6 + VB/5 - 18 =0
# ...
# 25 VB + (-3) VA = 1080
VA_nodeB = -(1/R1)*60
VB_nodeB = ((1/R1) + (1/R2) + (1/R3))*60
b_nodeB = I*60

# 4. Solve the Linear System
# 1 VA + 0 VB = 25
# - 3 VA + 25 VB  = 1080
a = np.array([[VA_nodeA, VB_nodeA],[VA_nodeB, VB_nodeB]])
b = np.array([b_nodeA, b_nodeB])

# Solve System
x = np.linalg.solve(a,b)
print(x)

# 5. Solve for other Currents and Voltages
V20 = (x[0] - x[1])/R1
print("v20: ", V20)
V6 = (x[1])/R2
print("v6: ", V6)
V5 = (x[1])/R3
print("v5: ", V5)
