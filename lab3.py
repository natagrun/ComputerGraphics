import tkinter as tk
from tkinter import messagebox
import numpy as np
from matplotlib import pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
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

    def draw_curve(self):
        if len(self.points) < 2:
            messagebox.showerror("Error", "At least 2 points are required to draw the Bezier curve")
            return

        points = np.array(self.make_coordinates())

        x = [0, 0, 0, 0]
        y = [0, 0, 0, 0]
        z = [0, 0, 0, 0]
        coords = [x, y, z]
        print('points\n', points)
        for i in range(len(coords)):
            for j in range(len(points)):
                coords[i][j] = points[j][i]
        print('coordc\n', coords)

        # Формирование матрицы коэффициентов для билинейной поверхности
        # Уравнение билинейной поверхности имеет вид:
        # F(x, y) = a + b*x + c*y + d*x*y
        # Где a, b, c, d - коэффициенты, которые нужно найти
        # Преобразуем уравнение в вид матрицы:
        # |1 x1 y1 x1*y1|   |a|   |z1|
        # |1 x2 y2 x2*y2| * |b| = |z2|
        # |1 x3 y3 x3*y3|   |c|   |z3|
        # |1 x4 y4 x4*y4|   |d|   |z4|

        # Формируем матрицу коэффициентов A
        A_matrix = np.array([
            [1, points[0][0], points[0][1], points[0][0] * points[0][1]],
            [1, points[1][0], points[1][1], points[1][0] * points[1][1]],
            [1, points[2][0], points[2][1], points[2][0] * points[2][1]],
            [1, points[3][0], points[3][1], points[3][0] * points[3][1]]
        ])

        # Формируем матрицу значений Z
        Z_matrix = np.array([points[0][2], points[1][2], points[2][2], points[3][2]])

        # Находим коэффициенты a, b, c, d решая систему линейных уравнений
        coefficients = np.linalg.solve(A_matrix, Z_matrix)

        # Поворот билинейной поверхности относительно оси X
        # Для поворота билинейной поверхности относительно оси X на угол alpha, мы можем использовать матрицу поворота:
        # |1    0      0|   |x|   |x'|
        # |0  cos(a) -sin(a)| * |y| = |y'|
        # |0  sin(a)  cos(a)|   |z|   |z'|

        alpha = np.radians(45)  # Угол поворота в радианах
        rotation_matrix_x = np.array([
            [1, 0, 0],
            [0, np.cos(alpha), -np.sin(alpha)],
            [0, np.sin(alpha), np.cos(alpha)]
        ])

        # Поворачиваем координаты точек A, B, C, D на угол alpha относительно оси X
        A_rotated = np.dot(rotation_matrix_x, points[0])
        B_rotated = np.dot(rotation_matrix_x, points[1])
        C_rotated = np.dot(rotation_matrix_x, points[2])
        D_rotated = np.dot(rotation_matrix_x, points[3])

        # Поворот билинейной поверхности относительно оси Y
        # Поворот билинейной поверхности относительно оси Y происходит аналогичным образом, заменить угол поворота и матрицу поворота
        # alpha_y = np.radians(30)  # Угол поворота в радианах
        # rotation_matrix_y = np.array([
        #     [np.cos(alpha_y), 0, np.sin(alpha_y)],
        #     [0, 1, 0],
        #     [-np.sin(alpha_y), 0, np.cos(alpha_y)]
        # ])

        fig, ax = plt.subplots()

        fig = plt.figure()
        ax = fig.add_subplot(111, projection='3d')
        ax.plot_surface(x, y, z, alpha=0.5)
        ax.scatter(A_rotated[0], A_rotated[1], A_rotated[2], color='r', marker='o')  # точка A
        ax.scatter(B_rotated[0], B_rotated[1], B_rotated[2], color='g', marker='o')  # точка B
        ax.scatter(C_rotated[0], C_rotated[1], C_rotated[2], color='b', marker='o')  # точка C
        ax.scatter(D_rotated[0], D_rotated[1], D_rotated[2], color='y', marker='o')  # точка D


        ax.legend()
        if self.canvas is None:
            self.canvas = FigureCanvasTkAgg(fig, master=self)
        else:
            self.canvas.get_tk_widget().destroy()
        self.canvas = FigureCanvasTkAgg(fig, master=self)
        self.canvas.draw()
        self.canvas.get_tk_widget().pack(side="right", fill="both", expand=True)

        if __name__ == "__main__":
            app = BezierCurveApp()
        app.mainloop()
