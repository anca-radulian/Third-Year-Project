import numpy as np

# Method to write the data to pgm files of type P2
def generate_pgm_files_p2(file_name, axis, k, pgm_size):

    file_handle = open(file_name + '_' + str(k) + '.pgm', 'w')
    file_handle.write('P2\n')
    file_handle.write('#grapestempgm\n')
    file_handle.write(str(int(pgm_size)) + ' ' + str(int(pgm_size)) + '\n')
    file_handle.write(str(255) + '\n')
    for i in axis[k]:
        for j in i:
            value = str(j) + '\n'
            file_handle.write(value)


# Generate the digital phantom on 3 cross sections (x-plane, y-plane, z-plane)
# The number of files are established based on the maximum value and minimum value of the axis we have fixed
def determine_pgm_values(selected_axis, X_all, Y_all, Z_all, pgm_size):
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

    matrix_of_files = np.zeros([num_of_files, pgm_size, pgm_size], dtype=int)

    for index in range(num_of_files):
        points_same_z_index, = np.where(selected_axis_coord == plane_index)
        plane_index = plane_index + 1
        for q in points_same_z_index:
            if plane_coord_1[q] < pgm_size and plane_coord_2[q] < pgm_size:
                matrix_of_files[index][plane_coord_1[q]][plane_coord_2[q]] = 128

    return matrix_of_files, num_of_files


# Method to generate the files based on the created model and selected axis to create planes
# The input arrays of coordinates must be transformed in integers as they are used as indexes
def create_digital_phantom_of_models(selected_axis, X_all, Y_all, Z_all, pgm_size):
    X_all = np.array(X_all, dtype=int)
    Y_all = np.array(Y_all, dtype=int)
    Z_all = np.array(Z_all, dtype=int)

    # Shift all elements to have only positive values
    x_min = min(X_all)
    y_min = min(Y_all)
    z_min = min(Z_all)

    if x_min < 0:
        abs_val_x = abs(x_min)
        X_all = [elem + abs_val_x for elem in X_all]
    if y_min < 0:
        abs_val_y = abs(y_min)
        Y_all = [elem + abs_val_y for elem in Y_all]
    if z_min < 0:
        abs_val_z = abs(z_min)
        Z_all = [elem + abs_val_z for elem in Z_all]

    matrix_of_files, num_of_files = determine_pgm_values(selected_axis, X_all, Y_all, Z_all, pgm_size)
    for k in range(num_of_files):
        generate_pgm_files_p2('pgm_axis_' + selected_axis, matrix_of_files, k, pgm_size)
