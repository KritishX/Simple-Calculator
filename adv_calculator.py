import tkinter as tk
from tkinter import messagebox
import math

class CasioClasswiz(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Casio fx-991EX ClassWiz")
        self.geometry("400x700")
        self.configure(bg="#1a1a1a")  # Dark casing
        self.resizable(False, False)

        self.expression = ""
        self.shift_mode = False
        self.alpha_mode = False
        self.ans = "0"

        self._init_styles()
        self._create_widgets()

    def _init_styles(self):
        self.bg_color = "#1a1a1a"
        self.display_bg = "#98a693"  # Classic LCD greenish-grey
        self.btn_dark = "#333333"    # Dark grey keys for functions
        self.btn_light = "#f5f5f5"   # Off-white keys for numbers
        self.btn_action = "#d35400"  # Orange for AC/DEL
        self.accent_shift = "#f1c40f" # Yellow for shift
        self.accent_alpha = "#e74c3c" # Red for alpha

    def _create_widgets(self):
        # Header area
        header = tk.Frame(self, bg=self.bg_color, pady=10)
        header.pack(fill="x")
        tk.Label(header, text="CASIO", fg="white", bg=self.bg_color, font=("Arial", 12, "bold")).pack(side="left", padx=20)
        tk.Label(header, text="fx-991EX", fg="white", bg=self.bg_color, font=("Arial", 10)).pack(side="left")
        
        # Solar Panel
        solar = tk.Frame(header, bg="#332211", height=25, width=80, relief="sunken", borderwidth=2)
        solar.pack(side="right", padx=20)

        # LCD Display Area
        display_frame = tk.Frame(self, bg="#2c3e50", padx=15, pady=15, relief="flat")
        display_frame.pack(fill="x", padx=10, pady=5)

        self.screen_top = tk.Label(
            display_frame, 
            text="", 
            font=("Courier", 12),
            anchor="w", 
            bg=self.display_bg, 
            fg="#2c3e50",
            padx=5
        )
        self.screen_top.pack(fill="x")

        self.screen_main = tk.Label(
            display_frame, 
            text="0", 
            font=("Courier", 28, "bold"), 
            anchor="e", 
            bg=self.display_bg, 
            fg="black",
            padx=5, 
            pady=10
        )
        self.screen_main.pack(fill="x")

        # Control Row (Shift, Alpha, Nav, Menu, On)
        ctrl_frame = tk.Frame(self, bg=self.bg_color, pady=10)
        ctrl_frame.pack(fill="x")

        # Shift/Alpha/Menu
        tk.Button(ctrl_frame, text="SHIFT", fg=self.accent_shift, bg=self.btn_dark, font=("Arial", 7, "bold"), width=5, command=self.toggle_shift).grid(row=0, column=0, padx=5)
        tk.Button(ctrl_frame, text="ALPHA", fg=self.accent_alpha, bg=self.btn_dark, font=("Arial", 7, "bold"), width=5, command=self.toggle_alpha).grid(row=0, column=1, padx=5)
        
        # Navigation D-Pad
        nav_pad = tk.Frame(ctrl_frame, bg=self.bg_color)
        nav_pad.grid(row=0, column=2, padx=10)
        tk.Button(nav_pad, text="▲", width=2, height=1, bg=self.btn_dark, fg="white", font=("Arial", 6)).grid(row=0, column=1)
        tk.Button(nav_pad, text="◀", width=2, height=1, bg=self.btn_dark, fg="white", font=("Arial", 6)).grid(row=1, column=0)
        tk.Button(nav_pad, text="▶", width=2, height=1, bg=self.btn_dark, fg="white", font=("Arial", 6)).grid(row=1, column=2)
        tk.Button(nav_pad, text="▼", width=2, height=1, bg=self.btn_dark, fg="white", font=("Arial", 6)).grid(row=2, column=1)

        tk.Button(ctrl_frame, text="MENU", fg="white", bg=self.btn_dark, font=("Arial", 7, "bold"), width=5).grid(row=0, column=3, padx=5)
        tk.Button(ctrl_frame, text="ON", fg="white", bg=self.btn_dark, font=("Arial", 7, "bold"), width=5, command=self.clear_all).grid(row=0, column=4, padx=5)

        # Scientific/Function Keys
        sci_frame = tk.Frame(self, bg=self.bg_color)
        sci_frame.pack(fill="x", padx=10)

        sci_keys = [
            ("OPTN", ""), ("CALC", ""), ("∫dx", ""), ("x⁻¹", "**-1"), ("logₓ□", ""),
            ("fraction", "/"), ("√", "math.sqrt("), ("x²", "**2"), ("x□", "**"), ("log", "math.log10("), ("ln", "math.log("),
            ("(-)", "-"), ("°'\"", ""), ("hyp", ""), ("sin", "math.sin(math.radians("), ("cos", "math.cos(math.radians("), ("tan", "math.tan(math.radians("),
            ("STO", ""), ("ENG", ""), ("(", "("), (")", ")"), ("S⇔D", ""), ("M+", "")
        ]

        r, c = 0, 0
        for text, val in sci_keys:
            btn = tk.Button(sci_frame, text=text, bg=self.btn_dark, fg="white", font=("Arial", 8), width=7, height=1,
                            command=lambda v=val: self.add_to_expression(v))
            btn.grid(row=r, column=c, padx=2, pady=2)
            c += 1
            if c > 5:
                c = 0
                r += 1

        # Number Pad Area
        num_frame = tk.Frame(self, bg=self.bg_color, pady=10)
        num_frame.pack(expand=True, fill="both", padx=10)

        num_keys = [
            ("7", "7"), ("8", "8"), ("9", "9"), ("DEL", "del"), ("AC", "ac"),
            ("4", "4"), ("5", "5"), ("6", "6"), ("×", "*"), ("÷", "/"),
            ("1", "1"), ("2", "2"), ("3", "3"), ("+", "+"), ("-", "-"),
            ("0", "0"), (".", "."), ("x10ˣ", "*10**"), ("Ans", "ans"), ("=", "calc")
        ]

        r, c = 0, 0
        for text, val in num_keys:
            color = self.btn_light
            fg = "black"
            if text in ["DEL", "AC"]:
                color = self.btn_action
                fg = "white"
            elif not text.isdigit() and text != ".":
                color = "#e0e0e0"

            btn = tk.Button(num_frame, text=text, bg=color, fg=fg, font=("Arial", 14, "bold"), width=5, height=2,
                            command=lambda v=val: self.handle_input(v))
            btn.grid(row=r, column=c, padx=3, pady=3, sticky="nsew")
            c += 1
            if c > 4:
                c = 0
                r += 1

        for i in range(5):
            num_frame.columnconfigure(i, weight=1)

    def handle_input(self, val):
        if val == "ac":
            self.clear_all()
        elif val == "del":
            self.expression = self.expression[:-1]
            self.update_display()
        elif val == "calc":
            self.calculate()
        elif val == "ans":
            self.add_to_expression(self.ans)
        else:
            self.add_to_expression(val)

    def add_to_expression(self, val):
        if val:
            self.expression += str(val)
            self.update_display()

    def calculate(self):
        try:
            # Auto-close parentheses
            open_p = self.expression.count("(")
            close_p = self.expression.count(")")
            if open_p > close_p:
                self.expression += ")" * (open_p - close_p)

            # Evaluate using math module
            result = eval(self.expression, {"math": math, "__builtins__": None})
            
            # Format result
            if isinstance(result, float) and result.is_integer():
                result = int(result)
            
            self.ans = str(result)
            self.screen_top.config(text=self.expression.replace("math.", "").replace("radians(", ""))
            self.expression = str(result)
            self.update_display()
        except Exception:
            self.screen_main.config(text="Math ERROR")
            self.expression = ""

    def clear_all(self):
        self.expression = ""
        self.screen_top.config(text="")
        self.update_display()

    def update_display(self):
        # Display cleanup
        disp = self.expression.replace("math.", "").replace("radians(", "").replace("*", "×").replace("/", "÷")
        if not disp:
            self.screen_main.config(text="0")
        else:
            self.screen_main.config(text=disp[-15:]) # Show tail of long expressions

    def toggle_shift(self):
        self.shift_mode = not self.shift_mode
        self.screen_top.config(text="SHIFT" if self.shift_mode else "")

    def toggle_alpha(self):
        self.alpha_mode = not self.alpha_mode
        self.screen_top.config(text="ALPHA" if self.alpha_mode else "")

if __name__ == "__main__":
    app = CasioClasswiz()
    app.mainloop()