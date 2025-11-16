import tkinter as tk 
import random

win = tk.Tk()
win.title('Car Parking Simulation')
win.geometry("900x500")

canvas = tk.Canvas(win, width=900, height=500, bg="#e0e0e0")
canvas.pack()

Num_slots = 10 
slot_position = []
slot_width = 80
slot_height = 120

for i in range(Num_slots):
    x = 50 + i * (slot_width + 20)
    y = 50
    slot = canvas.create_rectangle(x, y, x + slot_width, y + slot_height, fill="white")
    slot_position.append((slot, x, y))

# Parking slot status
slot_free = [True] * Num_slots

# Counters
in_count = 0
out_count = 0 

label_info = tk.Label(win, text="Cars In: 0 | Cars out: 0 | Occupancy: 0%", font=("Arial", 14))
label_info.pack()

cars = []

# Car body color options
CAR_COLORS = ["#f44336", "#2196F3", "#4CAF50", "#FFEB3B", "#9C27B0", "#FF9800", "#009688", "#795548", "#607D8B", "#E91E63"]

# Helper: create a car shape and return a list of items (body, wheel1, wheel2)
def create_car_shape(x, y, car_color=None):
    """Draws a simple car shape at (x, y) top-left."""
    if car_color is None:
        car_color = random.choice(CAR_COLORS)
    # Main body
    body = canvas.create_rectangle(x, y, x + 30, y + 20, fill=car_color, outline="black", width=2)
    # Top (window)
    top = canvas.create_rectangle(x + 6, y - 8, x + 24, y + 8, fill="white", outline="black", width=1)
    # Wheels
    wheel1 = canvas.create_oval(x + 3, y + 16, x + 11, y + 24, fill="black")
    wheel2 = canvas.create_oval(x + 19, y + 16, x + 27, y + 24, fill="black")
    # Group as a tag for easier moving/deleting
    car_tag = f'car{random.randint(100000,999999)}'
    for item in (body, top, wheel1, wheel2):
        canvas.addtag_withtag(car_tag, item)
    return (car_tag, [body, top, wheel1, wheel2])

# Utility: get a car's bounding box [x1,y1,x2,y2] based on its tag
def car_coords(car_tag):
    # We'll use the main body rectangle, which is the first id in car_tag_items.
    items = canvas.find_withtag(car_tag)
    # Use the 'body' (first item) for reference
    return canvas.coords(items[0]) if items else [0,0,0,0]

# Utility: move the whole car as a group
def car_move(car_tag, dx, dy):
    canvas.move(car_tag, dx, dy)

# Utility: delete car as a group
def car_delete(car_tag):
    canvas.delete(car_tag)

# Update counter/info label
def update_info():
    global in_count, out_count
    occupied = sum([not s for s in slot_free])
    occ_rate = int((occupied / Num_slots) * 100)
    label_info.config(text=f'Cars in : {in_count} | Cars Out: {out_count} | Occupancy: {occ_rate}%')

def generate_car():
    """Create a new car entering the parking."""
    car_color = random.choice(CAR_COLORS)
    # Create at (10, 350) (body top-left), initially
    car_tag, car_items = create_car_shape(10, 350, car_color=car_color)
    cars.append(car_tag)
    move_car_in(car_tag)
    win.after(random.randint(1500, 3500), generate_car)

def move_car_in(car_tag):
    """Move car forward until finding a free slot."""
    x1, y1, x2, y2 = car_coords(car_tag)

    # If car reached parking area, try to park
    if y1 <= 200:
        assign_slot(car_tag)
        return

    car_move(car_tag, 0, -5)  # move upward
    win.after(30, lambda: move_car_in(car_tag))

def assign_slot(car_tag):
    global in_count
    for i in range(Num_slots):
        if slot_free[i]:
            slot_free[i] = False
            in_count += 1
            update_info()
            slot_rect, sx, sy = slot_position[i]
            move_to_slot(car_tag, sx + 10, sy + 40, i)  # +40 for better y centering
            return

def move_to_slot(car_tag, target_x, target_y, slot_index):
    def step():
        x1, y1, x2, y2 = car_coords(car_tag)
        dx = 2 if x1 < target_x else -2
        dy = 2 if y1 < target_y else -2
        if abs(x1 - target_x) < 3 and abs(y1 - target_y) < 3:
            win.after(random.randint(3000, 6000), lambda: remove_car(car_tag, slot_index))
            return
        car_move(car_tag, dx, dy)
        win.after(20, step)
    step()

def remove_car(car_tag, slot_index):
    """Car leaves its slot."""
    global out_count
    slot_free[slot_index] = True
    out_count += 1
    update_info()
    def step_out():
        x1, y1, x2, y2 = car_coords(car_tag)
        if y1 > 450:
            car_delete(car_tag)
            return
        car_move(car_tag, 0, 5)
        win.after(20, step_out)
    step_out()

# Start generating cars
generate_car()

win.mainloop()