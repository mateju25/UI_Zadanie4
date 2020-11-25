from tkinter import *

CONSTANT = 10
SIZE_OF_OVAL = 3
SIZE = 5000


def print_path(canvas, points: []):
    for x in points:
        filling = "white"
        if x[0] == 'R':
            filling = "red"
        elif x[0] == 'G':
            filling = "green"
        elif x[0] == 'B':
            filling = "blue"
        elif x[0] == 'P':
            filling = "purple"

        canvas.create_oval(x[1]/CONSTANT + SIZE/CONSTANT - SIZE_OF_OVAL, -1*(x[2]/CONSTANT - SIZE/CONSTANT) - SIZE_OF_OVAL,
                           x[1]/CONSTANT + SIZE/CONSTANT + SIZE_OF_OVAL, -1*(x[2]/CONSTANT - SIZE/CONSTANT) + SIZE_OF_OVAL, fill=filling, outline="")


def make_gui(points: []):
    master = Tk()
    master.geometry("1000x1000")
    master.title("Skuska")
    canvas = Canvas(master, width=SIZE, height=SIZE)
    canvas.pack()

    print_path(canvas, points)

    mainloop()