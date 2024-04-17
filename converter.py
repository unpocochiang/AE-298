import numpy as np
def first():
    matlab_array = '''5.8133507	0.1991607
        6.235988	0.18024334
        6.658267	0.15938659
        7.1280737	0.13949862
        7.7872734	0.11960698
        8.588518	0.09971258
        9.626504	0.07981359
        10.760263	0.065730944
        11.658536	0.05844077
        12.887979	0.049689624
        14.259555	0.041420568
        15.678749	0.03460514
        17.098122	0.028759412
        19.038326	0.022903582
        21.073498	0.018500458
        22.682713	0.015075298
        24.907724	0.013092746'''

    # Split the MATLAB-style array into lines and then into elements
    rows = [line.split() for line in matlab_array.split('\n')]

    # Convert elements into floats
    rows_float = [[float(entry) for entry in row] for row in rows]

    # Convert the list of lists into a NumPy array
    np_array = np.array(rows_float)

    # Print the NumPy array in the original format
    for row in np_array:
        print("[", end="")
        for i in range(len(row)):
            elem = row[i]
            if i < len(row) - 1:
                print(f'{elem},', end="")
            else: 
                print(f'{elem}', end="")
            if i < len(row) - 1:
                print("\t", end="")
        print("],")

import numpy as np

# Your original structured array
