import tkinter as tk
from tkinter import ttk
from src.api.ecb_api import load_rates
from src.logic.converter import convert

def start_app():
    date, rates = load_rates()
    window = tk.Tk()
    window.title("Currency Converter")

    amount_label = tk.Label(window, text="Amount")
    amount_label.pack()
    amount_entry = tk.Entry(window)
    amount_entry.pack()

    from_label = tk.Label(window, text="From")
    from_label.pack()
    from_combo = ttk.Combobox(window, values=list(rates.keys()))
    from_combo.pack()

    to_label = tk.Label(window, text="To")
    to_label.pack()
    to_combo = ttk.Combobox(window, values=list(rates.keys()))
    to_combo.pack()

    result_label = tk.Label(window, text="")
    result_label.pack()

    def on_convert():
        try:
            amount = float(amount_entry.get())
            src = from_combo.get()
            dst = to_combo.get()
            result = convert(amount, rates[src], rates[dst])
            result_label.config(text=str(result))
        except:
            result_label.config(text="Invalid input")

    button = tk.Button(window, text="Convert", command=on_convert)
    button.pack()

    date_label = tk.Label(window, text="Rates updated: " + date)
    date_label.pack()

    window.mainloop()
