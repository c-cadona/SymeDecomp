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

#   Plotting the voltage and current components in cartesian form

import matplotlib.pyplot as plt
from matplotlib.patches import Arc
import numpy as np

def plot_components(components, labels=None, colors=None):
    fig = plt.figure()
    ax = plt.gca()

    ax.spines['left'].set_position('zero')
    ax.spines['bottom'].set_position('zero')
    ax.spines['right'].set_color('none')
    ax.spines['top'].set_color('none')

    if labels is None:
        labels = [f'Component {i}' for i in range(len(components))]
    if colors is None:
        colors = plt.cm.tab10(np.linspace(0, 1, len(components)))

    values = [c[0] if np.ndim(c) else c for c in components]
    limit = max(abs(v) for v in values) * 1.3
    limit = max(limit, 1)

    for idx, (value, label, color) in enumerate(zip(values, labels, colors)):
        x, y = value.real, value.imag
        angle_deg = np.degrees(np.arctan2(y, x))  # ângulo do vetor, em graus

        # vetor
        ax.annotate('', xy=(x, y), xytext=(0, 0),
                    arrowprops=dict(arrowstyle='->', color=color, lw=2))
        ax.annotate(label, (x, y), textcoords="offset points",
                    xytext=(8, 8), fontsize=9, color=color)

        # arco pontilhado do ângulo, do eixo real (0°) até o vetor
        arc_radius = limit * (0.15 + 0.08 * idx)  # raio cresce a cada vetor, evita sobrepor
        theta1, theta2 = sorted([0, angle_deg])   # Arc exige theta1 < theta2
        arc = Arc((0, 0), arc_radius * 2, arc_radius * 2,
                   angle=0, theta1=theta1, theta2=theta2,
                   linestyle='--', color=color, lw=1)
        ax.add_patch(arc)

        # rótulo do ângulo, no meio do arco
        mid_angle_rad = np.radians(angle_deg / 2)
        label_x = arc_radius * 1.25 * np.cos(mid_angle_rad)
        label_y = arc_radius * 1.25 * np.sin(mid_angle_rad)
        ax.annotate(f'{angle_deg:.1f}°', (label_x, label_y),
                    fontsize=8, color=color, ha='center', va='center')

    ax.text(0, limit * 1.05, 'Img', fontsize=10, ha='center')
    ax.text(limit * 1.05, 0, 'Real', fontsize=10, va='center')

    ax.set_xlim(-limit, limit)
    ax.set_ylim(-limit, limit)
    ax.set_aspect('equal', adjustable='box')
    ax.grid(True, linestyle='--', alpha=0.5)

    plt.show()

plot_components(
    voltage_components,
    labels=['V_a', 'V_b', 'V_c'],
    colors=['r', 'g', 'b']
)