import glob
import os
import time
from tkinter import *


CONSTANT = 10
SIZE_OF_OVAL = 2
SIZE = 5000
DEL = 0.5
DETAIL = 10

TYPE1 = "firebrick"
TYPE2 = "dark green"
TYPE3 = "navy"
TYPE4 = "dark violet"

def get_type_neighbours(points):
    types = [0]*4
    for x in range(len(points)):
        for y in range(len(points)):
            if points[x][y] is None:
                continue
            for z in range(len(points[x][y])):
                if points[x][y][z] is None:
                    continue
                types[points[x][y][z][0]] += 1

    return [types.index(max(types))]


def create_areas(canvas, points: [], startx, starty, size, depth=0):
    if points is None:
        return
    count = int(size/(size * DEL))
    boxes = [None] * count
    for x in range(len(boxes)):
        boxes[x] = [None] * count

    for point in points:
        x = int((point[1]+5000)/(DEL * size)) % count
        y = int((-1*(point[2] - 5000)) / (DEL * size)) % count
        if boxes[x][y] is None:
            boxes[x][y] = []
        boxes[x][y].append(point)

    for x in range(count):
        for y in range(count):
            draw = True
            if boxes[x][y] is None:
                pivot = get_type_neighbours(boxes)
            else:
                pivot = boxes[x][y][0]
                if len(boxes[x][y]) == 1:
                    pivot = get_type_neighbours(boxes)
                else:
                    for z in range(len(boxes[x][y])):
                        if pivot[0] != boxes[x][y][z][0]:
                            draw = False
                            break

            if draw:
                if pivot[0] == 0:
                    filling = TYPE1
                elif pivot[0] == 1:
                    filling = TYPE2
                elif pivot[0] == 2:
                    filling = TYPE3
                elif pivot[0] == 3:
                    filling = TYPE4
                elif pivot[0] == 4:
                    filling = "black"
                canvas.create_rectangle((x * (DEL * size) + startx) / CONSTANT,
                                        (y * (DEL * size) + starty) / CONSTANT,
                                        ((x + 1) * (DEL * size) + startx) / CONSTANT,
                                        ((y + 1) * (DEL * size) + starty) / CONSTANT, fill=filling, outline=""
                                        )
                # canvas.update()
                # time.sleep(0.1)

            else:
                if depth < DETAIL:
                    create_areas(canvas, boxes[x][y], startx + x * (DEL * size), starty + y * (DEL * size), size * DEL, depth+1)


def print_path(canvas, points: []):
    i = -1
    canvas.create_rectangle(-10, -10, SIZE+10, SIZE+10, fill="white", outline="")
    choice = input("Iba body? y/n")
    if choice != "y":
        create_areas(canvas, points, 0, 0, 10000)
    else:
        for x in points:
            i += 1
            filling = "white"
            if x[0] == 'R' or x[0] == 0:
                filling = TYPE1
            elif x[0] == 'G' or x[0] == 1:
                filling = TYPE2
            elif x[0] == 'B' or x[0] == 2:
                filling = TYPE3
            elif x[0] == 'P' or x[0] == 3:
                filling = TYPE4
            elif x[0] == 'B' or x[0] == 4:
                filling = "black"
            canvas.create_rectangle(x[1]/CONSTANT + SIZE/CONSTANT - SIZE_OF_OVAL, -1*(x[2]/CONSTANT - SIZE/CONSTANT) - SIZE_OF_OVAL,
                               x[1]/CONSTANT + SIZE/CONSTANT + SIZE_OF_OVAL, -1*(x[2]/CONSTANT - SIZE/CONSTANT) + SIZE_OF_OVAL, fill=filling, outline="")


def make_gui(points: []):
    master = Tk()
    master.geometry("1000x1000")
    master.title("Skuska")
    canvas = Canvas(master, width=SIZE, height=SIZE)
    canvas.pack()

    print_path(canvas, points)

    mainloop()