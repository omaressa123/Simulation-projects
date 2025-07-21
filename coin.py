import tkinter as tk
import random

class CoinGameGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Coin Game: Play with Computer")
        self.h_count = 0
        self.t_count = 0
        self.play_num = 0
        self.total_plays = 0

        self.setup_widgets()

    def setup_widgets(self):
        self.instructions = tk.Label(self.root, text="Enter number of plays (rounds):")
        self.instructions.pack(pady=5)

        self.entry_plays = tk.Entry(self.root, width=10)
        self.entry_plays.pack(pady=5)

        self.start_btn = tk.Button(self.root, text="Start Game", command=self.start_game)
        self.start_btn.pack(pady=5)

        self.status = tk.Label(self.root, text="", font=("Arial", 12))
        self.status.pack(pady=10)

        self.input_label = tk.Label(self.root, text="Enter a number (1-10):")
        self.input_entry = tk.Entry(self.root, width=10)
        self.play_btn = tk.Button(self.root, text="Play", command=self.play_round)

        self.coin_canvas = tk.Canvas(self.root, width=100, height=100, bg="white")
        self.coin_text = None

        self.result_label = tk.Label(self.root, text="", font=("Arial", 12, "bold"))

    def start_game(self):
        try:
            self.total_plays = int(self.entry_plays.get())
            if self.total_plays <= 0:
                raise ValueError
        except ValueError:
            self.status.config(text="Please enter a valid positive integer for plays.", fg="red")
            return

        self.h_count = 0
        self.t_count = 0
        self.play_num = 0
        self.status.config(text=f"Game started! Round 1 of {self.total_plays}", fg="blue")
        self.result_label.pack_forget()
        self.coin_canvas.pack_forget()

        self.input_label.pack(pady=5)
        self.input_entry.pack(pady=5)
        self.input_entry.delete(0, tk.END)
        self.play_btn.pack(pady=5)
        self.coin_canvas.pack(pady=10)
        self.result_label.pack_forget()

    def play_round(self):
        if self.play_num >= self.total_plays:
            return

        try:
            user_number = int(self.input_entry.get())
        except ValueError:
            self.status.config(text="Please enter a valid number between 1 and 10.", fg="red")
            return

        if not (1 <= user_number <= 10):
            self.status.config(text="Number must be between 1 and 10.", fg="red")
            return

        # Simulate computer's number
        comp_number = random.randint(1, 10)
        # Coin logic: 1-5 is H, 6-10 is T
        if 1 <= user_number <= 5:
            user_choice = "H"
        else:
            user_choice = "T"

        if 1 <= comp_number <= 5:
            comp_choice = "H"
        else:
            comp_choice = "T"

        # Simulate coin flip (randomly H or T)
        coin_result = random.choice(["H", "T"])

        # Update counts
        if coin_result == "H":
            self.h_count += 1
        else:
            self.t_count += 1

        # Draw coin
        self.draw_coin(coin_result)

        self.play_num += 1
        self.status.config(
            text=f"Round {self.play_num} of {self.total_plays} | "
                 f"Your number: {user_number} ({user_choice}), "
                 f"Computer: {comp_number} ({comp_choice}) | "
                 f"Coin: {coin_result}",
            fg="black"
        )

        if self.play_num == self.total_plays:
            self.show_result()
        else:
            self.input_entry.delete(0, tk.END)

    def draw_coin(self, result):
        self.coin_canvas.delete("all")
        # Draw coin circle
        self.coin_canvas.create_oval(20, 20, 80, 80, fill="#FFD700", outline="#B8860B", width=3)
        # Draw H or T in the center
        self.coin_canvas.create_text(50, 50, text=result, font=("Arial", 36, "bold"), fill="black")

    def show_result(self):
        self.input_label.pack_forget()
        self.input_entry.pack_forget()
        self.play_btn.pack_forget()
        result_text = f"Total H: {self.h_count}\nTotal T: {self.t_count}\n"
        if self.h_count > self.t_count:
            result_text += "H wins!"
        elif self.t_count > self.h_count:
            result_text += "T wins!"
        else:
            result_text += "It's a tie!"
        self.result_label.config(text=result_text, fg="blue")
        self.result_label.pack(pady=10)

if __name__ == "__main__":
    root = tk.Tk()
    app = CoinGameGUI(root)
    root.mainloop()
