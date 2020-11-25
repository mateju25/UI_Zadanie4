import random
from math import sqrt
import bisect

import input_loader
import gui

# vrati euklidovnsku vzdialenost dvoch bodov
def euclid_distance(first: [], second: []) -> float:
    return sqrt(abs(first[0] - second[0]) ** 2 + abs(first[1] - second[1]) ** 2)


def classify(x, y, k, basepoints):
    euklid_dists = []
    for j in range(0, len(basepoints)):
        bisect.insort(euklid_dists, (euclid_distance([x, y], basepoints[j][1:]), j))

    colors = [0] * 4
    for j in range(0, k):
        choice = euklid_dists.pop(0)[1]
        if basepoints[choice][0] == 'R':
            colors[0] += 1
        elif basepoints[choice][0] == 'G':
            colors[1] += 1
        elif basepoints[choice][0] == 'B':
            colors[2] += 1
        elif basepoints[choice][0] == 'P':
            colors[3] += 1

    max = 0
    for j in range(0, 4):
        if colors[j] > colors[max]:
            max = j

    choose = []
    for j in range(0, 4):
        if colors[j] == colors[max]:
            choose.append(j)

    max = random.choice(choose)

    return max


def num_of_errors(new_points, k_nn):
    basepoints = []
    input_loader.load_input_to_list("dataset", basepoints)
    points = []
    last_type = None
    errors = 0
    for i in range(0, new_points):
        rand_type = random.randint(0, 3)
        while rand_type == last_type:
            rand_type = random.randint(0, 3)
        last_type = rand_type

        if rand_type == 0:
            x = random.randint(-5000, 500)
            y = random.randint(-5000, 500)
            if random.random() < 0.01:
                while x < 500 and y < 500:
                    x = random.randint(-5000, 5000)
                    y = random.randint(-5000, 5000)

        elif rand_type == 1:
            x = random.randint(-500, 5000)
            y = random.randint(-5000, 500)
            if random.random() < 0.01:
                while x > -500 and y < 500:
                    x = random.randint(-5000, 5000)
                    y = random.randint(-5000, 5000)
        elif rand_type == 2:
            x = random.randint(-5000, 500)
            y = random.randint(-500, 5000)
            if random.random() < 0.01:
                while x < 500 and y > -500:
                    x = random.randint(-5000, 5000)
                    y = random.randint(-5000, 5000)
        else: # rand_type == 3:
            x = random.randint(-500, 5000)
            y = random.randint(-500, 5000)
            if random.random() < 0.01:
                while x > -500 and y > -500:
                    x = random.randint(-5000, 5000)
                    y = random.randint(-5000, 5000)

        expected_type = classify(x, y, k_nn, basepoints)

        if expected_type != rand_type:
            errors += 1

        if expected_type == 0:
            expected_type = 'R'
        elif expected_type == 1:
            expected_type = 'G'
        elif expected_type == 2:
            expected_type = 'B'
        elif expected_type == 3:
            expected_type = 'P'

        points.append((expected_type, x, y))

    return errors
    gui.make_gui(points)


sum = 0
k = 1
for i in range(0, 100):
    sum += num_of_errors(40000, k)

print("K: ", k, "Errors: ", sum/100)
