import matplotlib.pyplot as plt

def shoelace_area(x, y):
    """Calculate the area enclosed by a polygon using the Shoelace formula."""
    if len(x) != len(y):
        raise ValueError("x and y must be of the same length.")
    
    # Number of vertices
    n = len(x)
    
    # Apply the Shoelace formula
    area = 0.0
    for i in range(n):
        j = (i + 1) % n  # Next vertex
        area += x[i] * y[j] - x[j] * y[i]
    
    return abs(area) / 2.0

def compute_sref(sections):
    # Build the polygon outline: first leading edges (root to tip), then trailing edges (tip to root)
    x = []
    y = []

    # Leading edge from root to tip
    for sec in sections:
        x.append(sec['x'])
        y.append(sec['y'])

    # Trailing edge from tip back to root
    for sec in reversed(sections):
        x.append(sec['x'] + sec['chord'])
        y.append(sec['y'])
    print(x)
    print(y)
    # Compute area using shoelace
    area = shoelace_area(x, y)

    # Double the area to account for both wing halves
    return 2 * area

wing_sections = [
    {"x": 0, "y": 0, "z": 0, "chord": 2.09, "airfoil": "naca652415"},
    {"x": 0.48, "y": 1.25, "z": 0, "chord": 1.61, "airfoil": "naca652415"},
    {"x": 0.48, "y": 2.51, "z": 0, "chord": 1.61, "airfoil": "naca652415"},
    {"x": 0.66, "y": 5.04, "z": 0, "chord": 1.1, "airfoil": "naca652415"},
    {"x": 0.7, "y": 5.13, "z": 0, "chord": 0.91, "airfoil": "naca652415"},
]

area = compute_sref(wing_sections)

print(area)

x = [0, 0.48, 0.48, 0.66, 0.7, 1.6099999999999999, 1.7600000000000002, 2.09, 2.09, 2.09]
y = [0, 1.25, 2.51, 5.04, 5.13, 5.13, 5.04, 2.51, 1.25, 0]

plt.figure(figsize=(8, 8))
plt.plot(x, y, 'bo-', label='Original')
plt.xlabel("X")
plt.ylabel("Y")
plt.title("Original and 180° Flipped Coordinates")
plt.axis('equal')  # Set same scale for x and y axes
plt.grid(True)
plt.legend()
plt.show()