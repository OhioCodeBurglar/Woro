import tkinter as tk
from tkinter import ttk
import time

class TimerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Timer App")
        
        self.progress = tk.DoubleVar()
        self.progress.set(0)
        
        self.progress_bar = ttk.Progressbar(root, variable=self.progress, length=1500, maximum=10000)
        self.progress_bar.pack(pady=20)
        
        self.break_label = tk.Label(root, text="Break", fg="green")
        
        self.running = True
        self.in_break = False
        self.load_elapsed_time()  # Load elapsed time from file
        self.update_progress()
        
        self.root.bind("<F1>", self.toggle_timer)
        
    def update_progress(self):
        if self.running and not self.in_break:
            elapsed_time = time.time() - self.start_time
            self.progress.set(elapsed_time / (3600 * 10000) * 100)
            self.save_elapsed_time(elapsed_time)  # Save elapsed time to file
            self.root.after(100, self.update_progress)
        else:
            self.break_label.pack()
    
    def toggle_timer(self, event):
        if self.in_break:
            self.running = True
            self.in_break = False
            self.break_label.pack_forget()
            self.start_time = time.time()
            self.update_progress()
        else:
            self.running = False
            self.in_break = True
            self.break_label.pack_forget()
            self.update_progress()
    
    def save_elapsed_time(self, elapsed_time):
        with open("timed_worked.txt", 'w') as file:
            file.write(str(elapsed_time))
    
    def load_elapsed_time(self):
        try:
            with open("timed_worked.txt", 'r') as file:
                content = file.read().strip()
                if content:
                    elapsed_time = float(content)
                    self.start_time = time.time() - elapsed_time
                else:
                    self.start_time = time.time()  # Set start_time to current time
        except FileNotFoundError:
            self.start_time = time.time()  # Set start_time to current time if the file doesn't exist

if __name__ == "__main__":
    root = tk.Tk()
    app = TimerApp(root)
    root.mainloop()

