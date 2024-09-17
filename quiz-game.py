import tkinter as tk
from tkinter import ttk, messagebox
import json
import random
import os

class FlexibleQuizGame:
    def __init__(self, master):
        self.master = master
        self.master.title("Python Quiz")
        self.master.geometry("500x400")
        self.master.config(bg="#f0f0f0")

        self.style = ttk.Style()
        self.style.theme_use('clam')
        self.style.configure('TFrame', background='#f0f0f0')
        self.style.configure('TButton', background='#4CAF50', foreground='white', font=('Arial', 10, 'bold'))
        self.style.configure('TRadiobutton', background='#f0f0f0', font=('Arial', 10))
        self.style.configure('TLabel', background='#f0f0f0', font=('Arial', 10))

        self.questions = []
        self.score = 0
        self.current_question = 0

        self.create_widgets()
        self.load_quiz_file()

    def create_widgets(self):
        self.main_frame = ttk.Frame(self.master, padding="20")
        self.main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        self.master.columnconfigure(0, weight=1)
        self.master.rowconfigure(0, weight=1)

        self.question_label = ttk.Label(self.main_frame, text="", wraplength=460, font=("Arial", 12, "bold"))
        self.question_label.grid(row=0, column=0, columnspan=2, pady=(0, 20), sticky=tk.W)

        self.var = tk.StringVar()
        self.option_buttons = []
        for i in range(4):  # Assuming all questions have 4 options
            button = ttk.Radiobutton(self.main_frame, text="", variable=self.var, value="")
            button.grid(row=i+1, column=0, columnspan=2, sticky=tk.W, pady=5)
            self.option_buttons.append(button)

        self.button_frame = ttk.Frame(self.main_frame)
        self.button_frame.grid(row=5, column=0, columnspan=2, sticky=tk.E, pady=20)

        self.submit_button = ttk.Button(self.button_frame, text="Submit", command=self.check_answer)
        self.submit_button.pack(side=tk.RIGHT)

        self.main_frame.columnconfigure(0, weight=1)
        self.main_frame.columnconfigure(1, weight=0)

    def load_quiz_file(self):
        file_path = os.path.join(os.path.dirname(__file__), "quiz-data.json")
        try:
            with open(file_path, 'r') as file:
                self.questions = json.load(file)
            self.load_question()
        except FileNotFoundError:
            messagebox.showerror("Error", f"The file 'quiz-data.json' was not found in the script's directory.")
            self.master.quit()
        except json.JSONDecodeError:
            messagebox.showerror("Invalid File", f"The file 'quiz-data.json' is not a valid JSON file.")
            self.master.quit()
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred while reading the file: {str(e)}")
            self.master.quit()

    def load_question(self):
        if self.current_question < len(self.questions):
            question = self.questions[self.current_question]
            self.question_label.config(text=question["question"])
            options = question["options"]
            random.shuffle(options)
            for i, option in enumerate(options):
                self.option_buttons[i].config(text=option, value=option)
            self.var.set(None)
            self.submit_button.config(state=tk.NORMAL)
        else:
            self.show_result()

    def check_answer(self):
        if not self.var.get():
            return  # If no answer selected, do nothing

        question = self.questions[self.current_question]
        if self.var.get() == question["correct_answer"]:
            self.score += 1

        self.current_question += 1
        self.load_question()

    def show_result(self):
        percentage = (self.score / len(self.questions)) * 100
        result_text = f"Quiz completed!\nYour score: {self.score}/{len(self.questions)}\nPercentage: {percentage:.2f}%"
        self.question_label.config(text=result_text)
        for button in self.option_buttons:
            button.grid_remove()
        self.button_frame.grid_remove()

if __name__ == "__main__":
    root = tk.Tk()
    quiz_game = FlexibleQuizGame(root)
    root.mainloop()