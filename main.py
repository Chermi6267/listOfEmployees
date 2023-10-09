import sqlite3
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox


# Класс главного окна
class Main(tk.Frame):
    def __init__(self, root):
        super().__init__(root)
        self.init_main()
        self.db = db
        self.view_records()

    # Инициализация виджетов главного окна
    def init_main(self):
        toolbar = tk.Frame(bg="#d7d7d7", bd=2)
        toolbar.pack(side=tk.TOP, fill=tk.X)

        # Кнопка добавления
        self.img_add = tk.PhotoImage(file='img/add.png')
        btn_add = tk.Button(toolbar, text='Add', bg='#d7d7d7', bd=0,
                            image=self.img_add, command=self.open_child)
        btn_add.pack(side=tk.LEFT)

        # Кнопка изменения
        self.img_upd = tk.PhotoImage(file='img/upd.png')
        btn_upd = tk.Button(toolbar, text='Upd', bg='#d7d7d7', bd=0,
                            image=self.img_upd, command=self.open_update_child)
        btn_upd.pack(side=tk.LEFT)

        # Кнопка удаления
        self.img_del = tk.PhotoImage(file='img/del.png')
        btn_del = tk.Button(toolbar, text='Del', bg='#d7d7d7', bd=0,
                            image=self.img_del, command=self.delete_records)
        btn_del.pack(side=tk.LEFT)

        # Кнопка поиска
        self.img_search = tk.PhotoImage(file='img/search.png')
        btn_search = tk.Button(toolbar, text='Search', bg='#d7d7d7', bd=0,
                               image=self.img_search, command=self.open_search)
        btn_search.pack(side=tk.LEFT)

        # Кнопка обновления
        self.img_refresh = tk.PhotoImage(file='img/refresh.png')
        btn_refresh = tk.Button(toolbar, text='Refresh', bg='#d7d7d7', bd=0,
                                image=self.img_refresh, command=self.view_records)
        btn_refresh.pack(side=tk.LEFT)

        # Отображение элементов через treeview
        self.tree = ttk.Treeview(root,
                                 columns=('id', 'name', 'phone', 'salary', 'email'),
                                 height=45, show='headings')
        self.tree.column('id', width=50, anchor=tk.CENTER)
        self.tree.column('name', width=250, anchor=tk.CENTER)
        self.tree.column('phone', width=190, anchor=tk.CENTER)
        self.tree.column('salary', width=190, anchor=tk.CENTER)
        self.tree.column('email', width=200, anchor=tk.CENTER)

        self.tree.heading('id', text='id')
        self.tree.heading('name', text='ФИО')
        self.tree.heading('phone', text='Телефон')
        self.tree.heading('salary', text='Заработная плата')
        self.tree.heading('email', text='E-mail')
        self.tree.pack(side=tk.LEFT)

        # Добавление скроллбара
        scroll = tk.Scrollbar(root, command=self.tree.yview)
        scroll.pack(side=tk.RIGHT, fill=tk.Y)
        self.tree.configure(yscrollcommand=scroll.set)

    # Метод добавления сотрудника
    def records(self, name, phone, salary, email):
        if name == '' or phone == '' or salary == '' or email == '':
            tk.messagebox.showerror("Ошибка", "Вы ввели не все поля")
        else:
            self.db.insert_data(name, phone, salary, email)
            self.view_records()

    # Отображение данных в treeview
    def view_records(self):
        self.db.cur.execute('SELECT * FROM staff')
        [self.tree.delete(i) for i in self.tree.get_children()]
        [self.tree.insert('', 'end', values=i) for i in self.db.cur.fetchall()]

    # Метод поиска сотрудника по ФИО
    def search_records(self, name):
        self.db.cur.execute('SELECT * FROM staff WHERE name LIKE ?',
                            ('%' + name + '%',))
        [self.tree.delete(i) for i in self.tree.get_children()]
        [self.tree.insert('', 'end', values=i) for i in self.db.cur.fetchall()]

    # Метод изменения данных о сотруднике 
    def update_record(self, name, phone, salary, email):
        id = self.tree.set(self.tree.selection()[0], '#1')
        self.db.cur.execute('''
            UPDATE staff
            SET name = ?, phone = ?, salary = ?, email = ?
            WHERE id = ?
        ''', (name, phone, salary, email, id))
        self.db.conn.commit()
        self.view_records()

    # Метод удаления сотрудника
    def delete_records(self):
        for row in self.tree.selection():
            self.db.cur.execute('DELETE FROM staff WHERE id = ?',
                                (self.tree.set(row, '#1'), ))
        self.db.conn.commit()
        self.view_records()

    # Метод вызывающий дочернее окно - добавления сотрудника
    def open_child(self):
        Child()

    # Метод вызывающий дочернее окно - изменение данных сотрудника 
    def open_update_child(self):
        selected_item = self.tree.selection()
        if not selected_item:
            tk.messagebox.showerror("Ошибка", "Выберите сотрудника для изменения.")
            return
        Update()

    # Метод вызывающий дочернее окно - поиск сотрудника по ФИО
    def open_search(self):
        Search()


# Класс дочернего окна
class Child(tk.Toplevel):
    def __init__(self):
        super().__init__(root)
        self.init_child()
        self.view = app

    # Инициализация виджетов дочернего окна
    def init_child(self):
        self.title("Добавление сотрудника")
        self.geometry("400x230")
        self.resizable(False, False)
        # Перехватываем все события
        self.grab_set()
        # Перехватываем фокус
        self.focus_set()

        label_name = tk.Label(self, text="ФИО: ")
        label_name.place(x=50, y=50)
        self.entry_name = tk.Entry(self)
        self.entry_name.place(x=200, y=50)

        label_phone = tk.Label(self, text="Телефон: ")
        label_phone.place(x=50, y=80)
        self.entry_phone = tk.Entry(self)
        self.entry_phone.place(x=200, y=80)

        label_salary = tk.Label(self, text="Заработная плата: ")
        label_salary.place(x=50, y=110)
        self.entry_salary = tk.Entry(self)
        self.entry_salary.place(x=200, y=110)

        label_email = tk.Label(self, text="E-mail: ")
        label_email.place(x=50, y=140)
        self.entry_email = tk.Entry(self)
        self.entry_email.place(x=200, y=140)

        btn_cancel = tk.Button(self, text='Закрыть', command=self.destroy)
        btn_cancel.place(x=50, y=180)

        self.btn_add = tk.Button(self, text='Добавить')
        self.btn_add.bind('<Button-1>', lambda ev: self.view.records(self.entry_name.get(),
                                                                self.entry_phone.get(),
                                                                self.entry_salary.get(),
                                                                self.entry_email.get()))
        self.btn_add.bind('<Button-1>', lambda ev: self.destroy(), add='+')
        self.btn_add.place(x=260, y=180)


# Класс для поиска
class Search(tk.Toplevel):
    def __init__(self):
        super().__init__(root)
        self.init_child()
        self.view = app

    def init_child(self):
        self.title('Поиск сотрудника')
        self.geometry('300x100')
        self.resizable(False, False)
        # Перехватываем все события
        self.grab_set()
        # Перехватываем фокус
        self.focus_set()

        label_name = tk.Label(self, text='ФИО:')
        label_name.place(x=30, y=30)

        self.entry_name = tk.Entry(self)
        self.entry_name.place(x=130, y=30)

        btn_cancel = tk.Button(self, text='Закрыть', command=self.destroy)
        btn_cancel.place(x=150, y=70)

        self.btn_add = tk.Button(self, text='Найти')
        self.btn_add.bind('<Button-1>',
                          lambda ev: self.view.search_records(self.entry_name.get()))
        self.btn_add.bind('<Button-1>', lambda ev: self.destroy(), add='+')
        self.btn_add.place(x=225, y=70)


# Класс для обновления данных о сотруднике
class Update(Child):
    def __init__(self):
        super().__init__()
        self.init_update()
        self.db = db
        self.default_data()

    def init_update(self):
        self.title('Изменение данных сотрудника')
        self.btn_add.destroy()
        self.btn_upd = tk.Button(self, text='Изменить')
        self.btn_upd.bind('<Button-1>',
                          lambda ev: self.view.update_record(self.entry_name.get(),
                                                             self.entry_phone.get(),
                                                             self.entry_salary.get(),
                                                             self.entry_email.get()))
        self.btn_upd.bind('<Button-1>', lambda ev: self.destroy(), add='+')
        self.btn_upd.place(x=265, y=180)

    # Автозаполнение данных сотрудника
    def default_data(self):
        id = self.view.tree.set(self.view.tree.selection()[0], '#1')
        self.db.cur.execute('SELECT * FROM staff WHERE id = ?', (id, ))
        row = self.db.cur.fetchone()
        self.entry_name.insert(0, row[1])
        self.entry_phone.insert(0, row[2])
        self.entry_salary.insert(0, row[3])
        self.entry_email.insert(0, row[4])


# Класс БД
class Db:
    def __init__(self) -> None:
        self.conn = sqlite3.connect('staff.db')
        self.cur = self.conn.cursor()
        self.cur.execute('''
        CREATE TABLE IF NOT EXISTS staff (
                        id INTEGER PRIMARY KEY, 
                        name TEXT NOT NULL,
                        phone TEXT NOT NULL,
                        salary FLOAT NOT NULL,
                        email TEXT NOT NULL
                        )''')
        self.conn.commit()

    def insert_data(self, name, phone, salary, email):
        self.cur.execute('''
                        INSERT INTO staff (name, phone, salary, email)
                        VALUES(?, ?, ?, ?)''', (name, phone, salary, email))
        self.conn.commit()


# При запуске программы
if __name__ == "__main__":
    root = tk.Tk()
    db = Db()
    app = Main(root)
    root.title('Сотрудники')
    root.geometry('900x450')
    root.resizable(False, False)
    root.mainloop()
