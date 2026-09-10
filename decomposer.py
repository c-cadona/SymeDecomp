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
fortescue_matrix = np.array(np.asmatrix(f'1 1 1; 1 {a**2} {a}; 1 {a} {a**2}'))

print(fortescue_matrix)