import tkinter as tk
from tkinter import ttk
import time

class MiniTuringMachine:
    def __init__(self):
        self.tape = []
        self.head = 0
        self.state = 'q0'
        
        self.transitions = {
            ('q0', '1'): ('q1', '1', 'R'),
            ('q1', '0'): ('q2', '0', 'R'),
            ('q2', '+'): ('q3', '+', 'R'),
            ('q3', '0'): ('q3', '0', 'R'),
            ('q3', '1'): ('q3', '1', 'R'),
            ('q3', '='): ('q4', '=', 'R'),
            ('q4', ''): ('q5', '', 'S')
        }
        
    def step(self):
        if self.head >= len(self.tape):
            self.tape.append('')
            
        current = self.tape[self.head]
        key = (self.state, current)
        
        if key not in self.transitions:
            return False
            
        self.state, symbol, move = self.transitions[key]
        self.tape[self.head] = symbol
        
        if move == 'R':
            self.head += 1
        return True
        
    def get_result(self):
        try:
            expr = ''.join(self.tape)
            parts = expr.split('+')
            if len(parts) != 2:
                return None
            num1 = int(parts[0].strip(), 2)
            num2 = int(parts[1].split('=')[0].strip(), 2)
            return f"{bin(num1 + num2)[2:]} (bin) = {num1 + num2} (dec)"
        except:
            return None

class MiniTuringGUI:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Mini Turing")
        self.root.geometry("600x400")
        self.root.configure(bg="#2d2d2d")
        
        self.machine = MiniTuringMachine()
        self.running = False
        self.delay = 300
        
        self.setup_ui()
        
    def setup_ui(self):
        # Estilo
        style = ttk.Style()
        style.configure("TFrame", background="#2d2d2d")
        style.configure("TLabel", 
                       background="#2d2d2d", 
                       foreground="#ffffff",
                       font=("Courier", 10))
        
        # Marco principal
        main = ttk.Frame(self.root)
        main.pack(expand=True, fill='both', padx=10, pady=10)

        # Texto de ejemplo
        example_text = ttk.Label(main, 
                               text="Formato de entrada: 10+10= (números binarios)",
                               font=("Courier", 10))
        example_text.pack(pady=5)
        
        # Entrada
        input_frame = ttk.Frame(main)
        input_frame.pack(fill='x', pady=5)
        
        self.input_var = tk.StringVar()
        entry = tk.Entry(input_frame,
                        textvariable=self.input_var,
                        bg="#404040",
                        fg="#ffffff",
                        insertbackground="#ffffff",
                        font=("Courier", 12))
        entry.pack(side='left', expand=True, fill='x')
        
        # Botones
        btn_frame = ttk.Frame(main)
        btn_frame.pack(fill='x', pady=5)
        
        buttons = [
            ("▶", self.toggle_run, "#4CAF50"),
            ("⏩", self.step, "#2196F3"),
            ("⟲", self.reset, "#f44336")
        ]
        
        for text, cmd, color in buttons:
            btn = tk.Button(btn_frame,
                          text=text,
                          command=cmd,
                          bg=color,
                          fg="#ffffff",
                          font=("Courier", 12, "bold"),
                          width=3,
                          relief='flat')
            btn.pack(side='left', padx=2)
        
        # Canvas para la cinta
        self.tape_canvas = tk.Canvas(main,
                                   bg="#1a1a1a",
                                   height=100,
                                   highlightthickness=0)
        self.tape_canvas.pack(fill='x', pady=10)
        
        # Panel de estado
        status = ttk.Frame(main)
        status.pack(fill='x')
        
        self.state_var = tk.StringVar(value="Estado: q0")
        ttk.Label(status, textvariable=self.state_var).pack(side='left')

        # Panel de resultado (más grande y centrado)
        result_frame = ttk.Frame(main)
        result_frame.pack(fill='x', pady=10)
        
        self.result_var = tk.StringVar()
        result_label = ttk.Label(result_frame, 
                               textvariable=self.result_var,
                               font=("Courier", 16, "bold"),
                               foreground="#4CAF50")
        result_label.pack(expand=True)
        
    def draw_tape(self):
        self.tape_canvas.delete('all')
        
        # Dimensiones
        w, h = 40, 40
        margin = 5
        start_x = 10
        y = 30
        
        for i, symbol in enumerate(self.machine.tape):
            x = start_x + (i * (w + margin))
            
            # Celda
            color = "#404040" if i != self.machine.head else "#1e881e"
            self.tape_canvas.create_rectangle(x, y, x+w, y+h, 
                                           fill=color, outline="#666666")
            
            # Símbolo
            self.tape_canvas.create_text(x + w/2, y + h/2,
                                       text=symbol,
                                       fill="#ffffff",
                                       font=("Courier", 14))
            
            # Posición
            self.tape_canvas.create_text(x + w/2, y - 15,
                                       text=str(i),
                                       fill="#666666",
                                       font=("Courier", 8))
        
        # Cabezal
        head_x = start_x + (self.machine.head * (w + margin))
        self.tape_canvas.create_polygon(
            head_x + w/2, y + h + 5,
            head_x + w/2 - 8, y + h + 15,
            head_x + w/2 + 8, y + h + 15,
            fill="#4CAF50"
        )
        
    def initialize(self):
        if not self.machine.tape:
            expr = self.input_var.get().strip()
            if not expr:
                return False
            self.machine.tape = list(expr)
            self.machine.head = 0
            self.machine.state = 'q0'
            self.draw_tape()
            return True
        return True
        
    def step(self):
        if not self.initialize():
            return
            
        if self.machine.step():
            self.state_var.set(f"Estado: {self.machine.state}")
            self.draw_tape()
            
            if self.machine.state == 'q5':
                result = self.machine.get_result()
                if result:
                    self.result_var.set(f"Resultado: {result}")
                else:
                    self.result_var.set("Error: Expresión inválida")
                self.running = False
                return False
            return True
        else:
            self.result_var.set("Error: Expresión inválida")
            self.running = False
            return False
            
    def toggle_run(self):
        self.running = not self.running
        if self.running:
            self.run_step()
            
    def run_step(self):
        if self.running and self.step():
            self.root.after(self.delay, self.run_step)
            
    def reset(self):
        self.running = False
        self.machine = MiniTuringMachine()
        self.input_var.set("")
        self.state_var.set("Estado: q0")
        self.result_var.set("")
        self.draw_tape()
        
    def run(self):
        self.root.mainloop()

if __name__ == "__main__":
    app = MiniTuringGUI()
    app.run()