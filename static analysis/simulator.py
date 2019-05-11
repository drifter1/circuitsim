
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


# MAIN FUNCTION

# Initialize component counters
voltageCount = 0
currentCount = 0
resistorCount = 0
capacitorCount = 0
inductorCount = 0

# Parse File
fileName = "circuit1.sp"
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
