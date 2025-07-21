import tkinter as tk
from tkinter import messagebox
import matplotlib.pyplot as plt

def calculate_errors():
    try:
        # قراءة القيم من الإدخال وتحويلها لقوائم من الأرقام
        true_values = [float(x.strip()) for x in entry_true.get().split(',') if x.strip() != '']
        measured_values = [float(x.strip()) for x in entry_measured.get().split(',') if x.strip() != '']

        if len(true_values) != len(measured_values):
            messagebox.showerror("Input Error", "Lists must be of the same length.")
            return

        abs_errors = []
        rel_errors = []
        perc_errors = []
        result_lines = []

        for t, m in zip(true_values, measured_values):
            abs_err = abs(t - m)
            # Avoid division by zero for true value
            if t == 0:
                rel_err = float('inf')
                perc_err = float('inf')
                rel_str = "inf"
                perc_str = "inf"
            else:
                rel_err = abs_err / abs(t)
                perc_err = rel_err * 100
                rel_str = f"{rel_err:.4f}"
                perc_str = f"{perc_err:.2f}%"

            abs_errors.append(abs_err)
            rel_errors.append(rel_err)
            perc_errors.append(perc_err)

            result_lines.append(
                f"True: {t}, Measured: {m} | Abs: {abs_err:.4f}, Rel: {rel_str}, Perc: {perc_str}"
            )

        result_text.set('\n'.join(result_lines))

        # رسم بياني
        draw_plot(abs_errors, rel_errors, perc_errors)

    except ValueError:
        messagebox.showerror("Input Error", "Please enter valid comma-separated numerical values.")

def draw_plot(abs_errors, rel_errors, perc_errors):
    plt.figure(figsize=(10, 5))
    indices = list(range(1, len(abs_errors) + 1))

    plt.plot(indices, abs_errors, marker='o', label='Absolute Error')
    # Only plot rel_errors and perc_errors if they are finite
    rel_errors_plot = [e if e != float('inf') else None for e in rel_errors]
    perc_errors_plot = [e if e != float('inf') else None for e in perc_errors]
    plt.plot(indices, rel_errors_plot, marker='s', label='Relative Error')
    plt.plot(indices, perc_errors_plot, marker='^', label='Percentage Error')

    plt.title('Measurement Errors')
    plt.xlabel('Measurement Index')
    plt.ylabel('Error Value')
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.show()

# واجهة المستخدم
root = tk.Tk()
root.title("Measurement Error System")
root.geometry("600x500")

tk.Label(root, text="True Values (comma-separated):").pack()
entry_true = tk.Entry(root, width=70)
entry_true.pack()

tk.Label(root, text="Measured Values (comma-separated):").pack()
entry_measured = tk.Entry(root, width=70)
entry_measured.pack()

tk.Button(root, text="Calculate & Plot Errors", command=calculate_errors).pack(pady=10)

result_text = tk.StringVar()
tk.Label(root, textvariable=result_text, justify="left", font=("Courier", 10), fg="blue").pack()

root.mainloop()
