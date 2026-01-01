import math


# cos(Delta psi)x - sin(Delta psi)y - x' = -cos(Delta psi)v^x + sin(Delta psi)v^y + 200 \
# sin(Delta psi)x + cos(Delta psi)y - y' = -sin(Delta psi)v^x - cos(Delta psi)v^y \


def get_arc_bounding_box(psi_min, psi_max, speed):
    """
    Calculates the minimum bounding box for a circular arc
    defined by two angles (psi_min and psi_max) and radius rho.

    Args:
        psi_min: The starting angle in radians.
        psi_max: The ending angle in radians.
        speed: The radius (e.g., 200.0 for velocity magnitude).

    Returns:
        A dictionary with the coordinates of the bounding box.
    """

    x_start = math.cos(psi_min)
    y_start = math.sin(psi_min)
    x_end = math.cos(psi_max)
    y_end = math.sin(psi_max)

    # Initialize the bounding box limits with the endpoints' coordinates
    vx_lower = min(x_start, x_end)
    vx_upper = max(x_start, x_end)
    vy_lower = min(y_start, y_end)
    vy_upper = max(y_start, y_end)

    # Check critical angles where cos or sin reach their extrema
    # We need to check if these angles fall within [psi_min, psi_max]

    # x = 1 at θ = 0, ±2π, ±4π, ...
    for k in range(-2, 3):
        theta = k * 2 * math.pi
        if psi_min <= theta <= psi_max:
            vx_upper = 1.0

    # x = -1 at θ = π, ±π, ±3π, ...
    for k in range(-2, 3):
        theta = math.pi + k * 2 * math.pi
        if psi_min <= theta <= psi_max:
            vx_lower = -1.0

    # y = 1 at θ = π/2, π/2±2π, ...
    for k in range(-2, 3):
        theta = math.pi / 2 + k * 2 * math.pi
        if psi_min <= theta <= psi_max:
            vy_upper = 1.0

    # y = -1 at θ = 3π/2, 3π/2±2π, ...
    for k in range(-2, 3):
        theta = 3 * math.pi / 2 + k * 2 * math.pi
        if psi_min <= theta <= psi_max:
            vy_lower = -1.0

    return {
        "vx_lower": vx_lower * speed,
        "vx_upper": vx_upper * speed,
        "vy_lower": vy_lower * speed,
        "vy_upper": vy_upper * speed
    }
    # dx = np.cos(u) * (x) + np.sin(u) * (y)
    # dy = -np.sin(u) * (x) + np.cos(u) * (y)


# cos(Delta psi)x + sin(Delta psi) y -x' = - cos(Delta psi)v^x -sin(Delta psi)v^y + 200
def compute_equation_info_xup(cosdth, sindth, bounding_box):
    assert bounding_box["vx_lower"] <= bounding_box["vx_upper"]
    assert bounding_box["vy_lower"] <= bounding_box["vy_upper"]
    x_lower = bounding_box["vx_lower"]
    y_lower = bounding_box["vy_lower"]
    x_upper = bounding_box["vx_upper"]
    y_upper = bounding_box["vy_upper"]

    max_vx = max(-cosdth * x_upper, -cosdth * x_lower)
    max_vy = max(-sindth * y_upper, -sindth * y_lower)

    scalar = max_vx + 200 + max_vy

    return [cosdth, sindth, -1.0], scalar


def compute_equation_info_xlo(cosdth, sindth, bounding_box):
    assert bounding_box["vx_lower"] <= bounding_box["vx_upper"]
    assert bounding_box["vy_lower"] <= bounding_box["vy_upper"]

    min_vx = min(-cosdth * bounding_box["vx_upper"], -cosdth * bounding_box["vx_lower"])
    min_vy = min(-sindth * bounding_box["vy_upper"], -sindth * bounding_box["vy_lower"])
    scalar = min_vx + 200 + min_vy

    return [cosdth, sindth, -1.0], scalar


# -sin(Delta psi)x + cos(Delta psi)y - y' = +sin(Delta psi) v^x - cos(Delta psi)v^y
def compute_equation_info_ylo(cosdps, sindps, bounding_box):
    assert bounding_box["vx_lower"] <= bounding_box["vx_upper"]
    assert bounding_box["vy_lower"] <= bounding_box["vy_upper"]

    min_vx = min(sindps * bounding_box["vx_upper"], sindps * bounding_box["vx_lower"])
    min_vy = min(-cosdps * bounding_box["vy_upper"], -cosdps * bounding_box["vy_lower"])
    scalar = min_vx + min_vy

    return [-sindps, cosdps, -1.0], scalar


def compute_equation_info_yup(cosdps, sindps, bounding_box):
    assert bounding_box["vx_lower"] <= bounding_box["vx_upper"]
    assert bounding_box["vy_lower"] <= bounding_box["vy_upper"]

    max_vx = max(sindps * bounding_box["vx_upper"], sindps * bounding_box["vx_lower"])
    max_vy = max(-cosdps * bounding_box["vy_upper"], -cosdps * bounding_box["vy_lower"])

    scalar = max_vx + max_vy

    return [-sindps, cosdps, -1.0], scalar

def getthetarho(x, y):
    rho = math.hypot(x, y)
    theta = math.atan2(y, x)        # angle from x-axis
    return theta, rho
#
# # --- Example Usage ---
# # The arc from 3 degrees to 4.5 degrees (very small arc in the first quadrant)
# a_deg = 180.0
# b_deg = 181.5
# bounding_box = get_arc_bounding_box(math.radians(a_deg), math.radians(b_deg), 200.0)
#
# print(f"Bounding Box for arc from {a_deg}° to {b_deg}°:")
# print(bounding_box)
#
#
# turn = math.radians(3.0)
# m, n = math.cos(turn), math.sin(turn)
#
# yL1, yC1 = compute_equation_info_yup(m, n, bounding_box)
# yA1, yB1, yD1 = yL1
# yL2, yC2 = compute_equation_info_ylo(m, n, bounding_box)
# yA2, yB2, yD2 = yL2
#
# xL1, xC1 = compute_equation_info_xup(m, n, bounding_box)
# xA1, xB1, xD1 = xL1
# xL2, xC2 = compute_equation_info_xlo(m, n, bounding_box)
# xA2, xB2, XD2 = xL2
# verbose = False
# if verbose:
#     print(f"lower bound x eq.: {xA2}x +{xB2}y {XD2}x'= {xC2}")
#     print(f"upper bound x eq.: {xA1}x +{xB1}y {xD1}x'= {xC1}")
#     print(f"lower bound y eq.: {yA2}x {yB2}y {yD2}y'= {yC2}")
#     print(f"upper bound y eq.: {yA1}x {yB1}y {yD1}y'= {yC1}")
# import numpy as np
# import matplotlib.pyplot as plt
#
# # --- 1. Define a range for X-values ---
# # We'll center the plot around the X-intercepts, which are near 200.
# x_range = np.linspace(200, 201.5, 100)  # 100 points between 200 and 201.5
#
# # --- 2. Calculate Y-values (Convert Ax + By = C to y = (-A/B)x + C/B) ---
#
# # Line 1
# # Slope (m1) = -A1 / B1
# # Y-intercept (b1) = C1 / B1
# y1 = (-yA1 / yB1) * x_range + (yC1 / yB1)
#
# # Line 2
# # Slope (m2) = -A2 / B2 (Same slope as Line 1)
# # Y-intercept (b2) = C2 / B2
# y2 = (-yA2 / yB2) * x_range + (yC2 / yB2)
#
# # --- 3. Plotting ---
# plt.figure(figsize=(10, 8))
#
# # Plot Line 1
# plt.plot(x_range, y1, label=f'Line 1: {yA1:.4f}x + {yB1:.4f}y = {yC1:.4f}', color='blue')
#
# # Plot Line 2
# plt.plot(x_range, y2, label=f'Line 2: {yA2:.4f}x + {yB2:.4f}y = {yC2:.4f}', color='red', linestyle='--')
#
# # --- 4. Customizing the Plot ---
# plt.title('Plot of Two Parallel Linear Equations')
# plt.xlabel('X-axis')
# plt.ylabel('Y-axis')
# plt.legend()
# plt.grid(True)
# # This command is crucial because the y-range is much larger than the x-range.
# # It makes the plot look less stretched vertically.
# plt.gca().set_aspect(abs(x_range.max() - x_range.min()) / (abs(y1.max() - y1.min())))
# # A more common way to visualize parallel lines is to manually set equal scales, but
# # due to the extreme steepness, we'll zoom in on the relevant area:
# plt.xlim(200.5, 201)
# plt.ylim(3700, 3900)
