import numpy as np
import scipy.sparse as sparse
from scipy.sparse.linalg.dsolve import linsolve

np.set_printoptions(precision=3, suppress=True)


class Component:  # circuit component structure
    def __init__(self, comp_type, high_str, low_str, value):
        # component type
        self.comp_type = comp_type
        # nodes as strings
        self.high_str = high_str
        self.low_str = low_str
        # mapped nodes
        self.high = -1
        self.low = -1
        # component value
        self.value = value

    def __repr__(self):
        return str(self.comp_type) + " " + str(self.high) + " " + str(self.low) + " " + str(self.value)


class NodeHashtable:  # nodes hash table
    def __init__(self):
        self.nodes = {}
        self.nodeCount = 0

    def addToNodes(self, node_str):
        # check if node not already added
        if node_str not in self.nodes:
            self.nodes[node_str] = self.nodeCount
            self.nodeCount = self.nodeCount + 1
        return self.nodes[node_str]

    def __del__(self):
        del self.nodes


class Triplet:  # triplet structure
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


def parseFile(fileName):
    # open file for reading
    file = open(fileName, "r")

    # use global scope variables for component counts
    global voltageCount, currentCount, resistorCount, capacitorCount, inductorCount

    # component list
    components = []

    # read netlist
    for line in file:
        # split line
        parts = line.split()

        # comment or option
        if(parts[0][0] == '*' or parts[0][0] == '.'):
            continue

        # add component to list
        components.append(
            Component(parts[0][0].upper(), parts[1].upper(), parts[2].upper(), float(parts[3])))

        # update component counts
        if parts[0][0] == 'V':
            voltageCount = voltageCount + 1
        elif parts[0][0] == 'I':
            currentCount = currentCount + 1
        elif parts[0][0] == 'R':
            resistorCount = resistorCount + 1
        elif parts[0][0] == 'C':
            capacitorCount = capacitorCount + 1
        elif parts[0][0] == 'L':
            inductorCount = inductorCount + 1

    # return components
    return components


def mapNodes(components):
    # create hashtable
    hashtable = NodeHashtable()

    # add '0' node
    hashtable.addToNodes('0')

    # for all components
    for component in components:
        component.high = hashtable.addToNodes(component.high_str)
        component.low = hashtable.addToNodes(component.low_str)

    return components, hashtable


def calculateMatrices(components, nodeCount):

    # use global scope variables for component counts
    global voltageCount, inductorCount

    # calculate g2 components
    g2Count = voltageCount + inductorCount
    print("Group 2 count:", g2Count)

    # calculate matrix size
    matrixSize = nodeCount + g2Count - 1
    print("Matrix size:", matrixSize, "\n")

    # triplets lists
    triplets = Triplet()

    # define matrix b
    b = np.zeros(matrixSize)

    # Group 2 component index
    if(g2Count > 0 ):
        g2Index = matrixSize - g2Count
    else:
        g2Index = 0

    # loop through all components
    for component in components:
        # store component info in temporary variable
        high = component.high
        low = component.low
        value = component.value

        if component.comp_type == 'R':
            # affects G-matrix of A
            # diagonal self-conductance of node
            if high != 0:
                triplets.insert(high-1, high-1, 1/value)
            if low != 0:
                triplets.insert(low-1, low-1, 1/value)

            # mutual conductance between nodes
            if high != 0 and low != 0:
                triplets.insert(high-1, low-1, -1/value)
                triplets.insert(low-1, high-1, -1/value)

        # elif component.comp_type == 'C':
            # Capacitance is an open circuit for Static Analysis

        elif component.comp_type == 'L':
            # closed circuit  in Static Analysis: 0 resistance and 0 voltage
            # affects the B and C matrices of A
            if high != 0:
                triplets.insert(high-1, g2Index, 1)
                triplets.insert(g2Index, high-1, 1)
            if low != 0:
                triplets.insert(low-1, g2Index, -1)
                triplets.insert(g2Index, low-1, -1)

            # affects b-matrix
            b[g2Index] = 0

            # increase G2 index
            g2Index = g2Index + 1

        elif component.comp_type == 'V':
            # affects the B and C matrices of A
            if high != 0:
                triplets.insert(high-1, g2Index, 1)
                triplets.insert(g2Index, high-1, 1)
            if low != 0:
                triplets.insert(low-1, g2Index, -1)
                triplets.insert(g2Index, low-1, -1)

            # affects b-matrix
            b[g2Index] = value

            # increase G2 counter
            g2Index = g2Index + 1

        elif component.comp_type == 'I':
            # affects b-matrix
            if high != 0:
                b[high - 1] = b[high - 1] - value
            if low != 0:
                b[low - 1] = b[low - 1] + value

    # setup sparse matrix A
    mtx = sparse.coo_matrix(
        (triplets.data, (triplets.rows, triplets.cols)), shape=(matrixSize, matrixSize))

    del triplets

    # convert to CSC
    A = mtx.tocsc()

    return A, b


def solveSystem(A, b):
    x = linsolve.spsolve(A, b)
    return x


# MAIN FUNCTION

# Initialize component counters
voltageCount = 0
currentCount = 0
resistorCount = 0
capacitorCount = 0
inductorCount = 0

# Parse File
fileName = "example.spice"
print("Parsing file...\n")
components = parseFile(fileName)

# Map nodes
print("Mapping nodes...\n")
components, hashtable = mapNodes(components)

# Print Information
print("Circuit Info")
print("Component count: ", len(components))
print("Voltage count: ", voltageCount)
print("Current count: ", currentCount)
print("Resistance count: ", resistorCount)
print("Capacitance count: ", capacitorCount)
print("Inductance count: ", inductorCount)
print("Node count: ", hashtable.nodeCount)

print("\nNodes are mapped as following:")
for key, val in hashtable.nodes.items():
    print("\"" + key + "\" :", val)

print("\nCircuit Components:")
for i in range(0, len(components)):
    print(components[i])

# Calculate and solve system
print("\nCalculating MNA Matrices...\n")
A, b = calculateMatrices(components, hashtable.nodeCount)
print("A:\n", A.todense())
print("b:\n", b)

print("\nSolving System...\n")
x = solveSystem(A, b)
print("x:\n", x)
