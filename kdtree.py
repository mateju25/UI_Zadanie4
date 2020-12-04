from math import sqrt


class Node:
    val = None
    left = None
    right = None
    used = None


def euclid_distance(first: [], second: []) -> float:
    return sqrt((first[0] - second[0]) ** 2 + (first[1] - second[1]) ** 2)


def smaller_dist(find: [], first: Node, second: Node):
    if first is None:
        return second

    if second is None:
        return first

    if first.used:
        return second

    if second.used:
        return first

    if euclid_distance(find[1:3], first.val[1:3]) < euclid_distance(find[1:3], second.val[1:3]):
        return first
    else:
        return second


def find_node(root, find, depth=0):
    if root is None:
        return None

    act = depth % 2
    depth += 1
    if root.val[1:3] == find[1:3]:
        return root

    if root.val[act + 1] >= find[act + 1]:
        return find_node(root.left, find, depth)
    else:
        return find_node(root.right, find, depth)


def clear_tree(root, best):
    for x in best:
        bestof = find_node(root, x)
        if bestof is not None:
            bestof.used = False

    return root


def insert_tree(root, new, depth=0):
    if root is None:
        rootN = Node()
        rootN.val = new
        rootN.used = False
        return rootN

    act = depth % 2
    depth += 1
    if root.val[act+1] >= new[act+1]:
        root.left = insert_tree(root.left, new, depth)
    else:
        root.right = insert_tree(root.right, new, depth)

    return root


def search_tree(root: Node, new, depth=0):
    act = depth % 2
    if root is None:
        return
    depth += 1
    if root.val[act+1] >= new[act+1]:
        nextB = 0
    else:
        nextB = 1

    if nextB == 0:
        best = smaller_dist(new, search_tree(root.left, new, depth), root)
    else:
        best = smaller_dist(new, search_tree(root.right, new, depth), root)

    if euclid_distance(new[1:3], best.val[1:3]) > euclid_distance([new[act+1], 0], [root.val[act+1], 0]): #abs(new[act] - root.val[act]):
        if nextB == 0:
            best = smaller_dist(new, search_tree(root.right, new, depth), best)
        else:
            best = smaller_dist(new, search_tree(root.left, new, depth), best)

    return best


def search_k_tree(root: Node, new, k):
    best = []
    for _ in range(0, k):
        bestof = search_tree(root, new)
        bestof.used = True
        best.append(bestof.val)
    return best

