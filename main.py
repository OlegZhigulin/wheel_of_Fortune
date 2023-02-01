import customtkinter
from tkinter import messagebox
from PIL import Image, ImageTk
import sqlite3


class App(customtkinter.CTk):
    con = sqlite3.connect("main.db")
    cursor = con.cursor()
    cursor.execute("""CREATE TABLE IF NOT EXISTS tasks
                (id INTEGER PRIMARY KEY AUTOINCREMENT,
                 task TEXT)
            """)
    customtkinter.set_appearance_mode("dark")

    def __init__(self):
        super().__init__()

        self.geometry("640x480")
        self.title("Рандомная задача")
        self.resizable(False, False)
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure((0, 1), weight=1)
        self.textbox = customtkinter.CTkTextbox(self,
                                                fg_color='#e6e7e8',
                                                text_color='#0f0f0f',
                                                state=customtkinter.DISABLED,
                                                font=('Roboto', 18))
        self.textbox.grid(row=0,
                          column=0,
                          columnspan=2,
                          padx=20,
                          pady=(20, 0),
                          sticky="nsew")
        self.text_input_frame = customtkinter.CTkEntry(self,
                                                       placeholder_text='Текст задачи')
        self.text_input_frame.grid(row=1,
                                   column=0,
                                   padx=20,
                                   pady=20,
                                   sticky="ew")
        self.btn_add = customtkinter.CTkButton(self,
                                               command=self.add_task,
                                               corner_radius=4,
                                               fg_color='#47A76A',
                                               font=('Roboto', 18),
                                               text="Добавить")

        self.btn_add.grid(row=1,
                          column=1,
                          padx=20,
                          pady=20,
                          sticky="ew")

        self.btn_random = customtkinter.CTkButton(self,
                                                  command=self.random_task,
                                                  corner_radius=4,
                                                  fg_color='#fc7514',
                                                  font=('Roboto', 18),
                                                  text="Великий и могучий рандом!!")

        self.btn_random.grid(row=2,
                             column=0,
                             columnspan=2,
                             padx=20,
                             pady=20,
                             sticky="ew")
        self.load_all_data = self.show_all()

    def create_toplevel(self, text):
        window = customtkinter.CTkToplevel(self,
                                           )
        window.geometry("400x200")
        label = customtkinter.CTkLabel(window,
                                       compound='center',
                                       text=(
                                           f"А сегодня тебя ждет \n задача: {text}"),
                                       font=('Roboto', 18))
        label.grid(row=0,
                   column=0,
                   padx=40,
                   pady=40)

    def add_task(self):
        text = self.text_input_frame.get()
        task = (text,)
        self.text_input_frame.delete(0, 'end')
        self.cursor.execute("INSERT INTO tasks (task) VALUES (?)", task)
        self.con.commit()
        self.show_all()

    def show_all(self):
        self.textbox.configure(state=customtkinter.NORMAL,)
        self.textbox.delete('0.0', 'end')
        self.cursor.execute("SELECT * FROM tasks")
        for task in self.cursor.fetchall():
            self.textbox.insert("end", text=f'{task[0]}. {task[1]}' + '\n')
        self.textbox.configure(state=customtkinter.DISABLED,)
    def random_task(self):
        self.cursor.execute(
            "SELECT * FROM tasks ORDER BY random() LIMIT 1")
        try:
            id, text = self.cursor.fetchone()
            self.create_toplevel(text)
            self.cursor.execute(f"DELETE FROM tasks WHERE ID = {id}")
            self.con.commit()
            self.show_all()
        except TypeError:
            text = 'Добавь пару задачек для себя'
            self.create_toplevel(text)

    def on_closing(self):
        if messagebox.askokcancel("Все дела сделаны?", "это выход"):
            app.destroy()


if __name__ == "__main__":
    app = App()
    app.protocol("WM_DELETE_WINDOW", app.on_closing)
    app.mainloop()
