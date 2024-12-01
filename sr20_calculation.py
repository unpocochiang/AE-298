import numpy as np
from scipy.optimize import curve_fit
import matplotlib.pyplot as plt

def read_airfoil_data(filename):
    with open(filename, 'r') as file:
        lines = file.readlines()
    
    coordinates = []
    for line in lines[2:]:  # Skip the first line
        parts = line.strip().split()
        if len(parts) == 2:
            x, y = map(float, parts)
            coordinates.append((x, y))
    
    return np.array(coordinates)

coordinates = read_airfoil_data('marske7.txt')

# Determine the index to split the array
split_index = len(coordinates) // 2

upper_surface = coordinates[:split_index]
lower_surface = coordinates[split_index:]

x_top = upper_surface[:, 0]  
y_top = upper_surface[:, 1]
x_bottom = lower_surface[:, 0]  
y_bottom = lower_surface[:, 1]

leading_edge_indices = np.where(x_top <= 0.015)

top_x_le = x_top[leading_edge_indices]
bottom_x_le = x_bottom[leading_edge_indices]
top_y_le = y_top[leading_edge_indices]
bottom_y_le = y_bottom[leading_edge_indices]
# Combine the leading-edge points from top and bottom surfaces
x_le = np.concatenate((top_x_le, bottom_x_le))
y_le = np.concatenate((top_y_le, bottom_y_le))

print(x_le, y_le)
# Circle equation: (x - xc)^2 + (y - yc)^2 = r^2
def circle_equation(coords, xc, yc, r):
    x, y = coords
    return (x - xc)**2 + (y - yc)**2 - r**2

# Initial guess for (xc, yc, r)
initial_guess = (0.0, 0.0, 0.08)

# Fit the circle to the leading edge points
params, _ = curve_fit(lambda coords, xc, yc, r: circle_equation(coords, xc, yc, r), 
                      (x_le, y_le), np.zeros_like(x_le), p0=initial_guess)

xc, yc, r = params

# Output leading-edge radius
print(f"Leading-edge radius (RLE): {r:.4f}")

# Plot the airfoil and the fitted circle
theta = np.linspace(0, 2 * np.pi, 100)
circle_x = xc + r * np.cos(theta)
circle_y = yc + r * np.sin(theta)

plt.figure(figsize=(8, 6))
plt.plot(x_top, y_top, label="Top Surface", color="blue")
plt.plot(x_bottom, y_bottom, label="Bottom Surface", color="green")
plt.plot(circle_x, circle_y, 'r--', label="Fitted Circle")
plt.scatter(x_le, y_le, color='purple', label="Leading Edge Points")
plt.title("Airfoil and Fitted Circle at Leading Edge")
plt.xlabel("x")
plt.ylabel("y")
plt.legend()
plt.axis('equal')
plt.grid(True)
plt.show()
