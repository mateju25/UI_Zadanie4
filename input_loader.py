

def load_input_to_list(file_name: '', list_of_points: []):
    with open(file_name) as f:
        lines = f.read().splitlines()

    for line in lines:
        line = line.split(" ")
        line = (line[0], int(line[1]), int(line[2]))
        list_of_points.append(line)
