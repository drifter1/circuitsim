import numpy as np
import scipy.sparse as sparse
from scipy.sparse.linalg.dsolve import linsolve

np.set_printoptions(precision=3, suppress=True)


class Triplet:
    def __init__(self):
        self.rows = []
        self.cols = []
        self.data = []

    def insert(self, row, col, data):
        self.rows.append(row)
        self.cols.append(col)
        self.data.append(data)

    def __repr__(self):
        return "rows: " + str(self.rows) + "\ncols: " + str(self.cols) + "\ndata: " + str(self.data)


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

# triplets lists
triplets = Triplet()

# add impact of R1
triplets.insert(0, 0, 0.25)
triplets.insert(0, 1, -0.25)
triplets.insert(1, 0, -0.25)
triplets.insert(1, 1, 0.25)

# add impact of R2
triplets.insert(1, 1, 0.5)

# add impact of V1
triplets.insert(0, 2, 1)
triplets.insert(2, 0, 1)

print(triplets, "\n")

# setup matrix
mtx = sparse.coo_matrix(
    (triplets.data, (triplets.rows, triplets.cols)), shape=(3, 3))

del triplets

# convert to CSR
A = mtx.tocsr()

print("A:")
print(A, "\n")
print(A.todense())

b = np.array([0, 2, 3])
print("\nB:", b)

x = linsolve.spsolve(A, b)
print("\nX:", x)
