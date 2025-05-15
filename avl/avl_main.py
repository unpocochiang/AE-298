import os
import subprocess
import matplotlib.pyplot as plt
import re
from numpy import linspace
import sys

parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.insert(0, parent_dir)

# Step 2: Now you can import python_file_1
import airfoil

def compute_sref(sections):
    area = 0
    for i in range(len(sections) - 1):
        dy = abs(sections[i+1]['y'] - sections[i]['y'])
        chord_avg = 0.5 * (sections[i]['chord'] + sections[i+1]['chord'])
        area += dy * chord_avg
    return 2 * area  # Full span (mirror image)

def compute_bref(sections):
    return 2 * max(abs(sec['y']) for sec in sections)

def compute_cref(sections):
    Sref = compute_sref(sections)
    mac_numerator = 0
    for i in range(len(sections) - 1):
        c1 = sections[i]['chord']
        c2 = sections[i+1]['chord']
        dy = abs(sections[i+1]['y'] - sections[i]['y'])
        mac_numerator += (dy * (c1**2 + c1*c2 + c2**2)) / 3
    return mac_numerator * 2 / Sref

def compute_xyz_ref(sections):
    area_total = 0
    x_qc_total = 0
    y_qc_total = 0
    z_qc_total = 0

    for i in range(len(sections) - 1):
        sec1, sec2 = sections[i], sections[i+1]
        dy = abs(sec2['y'] - sec1['y'])
        chord_avg = 0.5 * (sec1['chord'] + sec2['chord'])

        x_qc = 0.5 * ((sec1['x'] + 0.25 * sec1['chord']) + (sec2['x'] + 0.25 * sec2['chord']))
        y_qc = 0.5 * (sec1['y'] + sec2['y'])
        z_qc = 0.5 * (sec1['z'] + sec2['z'])

        area = dy * chord_avg
        area_total += area
        x_qc_total += area * x_qc
        y_qc_total += area * y_qc
        z_qc_total += area * z_qc

    return (
        x_qc_total * 2 / area_total,
        y_qc_total * 2 / area_total,
        z_qc_total * 2 / area_total
    )


def write_avl_file(filename, aircraft_name, mach, surfaces):
    
    sections = surfaces[0]['sections']
    Sref = compute_sref(sections)
    Bref = compute_bref(sections)
    Cref = compute_cref(sections)
    x_ref, y_ref, z_ref = compute_xyz_ref(sections)

    with open(filename, "w") as f:
        f.write(f"{aircraft_name}\n")
        f.write(f"#Mach\n{mach:.3f}\n")
        f.write("#IYsym   IZsym   Zsym\n")
        f.write("0       0       0.0\n")
        f.write("#Sref    Cref    Bref\n")
        f.write(f"{Sref:.2f}   {Cref:.2f}   {Bref:.2f}\n")
        f.write("#Xref    Yref    Zref\n")
        f.write(f"{x_ref:.2f}     {y_ref:.2f}     {z_ref:.2f}\n")
        f.write("#\n#\n#====================================================================\n")
        
        for surf in surfaces:
            f.write("SURFACE\n")
            f.write(f"{surf['name']}\n")
            f.write("#Nchordwise  Cspace   Nspanwise   Sspace\n")
            f.write(f"{surf.get('Nchord',10)}    {surf.get('Cspace',1.0)}    {surf.get('Nspan',20)}    {surf.get('Sspace',1.0)}\n")
            f.write("#\nYDUPLICATE\n0.0\n")
            f.write("#\nANGLE\n0.0\n\n")
            
            for sec in surf['sections']:
                project_root = os.path.dirname(os.path.abspath(__file__))
                airfoil_filename = os.path.join(project_root, 'airfoils', f'{sec["airfoil"]}.dat')
                if not os.path.exists(airfoil_filename):
                    airfoil.airfoil_shape(sec['airfoil'])

                f.write("#-------------------------------------------------------------\n")
                f.write("SECTION\n")
                f.write(f"# Xle Yle Zle Chord Ainc Nspan Sspace\n")
                f.write(f"{sec['x']} {sec['y']} {sec['z']} {sec['chord']} {sec.get('a_inc', 0)} 0 0\n")
                f.write("AFILE\n")
                f.write(f"{airfoil_filename}\n")

def generate_mass_file(filepath, rho, g):
    """
    Generate a basic AVL .mass file with specified air density and gravity.
    
    Parameters:
    - filepath (str): Where to save the .mass file
    - rho (float): Air density in kg/m^3
    - g (float): Gravitational acceleration in m/s^2
    """
    content = f"""\
Lunit = 1.0 m
Munit = 1.0 kg
Tunit = 1.0 s

g = {g}
rho = {rho}

# mass x y z Ixx Iyy Izz Ixy Ixz Iyz
# Placeholder mass item (replace with real aircraft components)
10.0  0.0  0.0  0.0  0  0  0  0  0  0
"""
    with open(filepath, 'w') as f:
        f.write(content)
    #print(f"Mass file saved to {filepath}")


def plot_plane_2d(surfaces):
    fig, ax = plt.subplots()

    for surf in surfaces:
        sections = surf['sections']
        leading_edges_x = [sec['x'] for sec in sections]
        leading_edges_y = [sec['y'] for sec in sections]

        trailing_edges_x = [sec['x'] + sec['chord'] for sec in sections]
        trailing_edges_y = [sec['y'] for sec in sections]

        # Draw outline of wing: leading edge -> trailing edge (reversed) -> close
        x_outline = leading_edges_x + trailing_edges_x[::-1] + [leading_edges_x[0]]
        y_outline = leading_edges_y + trailing_edges_y[::-1] + [leading_edges_y[0]]

        ax.fill(x_outline, y_outline, color='lightblue', edgecolor='black', alpha=0.7)
        ax.plot(x_outline, y_outline, 'k-')  # outline

    ax.set_aspect('equal')
    plt.xlabel("X (ft)")
    plt.ylabel("Y (ft)")
    plt.title("2D Top View of Wing")
    plt.grid()
    plt.show()



def run_avl(avl_path, cmds):
    # Launch AVL
    process = subprocess.Popen([avl_path],
                               stdin=subprocess.PIPE,
                               stdout=subprocess.PIPE,
                               stderr=subprocess.PIPE,
                               universal_newlines=True)

    stdout, stderr = process.communicate(input=cmds)

    # Show output
    return stdout

def extract_aero_coeffs(avl_output: str):
    # Dictionary to hold extracted values
    coeffs = {}

    # Patterns to search for (can expand this list!)
    patterns = {
        'CLtot': r'CLtot\s*=\s*([-+]?\d*\.\d+|\d+)',
        'CDtot': r'CDtot\s*=\s*([-+]?\d*\.\d+|\d+)',
        'CYtot': r'CYtot\s*=\s*([-+]?\d*\.\d+|\d+)',
        'Cmtot': r'Cmtot\s*=\s*([-+]?\d*\.\d+|\d+)',
        'CXtot': r'CXtot\s*=\s*([-+]?\d*\.\d+|\d+)',
        'CZtot': r'CZtot\s*=\s*([-+]?\d*\.\d+|\d+)',
        'e':     r'e\s*=\s*([-+]?\d*\.\d+|\d+)'  # Oswald efficiency
    }

    for key, pattern in patterns.items():
        match = re.search(pattern, avl_output)
        if match:
            coeffs[key] = float(match.group(1))
        else:
            coeffs[key] = None  # Optional: None if not found

    return coeffs


def main(mach, wing_sections, alpha, rho, g):
    surfaces = [{
        'name': 'Wing',
        'Nchord': 10,
        'Cspace': 1.0,
        'Nspan': 20,
        'Sspace': 1.0,
        'sections': wing_sections
    }]


    script_dir = os.path.dirname(os.path.abspath(__file__))
    avl_filename = os.path.join(script_dir, "test_aircraft.avl")

    write_avl_file(
        avl_filename,
        aircraft_name="Aircraft Test",
        mach=mach,
        surfaces=surfaces
    )

    script_dir = os.path.dirname(os.path.abspath(__file__))
    mass_filename = os.path.join(script_dir, "mass_file.mass")

    generate_mass_file(mass_filename, rho, g)

    #plot_plane_2d(surfaces)

    # If AVL is in your path, this runs it and loads the file
    avl_path = os.path.join(os.path.dirname(__file__), 'avl')

    cmds = f"""
LOAD {avl_filename}
MASS {mass_filename}
OPER
a
a
{alpha}
x
"""

    text = run_avl(avl_path, cmds)
    results = extract_aero_coeffs(text)
    cl = results['CLtot']
    cdi = results['CDtot']
    e = results['e']
    
    # print("CLtot:", results['CLtot'])
    # print("CDtot:", results['CDtot'])
    # print("Oswald efficiency (e):", results['e'])
    return cl, cdi, e

def solve_alpha_for_cl(target_cl, mach, wing_sections, rho, g):
    surfaces = [{
        'name': 'Wing',
        'Nchord': 10,
        'Cspace': 1.0,
        'Nspan': 20,
        'Sspace': 1.0,
        'sections': wing_sections
    }]


    script_dir = os.path.dirname(os.path.abspath(__file__))
    avl_filename = os.path.join(script_dir, "test_aircraft.avl")

    write_avl_file(
        avl_filename,
        aircraft_name="Aircraft Test",
        mach=mach,
        surfaces=surfaces
    )

    script_dir = os.path.dirname(os.path.abspath(__file__))
    mass_filename = os.path.join(script_dir, "mass_file.mass")

    generate_mass_file(mass_filename, rho, g)

    #plot_plane_2d(surfaces)

    # If AVL is in your path, this runs it and loads the file
    avl_path = os.path.join(os.path.dirname(__file__), 'avl')

    cmds = f"""
LOAD {avl_filename}
MASS {mass_filename}
OPER
a
c
{target_cl}
x
"""

    text = run_avl(avl_path, cmds)
    results = extract_aero_coeffs(text)
    cl = results['CLtot']
    cdi = results['CDtot']
    e = results['e']
    

    return cl, cdi, e

