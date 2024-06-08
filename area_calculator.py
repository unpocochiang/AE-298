import numpy as np
import sympy as sp
from sympy import Symbol

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

def scale_coordinates(coordinates, scale_factor):
    return coordinates * scale_factor

def calculate_perimeter(coordinates):
    perimeter = 0.0
    num_points = len(coordinates)
    
    for i in range(num_points - 1):
        x1, y1 = coordinates[i]
        x2, y2 = coordinates[i + 1]
        
        # Ensure coordinates are floats
        x1, y1, x2, y2 = float(x1), float(y1), float(x2), float(y2)
        
        distance = np.sqrt((x2 - x1)**2 + (y2 - y1)**2)
        perimeter += distance
    
    return perimeter

# Example usage
filename = 'n0012.txt'
coordinates = read_airfoil_data(filename)

# Determine the index to split the array
split_index = len(coordinates) // 2

# Split the array into two lists
upper_surface = coordinates[:split_index]
lower_surface = coordinates[split_index:]
upper_perimeter = calculate_perimeter(upper_surface)
lower_perimeter = calculate_perimeter(lower_surface)


area = 0
start = 13.1
finish = 15.639
increment = 0.001
for i in np.arange(start, finish + increment, increment):
    # Define the symbolic variable
    x = sp.Symbol('x')

    x_pos = i
    top_equation = 5.27
    bottom_equation = -0.372*x + 4.873  # Example equation for the bottom of the airfoil
    # Calculate the y-coordinate of the bottom equation at x = 0
    bottom_y_coord = bottom_equation.subs(x,x_pos)
    top_y_coord = top_equation
    length = top_y_coord - bottom_y_coord
    upper_surface_scaled = scale_coordinates(upper_surface, length)
    lower_surface_scaled = scale_coordinates(lower_surface, length)
    temp_area = (calculate_perimeter(upper_surface_scaled)+calculate_perimeter(lower_surface_scaled)) * increment
    area += temp_area
print(area)

start = 8.855
finish = 13.1
width = finish-start
length = 5.27
upper_surface_scaled = scale_coordinates(upper_surface, length)
lower_surface_scaled = scale_coordinates(lower_surface, length)
temp_area = (calculate_perimeter(upper_surface_scaled)+calculate_perimeter(lower_surface_scaled)) * length
area += temp_area
print(area)

start = 0.3
finish = 8.855
increment = 0.001
for i in np.arange(start, finish + increment, increment):
    # Define the symbolic variable
    x = sp.Symbol('x')
    x_pos = i
    top_equation = 0.109*x + 4.301
    bottom_equation = -0.1*x + 0.884  # Example equation for the bottom of the airfoil
    # Calculate the y-coordinate of the bottom equation at x = 0
    bottom_y_coord = bottom_equation.subs(x,x_pos)
    top_y_coord = top_equation.subs(x,x_pos)
    length = top_y_coord - bottom_y_coord
    upper_surface_scaled = scale_coordinates(upper_surface, length)
    lower_surface_scaled = scale_coordinates(lower_surface, length)
    temp_area = (calculate_perimeter(upper_surface_scaled)+calculate_perimeter(lower_surface_scaled)) * increment
    area += temp_area

print(area)
