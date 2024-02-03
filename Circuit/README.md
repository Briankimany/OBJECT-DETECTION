### Electrical Circuit Elements to Nearest Junctions
Problem Statement

Given a list of electrical circuit elements, each represented by its coordinates and label, assign each element to its nearest junction based on its position in the circuit. The goal is to assign each circuit element to its nearest 2 junctions, where junctions are shared between multiple elements.
Input

    A list of electrical circuit elements, each represented by a tuple (x1, y1, x2, y2, label)
        (x1, y1) and (x2, y2) are the coordinates of the two endpoints of the element
        label is a string representing the type of element (e.g., resistor, capacitor, wire)
    A list of junctions, each represented by a tuple (x, y, x2, y2)
        (x, y) and (x2, y2) are the coordinates of the two endpoints of the junction

Output

    A dictionary where each key is a circuit element and the corresponding value is a tuple containing the coordinates of the two nearest junctions

Objectives

    Analyze the circuit and identify the junctions
    Determine the nearest junction for each circuit element based on its position in the circuit
    Assign each element to its nearest junction

Handling Circuit Configurations

    Handle various circuit configurations, including vertical, horizontal, and diagonal elements
    Account for overlapping elements and shared junctions

Constraints

    The circuit elements may be arranged vertically, horizontally, or diagonally
    Junctions may be shared between multiple elements
    The coordinates of the circuit elements will be integers
    Each element label will be a string
    The number of elements in the circuit can vary
    The circuit elements may have different types, such as resistors, capacitors, and wires
    The junctions may have different coordinates, depending on the circuit configuration

Example

    Input: (130.00200778629318, 300.0004836174586, 130.00021822943188, 390.00101277079267, 'v', True), (130.00200778629318, 300.0004836174586, 130.00021822943188, 390.00101277079267, 'v', True)
    Output: {('resistor': (130.00200778629318, 300.0004836174586), 'capacitor': (130.00021822943188, 390.00101277079267)}

Note

    The input format is supported by some simulators like CircuitJS.
    For educational purposes, consider circuit elements with 2 terminals.
    The circuit elements may be arranged vertically, horizontally, or diagonally.
    Junctions may be shared between multiple elements.
    The output dictionary will have the circuit element as the key and the coordinates of the two nearest junctions as the value.
    In CircuitJS, junctions are counted as 1=2, then on the next top 3 and 4 on the next bottom, and so on. The y-values are measured from the top of the screen.
    For a start, consider a circuit with one layer on the y-axis and an n-x division of the circuit. This means that the circuit only has two upper and lower y-junction values, and on the x-axis, the circuit has n subcircuits. These are loops in which you can perform KVL or KCL.


algorithm files at briankimani328@gmail.com
