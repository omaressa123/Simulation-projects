import tkinter as tk
import random

# Number of cars
cars = [random.randint(0, 15) for _ in range(6)]

def show_traffic_status(index, car_count):
    if car_count == 0:
        phrase = "No cars in street yet"
        color = "grey"
        light_state = "red"
        delay = 1
    elif 0 < car_count <= 5:
        phrase = f"Number of cars: {car_count}"
        color = "green"
        light_state = "green"
        delay = 2
    elif 5 < car_count <= 12:
        phrase = "That's a lot of cars in street"
        color = "orange"
        light_state = "yellow"
        delay = 5
    else:
        phrase = "Stop Now!"
        color = "red"
        light_state = "red"
        delay = 7
    return phrase, color, light_state, delay

def draw_traffic_light(canvas, state):
    # Clear previous
    canvas.delete("all")
    # Draw traffic light body
    canvas.create_rectangle(40, 10, 110, 160, fill="black", outline="black")
    # Draw lights
    colors = {"red": "grey", "yellow": "grey", "green": "grey"}
    if state == "red":
        colors["red"] = "red"
    elif state == "yellow":
        colors["yellow"] = "yellow"
    elif state == "green":
        colors["green"] = "green"
    # Red light
    canvas.create_oval(55, 20, 95, 60, fill=colors["red"], outline="white")
    # Yellow light
    canvas.create_oval(55, 65, 95, 105, fill=colors["yellow"], outline="white")
    # Green light
    canvas.create_oval(55, 110, 95, 150, fill=colors["green"], outline="white")

def update_status():
    global current_index
    if current_index < len(cars):
        car_count = cars[current_index]
        phrase, color, light_state, delay = show_traffic_status(current_index, car_count)
        status_label.config(text=phrase, fg=color)
        draw_traffic_light(light_canvas, light_state)
        current_index += 1
        root.after(delay * 1000, update_status)
    else:
        status_label.config(
            text=f"All number of cars today: {cars}\nTotal number of cars today: {sum(cars)}",
            fg="blue"
        )
        draw_traffic_light(light_canvas, "green")

root = tk.Tk()
root.title("Traffic Light Simulation")

status_label = tk.Label(root, text="", font=("Arial", 16))
status_label.pack(pady=20)

light_canvas = tk.Canvas(root, width=150, height=170, bg="white")
light_canvas.pack(pady=10)

current_index = 0
root.after(500, update_status)

root.mainloop()