import numpy as np
import sympy as sp
from sympy import Symbol
from scipy.interpolate import interp1d
import CD_lg
import Piper_Archer_III_data
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

#wing
def wing_area(airfoil_filename):
    area = 0
    start = 13.1
    finish = 15.639
    increment = 0.001

    coordinates = read_airfoil_data(airfoil_filename)

    # Determine the index to split the array
    split_index = len(coordinates) // 2
    # Split the array into two lists
    upper_surface = coordinates[:split_index]
    lower_surface = coordinates[split_index:]

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
def horizontal_stab_area():
    length = 16.858332177318598 - 14.28583225600806
    width = 12.9791667/2
    upper_surface_scaled = scale_coordinates(upper_surface, length)
    lower_surface_scaled = scale_coordinates(lower_surface, length)
    print(length)
    print(calculate_perimeter(upper_surface_scaled)+calculate_perimeter(lower_surface_scaled))
    wetted_honrizontal_area = (calculate_perimeter(upper_surface_scaled)+calculate_perimeter(lower_surface_scaled)) * width
    S_h = (16.858332177318598 - 14.28583225600806)*12.9791667
    print(S_h)
    print(length*width)
    print(wetted_honrizontal_area*2)

#vertical
def vertical_stab_area():
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

    print(f'vertical wetted area: {vertical_wetted_area}')
    print(veritcal_reference_area)

#fuselage planform area #half of the aircraft
def fuselage(x_planform,y_planform, x_front, y_front):
    eq1 = x_planform[0] #center line
    increment = 0.001
    planform_area = 0
    y = sp.symbols('y')
    for i in range(len(x_planform)-1):
        x1 = x_planform[i]
        y1 = y_planform[i]
        x2 = x_planform[i+1]
        y2 = y_planform[i+1]
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
                planform_area += distance*increment

    print(f'planform area: {planform_area*2}')
    # planform_area = 31.2239431980914 #remember this is half of the area
    #fuselage maxfront #half of the area
    eq1 = x_front[0] #center line
    increment = 0.001
    maxfront_area = 0
    y = sp.symbols('y')
    for i in range(len(x_front)-1):
        x1 = x_front[i]
        y1 = y_front[i]
        x2 = x_front[i+1]
        y2 = y_front[i+1]
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
                maxfront_area += distance*increment

    print(f'maxfront area: {maxfront_area*2}')


def airfoil_tc(filename):
    coordinates = read_airfoil_data(filename)

    # Determine the index to split the array
    split_index = len(coordinates) // 2

    # Split the array into two lists
    upper_surface = coordinates[:split_index]
    lower_surface = coordinates[split_index:]
    diff =[]
    for i in range(len(upper_surface)):
        upper = upper_surface[i][1]
        lower = lower_surface[i][1]
        diff.append(abs(upper-lower))
    avg_thickness = sum(diff)/len(diff)
    tc_avg = avg_thickness
    tc_max = max(diff)
    print(f'tc_avg:{tc_avg}')
    print(f'tc_max:{tc_max}')
    index = diff.index(max(diff))
    tc_max_loc = upper_surface[index][0]
    print(tc_max_loc)
    return tc_avg, tc_max, tc_max_loc
#airfoil_tc('n0012.txt')
#vertical_stab_area()
#horizontal_stab_area()

'''takeoff_weight = Piper_Archer_III_data.takeoff_weight / 250
flate_plate_area = CD_lg.flat_plate_area_calc(takeoff_weight,1)
print(flate_plate_area)
'''

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

def wetted_wing_area(top_x_data, top_y_data, bottom_x_data, bottom_y_data, high_x, low_x, increment, airfoil_filename):
    # Example usage
    coordinates = read_airfoil_data(airfoil_filename)

    # Determine the index to split the array
    split_index = len(coordinates) // 2
    # Split the array into two lists
    upper_surface = coordinates[:split_index]
    lower_surface = coordinates[split_index:]

    x_list = np.arange(low_x, high_x+increment, increment).tolist()
    
    interpolator_top = interp1d(top_x_data, top_y_data, kind='linear',fill_value="extrapolate") 
    interpolator_bottom = interp1d(bottom_x_data, bottom_y_data, kind='linear',fill_value="extrapolate")
    area = 0
    length_list = []
    for i in range(len(x_list)):
        x_val = x_list[i]
        y_top_val = interpolator_top(x_val)
        y_bottom_val = interpolator_bottom(x_val)
        length = y_top_val - y_bottom_val
        length_list.append(length)
        upper_surface_scaled = scale_coordinates(upper_surface, length)
        lower_surface_scaled = scale_coordinates(lower_surface, length)
        temp_area = (calculate_perimeter(upper_surface_scaled)+calculate_perimeter(lower_surface_scaled)) * increment
        area += temp_area
    print(length_list)
    cbar = sum(length_list) / len(length_list)
    return area, cbar

 
# data to find wing_area 
# x_data = np.array([17.012520980414767, 8.358319569832576, 8.117798050798799, 0.8519988072594379, 0.5625960073466395, 0.3636317587358099, 
#      0.21694277581858465, 0.1305710816323441, 0.08523754464720289, 0.04761594240076679, 0.019679751516311583, 0.019679751516311583, 
#      0.019679751516311583, 0.366591268353846, 0.7274962720411984, 1.147532221471562, 16.618229097013554, 17.303145389159415, 
#      17.26240628631438, 17.183289481530217, 17.117034835324343, 17.076422689517262, 17.065718800584154, 17.05150525486855, 
#      17.071084851388257, 17.071084851388257, 17.071084851388257])
# y_data = np.array([7.696645976083354, 8.102390875465106, 8.008390038780282, 8.313130341978415, 8.470747032428811, 8.699399262873477, 
#      8.986491990323746, 9.293130482624779, 9.604853609412483, 9.915867706741164, 10.236614210404063, 10.580205978211302, 
#      10.891095855811924, 10.886392254873115, 10.852081091110875, 10.89907383295324, 12.558183226890339, 13.385556402117833, 
#      12.859833389887129, 12.257663602991602, 11.691486831232575, 11.08064957791865, 10.380108932219779, 9.85893319947235, 
#      9.256725727940221, 8.663227594644939, 8.140383967796062])

# top_x = [17.012520980414767, 8.358319569832576, 8.117798050798799, 0.8519988072594379, 0.5625960073466395, 0.3636317587358099, 
#      0.21694277581858465, 0.1305710816323441, 0.08523754464720289, 0.04761594240076679, 0.019679751516311583]  
# bottom_x = [0.019679751516311583, 0.366591268353846, 0.7274962720411984, 1.147532221471562, 16.618229097013554, 17.303145389159415]
# top_y = [7.696645976083354, 8.102390875465106, 8.008390038780282, 8.313130341978415, 8.470747032428811, 8.699399262873477, 8.986491990323746, 
#      9.293130482624779, 9.604853609412483, 9.915867706741164, 10.236614210404063]
# bottom_y = [10.891095855811924, 10.886392254873115, 10.852081091110875, 10.89907383295324, 12.558183226890339, 13.385556402117833]

# wetted_area, cbar = wetted_wing_area(top_x,top_y,bottom_x,bottom_y,17.303145389159415,0.019679751516311583,0.001,'marske7.txt')
# area = shoelace_area(x_data,y_data)
# print('wing area ',area*2)
# print('wetted area ', wetted_area*2)
# print('cbar', cbar)

# exposed horizontal (unknown)
# x = [18.88708960732339, 13.019242521348357, 12.676170749591991, 12.668643607875195, 12.69851518827154, 12.768005828311432, 12.86472734235827, 13.132702615532285, 18.800171997873957]
# y = [23.64635437912924, 23.35019221580349, 23.35019221580349, 22.989505580251876, 22.619478737732162, 22.273726384093088, 21.93150522047633, 21.695035521527725, 21.03143140260768]

# exposed horizontal
x = [18.81552398278107, 18.409180539428863, 13.094816949682693, 12.837306425712233, 12.724125779282033, 12.667071746715699, 12.672912569517383, 12.672912569517383, 18.90368073873492, 18.90368073873492, 18.90368073873492, 18.882473217255455, 18.876178260221884, 18.876178260221884]
y = [4.69358095988293, 4.613769160433275, 4.009897956427171, 3.7743678813699977, 3.4189971263488865, 3.092373814089415, 2.7392959675650257, 2.424675580356331,  2.0867271038413, 2.4886037276213067, 2.8979712479323196, 3.317417727165752, 3.7251591681495313, 4.132884211694717]

# horizontal area
# x = [19.138320406207917, 18.808813191992996, 18.409180539428863, 13.094816949682693, 12.837306425712233, 12.724125779282033, 12.667071746715699, 12.672912569517383, 12.672912569517383, 19.14268118913339]
# y = [4.739266956712129, 4.685210067480716, 4.613769160433275, 4.009897956427171, 3.7743678813699977, 3.4189971263488865, 3.092373814089415, 2.7392959675650257, 2.424675580356331, 2.0821467526607207]

h_area = shoelace_area(x,y)
print('horizontal area ', h_area*2)

# x = [17.775897669667586, 23.382111434925815, 23.669084496377515, 23.994576480110023, 24.29785538308637, 24.58060740525224, 
#      24.815988509364647, 24.994076483391066, 25.070119447827043, 25.13476892984425, 25.198904353533727, 25.266571712457655, 
#      25.339707588419607, 25.391603106064498, 25.44259680586722, 25.51740780293158, 25.579165706855342, 25.642040358180708, 
#      25.70318670995597, 25.751991230328557, 25.808506625616996, 25.88253324057785, 25.92439354198886, 26.01197179803746, 24.636819240235084, 
#      24.35701197461036, 24.085247949199584, 23.820095777452288, 23.677692757598233, 23.52826131957375, 23.361238894205314, 
#      23.235097400502827, 23.08323748003358, 22.917579968155994, 22.746737557628094, 22.61167094778737, 22.46244557624771, 22.27708323373027, 
#      22.04588993237389, 21.80254757148773, 21.514116534261706, 21.19049022773585, 20.86676642738922, 20.53451191772476, 20.181282941981717, 
#      19.816261645462188, 19.473225205527456, 19.122641857557266, 18.7658654361992]
# y = [5.294284672971662, 3.397007597108141, 3.4462176492773815, 3.487327712479671, 3.5445391486271705, 3.678491971495034, 3.890995993479884, 
#      4.142093597184773, 4.45425644867855, 4.747748034709326, 5.045496069418651, 5.351013355528689, 5.653640282907684, 5.95363979819215, 
#      6.241145239701065, 6.539530098295694, 6.836189369588209, 7.135397990692539, 7.403300555022369, 7.684027930693988, 7.976258194577742, 
#      8.249917852257783, 8.54633677389036, 8.85522100951012, 8.892773076037095, 8.793105002310478, 8.678252787460549, 8.479713696999243, 
#      8.240105628747601, 8.019829273956143, 7.770776696631319, 7.511855403354878, 7.267535865487285, 7.031143757856431, 6.7620004140855565, 
#      6.503813522547813, 6.282366233515633, 6.068572129595392, 5.879994197262604, 5.721780438635244, 5.590857664899071, 5.48594811974228, 
#      5.412719535744078, 5.351639908061005, 5.3370730752523174, 5.296010260273777, 5.296010260273777, 5.296010260273777, 5.318814718179464]
# v_area = shoelace_area(x,y)
# print('vertical area ', v_area)

#horizontal side profile
#top
# x_top = [0.1292816057208989, 0.2725088895524009, 0.42140303170134064, 0.5650683156858343, 0.719058065248451, 0.8457301771001182]
# y_top = [0.7992802768927095, 0.8087556231231438, 0.802500733865871, 0.8053744945794727, 0.8015470900576371, 0.8015470900576371]

#side profile
# x_bottom = [0.14405639961406635, 0.2863287197317218, 0.42971763178869393, 0.570962193800879, 0.7130272349728933, 0.8440608413057586]
# y_bottom = [0.7666147691384736, 0.7724258260916579, 0.7762532306134935, 0.7789486031195332, 0.7886964190094629, 0.7912799934265168]

def find_possible_airfoil(x_top, x_bottom, y_top, y_bottom):
    # Interpolate y_bottom to match x_top
    interp_func = interp1d(x_bottom, y_bottom, kind='linear', fill_value="extrapolate")
    y_bottom_interp = interp_func(x_top)

    # Compute delta_y and find the max delta
    delta_y = np.abs(np.array(y_top) - y_bottom_interp)
    max_delta_index = np.argmax(delta_y)
    x_max_delta = x_top[max_delta_index]
    y_max_delta = delta_y[max_delta_index]

    print(f"x position with largest delta y: {x_max_delta}")
    print(f"Largest delta y: {y_max_delta}")
# print('Naca 0012')
# airfoil_tc('n0012.txt')
# print('Naca 0015')
# airfoil_tc('naca0015.txt')

#Fuselage side view
# x_side = [0.06280009851570074, 0.28266795364790304, 0.5075094384630597, 0.7731437618371867, 1.0952078649786643, 1.3654882269395832, 
#      1.6690356860611435, 1.9635135200710414, 2.2348087503940586, 2.5018707511805154, 2.788582684103344, 3.0809455634349763, 
#      3.384702193898343, 3.660176424150785, 3.9346656676613865, 4.219306914972998, 4.503788793643234, 4.829175290266739, 5.19272614959318, 
#      5.498773704276332, 5.756376512161095, 6.0037177503039025, 6.250171393652377, 6.499382999878004, 6.784668362115179, 7.04120760566409, 
#      7.31722191853453, 7.623162120730088, 7.933145195473896, 8.220692707037275, 8.540156002489624, 8.824540489212351, 9.12360017166182, 
#      9.429685355051964, 9.758139698021964, 10.056566332812633, 10.348113554583886, 10.64282158774244, 10.94386231094235, 
#      11.260184716087574, 11.54710803380556, 11.882032300924772, 12.175711078274436, 12.46809941231962, 12.728695915863572, 
#      13.02832445582462, 13.298644659945884, 13.62539685728785, 13.912300253925665, 14.179592453860776, 14.490680041827456, 
#      14.789710949383343, 15.096154712216585, 15.435589997268087, 15.786373657657599, 16.13493501088125, 16.436292257910562, 
#      16.739179001206416, 17.0382054818556, 17.367813034022223, 17.630957222374846, 18.068466198566686, 18.663829814041822, 
#      19.246156189271034, 19.958113460086455, 23.5824485408277, 23.31078698397485, 22.880653234353375, 22.542227284030588, 22.1602914811587, 
#      21.78154305111434, 21.498380390642165, 21.136556024930634, 20.640784529595614, 20.209119070254243, 19.853603046597193, 
#      19.44808953861501, 19.086984545243027, 18.68785242327596, 18.38634244796533, 18.04020703961596, 17.740766643189872, 
#      17.457672599771623, 17.141518417081183, 16.85331572332548, 16.518703553128965, 16.120868514826434, 15.799366628836477, 
#      15.502527040099515, 15.147343034445335, 14.801473240498261, 14.469576977565202, 14.18010154813184, 13.688294347751057, 
#      13.341933167159741, 12.952504824689811, 12.595804603489201, 11.990150643378525, 11.552258739756711, 11.195961367066248, 
#      10.662200371843136, 10.326815706426617, 9.513099344639029, 9.024709716234428, 8.494574357602628, 7.899281572634769, 7.343659405376188, 
#      6.76626349748956, 5.89322437240297, 5.067433622577768, 4.280179095618716, 3.6234784742938464, 3.307574411832236, 2.961224298507681, 
#      2.7186862541396897, 2.405823476584345, 2.1568066542537334, 1.8801891753447515, 1.4579574541915186, 1.0894573131690002, 
#      0.763860538477013, 0.4782232371567987, 0.2590249516637124]
# y_side = [3.891862084769685, 4.0618454011956855, 4.1856055998476895, 4.3063332883885685, 4.360613571274393, 4.405139142627487, 
#      4.4813845225274545, 4.539527547572491, 4.576537767780622, 4.637424884855562, 4.675980201927379, 4.724799082432365, 4.781020006978977, 
#      4.776125140114823, 4.834068332632157, 4.8809403910889, 4.906024523638536, 4.906492172955944, 4.970133682706547, 5.132649030958071, 
#      5.351525392538513, 5.497990274570078, 5.654119222451705, 5.812353622326245, 5.948635285961551, 6.058712106788763, 6.161257095437798, 
#      6.24333676109504, 6.30676607754303, 6.3726469476814005, 6.437983943723753, 6.472606474245203, 6.477536363304933, 6.494250191111701, 
#      6.51135235326354, 6.4940544788423, 6.483401550999481, 6.461673368837769, 6.459615299815341, 6.459615299815341, 6.418225245030952, 
#      6.394772734769367, 6.355896037549905, 6.3194801646020045, 6.272015819014182, 6.231649648418128, 6.192033364833248, 6.157948528020361, 
#      6.084461661054358, 6.018601392207504, 5.999306222573808, 5.949776597511526, 5.867289026282272, 5.8068819192996495, 5.747583161800576, 
#      5.6702603343543325, 5.593351592867555, 5.546071628838799, 5.47236844831188, 5.4155974692817965, 5.358517470878975, 5.287154597068251, 
#      5.185627312220096, 5.079963288035569, 4.97813110407298, 4.175667536820469, 3.4068170368051334, 3.4013988971364784, 3.3884921880018313, 
#      3.3884921880018313, 3.3511420464836896, 3.337104326444825, 3.2839529943340664, 3.25331269346262, 3.207958950190591, 3.17937259808327, 
#      3.145957303244646, 3.10273373351535, 3.0671841448756894, 2.9947067411939607, 2.952214517313476, 2.9109954532486677, 2.874592971140253, 
#      2.82577821089357, 2.782764774337735, 2.750639120348, 2.6863404293980433, 2.6575830865711407, 2.589650327797797, 2.5627944841778034, 
#      2.5176364531751743, 2.4482533634791186, 2.427151460579487, 2.3659615045192637, 2.3310649768206537, 2.2799799542489296, 
#      2.2503285153702417, 2.208536735401294, 2.171081527296422, 2.171081527296422, 2.1312612909255364, 2.139454424561369, 2.096055743854189, 
#      2.096055743854189, 2.1034001042795714, 2.1115911777862526, 2.1157093759602605, 2.1431605969050613, 2.1800472093640972, 
#      2.226433077341068, 2.296681421280787, 2.4119992106696175, 2.481707800771623, 2.547450642256837, 2.668619198436154, 2.820335349675096, 
#      2.9769031050660084, 3.217077081815483, 3.367060664437947, 3.379967373572594, 3.483089198384072, 3.5964951879202363, 3.7149340729737097]

# x = [19.12644769675297, 18.558143435259943, 17.6283539814307, 17.447092729620362, 17.366341193639382, 17.31949249375508, 17.10079497875508, 
#      17.08348638624072, 17.071421826499527, 17.03876431133802, 17.05172933390926, 17.0602303598975, 17.09582464289074, 17.214494148620922, 
#      17.29971789209217, 17.50419958964758, 17.860927929708343, 18.095579237524003, 18.279142280337595, 18.42187795526113, 
#      18.525395600118525, 18.60184188372362, 18.70227222744942, 18.767669366845077, 18.8019362198305, 19.123141438094315]
# y = [24.50732313247058, 24.484892972089604, 24.315902012222555, 24.027699807632114, 23.680399784758244, 23.331430584794, 20.77162073517848, 
#      19.793256516210565, 18.34646913712108, 16.917128794280053, 15.915954748330588, 14.898320799294154, 14.206790629202475, 
#      13.326243442015679, 12.585031185334772, 11.782489213139927, 10.219792332799889, 9.339123109920052, 8.65942769014908, 8.03087878528383, 
#      7.414397854508213, 6.835550019562217, 6.138490276623625, 5.562470957851897, 4.906816569610046, 4.8769612152835835]
# x_front = [19.13787929129712, 18.47788927364224, 18.26858499417577, 17.9571952971761, 17.707826045566968, 17.45014576390992, 
#            17.24474772335193, 17.138706759546746, 17.06975315098835, 17.045576107084948, 17.173627330097457, 17.456585853442764, 
#            17.8265636554737, 18.207145279955355, 19.143020953591105]
# y_front = [1.6581013701608083, 1.6978098562206752, 1.4665268023743818, 1.4550525359146382, 1.6571017385160718, 1.9071789421561465, 
#            2.1585325571705485, 2.481233537237094, 2.9309361054583007, 3.913466524960598, 4.256369738105446, 4.535737223809035, 
#            4.662994094238561, 4.711175264642122, 4.711175264642122]
# planform_area = shoelace_area(x,y)
# front_area = shoelace_area(x_front, y_front)
# side_area = shoelace_area(x_side, y_side)
# print('planform area ',planform_area*2)
# print('front area ', front_area*2)
# wetted_fus_area = 3.4*(side_area+planform_area)/2
# print(wetted_fus_area)

# Sweep angle calculation
# Wing
# x = [17.044581037813646, 17.006201223722393, 1.1385979596674256, 1.144799901255912]
# y = [18.195040594697257, 12.995153190442268, 17.567915089858488, 14.976600539791065]

# horizontal stab
# x = [18.800690755038335, 18.850793250958734, 13.0738857387901, 13.029369641071597]
# y = [4.700467884092393, 2.074524676620963, 4.010788883924109, 2.3925639297764976]

# left_x = (x[0] + x[1])/2
# right_x = (x[2] + x[3])/2
# left_y = (y[0] - y[1]) / 4 * 3 + y[1]
# right_y = (y[2] - y[3]) / 4 * 3 + y[3]
# print(left_y,right_y)
# print(left_x,right_x)
# dif_y = (left_y-right_y)
# dif_x = left_x-right_x
# print(dif_y,dif_x)
# angle = np.arctan(dif_y/dif_x )
# print(np.rad2deg(angle))

# Plot
plt.figure(figsize=(8, 6))
plt.plot(x, y, marker='o', linestyle='-', color='b', label='x vs y')
plt.title('Plot of x vs y')
plt.xlabel('x')
plt.ylabel('y')
plt.legend()
plt.grid(True)

# Display
plt.show()