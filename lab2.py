import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from tkinter import Canvas


class BezierCurveApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.confirm_coords_button = None
        self.title("Bezier Curve App")
        self.geometry("800x600")

        self.points = []
        self.point_coords = []

        self.menu_frame = tk.Frame(self, width=200, height=600, bg="lightgrey")
        self.menu_frame.pack(side="left", fill="y")

        self.canvas = Canvas(self, width=600, height=600, bg="white")
        self.canvas.pack(side="right", fill="both", expand=True)

        self.add_point_button = tk.Button(self.menu_frame, text="Add Point", command=self.add_point)
        self.add_point_button.pack(pady=20)

        self.draw_curve_button = tk.Button(self, text="Draw Bezier Curve", command=self.draw_curve)
        self.draw_curve_button.pack(side="bottom")

    def add_point(self):
        new_point_label = tk.Label(self.menu_frame, text="Point " + str(len(self.points) + 1))
        new_point_label.pack()

        x_label = tk.Label(self.menu_frame, text="X:")
        x_label.pack()
        x_entry = tk.Entry(self.menu_frame)
        x_entry.pack()

        y_label = tk.Label(self.menu_frame, text="Y:")
        y_label.pack()
        y_entry = tk.Entry(self.menu_frame)
        y_entry.pack()

        self.point_coords.append((x_entry, y_entry))

        self.confirm_coords_button = tk.Button(self.menu_frame, text="Confirm Coordinates", command=self.confirm_coords)

        self.confirm_coords_button.pack(pady=20)

    def confirm_coords(self):
        for x_entry, y_entry in self.point_coords:
            x = x_entry.get()
            y = y_entry.get()
            if not x or not y:
                messagebox.showerror("Error", "All coordinates must be filled")
                return
            self.points.append((int(x), int(y)))

            self.point_coords.clear()
            self.confirm_coords_button.config()

    def draw_curve(self):
        if len(self.points) < 2:
            messagebox.showerror("Error", "At least 2 points are required to draw the Bezier curve")
            return

        # Draw x and y axis
        self.canvas.create_line(50, 550, 750, 550, arrow=tk.LAST)
        self.canvas.create_line(50, 550, 50, 50, arrow=tk.LAST)

        # Scale points for coordinate system
        scaled_points = [(50 + point[0] * 10, 550 - point[1] * 10) for point in self.points]

        # Draw points
        for point in scaled_points:
            self.canvas.create_oval(point[0] - 5, point[1] - 5, point[0] + 5, point[1] + 5, fill="black")
            self.canvas.create_line(scaled_points, fill="red", width=3)


        # Draw Bezier curve
        self.canvas.create_line(scaled_points, smooth=True, fill="blue", width=3)

if __name__ == "__main__":
    app = BezierCurveApp()
    app.mainloop()
