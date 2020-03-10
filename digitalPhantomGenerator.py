import numpy as np

PGM_SIZE = 250


# Method to write the data to pgm files of type P2
def generate_pgm_files_p2(file_name, axis, k):
    file_handle = open(file_name + '_' + str(k) + '.pgm', 'w')
    file_handle.write('P2\n')
    file_handle.write('#grapestempgm\n')
    file_handle.write(str(int(PGM_SIZE)) + ' ' + str(int(PGM_SIZE)) + '\n')
    file_handle.write(str(255) + '\n')
    for i in axis[k]:
        for j in i:
            value = str(j) + '\n'
            file_handle.write(value)


# Generate the digital phantom on 3 cross sections (x-plane, y-plane, z-plane)
# The number of files are established based on the maximum value and minimum value of the axis we have fixed
def determine_pgm_values(selected_axis, X_all, Y_all, Z_all):
    num_of_files = 0
    plane_index = 0
    selected_axis_coord = []
    plane_coord_1 = []
    plane_coord_2 = []
    if selected_axis == 'x':
        num_of_files = max(X_all) - min(X_all) + 1
        plane_index = min(X_all)
        selected_axis_coord = X_all
        plane_coord_1 = Y_all
        plane_coord_2 = Z_all
    elif selected_axis == 'y':
        num_of_files = max(Y_all) - min(Y_all) + 1
        plane_index = min(Y_all)
        selected_axis_coord = Y_all
        plane_coord_1 = X_all
        plane_coord_2 = Z_all
    elif selected_axis == 'z':
        num_of_files = max(Z_all) - min(Z_all) + 1
        plane_index = min(Z_all)
        selected_axis_coord = Z_all
        plane_coord_1 = X_all
        plane_coord_2 = Y_all

    matrix_of_files = np.zeros([num_of_files, PGM_SIZE, PGM_SIZE], dtype=int)
    for index in range(num_of_files):
        points_same_z_index, = np.where(selected_axis_coord == plane_index)
        plane_index = plane_index + 1
        for q in points_same_z_index:
            matrix_of_files[index][plane_coord_1[q]][plane_coord_2[q]] = 128

    return matrix_of_files, num_of_files


# Method to generate the files based on the created model and selected axis to create planes
# The input arrays of coordinates must be transformed in integers as they are used as indexes
def create_digital_phantom_of_models(selected_axis, X_all, Y_all, Z_all):
    X_all = np.array(X_all, dtype=int)
    Y_all = np.array(Y_all, dtype=int)
    Z_all = np.array(Z_all, dtype=int)
    matrix_of_files, num_of_files = determine_pgm_values(selected_axis, X_all, Y_all, Z_all)
    for k in range(num_of_files):
        generate_pgm_files_p2('pgm_axis_' + selected_axis, matrix_of_files, k)
