

def load_input_to_list(file_name: '', list_of_points: []):
    with open(file_name) as f:
        lines = f.read().splitlines()

    for line in lines:
        line = line.split(" ")
        if line[0] == "R":
            line = (0, int(line[1]), int(line[2]))
        elif line[0] == "G":
            line = (1, int(line[1]), int(line[2]))
        elif line[0] == "B":
            line = (2, int(line[1]), int(line[2]))
        elif line[0] == "P":
            line = (3, int(line[1]), int(line[2]))
        list_of_points.append(line)
