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


# ohodnoti bod na zaklade datasetu pouzitim k-NN algoritmu (kD strom)
def classify_knn_kdtree(x, y, k, root):
    colors = [0] * 4
    # struktura vrati pole k najblizsich susedov
    neighs = kdtree.search_k_tree(root, [0, x, y], k)
    for j in range(0, k):
        choice = neighs[j]
        colors[choice[0]] += 1

    # vyber typ, ktory sa najviac opakuje
    maxi = colors.index(max(colors))

    # ak viacero typov ma rovnaky pocet, tak vyber nahodne z nich jeden typ a ten pouzi
    choose = []
    for j in range(0, 4):
        if colors[j] == colors[maxi]:
            choose.append(j)

    root = kdtree.clear_tree(root, neighs)

    return random.choice(choose)


# ohodnoti bod na zaklade datasetu pouzitim k-NN algoritmu (brute force)
def classify_knn(x, y, k, basepoints):
    euklid_dists = []
    # vytvor utriedeny zoznam vzdialenosti od bodu ku kazdemu bodu z datasetu
    for j in range(0, len(basepoints)):
        bisect.insort(euklid_dists, (euclid_distance([x, y], basepoints[j][1:]), j))

    # zrataj pocet jednotlivych typov vsetkych najblizsich susedov
    colors = [0] * 4
    for j in range(0, k):
        choice = euklid_dists.pop(0)[1]
        colors[basepoints[choice][0]] += 1

    # vyber typ, ktory sa najviac opakuje
    maxi = colors.index(max(colors))

    # ak viacero typov ma rovnaky pocet, tak vyber nahodne z nich jeden typ a ten pouzi
    choose = []
    for j in range(0, 4):
        if colors[j] == colors[maxi]:
            choose.append(j)

    return random.choice(choose)


# ohodnoti bod na zaklade datasetu pouzitim Wk-NN algoritmu (brute force)
def classify_wknn(x, y, k, basepoints):
    euklid_dists = []
    # vytvor utriedeny zoznam vzdialenosti od bodu ku kazdemu bodu z datasetu
    for j in range(0, len(basepoints)):
        bisect.insort(euklid_dists, (euclid_distance([x, y], basepoints[j][1:]), j))

    # vyrataj vzdialenost ku kazdemu bodu a cim je bod blizsie ,tym ma vacsiu vahu pri urcovani typu noveho bodu
    colors = [0] * 4
    for j in range(0, k):
        choice = euklid_dists.pop(0)
        colors[basepoints[choice[1]][0]] += (1 / (choice[0]+0.001))

    # vrat typ bodu, ktory ma najlepsie hodnotenie
    return colors.index(max(colors))


# vytvori mediany pociatocnych bodov a vytvori normalne rozlozenie bodov okolo tohoto medianu
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


# vytvori rozlozenie bodov take, ako v zadani
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
    root = None
    basepoints = []
    input_loader.load_input_to_list("dataset", basepoints)

    draw = [x for x in basepoints]

    #points = create_new_points_random(new_points)
    points = create_new_points_gauss(new_points, basepoints)

    if choice == 2:
        for i in range(0, len(basepoints)):
            root = kdtree.insert_tree(root, basepoints[i])

    errors = 0
    for i in range(0, len(points)):
        type = points[i][0]
        x = points[i][1]
        y = points[i][2]

        if choice == 0:
            expected_type = classify_knn(x, y, k_nn, basepoints)
        elif choice == 1:
            expected_type = classify_wknn(x, y, k_nn, basepoints)
        else:
            expected_type = classify_knn_kdtree(x, y, k_nn, root)

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
