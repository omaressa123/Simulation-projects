import tkinter as tk
from tkinter import ttk, messagebox
import numpy as np
import matplotlib.pyplot as plt

def generate_signal(mod_type, n_bits, snr):
    """
    Generate a digital modulated signal (BPSK or QPSK) with specified SNR.

    Arguments:
    mod_type -- "BPSK" or "QPSK" (str)
    n_bits   -- number of bits to generate (int)
    snr      -- signal-to-noise ratio in dB (float)

    Returns:
    bits    -- original random bits (np.ndarray)
    symbols -- modulated (transmitted) signal (np.ndarray)
    noisy   -- received (noisy) signal (np.ndarray)
    """
    # Generate random bits (0 or 1)
    bits = np.random.randint(0, 2, n_bits)
    if mod_type == "BPSK":
        # ----- BPSK -----
        # BPSK symbol mapping: 0 -> -1, 1 -> +1
        symbols = 2 * bits - 1
        # Calculate SNR (convert to linear scale)
        snr_linear = 10 ** (snr / 10)
        # Signal power (should be 1 for BPSK, but calculated for generality)
        power = np.mean(np.abs(symbols) ** 2)
        # AWGN noise power calculation
        noise_power = power / snr_linear
        # Add real-valued gaussian noise to BPSK signal
        noisy = symbols + np.sqrt(noise_power) * np.random.randn(*symbols.shape)
        return bits, symbols, noisy
    elif mod_type == "QPSK":
        # ----- QPSK -----
        # QPSK requires even number of bits (2 bits per symbol)
        if n_bits % 2 != 0:
            raise ValueError("QPSK requires EVEN number of bits")
        # Group bits into pairs
        bits = bits.reshape(-1, 2)
        # Define QPSK mapping (Gray code)
        mapping = {
            (0, 0): (1+1j)/np.sqrt(2),
            (0, 1): (1-1j)/np.sqrt(2),
            (1, 0): (-1+1j)/np.sqrt(2),
            (1, 1): (-1-1j)/np.sqrt(2),
        }
        # Map each bit-pair to a QPSK symbol
        symbols = np.array([mapping[tuple(b)] for b in bits])
        # Calculate SNR in linear scale
        snr_linear = 10 ** (snr / 10)
        # Compute power of the QPSK symbols (should be 1)
        power = np.mean(np.abs(symbols) ** 2)
        # Noise power for the complex noise
        noise_power = power / snr_linear
        # Create complex AWGN (both I and Q components)
        noise = (np.random.randn(*symbols.shape) + 1j * np.random.randn(*symbols.shape)) * np.sqrt(noise_power/2)
        noisy = symbols + noise
        # Return bits as flattened 1D array, symbols, and noisy
        return bits.flatten(), symbols, noisy
    else:
        # Unsupported modulation
        raise ValueError("Unknown modulation")

def plot_signal(t, s, title, ylabel):
    """
    Utility function to plot signal waveform with Matplotlib.

    Arguments:
    t      -- array of sample indices (X-axis)
    s      -- signal samples (Y-axis)
    title  -- plot title (str)
    ylabel -- label for Y-axis (str)
    """
    plt.figure(figsize=(8,2.5))
    plt.plot(t, s, drawstyle='steps-post')
    plt.title(title)
    plt.xlabel("Sample")
    plt.ylabel(ylabel)
    plt.tight_layout()
    plt.grid(True)
    plt.show()

def on_calculate_and_plot():
    """
    Callback function for the GUI button.
    Gets user input, generates signal, and plots results.
    Handles input errors and displays error messages.
    """
    try:
        # Read number of bits from the GUI entry
        n_bits = int(bits_entry.get())
        # Read SNR from the GUI entry
        snr = float(snr_entry.get())
        # Get selected modulation type from combobox
        mod_type = mod_choice.get()
        # Generate signal and noisy version
        bits, symbols, noisy = generate_signal(mod_type, n_bits, snr)
        # Generate time/sample index for plotting
        t = np.arange(len(symbols))
        # Plot different signals depending on modulation type
        if mod_type == "BPSK":
            # For BPSK, plot both clean and noisy signals as real-valued waveforms
            plot_signal(t, symbols, "BPSK Transmitted Signal", "Symbol")
            plot_signal(t, noisy, "BPSK Received Signal (Noisy)", "Value")
        elif mod_type == "QPSK":
            # For QPSK, plot I (real) and Q (imaginary) parts separately
            plot_signal(t, np.real(symbols), "QPSK Transmitted Signal (I component)", "I")
            plot_signal(t, np.imag(symbols), "QPSK Transmitted Signal (Q component)", "Q")
            plot_signal(t, np.real(noisy), "QPSK Received Signal (I, Noisy)", "I")
            plot_signal(t, np.imag(noisy), "QPSK Received Signal (Q, Noisy)", "Q")
    except Exception as e:
        # Show any errors (e.g., input errors) in a pop-up dialog
        messagebox.showerror("Error", str(e))

# --- Tkinter UI Setup ---

# Create main application window
root = tk.Tk()
root.title("Signal Format Visualizer (BPSK / QPSK)")

# Create label and entry for number of bits
tk.Label(root, text="Bits:").grid(row=0, column=0)
bits_entry = tk.Entry(root)
bits_entry.insert(0, "10")  # default value for bits
bits_entry.grid(row=0, column=1)

# Create label and entry for SNR (dB)
tk.Label(root, text="SNR (dB):").grid(row=1, column=0)
snr_entry = tk.Entry(root)
snr_entry.insert(0, "10")  # default SNR value
snr_entry.grid(row=1, column=1)

# Create label and dropdown for modulation type selection
tk.Label(root, text="Modulation Type:").grid(row=2, column=0)
mod_choice = ttk.Combobox(root, values=["BPSK", "QPSK"])
mod_choice.current(0)  # default to "BPSK"
mod_choice.grid(row=2, column=1)

# Add the main button that triggers calculation and plotting
tk.Button(root, text="Show Signal Format", command=on_calculate_and_plot).grid(row=3, column=0, columnspan=2, pady=10)

# Start the Tkinter event loop
root.mainloop()