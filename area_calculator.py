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

# Function to find the linear equation
def find_linear_equation(x1, y1, x2, y2):
    slope = (y2 - y1) / (x2 - x1)
    intercept = y1 - slope * x1
    return slope, intercept

# Example usage
filename = 'n0012.txt'
coordinates = read_airfoil_data(filename)

# Determine the index to split the array
split_index = len(coordinates) // 2

# Split the array into two lists
upper_surface = coordinates[:split_index]
lower_surface = coordinates[split_index:]


'''
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

#Horizontal Stab
length = 16.858332177318598 - 14.28583225600806
width = 12.9791667/2
upper_surface_scaled = scale_coordinates(upper_surface, length)
lower_surface_scaled = scale_coordinates(lower_surface, length)
wetted_honrizontal_area = (calculate_perimeter(upper_surface_scaled)+calculate_perimeter(lower_surface_scaled)) * width

print(wetted_honrizontal_area)

#vertical
x_coord = [-5.872641509433962, -4.976415094339623, -4.10377358490566, -3.419811320754717, -2.8537735849056607, -2.2877358490566038, -1.768867924528302, -1.2971698113207548, -0.8962264150943396, -0.5188679245283019, -0.18867924528301888, 0.14150943396226418, 0.6603773584905661, 1.179245283018868]
y_coord = [3.0592485549132946, 3.206936416184971, 3.3546242774566473, 3.4601156069364163, 3.6078034682080924, 3.839884393063584, 4.15635838150289, 4.557225433526011, 5.10578034682081, 5.6754335260115605, 6.160693641618497, 6.645953757225434, 7.004624277456648, 7.067919075144508]

x1 = 1.5566037735849059
y1 = 3.038150289017341
x2 = 2.1226415094339623
y2 = 7.152312138728323

y = sp.symbols('y')
lower_slope, lower_intercept = find_linear_equation(x1,y1,x2,y2)
lower_equation = (y - lower_intercept)/lower_slope

veritcal_reference_area = 0
vertical_wetted_area = 0
increment = 0.001

for i in range(len(x_coord)-1):
    x1 = x_coord[i]
    y1 = y_coord[i]
    x2 = x_coord[i+1]
    y2 = y_coord[i+1]
    upper_slope, upper_intercept = find_linear_equation(x1,y1,x2,y2)
    upper_equation = (y-upper_intercept) / upper_slope
    for j in np.arange(y1, y2+increment, increment):
        upper_x_coord = upper_equation.subs(y,j)
        lower_x_coord = lower_equation.subs(y,j)
        distance = lower_x_coord - upper_x_coord
        upper_surface_scaled = scale_coordinates(upper_surface, distance)
        lower_surface_scaled = scale_coordinates(lower_surface, distance)
        vertical_wetted_area += (calculate_perimeter(upper_surface_scaled)+calculate_perimeter(lower_surface_scaled)) * increment
        veritcal_reference_area += distance*increment

print(vertical_wetted_area)
print(veritcal_reference_area)

#fuselage planform area #half of the aircraft
x_coord = [17.37735378296433, 17.001184284905683, 16.875794452219466, 16.786230286015027, 16.696666119810587, 16.58918912036526, 16.517537787401707, 16.46379928767904, 16.39214795471549, 16.32049662175194, 16.2309324555475, 16.177193955824833, 16.12345545610217, 16.015978456656843, 15.998065623415954, 15.926414290452403, 15.890588623970626, 15.818937291007074, 15.76519879128441, 15.729373124802635, 15.711460291561746, 15.657721791839082, 15.657721791839071, 15.603983292116418, 15.58607045887553, 15.568157625634642, 15.550244792393753, 15.514419125911978, 15.514419125911978, 15.514419125911978, 15.514419125911978, 15.532331959152867, 15.532331959152867, 15.514419125911978, 15.514419125911978, 15.550244792393753, 15.550244792393753, 15.550244792393753, 15.603983292116418, 15.603983292116418, 15.639808958598195, 15.639808958598195, 15.67563462507997, 15.747285958043522, 15.783111624525299, 15.818937291007074, 15.872675790729739, 15.980152790175067, 16.21301962230661, 17.341528116482554]
y_coord = [16.042380701485566, 15.642853957507716, 15.043563841540944, 14.51691495175196, 13.953945448874084, 13.318334719818415, 12.846166749662776, 12.410319392596032, 12.010792648618184, 11.55678498500699, 11.048296401762457, 10.594288738151265, 10.122120767995625, 9.631792491295538, 9.214105440773242, 8.705616857528707, 8.269769500461962, 7.779441223761875, 7.289112947061788, 6.835105283450596, 6.417418232928299, 6.0542121020393465, 5.6546853580614975, 5.146196774816962, 4.655868498116876, 4.274502060683474, 3.911295929794521, 3.4572882661833293, 2.9306393763943466, 2.3858301800609167, 1.9863034360830678, 1.5686163855607713, 1.0782881088606842, 0.6242804452494923, 0.11579186200495756, -0.3018951885173389, -0.737742545584083, -1.2099105157397225, -1.5549563400842283, -1.9181624709731817, -2.3176892149510304, -2.699055652384432, -3.0804220898178327, -3.443628220706786, -3.897635884317978, -4.333483241384722, -4.787490904995914, -5.187017648973763, -5.477582553684925, -5.5139031667738205]

eq1 = 17.37735378296433
increment = 0.001
planform_area = 0
y = sp.symbols('y')
for i in range(len(x_coord)-1):
    print(i)
    x1 = x_coord[i]
    y1 = y_coord[i]
    x2 = x_coord[i+1]
    y2 = y_coord[i+1]
    if x1 == x2:
        print('vertical line')
        print(abs(y2-y1)*abs(x2-eq1))
        planform_area += abs(y2-y1)*abs(x2-eq1)
    else:
        upper_slope, upper_intercept = find_linear_equation(x1,y1,x2,y2)
        upper_equation = (y-upper_intercept) / upper_slope
        for j in np.arange(y2, y1+increment, increment):
            upper_x_coord = upper_equation.subs(y,j)
            lower_x_coord = eq1
            distance = abs(lower_x_coord - upper_x_coord)
            print(distance*increment)
            planform_area += distance*increment

print(f'final area: {planform_area}')
# planform_area = 31.2239431980914 #remember this is half of the area
'''
#fuselage maxfront #half of the area
x_coord = [17.413179449446105, 16.92953295194213, 16.46379928767904, 16.05180412313862, 15.890588623970626, 15.711460291561746, 15.657721791839082, 15.58607045887553, 15.568157625634642, 15.568157625634642, 15.603983292116418, 15.621896125357306, 15.639808958598195, 17.39526661620522]
y_coord = [-12.015292909686087, -12.033453216230535, -12.087934135863877, -12.215056281675011, -12.687224251830651, -13.159392221986291, -13.613399885597483, -14.067407549208674, -14.539575519364314, -15.029903796064401, -15.538392379308936, -15.919758816742338, -16.2103237214535, -16.301125254175737]

eq1 = 17.413179449446105
increment = 0.001
maxfront_area = 0
y = sp.symbols('y')
for i in range(len(x_coord)-1):
    print(i)
    x1 = x_coord[i]
    y1 = y_coord[i]
    x2 = x_coord[i+1]
    y2 = y_coord[i+1]
    if x1 == x2:
        print('vertical line')
        print(abs(y2-y1)*abs(x2-eq1))
        maxfront_area += abs(y2-y1)*abs(x2-eq1)
    else:
        upper_slope, upper_intercept = find_linear_equation(x1,y1,x2,y2)
        upper_equation = (y-upper_intercept) / upper_slope
        for j in np.arange(y2, y1+increment, increment):
            upper_x_coord = upper_equation.subs(y,j)
            lower_x_coord = eq1
            distance = abs(lower_x_coord - upper_x_coord)
            print(distance*increment)
            maxfront_area += distance*increment

print(f'final area: {maxfront_area}')