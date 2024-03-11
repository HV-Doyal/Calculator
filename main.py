import tkinter as tk
from tkinter import messagebox
import math
import threading


class Calculator:
    def __init__(self, master):
        self.master = master
        self.master.title("Calculator")
        self.master.configure(bg='aquamarine4')  # Background color of the GUI
        self.equation = ""

        self.text_input = tk.StringVar()

        screen_width = master.winfo_screenwidth()
        screen_height = master.winfo_screenheight()
        window_width = 522
        window_height = 650

        # Calculate the centered position of the window
        x = (screen_width - window_width) // 2
        y = (screen_height - window_height) // 2

        self.master.geometry(f"{window_width}x{window_height}+{x}+{y}")

        # Increase the font size of the entry field
        self.entry = tk.Entry(master, textvariable=self.text_input, font=('arial', 20, 'bold'), bd=30, insertwidth=4,
                              bg="powder blue", justify='right')
        self.entry.grid(row=0, column=0, columnspan=3)

        # Clear button
        tk.Button(master, text="C", width=10, height=3, font=('arial', 15, 'bold'), bg='aquamarine4',
                  command=lambda: self.click_button("C")).grid(row=0, column=3)

        buttons = [
            'sin', 'cos', 'tan', 'log',
            'ln', '!', 'sqrt', '/',
            '7', '8', '9', '*',
            '4', '5', '6', '-',
            '1', '2', '3', '+',
            '0', '.', '=', '<-'
        ]

        row_val = 1
        col_val = 0

        # Creating buttons and placing them in the grid layout
        for button in buttons:
            tk.Button(master, text=button, width=10, height=3, font=('arial', 15, 'bold'), bg='aquamarine4',
                      command=lambda button=button: self.click_button(button)).grid(row=row_val, column=col_val)
            col_val += 1

            if col_val > 3:
                col_val = 0
                row_val += 1

    # Function that handles button clicks
    def click_button(self, button):
        if button == "=":
            # Start a new thread to calculate the result when "=" is clicked
            try:
                threading.Thread(target=self.calculate_result).start()
            except Exception as e:
                messagebox.showerror("Error", str(e))
        elif button == "C":
            # Clear the input field when "C" is clicked
            self.equation = ""
        elif button in ('sin', 'cos', 'tan', 'log', 'ln', '!', 'sqrt'):
            if self.equation:
                # Start a new thread to calculate functions
                try:
                    threading.Thread(target=self.calculate_function, args=(button,)).start()
                except Exception as e:
                    messagebox.showerror("Error", str(e))
            else:
                messagebox.showerror("Error", "Input value before pressing")
        elif button == "<-":
            self.equation = self.equation[:-1]
        else:
            # Add the clicked button's value to the equation string
            self.equation += str(button)
        self.text_input.set(self.equation)

    # Function that calculates the result of the equation
    def calculate_result(self):
        try:
            self.equation = str(eval(self.equation))
        except Exception as e:
            messagebox.showerror("Error", str(e))
        self.text_input.set(self.equation)

    # Function that calculates functions
    def calculate_function(self, func):
        try:
            number = float(self.equation)
            if func == 'sin':
                result = math.sin(math.radians(number))
            elif func == 'cos':
                result = math.cos(math.radians(number))
            elif func == 'tan':
                result = math.tan(math.radians(number))
            elif func == 'log':
                result = math.log10(number)
            elif func == 'ln':
                result = math.log(number)
            elif func == '!':
                result = math.factorial(int(number))
            elif func == 'sqrt':
                result = number * number
            self.equation = str(result)
        except Exception as e:
            messagebox.showerror("Error", str(e))
        self.text_input.set(self.equation)


root = tk.Tk()
root.overrideredirect(False)  # Disable full window mode
root.resizable(False, False)  # Disable resizing
Calculator(root)
root.mainloop()
