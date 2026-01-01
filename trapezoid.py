import math
import numpy as np
from typing import Tuple
from matplotlib import pyplot as plt
from sympy.codegen import Print


def psi_to_xy(psi:float, radius:float = 200.0) -> Tuple[float, float]:
    x = radius * math.cos(psi)
    y = radius * math.sin(psi)
    return x, y


def tangent_line_coeffs(x:float, y:float) -> Tuple[float, float, float]:
    return x, y, -(x**2 + y**2)


def secant_line_coeffs(x1, y1, x2, y2) -> Tuple[float, float, float]:
    if x1 == x2 and y1 == y2:
        raise ValueError("Points must be distinct")

    A = y2 - y1
    B = x1 - x2
    C = -(A*x1 + B*y1)

    return A, B, C

if __name__ == "__main__":
    deg1 = 3.0
    deg2 = 6.0

    rad1 = math.radians(deg1)
    rad2 = math.radians(deg2)

    print()
    A,B,C = secant_line_coeffs(*psi_to_xy(rad1), *psi_to_xy(rad2))

    # Generate X values
    X = np.linspace(-300, 300, 400)

    # Compute Y from AX + BY + C = 0
    Y = -(A*X + C) / B

    plt.plot(X, Y, label="Line")
    plt.axhline(0)
    plt.axvline(0)
    plt.gca().set_aspect("equal")
    plt.grid(True)
    plt.legend()
    plt.show()

    psi_deg_init = 3.0
    psi_interval = 3.0
    A1,B1,C1 = tangent_line_coeffs(*psi_to_xy(math.radians(psi_deg_init), 200.0))
    A2,B2,C2 = tangent_line_coeffs(*psi_to_xy(math.radians(psi_deg_init + psi_interval/2.0), 200.0))
    A3,B3,C3 = tangent_line_coeffs(*psi_to_xy(math.radians(psi_deg_init + psi_interval), 200.0))
    A4,B4,C4 = secant_line_coeffs(*psi_to_xy(math.radians(psi_deg_init), 200.0), *psi_to_xy(math.radians(psi_deg_init + psi_interval), 200.0))

    print(f"{A1:.1f}x + {B1:.1f}y {C1:.1f} < 0")
    print(f"{A2:.1f}x + {B2:.1f}y {C2:.1f} < 0")
    print(f"{A3:.1f}x + {B3:.1f}y {C3:.1f} < 0")
    print(f"{A4:.1f}x + {B4:.1f}y {C4:.1f} > 0")