import numpy as np
import math
import cmath

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

v_a, v_b, v_c = 0, 0, 0
i_a, i_b, i_c = 0, 0, 0

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