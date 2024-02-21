import tkinter as tk
from tkinter import Canvas
from tkinter import messagebox
from tkinter import *

import numpy as np
from matplotlib import pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg


class Point(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.coordinates = [0, 0]
        self.confirm_button = tk.Button
        self.number = ''
        self.point_frame = tk.Frame(self, width=100, height=50)
        self.point_frame.pack()
        new_point_label = tk.Label(self.point_frame, text="Point " + self.number)
        new_point_label.pack()

        x_label = tk.Label(self.point_frame, text="X:")
        x_label.pack()
        self.x_entry = tk.Entry(self.point_frame)
        self.x_entry.pack()

        y_label = tk.Label(self.point_frame, text="Y:")
        y_label.pack()
        self.y_entry = tk.Entry(self.point_frame)
        self.y_entry.pack()

        self.confirm_button = tk.Button(self.point_frame, text="Confirm coordinates", command=self.confirm_coordinates)
        self.confirm_button.pack(pady=20)

    def confirm_coordinates(self):
        self.coordinates[0] = int(self.x_entry.get())
        self.coordinates[1] = int(self.y_entry.get())
        self.x_entry.config(bg="lightgrey", fg="black")
        self.y_entry.config(bg="lightgrey", fg="black")


class BezierCurveApp(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("Bezier Curve App")
        self.geometry("1020x800")
        self.figs = []
        self.points = []
        self.point_coordinates = []

        self.menu_frame = tk.Frame(self, width=200, height=600)
        self.menu_frame.pack(side="left", fill="y")


        self.add_point_button = tk.Button(self.menu_frame, text="Add Point", command=self.add_point)
        self.add_point_button.pack(pady=20)

        self.draw_curve_button = tk.Button(self, text="Draw Bezier Curve", command=self.draw_curve)
        self.draw_curve_button.pack(side="bottom")
        self.make_default_coords()

    def make_default_coords(self):
        p1 = Point(self.menu_frame)
        p1.coordinates[0] = 5
        p1.coordinates[1] = 0
        self.points.append(p1)

        p2 = Point(self.menu_frame)
        p2.coordinates[0] = 0
        p2.coordinates[1] = 20
        self.points.append(p2)

        p3 = Point(self.menu_frame)
        p3.coordinates[0] = 21
        p3.coordinates[1] = 23
        self.points.append(p3)

        p4 = Point(self.menu_frame)
        p4.coordinates[0] = 34
        p4.coordinates[1] = 3
        self.points.append(p4)

        # p5 = Point(self.menu_frame)
        # p5.coordinates[0] = 40
        # p5.coordinates[1] = 30
        # self.points.append(p5)



    def add_point(self):
        print('buttoned')
        new_point = Point(self.menu_frame)
        self.points.append(new_point)
        new_point.pack(side='top', fill="both", expand=False)

    def draw_curve(self):
        plt.clf()
        if len(self.points) < 2:
            messagebox.showerror("Error", "At least 2 points are required to draw the Bezier curve")
            return

        x = np.array([point.coordinates[0] for point in self.points])
        y = np.array([point.coordinates[1] for point in self.points])

        # Calculate the Bezier curve
        t = np.linspace(0, 1, 1000)
        bezier_x = np.zeros_like(t)
        bezier_y = np.zeros_like(t)

        for i in range(len(self.points)):
            bezier_x += self.points[i].coordinates[0] * (1 - t) ** (len(self.points) - 1 - i) * t ** i
            bezier_y += self.points[i].coordinates[1] * (1 - t) ** (len(self.points) - 1 - i) * t ** i

        fig = plt.figure()
        plt.scatter(x, y, color='gray')
        plt.plot(bezier_x, bezier_y, color='red', linewidth=5)

        for i in range(len(self.points) - 1):
            plt.plot([self.points[i].coordinates[0], self.points[i + 1].coordinates[0]],
                     [self.points[i].coordinates[1], self.points[i + 1].coordinates[1]],
                     color='blue', linewidth=1)

        # Create a canvas to embed the matplotlib figure
        canvas = FigureCanvasTkAgg(fig, master=self)
        canvas.draw()

        # Embed the canvas in the tkinter window
        canvas.get_tk_widget().pack(side="right", fill="both", expand=True)

if __name__ == "__main__":
    app = BezierCurveApp()
    app.mainloop()
