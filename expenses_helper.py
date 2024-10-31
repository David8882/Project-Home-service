# import sqlite3
import tkinter as tk
from tkinter import ttk, filedialog
from tkcalendar import DateEntry, Calendar
# from datetime import datetime
# from reportlab.lib.pagesizes import A4
# from reportlab.pdfgen import canvas
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfbase import pdfmetrics
pdfmetrics.registerFont(TTFont('Hebrew', 'NotoSansHebrew_Condensed-ExtraBold.ttf'))
items_months = ['', 'ינואר', 'פברואר', 'מרץ', 'אפריל', 'מאי', 'יוני', 'יולי', 'אוגוסט', 'ספטמבר', 'אוקטובר', 'נובמבר',
                'דצמבר']
items = ['E1', 'E2', 'E3', 'E4', 'E5', 'E6', 'E7', 'E8', 'E9', 'E10', 'E11', 'G', 'F', 'F +G', '']
items2 = ['עמית סבג', "יוסף ג'אנו", 'אאידה בראודסקי', 'מתן ומור קדוש', 'נאמן משה', 'אילנה צבאג', 'מיטל נומה',
          'עדי אברדם', 'טליה ויעקב עובדיה', 'פטריסיה',  'נעמי ויואל סבג', '', '', '', '']

# יצירת מילון שמקשר בין items, items2, items_months
items_dict = dict(zip(items, items2))


class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.frame_add_from = FrameAddForm(self)
        self.frame_list = FrameList(self)
        self.frame_resit = FrameResit(self)
        self.frame_explor = FrameExplor(self)
        self.title('ועד בית')
        self.geometry('1540x850')
        self.put_frames()

    def put_frames(self):
        self.frame_add_from.place(relx=0, rely=0, relwidth=0.5, relheight=0.5)
        self.frame_list.place(relx=0.5, rely=0, relwidth=0.5, relheight=0.5)
        self.frame_explor.place(relx=0, rely=0.5, relwidth=0.5, relheight=0.5)
        self.frame_resit.place(relx=0.5, rely=0.5, relwidth=0.5, relheight=0.5)


class FrameAddForm(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.put_widgets()
        self.f_resit = tk.Entry(self, justify=tk.RIGHT)
        self.l_resit = tk.Label(self, text=":מספר קבלה", font="Helvetica 14 bold")
        self.f_num_house = tk.Label(self, text=":דירה", font="Helvetica 14 bold")
        self.l_num_house = ttk.Combobox(self, values=items, state="readonly")

        self.f_dayp = tk.Label(self, text=":יום", font="Helvetica 14 bold")
        self.l_dayp = DateEntry(self, foreground='black', normalforeground='black',
                                selectforeground='red', background='white',
                                data_pattern='dd-mm-YYYY')

        self.f_money_ = tk.Entry(self, justify=tk.RIGHT)
        self.l_money_ = tk.Label(self, text=":כמה שילם", font="Helvetica 14 bold")

        self.f_why_ = tk.Entry(self, justify=tk.RIGHT)
        self.l_why_ = tk.Label(self, text=":עבור", font="Helvetica 14 bold")

        self.f_months = ttk.Combobox(self, values=items_months, state="readonly")
        # submit button
        # self.btn_submit = ttk.Button(self, text="הגשה", command=form_submit)
        # self.btn_delete = ttk.Button(self, text="מחיקה", command=delete_row)

    def put_widgets(self):
        tk.Label(self, width=150, height=150, bg='green').pack(expand=True)

        self.f_num_house = tk.Label(self, text=":דירה", font="Helvetica 14 bold")
        self.l_num_house = ttk.Combobox(self, values=items, state="readonly")

        self.f_dayp = tk.Label(self, text=":יום", font="Helvetica 14 bold")
        self.l_dayp = DateEntry(self, foreground='black', normalforeground='black',
                                selectforeground='red', background='white',
                                data_pattern='dd-mm-YYYY')

        self.f_money_ = tk.Entry(self, justify=tk.RIGHT)
        self.l_money_ = tk.Label(self, text=":כמה שילם", font="Helvetica 14 bold")

        self.f_why_ = tk.Entry(self, justify=tk.RIGHT)
        self.l_why_ = tk.Label(self, text=":עבור", font="Helvetica 14 bold")

        self.f_months = ttk.Combobox(self, values=items_months, state="readonly")
        # l_months = tk.Label(frame_add_from, text=":חודש", font="Helvetica 14 bold")
        # כפתור הגשה
        # self.btn_submit = ttk.Button(self, text="הגשה", command=form_submit)
        # self.btn_delete = ttk.Button(self, text="מחיקה", command=delete_row)

        self.f_resit.grid(row=0, column=0, sticky='w', padx=150, pady=10)
        self.l_resit.grid(row=0, column=1, sticky='w', padx=10, pady=10)
        self.f_num_house.grid(row=1, column=1, sticky='w', padx=10, pady=10)
        self.l_num_house.grid(row=1, column=0, sticky='w', padx=150, pady=10)
        self.f_dayp.grid(row=2, column=1, sticky='w', padx=10, pady=10)
        self.l_dayp.grid(row=2, column=0, sticky='w', padx=150, pady=10)
        self.f_money_.grid(row=3, column=0, sticky='w', padx=150, pady=10)
        self.l_money_.grid(row=3, column=1, sticky='w', padx=10, pady=10)
        self.f_why_.grid(row=4, column=0, sticky='w', padx=150, pady=10)
        self.l_why_.grid(row=4, column=1, sticky='w', padx=10, pady=10)
        self.f_months.grid(row=5, column=0, sticky='w', padx=150, pady=10)

        self.btn_submit.grid(row=6, column=0, columnspan=1, sticky='n', padx=160, pady=10)
        self.btn_delete.grid(row=6, column=1, columnspan=2, sticky='n', padx=10, pady=10)

    # def form_submit(self):
    #     selected_item = self.l_num_house.get()  # מקבל את ה-e1, e2 שנבחר
    #
    #     # מייבא את השם לפי הערך שנבחר ב-Combobox
    #     name_ = items_dict.get(selected_item)
    #     num_house = selected_item  # הקוד של הדירה הוא אותו קוד כמו ה-e1, e2
    #
    #     resit = self.f_resit.get()
    #     if not resit:
    #         resit = last_resit_to_now()
    #
    #     dayp = self.l_dayp.get()
    #     dayp = datetime.strptime(dayp, '%m/%d/%y').strftime('%d/%m/%Y')
    #     money_ = self.f_money_.get()
    #     why_ = f' {f_why_.get()}  {f_months.get()}'
    #     print(type(resit), type(num_house), type(name_), type(dayp), type(money_), type(why_))
    #
    #     insert_home = (resit, num_house, name_, dayp, money_, why_)
    #
    #     # Insert the new data into the database
    #     with sqlite3.connect('C:/Users/jacki/PycharmProjects/python122/database.db') as db:
    #         cursor = db.cursor()
    #         query = """INSERT INTO home(resit, house_number, name, dayp, money_, why)
    #                    VALUES (?,?,?,?,?,?)"""
    #         cursor.execute(query, insert_home)
    #         db.commit()
    #
    #     update_table()  # Update the table with the new data
    #
    #     # Reset input fields after saving data
    #     self.f_resit.delete(0, tk.END)  # Reset receipt field
    #     self.l_num_house.set('')  # Reset combo box for house number
    #     self.l_dayp.set_date(datetime.now())  # Reset date to today
    #     self.f_money_.delete(0, tk.END)  # Reset money field
    #     self.f_why_.delete(0, tk.END)  # Reset reason field


class FrameList(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.put_widgets()

    def put_widgets(self):
        tk.Label(self, width=150, height=150, bg='blue').pack(expand=True)


class FrameResit(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.put_widgets()

    def put_widgets(self):
        tk.Label(self, width=150, height=150, bg='yellow').pack(expand=True)


class FrameExplor(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.put_widgets()

    def put_widgets(self):
        tk.Label(self, width=150, height=150, bg='red').pack(expand=True)


app = App()
app.mainloop()
