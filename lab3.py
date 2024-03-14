import tkinter as tk
from tkinter import messagebox
import numpy as np
from matplotlib import pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.pyplot import step

from bezier_functions import bernstein_poly


class Point(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.coordinates = [0, 0, 0]
        self.confirm_button = tk.Button
        self.number = ''
        self.point_frame = tk.Frame(self, width=100, height=50)
        self.point_frame.pack()
        new_point_label = tk.Label(self.point_frame, text="Point " + self.number)
        new_point_label.pack()

        self.x_frame = tk.Frame(self, width=50, height=25)

        x_label = tk.Label(self.x_frame, text="X:")
        x_label.pack(side="left")
        self.x_entry = tk.Entry(self.x_frame)
        self.x_entry.pack(side='right')

        self.fig = plt.figure()
        self.ax = self.fig.add_subplot(111, projection='3d')



        self.x_frame.pack()

        self.y_frame = tk.Frame(self, width=50, height=25)
        y_label = tk.Label(self.y_frame, text="Y:")
        y_label.pack(side="left")
        self.y_entry = tk.Entry(self.y_frame)
        self.y_entry.pack(side='right')
        self.y_frame.pack()

        self.z_frame = tk.Frame(self, width=50, height=25)
        z_label = tk.Label(self.z_frame, text="Z:")
        z_label.pack(side="left")
        self.z_entry = tk.Entry(self.z_frame)
        self.z_entry.pack(side='right')
        self.z_frame.pack()

        self.confirm_button = tk.Button(self, text="Confirm coordinates", command=self.confirm_coordinates)
        self.confirm_button.pack()

    def confirm_coordinates(self):
        self.coordinates[0] = int(self.x_entry.get())
        self.coordinates[1] = int(self.y_entry.get())
        self.coordinates[2] = int(self.z_entry.get())
        self.x_entry.config(bg="lightgrey", fg="black")
        self.y_entry.config(bg="lightgrey", fg="black")
        self.z_entry.config(bg="lightgrey", fg="black")


class BezierCurveApp(tk.Tk):
    def __init__(self):
        super().__init__()

        self.ax = None
        self.fig = None
        self.canvas = None
        self.title("Bezier Curve App")
        self.geometry("1020x800")
        self.figs = []
        self.points = []
        self.point_coordinates = []

        self.menu_frame = tk.Frame(self, width=200, height=600)
        self.menu_frame.pack(side="left", fill="y")

        self.draw_curve_button = tk.Button(self, text="Draw Bezier Curve", command=self.draw_curve)
        self.draw_curve_button.pack(side="bottom")

        point1 = Point(self.menu_frame)
        self.points.append(point1)
        point1.pack(side='top', fill="both", expand=False)

        point2 = Point(self.menu_frame)
        self.points.append(point2)
        point2.pack(side='top', fill="both", expand=False)

        point3 = Point(self.menu_frame)
        self.points.append(point3)
        point3.pack(side='top', fill="both", expand=False)

        point4 = Point(self.menu_frame)
        self.points.append(point4)
        point4.pack(side='top', fill="both", expand=False)

    def make_coordinates(self):
        points_correct = []
        for i in range(len(self.points)):
            a = [self.points[i].coordinates[0], self.points[i].coordinates[1], self.points[i].coordinates[2]]
            points_correct.append(a)
        print(points_correct)
        return points_correct


    def flip_by_x(self):
        goida = 'ZZZVVV'


    def draw_curve(self):
        if len(self.points) < 2:
            messagebox.showerror("Error", "At least 2 points are required to draw the Bezier curve")
            return

        points = np.array(self.make_coordinates())


        u = np.linspace(0, 1, 100)  # параметр u
        v = np.linspace(0, 1, 100)  # параметр v
        x_values = []

        x1 = points[0][0]
        x2 = points[1][0]
        x3 = points[2][0]
        x4 = points[3][0]
        for i in range(len(u)):
            for j in range(len(v)):
                x = x1 * (1 - u[i]) * (1 - v[j]) + x2 * v[j] * (1 - u[i]) + x3 * (1 - v[j]) * u[i] + x4 * u[i] * v[j]
                x_values.append(x)

        y_values = []

        y1 = points[0][1]
        y2 = points[1][1]
        y3 = points[2][1]
        y4 = points[3][1]
        for i in range(len(u)):
            for j in range(len(v)):
                y = y1 * (1 - u[i]) * (1 - v[j]) + y2 * v[j] * (1 - u[i]) + y3 * (1 - v[j]) * u[i] + y4 * u[i] * v[j]
                y_values.append(y)

        z_values = []

        z1 = points[0][2]
        z2 = points[1][2]
        z3 = points[2][2]
        z4 = points[3][2]
        for i in range(len(u)):
            for j in range(len(v)):
                z = z1 * (1 - u[i]) * (1 - v[j]) + z2 * v[j] * (1 - u[i]) + z3 * (1 - v[j]) * u[i] + z4 * u[i] * v[j]
                z_values.append(z)



        u_mesh, v_mesh = np.meshgrid(u, v)
        x_mesh = np.array(x_values).reshape((100, 100))  # assuming you have 100 points in u and v
        y_mesh = np.array(y_values).reshape((100, 100))  # assuming you have 100 points in u and v
        z_mesh = np.array(z_values).reshape((100, 100))  # assuming you have 100 points in u and v
        # x_mesh, y_mesh = np.meshgrid(x_mesh, y_mesh)

        surf = self.ax.plot_surface(z_mesh, y_mesh, x_mesh, cmap='pink')

        self.ax.set_xlabel("X", loc='right')
        self.ax.set_ylabel("Y")
        self.ax.set_zlabel("Z")

        # ax.legend()
        if self.canvas is None:
            self.canvas = FigureCanvasTkAgg(self.fig, master=self)
        else:
            self.canvas.get_tk_widget().destroy()
        self.canvas = FigureCanvasTkAgg(self.fig, master=self)
        self.canvas.draw()
        self.canvas.get_tk_widget().pack(side="right", fill="both", expand=True)

    def mat_number(self, matrix, num):
        for i in range(len(matrix)):
            matrix[i] *= num


if __name__ == "__main__":
    app = BezierCurveApp()
    app.mainloop()
