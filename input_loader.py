import numpy


def load_input_to_list(file_name: '', list_of_points):
    with open(file_name) as f:
        lines = f.read().splitlines()

    i = 0
    for line in lines:
        line = line.split(" ")
        if line[0] == "R" or line[0] == "0":
            line = [0, int(line[1]), int(line[2])]
        elif line[0] == "G" or line[0] == "1":
            line = [1, int(line[1]), int(line[2])]
        elif line[0] == "B" or line[0] == "2":
            line = [2, int(line[1]), int(line[2])]
        elif line[0] == "P" or line[0] == "3":
            line = [3, int(line[1]), int(line[2])]

        list_of_points[i] = line
        i += 1
