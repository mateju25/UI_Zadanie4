import random
import time
from math import sqrt
import bisect
import statistics
import input_loader
import gui
import kdtree


# vrati euklidovnsku vzdialenost dvoch bodov
def euclid_distance(first: [], second: []) -> float:
    return sqrt(abs(first[0] - second[0]) ** 2 + abs(first[1] - second[1]) ** 2)


root = None


def classify_kNN_kdtree(x, y, k, root):
    #global root
    colors = [0] * 4
    neighs = kdtree.search_k_tree(root, [0, x, y], k)
    for j in range(0, k):
        choice = neighs[j]
        colors[choice[0]] += 1


    max = 0
    for j in range(0, 4):
        if colors[j] > colors[max]:
            max = j

    choose = []
    for j in range(0, 4):
        if colors[j] == colors[max]:
            choose.append(j)

    #root = kdtree.clear_tree(root, neighs)

    #root = kdtree.insert_tree(root, [max, x, y])

    return random.choice(choose)


def classify(x, y, k, basepoints):
    euklid_dists = []
    for j in range(0, len(basepoints)):
        bisect.insort(euklid_dists, (euclid_distance([x, y], basepoints[j][1:]), j))

    colors = [0] * 4
    for j in range(0, k):
        choice = euklid_dists.pop(0)[1]
        colors[basepoints[choice][0]] += 1

    max = 0
    for j in range(0, 4):
        if colors[j] > colors[max]:
            max = j

    choose = []
    for j in range(0, 4):
        if colors[j] == colors[max]:
            choose.append(j)

    return random.choice(choose)


def classify_weighted(x, y, k, basepoints):
    euklid_dists = []
    for j in range(0, len(basepoints)):
        bisect.insort(euklid_dists, (euclid_distance([x, y], basepoints[j][1:]), j))

    colors = [0] * 4
    for j in range(0, k):
        choice = euklid_dists.pop(0)
        if basepoints[choice[1]][0] == 'R':
            colors[0] += (1 / (choice[0]+0.001))
        elif basepoints[choice[1]][0] == 'G':
            colors[1] += (1 / (choice[0]+0.001))
        elif basepoints[choice[1]][0] == 'B':
            colors[2] += (1 / (choice[0]+0.001))
        elif basepoints[choice[1]][0] == 'P':
            colors[3] += (1 / (choice[0]+0.001))

    max = 0
    for j in range(0, 4):
        if colors[j] > colors[max]:
            max = j

    return max


def create_new_points_gauss(number_of_points, basepoints):
    median = {}
    for x in basepoints:
        if x[0] not in median:
            median[x[0]] = []
        median[x[0]].append(x[1:3])
    for group in median:
        x = []
        y = []
        for point in median[group]:
            x.append(point[0])
            y.append(point[1])
        x = statistics.median(x)
        y = statistics.median(y)
        median[group] = (x, y)
    points = []
    type = -1
    for i in range(0, number_of_points):
        type = (type + 1) % 4
        x = random.gauss(median[type][0], 1400)
        y = random.gauss(median[type][1], 1400)
        points.append((type, x, y))

    return points


def create_new_points_random(number_of_points):
    points = []
    type = 0
    for i in range(0, number_of_points):
        type = (type + 1) % 4

        if type == 0:
            x = random.randint(-5000, 500)
            y = random.randint(-5000, 500)
            if random.random() < 0.01:
                while x < 500 and y < 500:
                    x = random.randint(-5000, 5000)
                    y = random.randint(-5000, 5000)

        elif type == 1:
            x = random.randint(-500, 5000)
            y = random.randint(-5000, 500)
            if random.random() < 0.01:
                while x > -500 and y < 500:
                    x = random.randint(-5000, 5000)
                    y = random.randint(-5000, 5000)
        elif type == 2:
            x = random.randint(-5000, 500)
            y = random.randint(-500, 5000)
            if random.random() < 0.01:
                while x < 500 and y > -500:
                    x = random.randint(-5000, 5000)
                    y = random.randint(-5000, 5000)
        else:
            x = random.randint(-500, 5000)
            y = random.randint(-500, 5000)
            if random.random() < 0.01:
                while x > -500 and y > -500:
                    x = random.randint(-5000, 5000)
                    y = random.randint(-5000, 5000)

        points.append((type, x, y))
    return points


def num_of_errors(new_points, k_nn, choice):
    global root
    basepoints = []
    input_loader.load_input_to_list("dataset", basepoints)
    base = len(basepoints)

    draw = [x for x in basepoints]

    #points = create_new_points_random(new_points)
    points = create_new_points_gauss(new_points, basepoints)

    if choice == 2:
        for i in range(0, base):
            root = kdtree.insert_tree(root, points[i])

    errors = 0
    for i in range(base, len(points)):
        if i % 1000 == 0:
            print(i)
        type = points[i][0]
        x = points[i][1]
        y = points[i][2]

        if choice == 0:
            expected_type = classify(x, y, k_nn, basepoints)
        elif choice == 1:
            expected_type = classify_weighted(x, y, k_nn, basepoints)
        elif choice == 2:
            expected_type = classify_kNN_kdtree(x, y, k_nn)

        if expected_type != type:
            errors += 1

        draw.append((expected_type, x, y))
    gui.make_gui(draw)
    return errors



# sum = 0
#
# for k in range(1, 21):
#     sum = 0
#     for i in range(0, 100):
#         sum += num_of_errors(40000, k)
#
#     print("K: ", k, "Errors: ", sum/100)
# random.seed(1)
start = time.time()
print("Chyby: ", num_of_errors(40000, 15, 1))
end = time.time()
print("Cas: ", end - start)
