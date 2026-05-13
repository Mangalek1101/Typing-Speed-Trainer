import customtkinter as ctk
import time
import random
from tkinter import messagebox

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")


class TypingApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        # Словари с текстами
        self.text_data = {
            "RU": [
                "Системный анализ и проектирование программного обеспечения.",
                "Разработка веб-приложений на языке программирования Питон.",
                "Автоматизированные системы обучения упрощают процесс познания.",
                "Слепая печать значительно повышает скорость работы."
            ],
            "EN": [
                "System analysis and software engineering projects.",
                "Developing web applications using the Python language.",
                "Automated learning systems simplify the process of cognition.",
                "Touch typing significantly increases your working speed."
            ]
        }

        self.current_lang = "RU"
        self.title("SpeedType Pro Multi")
        self.geometry("800x550")

        # Настройки UI
        self.setup_ui()

    def setup_ui(self):
        # Переключатель языка
        self.lang_var = ctk.StringVar(value=self.current_lang)
        self.lang_switch = ctk.CTkSegmentedButton(self, values=["RU", "EN"],
                                                  variable=self.lang_var,
                                                  command=self.change_language)
        self.lang_switch.pack(pady=10)

        self.label_title = ctk.CTkLabel(self, text="ТРЕНАЖЕР ПЕЧАТИ", font=("Arial", 28, "bold"))
        self.label_title.pack(pady=10)

        self.target_text = random.choice(self.text_data[self.current_lang])
        self.start_time = None
        self.is_running = False

        self.text_display = ctk.CTkTextbox(self, width=700, height=120, font=("Consolas", 22))
        self.text_display.pack(padx=20, pady=10)

        self.text_display.tag_config("correct", foreground="#2ECC71")
        self.text_display.tag_config("wrong", foreground="#E74C3C")
        self.text_display.tag_config("current", background="#34495E")

        self.update_display()

        self.entry = ctk.CTkEntry(self, width=700, height=50, font=("Arial", 18))
        self.entry.pack(pady=20)
        self.entry.bind("<KeyRelease>", self.process_typing)

        self.stats_label = ctk.CTkLabel(self, text="WPM: 0 | Точность: 100%", font=("Arial", 16))
        self.stats_label.pack(pady=10)

        self.btn_restart = ctk.CTkButton(self, text="НОВЫЙ ТЕКСТ / NEW TEXT", command=self.reset_game)
        self.btn_restart.pack(pady=10)

    def change_language(self, lang):
        self.current_lang = lang
        title = "ТРЕНАЖЕР ПЕЧАТИ" if lang == "RU" else "TYPING TRAINER"
        self.label_title.configure(text=title)
        self.reset_game()

    def update_display(self):
        self.text_display.configure(state="normal")
        self.text_display.delete("0.0", "end")
        self.text_display.insert("0.0", self.target_text)
        self.text_display.configure(state="disabled")

    def process_typing(self, event):
        if not self.is_running:
            self.start_time = time.time()
            self.is_running = True

        typed = self.entry.get()
        self.highlight_text(typed)

        if len(typed) > 0:
            elapsed = (time.time() - self.start_time) / 60
            wpm = round((len(typed) / 5) / elapsed) if elapsed > 0 else 0
            self.stats_label.configure(text=f"WPM: {wpm} | Lng: {self.current_lang}")

        if typed == self.target_text:
            self.is_running = False
            msg = "Победа!" if self.current_lang == "RU" else "Victory!"
            messagebox.showinfo(self.current_lang, f"{msg} WPM: {wpm}")
            self.reset_game()

    def highlight_text(self, typed):
        self.text_display.configure(state="normal")
        self.text_display.tag_remove("correct", "1.0", "end")
        self.text_display.tag_remove("wrong", "1.0", "end")
        self.text_display.tag_remove("current", "1.0", "end")

        for i, char in enumerate(typed):
            if i < len(self.target_text):
                tag = "correct" if char == self.target_text[i] else "wrong"
                self.text_display.tag_add(tag, f"1.{i}")

        if len(typed) < len(self.target_text):
            self.text_display.tag_add("current", f"1.{len(typed)}")
        self.text_display.configure(state="disabled")

    def reset_game(self):
        self.is_running = False
        self.target_text = random.choice(self.text_data[self.current_lang])
        self.update_display()
        self.entry.delete(0, 'end')
        self.stats_label.configure(text=f"WPM: 0 | Lng: {self.current_lang}")


if __name__ == "__main__":
    app = TypingApp()
    app.mainloop()
