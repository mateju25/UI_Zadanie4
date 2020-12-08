import random
import time
from heapq import heappush, nsmallest
import statistics
import numpy
import input_loader
from gui import make_gui
import kdtree


BRUTE_FORCE = True
KNN = True
RANDOM = True
ADDING = True


# vrati euklidovnsku vzdialenost dvoch bodov
def euclid_distance(first, second):
    return (first[0] - second[0]) ** 2 + (first[1] - second[1]) ** 2


def get_k_neighs_heap(x, y, k, base_points):

    neigh = []
    for j in range(0, len(base_points)):
        if base_points[j] is None:
            break
        heappush(neigh, (euclid_distance([x, y], base_points[j][1:]), base_points[j][0]))

    return nsmallest(k, neigh)


def get_k_neighs_kdtree(x, y, k, root):
    return kdtree.search_k_tree(root, [0, x, y], k)


# ohodnoti bod na zaklade datasetu pouzitim k-NN algoritmu (brute force)
def classify(x, y, k, base_points, root=None):
    global KNN, BRUTE_FORCE, RANDOM

    if BRUTE_FORCE:
        neigh = numpy.array(get_k_neighs_heap(x, y, k, base_points))
    else:
        neigh = get_k_neighs_kdtree(x, y, k, root)
        root = kdtree.clear_tree(root, neigh)
        neigh = [(euclid_distance([p[1], p[2]], [x, y]), p[0]) for p in neigh]

    if KNN:
        colors = [0] * 4
        for j in range(0, k):
            choice = neigh[j][1]
            colors[choice] += 1
    else:
        colors = [0] * 4
        for j in range(0, k):
            choice = neigh[j][1]
            colors[choice] += (1 / (neigh[j][0] + 0.001))

    maxi = colors.index(max(colors))

    if RANDOM:
        # ak viacero typov ma rovnaky pocet, tak vyber nahodne z nich jeden typ a ten pouzi
        choose = []
        for j in range(0, 4):
            if colors[j] == colors[maxi]:
                choose.append(j)

        return random.choice(choose)
    else:
        return maxi


# vytvori mediany pociatocnych bodov a vytvori normalne rozlozenie bodov okolo tohoto medianu
def create_new_points_gauss(number_of_points, base_points):
    median = {}
    for x in base_points:
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
    points = numpy.empty(number_of_points, dtype=numpy.object)
    type = -1
    for i in range(0, number_of_points):
        type = (type + 1) % 4
        x = random.gauss(median[type][0], 1200)
        while x <= -5000 or x >= 5000:
            x = random.gauss(median[type][0], 1200)

        y = random.gauss(median[type][1], 1200)
        while y <= -5000 or y >= 5000:
            y = random.gauss(median[type][1], 1200)

        points[i] = [type, x, y]

    return points


# vytvori rozlozenie bodov take, ako v zadani
def create_new_points_random(number_of_points):
    points = numpy.empty(number_of_points, dtype=numpy.object)
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

        points[i] = [type, x, y]
        #numpy.append(points, [type, x, y])
    return points


def num_of_errors(base_points, points, k_nn):
    global BRUTE_FORCE, ADDING
    root = None
    draw = numpy.copy(basepoints)

    if not BRUTE_FORCE:
        for i in range(0, len(base_points)):
            root = kdtree.insert_tree(root, base_points[i])

    errors = 0
    for i in range(0, len(points)):
        type = points[i][0]
        x = points[i][1]
        y = points[i][2]

        expected_type = classify(x, y, k_nn, base_points, root)

        if expected_type != type:
            errors += 1

        if ADDING:
            base_points[20+i] = [expected_type, x, y]
            if not BRUTE_FORCE:
                root = kdtree.insert_tree(root, (expected_type, x, y))
        draw[20+i] = [expected_type, x, y]

    return errors, draw


choice = "a" #input("Brute force/ kd-tree? a/n: ")
if choice == 'a':
    BRUTE_FORCE = True
else:
    BRUTE_FORCE = False

choice = "a" #input("Knn/ Wknn? a/n: ")
if choice == 'a':
    KNN = True
else:
    KNN = False

choice = "a" #input("Pridavat body? a/n: ")
if choice == 'a':
    ADDING = True
else:
    ADDING = False

choice = "a" #input("Random rozhodnutie o type? a/n: ")
if choice == 'a':
    RANDOM = True
else:
    RANDOM = False

num = int(input("Pocet bodov: "))
basepoints = numpy.empty(num+20, dtype=numpy.object)
input_loader.load_input_to_list("dataset", basepoints)

choice = "n" #input("Gaussove rozlozenie bodov/ zadanie? a/n: ")
if choice == 'a':
    points = create_new_points_gauss(num, basepoints)
else:
    points = create_new_points_random(num)

start = time.time()
error, draw = num_of_errors(basepoints, points, 5) #int(input("Ake k?:"))
print(error)
end = time.time()
print(end - start)
# from scipy.spatial import Voronoi, voronoi_plot_2d
# vor = Voronoi(numpy.array([x[1:] for x in draw]))
# import matplotlib.pyplot as plt
# fig = voronoi_plot_2d(vor)
# plt.show()
make_gui(draw)
# for i in range(1, 20):
#     errors = []
#     timeS = []
#     for _ in range(0, 100):
#         start = time.time()
#         errors.append(num_of_errors(basepoints, points, i, 0))
#         end = time.time()
#         timeS.append(end - start)
#     print(i, " ",  sum(errors) / len(errors), " ",  sum(timeS) / len(timeS))