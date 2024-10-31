import tkinter as tk
from tkinter import ttk
from tkcalendar import DateEntry, Calendar
import expenses_helper as eh
from datetime import datetime
import sqlite3

class App(tk.Tk):
    def __int__(self,parent):
        super().__init__()
        self.title('My App')
        self['background'] = '#EBEBEB'
        self.conf = {'(pax':(10,30), 'pady':10}
        self.bold_font = 'Helvetica 13 bold'
        self.put_frames()

    def put_frames(self):
        self.add_from_frame = AddForm(self).grid(row=0,column=0,sticky='nswe')
        self.stat_frame = TableFrame(self).grid(row=0,column=1,sticky='nswe')
        self.table_frame = FindFrame(self).grid(row=1,column=0,sticky='nswe')
        self.table_frame = StatFrame(self).grid(row=1,column=1,sticky='nswe')

class AddForm(tk.Frame):
    def __int__(self,parent):
        super().__init__(parent)
        self['background'] = self.master['background']

        def form_submit():
            selected_item = l_num_house.get()  # מקבל את ה-e1, e2 שנבחר

            # מייבא את השם לפי הערך שנבחר ב-Combobox
            name_ = items_dict.get(selected_item)
            num_house = selected_item  # הקוד של הדירה הוא אותו קוד כמו ה-e1, e2

            global last_resit  # Use global variable to keep track of the last used receipt number

            # Check if a receipt number is provided
            resit = f_resit.get()
            if not resit:
                last_resit += 1  # Increment the receipt number
                resit = str(last_resit)  # Use the next receipt number

            dayp = l_dayp.get()
            dayp = datetime.strptime(dayp, '%m/%d/%y').strftime('%d/%m/%Y')
            money_ = f_money_.get()
            why_ = f' {f_why_.get()}  {f_months.get()}'

            insert_home = (resit, num_house, name_, dayp, money_, why_)

            # Insert the new data into the database
            with sqlite3.connect('C:/Users/jacki/PycharmProjects/python122/database.db') as db:
                cursor = db.cursor()
                query = """INSERT INTO home(resit, house_number, name, dayp, money_, why)
                           VALUES (?,?,?,?,?,?)"""
                cursor.execute(query, insert_home)
                db.commit()

            update_table()  # Update the table with the new data

            # Reset input fields after saving data
            f_resit.delete(0, tk.END)  # Reset receipt field
            l_num_house.set('')  # Reset combo box for house number
            # l_name_.set('')  # Reset combo box for name
            l_dayp.set_date(datetime.now())  # Reset date to today
            f_money_.delete(0, tk.END)  # Reset money field
            f_why_.delete(0, tk.END)  # Reset reason field

        def put_widgets(self):
            items_months = ['ינואר', 'פברואר', 'מרץ', 'אפריל', 'מאי', 'יוני', 'יולי', 'אוגוסט', 'ספטמבר', 'אוקטובר',
                            'נובמבר', 'דצמבר']
            items = ['e1', 'e2', 'e3', 'e4', 'e5', 'e6', 'e7', 'e8', 'e9', 'e10', 'e11']
            items2 = ['עמית סבג', "יוסף דג'אנו", 'אאידה בראודסקי', 'מתן ומור קדוש', 'נאמן משה', 'אילנה צבאג',
                      'מיטל נומה',
                      'עדי אברדן', 'טליה ויעקוב עובדיה', 'פטריסיה', 'נעמי ויואל סבג']

            # Green
            f_resit = tk.Entry(AddForm, justify=tk.RIGHT)
            l_resit = tk.Label(AddForm, text=":מספר קבלה", font="Helvetica 14 bold")
            f_num_house = tk.Label(AddForm, text=":דירה", font="Helvetica 14 bold")
            l_num_house = ttk.Combobox(AddForm, values=items)
            f_name_ = tk.Label(AddForm, text=":שם", font="Helvetica 14 bold")
            l_name_ = ttk.Combobox(AddForm, values=items2)
            f_dayp = tk.Label(AddForm, text=":יום", font="Helvetica 14 bold")
            l_dayp = DateEntry(AddForm, foreground='balck', normalforeground='black',
                               selectforeground='red', background='white',
                               data_pattern='dd-mm-YYYY')
            f_money_ = tk.Entry(AddForm, justify=tk.RIGHT)
            l_money_ = tk.Label(AddForm, text=":כמה שילם", font="Helvetica 14 bold")
            f_why_ = tk.Entry(AddForm, justify=tk.RIGHT)
            l_why_ = tk.Label(AddForm, text=":למה", font="Helvetica 14 bold")
            btn_submit = ttk.Button(AddForm, text="Submit", command=form_submit)

            f_resit.grid(row=0, column=0, sticky='w', padx=150, pady=10)
            l_resit.grid(row=0, column=1, sticky='w', padx=10, pady=10)
            f_num_house.grid(row=1, column=1, sticky='w', padx=10, pady=10)
            l_num_house.grid(row=1, column=0, sticky='w', padx=150, pady=10)
            f_name_.grid(row=2, column=1, sticky='w', padx=10, pady=10)
            l_name_.grid(row=2, column=0, sticky='w', padx=150, pady=10)
            f_dayp.grid(row=3, column=1, sticky='w', padx=10, pady=10)
            l_dayp.grid(row=3, column=0, sticky='w', padx=150, pady=10)
            f_money_.grid(row=4, column=0, sticky='w', padx=150, pady=10)
            l_money_.grid(row=4, column=1, sticky='w', padx=10, pady=10)
            f_why_.grid(row=5, column=0, sticky='w', padx=150, pady=10)
            l_why_.grid(row=5, column=1, sticky='w', padx=10, pady=10)

            btn_submit.grid(row=6, column=0, columnspan=1, sticky='n', padx=160, pady=10)


class TableFrame(tk.Frame):
    def __int__(self, parent):
        super().__init__(parent)
        self['background'] = self.master['background']

        def put_widgets(self):
            # יצירת טבלת Treeview
            table = ttk.Treeview(TableFrame)

            # הגדרת עמודות
            table = ttk.Treeview(TableFrame, show='headings')
            table['columns'] = ('Number', 'Name', 'House', 'Day', 'Money', 'Type')

            # יצירת כותרות לעמודות

            table.heading('Number', text='Number')
            table.heading('Name', text='Name')
            table.heading('House', text='House')
            table.heading('Day', text='Day')
            table.heading('Money', text='Money')
            table.heading('Type', text='Type')

            # יצירת עמודות עבור נתונים

            table.column('Number', anchor=tk.CENTER, width=50)
            table.column('Name', anchor=tk.CENTER, width=50)
            table.column('House', anchor=tk.CENTER, width=50)
            table.column('Day', anchor=tk.CENTER, width=50)
            table.column('Money', anchor=tk.CENTER, width=50)
            table.column('Type', anchor=tk.CENTER, width=50)

            def update_table():
                # Clear the table first
                for row in table.get_children():
                    table.delete(row)

                # Fetch new data from the database
                with sqlite3.connect('C:/Users/jacki/PycharmProjects/python122/database.db') as db:
                    cursor = db.cursor()
                    cursor.execute("SELECT resit, name, house_number, dayp, money_, why FROM home")
                    rows = cursor.fetchall()

                # Insert new rows into the table
                for row in rows:
                    try:
                        # Reformat the date from MM/DD/YY to DD/MM/YYYY
                        dayp = datetime.strptime(row[3], '%m/%d/%y').strftime('%d/%m/%Y')
                    except ValueError as e:
                        print(f"Date parsing error: {e}")
                        dayp = row[3]  # Fallback to the original date if parsing fails

                    new_row = (row[0], row[1], row[2], dayp, row[4], row[5])
                    table.insert('', 'end', values=new_row)

            # הצגת הטבלה
            table.pack(expand=tk.YES, fill=tk.BOTH)
            scroll_pane = ttk.Scrollbar(TableFrame, command=table.yview)
            table.configure(yscrollcommand=scroll_pane.set)
            scroll_pane.pack(side=tk.RIGHT, fill=tk.Y)
            table.pack(expand=tk.YES, fill=tk.BOTH)


class FindFrame(tk.Frame):
    def __int__(self, parent):
        super().__init__(parent)
        self['background'] = self.master['background']

        def put_widgets(self):
            pass


class StatFrame(tk.Frame):
    def __int__(self, parent):
        super().__init__(parent)
        self['background'] = self.master['background']

        def put_widgets(self):
            # Yellow
            l_number_resit = tk.Label(StatFrame, text=":קבלה", font="Helvetica 14 bold")
            l_number_resit_copy = tk.Label(StatFrame, text=200, font="Helvetica 14 bold")
            l_number_house = tk.Label(StatFrame, text=":בית", font="Helvetica 14 bold")
            l_number_house_copy = tk.Label(StatFrame, text="3G", font="Helvetica 14 bold")
            l_name = tk.Label(StatFrame, text=":שם", font="Helvetica 14 bold")
            l_name_copy = tk.Label(StatFrame, text="Moshe", font="Helvetica 14 bold")
            l_day = tk.Label(StatFrame, text=":יום", font="Helvetica 14 bold")
            l_day_copy = tk.Label(StatFrame, text="1.9", font="Helvetica 14 bold")
            l_money = tk.Label(StatFrame, text=":שילם", font="Helvetica 14 bold")
            l_money_copy = tk.Label(StatFrame, text="300", font="Helvetica 14 bold")
            l_way = tk.Label(StatFrame, text=":סיבה", font="Helvetica 14 bold")
            l_way_copy = tk.Label(StatFrame, text="מים", font="Helvetica 14 bold")

            l_number_resit.grid(row="0", column="1", sticky="e", padx=200, pady=10)
            l_number_resit_copy.grid(row="0", column="0", sticky="w", padx=200, pady=10)
            l_number_house.grid(row="1", column="1", sticky="e", padx=200, pady=10)
            l_number_house_copy.grid(row="1", column="0", sticky="w", padx=200, pady=10)
            l_name.grid(row="2", column="1", sticky="e", padx=200, pady=10)
            l_name_copy.grid(row="2", column="0", sticky="w", padx=200, pady=10)
            l_day.grid(row="3", column="1", sticky="e", padx=200, pady=10)
            l_day_copy.grid(row="3", column="0", sticky="w", padx=200, pady=10)
            l_money.grid(row="4", column="1", sticky="e", padx=200, pady=10)
            l_money_copy.grid(row="4", column="0", sticky="w", padx=200, pady=10)
            l_way.grid(row="5", column="1", sticky="e", padx=200, pady=10)
            l_way_copy.grid(row="5", column="0", sticky="w", padx=200, pady=10)


app = App()
app.mainloop()
