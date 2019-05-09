
class Component:  # circuit component structure
    def __init__(self, comp_type, high_node, low_node, value):
        self.comp_type = comp_type
        self.high_node = high_node
        self.low_node = low_node
        self.value = value

    def __repr__(self):
        return str(self.comp_type) + " " + str(self.high_node) + " " + str(self.low_node) + " " + str(self.value)


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

# MAIN FUNCTION

# Initialize component counters
elementCount = 0
voltageCount = 0
currentCount = 0
resistorCount = 0
capacitorCount = 0
inductorCount = 0

# Parse File
fileName = "example.spice"
components = parseFile(fileName)

# Print Information
print("Component count: ", len(components))
print("Voltage count: ", voltageCount)
print("Current count: ", currentCount)
print("Resistance count: ", resistorCount)
print("Capacitance count: ", capacitorCount)
print("Inductance count: ", inductorCount)
print("\nCircuit Components:")
for i in range(0, len(components)):
    print(components[i])
