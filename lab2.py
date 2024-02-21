import tkinter as tk
from tkinter import Canvas
from tkinter import messagebox


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


class BezierCurveApp(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("Bezier Curve App")
        self.geometry("800x600")

        self.points = []
        self.point_coordinates = []

        self.menu_frame = tk.Frame(self, width=200, height=600)
        self.menu_frame.pack(side="left", fill="y")

        self.canvas = Canvas(self, width=600, height=600, bg="white")
        self.canvas.pack(side="right", fill="both", expand=True)

        self.add_point_button = tk.Button(self.menu_frame, text="Add Point", command=self.add_point)
        self.add_point_button.pack(pady=20)

        self.draw_curve_button = tk.Button(self, text="Draw Bezier Curve", command=self.draw_curve)
        self.draw_curve_button.pack(side="bottom")

    def add_point(self):
        print('buttoned')
        new_point = Point(self.menu_frame)
        self.points.append(new_point)
        new_point.pack(side='top', fill="both", expand=False)

    def draw_curve(self):

        if len(self.points) < 2:
            messagebox.showerror("Error", "At least 2 points are required to draw the Bezier curve")
            return
        self.canvas.delete('all')
        # Draw x and y axis
        self.canvas.create_line(50, 550, 750, 550, arrow=tk.LAST)
        self.canvas.create_line(50, 550, 50, 50, arrow=tk.LAST)

        # Add labels for x and y
        for i in range(1, 15):
            self.canvas.create_line(50 + i * 50, 550, 50 + i * 50, 545)
            self.canvas.create_text(50 + i * 50, 560, text=str(i))

        for i in range(1, 11):
            self.canvas.create_line(50, 550 - i * 50, 55, 550 - i * 50)
            self.canvas.create_text(40, 550 - i * 50, text=str(i))

        # Scale points for coordinate system
        scaled_points = [(20 + point.coordinates[0] * 10, 550 - point.coordinates[1] * 10) for point in self.points]

        # Draw points
        for point in scaled_points:
            self.canvas.create_oval(point[0] - 5, point[1] - 5, point[0] + 5, point[1] + 5, fill="black")
            self.canvas.create_line(scaled_points, fill="red", width=3)

        # Draw Bezier curve
        self.canvas.create_line(scaled_points, smooth=True, fill="blue", width=3)


if __name__ == "__main__":
    app = BezierCurveApp()
    app.mainloop()
