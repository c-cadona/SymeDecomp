import numpy as np
import math
import cmath
import matplotlib.pyplot as plt

#   Operador alfa (a)
a = cmath.rect(1, math.radians(120))


"""
A matriz é montada da seguinte forma:
            A       B       C
Zero        n1      n2      n3 
Positiva    n4      n5      n6
Negativa    n7      n8      n9
"""
fortescue_matrix = np.array(
    np.asmatrix(
        f'1 1 1; 1 {a**2} {a}; 1 {a} {a**2}'
    )
)

v_a, v_b, v_c = cmath.rect(1, math.radians(0)), cmath.rect(1, math.radians(45)), cmath.rect(1, math.radians(240))
i_a, i_b, i_c = cmath.rect(1, math.radians(30)), cmath.rect(1, math.radians(120)), cmath.rect(1, math.radians(240))

voltage_components = np.array(
    np.asmatrix(
        f'{v_a}; {v_b}; {v_c}'
    )
)

current_components = np.array(
    np.asmatrix(
        f'{i_a}; {i_b}; {i_c}'
    )
)

def invert_matrix(matrix):
    return np.linalg.inv(matrix)

voltage_symmetrical_components = (1/3) * (invert_matrix(fortescue_matrix) @ voltage_components)
current_symmetrical_components = (1/3) * (invert_matrix(fortescue_matrix) @ current_components)

print(
    f"Voltage Symmetrical Components:\n"
    "CARTESIAN FORM:\n"
    f"Zero = {voltage_symmetrical_components[0][0]:.3f}\n"
    f"Positive = {voltage_symmetrical_components[1][0]:.3f}\n"
    f"Negative = {voltage_symmetrical_components[2][0]:.3f}\n"
    "\nPOLAR FORM:\n"
    f"Zero = {abs(voltage_symmetrical_components[0][0]):.3f} ∠ {math.degrees(cmath.phase(voltage_symmetrical_components[0][0])):.3f}°\n"
    f"Positive = {abs(voltage_symmetrical_components[1][0]):.3f} ∠ {math.degrees(cmath.phase(voltage_symmetrical_components[1][0])):.3f}°\n"
    f"Negative = {abs(voltage_symmetrical_components[2][0]):.3f} ∠ {math.degrees(cmath.phase(voltage_symmetrical_components[2][0])):.3f}°\n"

    "\n==================================================================\n"

    f"\nCurrent Symmetrical Components:\n"
    "CARTESIAN FORM:\n"
    f"Zero = {current_symmetrical_components[0][0]:.3f}\n"
    f"Positive = {current_symmetrical_components[1][0]:.3f}\n"
    f"Negative = {current_symmetrical_components[2][0]:.3f}\n"
    "POLAR FORM:\n"
    f"Zero = {abs(current_symmetrical_components[0][0]):.3f} ∠ {math.degrees(cmath.phase(current_symmetrical_components[0][0])):.3f}°\n"
    f"Positive = {abs(current_symmetrical_components[1][0]):.3f} ∠ {math.degrees(cmath.phase(current_symmetrical_components[1][0])):.3f}°\n"
    f"Negative = {abs(current_symmetrical_components[2][0]):.3f} ∠ {math.degrees(cmath.phase(current_symmetrical_components[2][0])):.3f}°\n"
)