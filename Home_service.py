import sqlite3
import tkinter as tk
from tkinter import ttk, filedialog
from tkcalendar import DateEntry, Calendar
from datetime import datetime
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfbase import pdfmetrics


# Register Hebrew font
# pdfmetrics.registerFont(TTFont('Hebrew', 'C:/Users/jacki/PycharmProjects/python122/fonts/NotoSansHebrew_Condensed-ExtraBold.ttf'))
pdfmetrics.registerFont(TTFont('Hebrew', 'NotoSansHebrew_Condensed-ExtraBold.ttf'))

# יצירת חלון
window = tk.Tk()
window.title('ועד בית')
window.geometry('1540x850')

# יצירת מסגרות (Frames)
frame_add_from = tk.Frame(window, width=150, height=150, bg='green')
frame_list = tk.Frame(window, width=150, height=150, bg='blue')
frame_resit = tk.Frame(window, width=150, height=150, bg='yellow')
frame_explor = tk.Frame(window, width=150, height=150, bg='red')

# מיקום מסגרות
frame_add_from.place(relx=0, rely=0, relwidth=0.5, relheight=0.5)
frame_list.place(relx=0.5, rely=0, relwidth=0.5, relheight=0.5)
frame_explor.place(relx=0, rely=0.5, relwidth=0.5, relheight=0.5)
frame_resit.place(relx=0.5, rely=0.5, relwidth=0.5, relheight=0.5)


# Initialize the first receipt number
def last_resit_to_now():
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute("SELECT resit FROM home")  # יש להחליף את table_name בשם הטבלה שלך
    rows = cursor.fetchall()
    row = max(rows)[0] + 1
    return row



def delete_row():
    # בדיקת אם יש שורה שנבחרה
    selected_item = table.selection()
    if not selected_item:

        return

    # קבלת ה-resit של השורה שנבחרה
    item = table.item(selected_item)
    resit = item['values'][0]  # נקודת ההנחה שה-resit הוא הערך הראשון בשורה

    # מחיקת השורה ממסד הנתונים
    with sqlite3.connect('C:/Users/jacki/PycharmProjects/python122/database.db') as db:
        cursor = db.cursor()
        cursor.execute("DELETE FROM home WHERE resit=?", (resit,))
        db.commit()
    rows = cursor.fetchall()

    # מחיקת השורה מה-Treeview
    table.delete(selected_item)


items_months = ['', 'ינואר', 'פברואר', 'מרץ', 'אפריל', 'מאי', 'יוני', 'יולי', 'אוגוסט', 'ספטמבר', 'אוקטובר', 'נובמבר', 'דצמבר']
items = ['E1', 'E2', 'E3', 'E4', 'E5', 'E6', 'E7', 'E8', 'E9', 'E10', 'E11', 'G', 'F', 'F +G', '']
items2 = ['עמית סבג', "יוסף ג'אנו", 'אאידה בראודסקי', 'מתן ומור קדוש', 'נאמן משה', 'אילנה צבאג', 'מיטל נומה',
          'עדי אברדם', 'טליה ויעקב עובדיה', 'פטריסיה',  'נעמי ויואל סבג', '', '', '', '']

# יצירת מילון שמקשר בין e1, e2 וכו' לשמות
items_dict = dict(zip(items, items2))


def form_submit():
    selected_item = l_num_house.get()  # מקבל את ה-e1, e2 שנבחר

    # מייבא את השם לפי הערך שנבחר ב-Combobox
    name_ = items_dict.get(selected_item)
    num_house = selected_item  # הקוד של הדירה הוא אותו קוד כמו ה-e1, e2

    resit = f_resit.get()
    if not resit:
        resit = last_resit_to_now()

    dayp = l_dayp.get()
    dayp = datetime.strptime(dayp, '%m/%d/%y').strftime('%d/%m/%Y')
    money_ = f_money_.get()
    why_ = f' {f_why_.get()}  {f_months.get()}'
    print(type(resit), type(num_house), type(name_), type(dayp), type(money_), type(why_))

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
    l_dayp.set_date(datetime.now())  # Reset date to today
    f_money_.delete(0, tk.END)  # Reset money field
    f_why_.delete(0, tk.END)  # Reset reason field


def split_and_translate_digits_under_ten_only_with_zero_under(money_text):
    try:
        whole_part_under_ten = money_text.split(",")[1]
        whole_number_under_ten = int(whole_part_under_ten)
        if 0 < whole_number_under_ten <= 9:
            under_ten_only = {1: 'אחד', 2: 'שתיים', 3: 'שלוש', 4: 'ארבע', 5: 'חמש', 6: 'שש', 7: 'שבע', 8: 'שמונה',
                              9: 'תשע'}
            # אם המספר הוא 0
            if whole_part_under_ten == 0:
                return "אפס"

            translated_words_under_ten = []

            # אם המספר בין 1 ל-9 ואין עשרות
            if 0 < whole_number_under_ten <= 9:
                translated_words_under_ten.append(f" אגורות" + under_ten_only[whole_number_under_ten])
                return " ".join(translated_words_under_ten)
    except ValueError:
        return "שגיאה: הקלט אינו מספר תקין"


def split_and_translate_digits_under_ten_only_with_zero(money_text):
    try:
        whole_part_under_ten = money_text.split(",")[0]
        whole_number_under_ten = int(whole_part_under_ten)
        if 0 < whole_number_under_ten <= 9:
            under_ten_only = {1: 'אחד', 2: 'שתיים', 3: 'שלוש', 4: 'ארבע', 5: 'חמש', 6: 'שש', 7: 'שבע', 8: 'שמונה',
                              9: 'תשע'}
            # אם המספר הוא 0
            if whole_part_under_ten == 0:
                return "אפס"

            translated_words_under_ten = []

            # אם המספר בין 1 ל-9 ואין עשרות
            if 0 < whole_number_under_ten <= 9:
                translated_words_under_ten.append(under_ten_only[whole_number_under_ten])
                return " ".join(translated_words_under_ten)  # החזרת המחרוזת שנוצרת מהרשימה

    except ValueError:
        return "שגיאה: הקלט אינו מספר תקין"


def split_and_translate_digits_under_ten_(money_text):
    try:
        whole_part = money_text.split(",")[0]  # הנחה שיש פסיק
        decimal_part = money_text.split(",")[1]  # חלק העשרוני (אגורות)
        whole_number = int(whole_part)
        decimal_number = int(decimal_part)
    except ValueError:
        return "שגיאה: הקלט אינו מספר תקין"
    tens_under = {1: 'עשר', 2: 'עשרים', 3: 'שלושים', 4: 'ארבעים', 5: 'חמישים', 6: 'שישים', 7: 'שבעים',
                  8: 'שמונים', 9: 'תשעים'}
    ten = {1: 'אחד', 2: 'שתיים', 3: 'שלוש', 4: 'ארבע', 5: 'חמש', 6: 'שש', 7: 'שבע', 8: 'שמונה', 9: 'תשע'}
    tens = {10: 'עשר', 20: 'עשרים', 30: 'שלושים', 40: 'ארבעים', 50: 'חמישים', 60: 'שישים', 70: 'שבעים',
            80: 'שמונים', 90: 'תשעים'}

    translated_words = []

    # אם המספר הוא 0
    if whole_number == 0 and decimal_number == 0:
        return "אפס שקלים אפס אגורות"

    if whole_number > 0:
        if whole_number in ten:
            translated_words.append(ten[whole_number])
        elif whole_number >= 10 and whole_number in tens:
            translated_words.append(tens[whole_number])

    if whole_number == 0 and decimal_number > 0:
        if decimal_number in tens_under:
            translated_words.append(tens_under[decimal_number])

    if decimal_number > 0:
        if decimal_number in tens_under:
            translated_words.append(f"ו" + tens_under[decimal_number] + " אגורות")
        elif decimal_number >= 10 and decimal_number in tens:
            translated_words.append(f'ו' + tens[decimal_number] + " אגורות")
        elif decimal_number > 9:
            tens_place = (decimal_number // 10) * 10
            ones_place = decimal_number % 10
            if tens_place in tens:
                translated_words.append(f'ו' + tens[tens_place])
            if ones_place in ten:
                translated_words.append(f'ו' + ten[ones_place] + " אגורות")

    return " ".join(translated_words)


def split_and_translate_digits(money_text):
    try:
        whole_part = money_text.split(",")[0]  # הנחה שיש פסיק
        decimal_part = money_text.split(",")[1]  # חלק העשרוני (אגורות)
        whole_number = int(whole_part)
        decimal_number = int(decimal_part)
        if whole_number < 10:
            result = split_and_translate_digits_under_ten_(money_text)  # קריאה לפונקציה עם הפרמטר הנכון
            return result
        if decimal_number < 10 and whole_number == 0:
            result2 = split_and_translate_digits_under_ten_only_with_zero_under(money_text)
            return result2
    except (ValueError, IndexError):
        return "שגיאה: הקלט אינו מספר תקין"

        # מילונים לתרגום ספרות למילים
    under_ten_only = {1: 'ואחד', 2: 'ושתיים', 3: 'ושלוש', 4: 'וארבע', 5: 'וחמש', 6: 'ושש', 7: 'ושבע', 8: 'ושמונה',
                      9: 'ותשע'}
    tens = {10: 'עשר', 20: 'עשרים', 30: 'שלושים', 40: 'ארבעים', 50: 'חמישים', 60: 'שישים', 70: 'שבעים',
                80: 'שמונים', 90: 'תשעים'}
    hundreds = {100: 'מאה', 200: 'מאתיים', 300: 'שלוש מאות', 400: 'ארבע מאות', 500: 'חמש מאות', 600: 'שש מאות',
                700: 'שבע מאות', 800: 'שמונה מאות', 900: 'תשע מאות'}
    thousands = {1000: 'אלף', 2000: 'אלפיים', 3000: 'שלושת אלפים', 4000: 'ארבעת אלפים', 5000: 'חמשת אלפים',
                 6000: 'ששת אלפים', 7000: 'שבעת אלפים', 8000: 'שמונת אלפים', 9000: 'תשעת אלפים'}

    # אם המספר הוא 0
    if whole_number == 0:
        return "אפס"

    translated_words = []

    # אם המספר באלפים
    if whole_number >= 1000:
        thousands_place = (whole_number // 1000) * 1000
        if thousands_place in thousands:
            translated_words.append(thousands[thousands_place])
            whole_number %= 1000

        # אם המספר במאות
    if whole_number >= 100:
        hundreds_place = (whole_number // 100) * 100
        if hundreds_place in hundreds:
            translated_words.append(hundreds[hundreds_place])
            whole_number %= 100

        # אם המספר בעשרות
    if whole_number >= 10:
        tens_place = (whole_number // 10) * 10
        if tens_place in tens:
            translated_words.append(tens[tens_place])
            whole_number %= 10

        # אם המספר בין 1 ל-9
    if whole_number in under_ten_only:
        translated_words.append(under_ten_only[whole_number])

        # תרגום העשרונים (אגורות)
    if decimal_number >= 10:
        tens_place = (decimal_number // 10) * 10
        if tens_place in tens:
            translated_words.append(f"ו" + tens[tens_place])
            decimal_number %= 10

        # תרגום אגורות בודדות
    if decimal_number in under_ten_only:
        translated_words.append(under_ten_only[decimal_number] + " אגורות")

    return " ".join(translated_words)


f_resit = tk.Entry(frame_add_from, justify=tk.RIGHT)
l_resit = tk.Label(frame_add_from, text=":מספר קבלה", font="Helvetica 14 bold")

# ביטול האפשרות לכתוב באופן חופשי ב-Combobox של דירות
f_num_house = tk.Label(frame_add_from, text=":דירה", font="Helvetica 14 bold")
l_num_house = ttk.Combobox(frame_add_from, values=items, state="readonly")

f_dayp = tk.Label(frame_add_from, text=":יום", font="Helvetica 14 bold")
l_dayp = DateEntry(frame_add_from, foreground='black', normalforeground='black',
                   selectforeground='red', background='white',
                   data_pattern='dd-mm-YYYY')

f_money_ = tk.Entry(frame_add_from, justify=tk.RIGHT)
l_money_ = tk.Label(frame_add_from, text=":כמה שילם", font="Helvetica 14 bold")

f_why_ = tk.Entry(frame_add_from, justify=tk.RIGHT)
l_why_ = tk.Label(frame_add_from, text=":עבור", font="Helvetica 14 bold")

f_months = ttk.Combobox(frame_add_from, values=items_months, state="readonly")
# l_months = tk.Label(frame_add_from, text=":חודש", font="Helvetica 14 bold")
# כפתור הגשה
btn_submit = ttk.Button(frame_add_from, text="הגשה", command=form_submit)
btn_delete = ttk.Button(frame_add_from, text="מחיקה", command=delete_row)

# מיקום של הרכיבים בחלון
f_resit.grid(row=0, column=0, sticky='w', padx=150, pady=10)
l_resit.grid(row=0, column=1, sticky='w', padx=10, pady=10)
f_num_house.grid(row=1, column=1, sticky='w', padx=10, pady=10)
l_num_house.grid(row=1, column=0, sticky='w', padx=150, pady=10)
f_dayp.grid(row=2, column=1, sticky='w', padx=10, pady=10)
l_dayp.grid(row=2, column=0, sticky='w', padx=150, pady=10)
f_money_.grid(row=3, column=0, sticky='w', padx=150, pady=10)
l_money_.grid(row=3, column=1, sticky='w', padx=10, pady=10)
f_why_.grid(row=4, column=0, sticky='w', padx=150, pady=10)
l_why_.grid(row=4, column=1, sticky='w', padx=10, pady=10)
f_months.grid(row=5, column=0, sticky='w', padx=150, pady=10)

btn_submit.grid(row=6, column=0, columnspan=1, sticky='n', padx=160, pady=10)
btn_delete.grid(row=6, column=1, columnspan=2, sticky='n', padx=10, pady=10)


def display_selected_row():
    selected_items = table.selection()  # מקבל את ה-ID של כל השורות שנבחרו
    selected_data = []

    # עובר על כל ה-IDs ומקבל את הנתונים של כל שורה שנבחרה
    for item in selected_items:
        row_data = table.item(item, 'values')  # מחזיר את הערכים של השורה
        selected_data.append(row_data)

    # הכנסת כל השורות שנבחרו לטבלה החדשה
    for data in selected_data:
        table2.insert('', 'end', values=data)


# יצירת טבלת Treeview
table = ttk.Treeview(frame_list)

# הגדרת עמודות
table = ttk.Treeview(frame_list, show='headings')
table['columns'] = ('Number', 'Name', 'House', 'Day', 'Money', 'Type')

# יצירת כותרות לעמודות
table.heading('Number', text='קבלה')
table.heading('Name', text='שם')
table.heading('House', text='דירה')
table.heading('Day', text='תאריך')
table.heading('Money', text='שילם')
table.heading('Type', text='עבור')

# יצירת עמודות עבור נתונים
table.column('Number', anchor=tk.CENTER, width=50)
table.column('Name', anchor=tk.CENTER, width=50)
table.column('House', anchor=tk.CENTER, width=50)
table.column('Day', anchor=tk.CENTER, width=50)
table.column('Money', anchor=tk.CENTER, width=50)
table.column('Type', anchor=tk.CENTER, width=50)


# הצגת הטבלה
table.pack(expand=tk.YES, fill=tk.BOTH)
scroll_pane = ttk.Scrollbar(frame_list,command=table.yview)
table.configure(yscrollcommand=scroll_pane.set)
scroll_pane.pack(side=tk.RIGHT, fill=tk.Y)
table.pack(expand=tk.YES, fill=tk.BOTH)


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

        # הוספת נתונים לטבלה
    for row in rows:

        new_row = (row[0], row[1], row[2], row[3], row[4], row[5])
        table.insert('', 'end', values=new_row)

        # Bind the selection event to the table
        table.bind('<<TreeviewSelect>>', lambda event: display_selected_row())


def show_all_data():
    # איפוס הטבלה לפני הצגת כל הנתונים
    for row in table.get_children():
        table.delete(row)

    # חיבור למסד הנתונים ושליפת כל השורות מהטבלה
    with sqlite3.connect('C:/Users/jacki/PycharmProjects/python122/database.db') as db:
        cursor = db.cursor()
        # שליפת כל השורות מהטבלה home
        cursor.execute("SELECT resit, name, house_number, dayp, money_, why FROM home")
        rows = cursor.fetchall()

    # עדכון הטבלה עם הנתונים שהתקבלו
    for row in rows:
        new_row = (row[0], row[1], row[2], row[3], row[4], row[5])
        table.insert('', 'end', values=new_row)

    update_table()


# red
def find_resit():
    # מקבל את הערך שנבחר בקומבו-בוקס לחיפוש (שם או מספר קבלה)
    search_resit = k_resit.get()

    # חיפוש במסד הנתונים לפי שם הדייר או מספר קבלה
    with sqlite3.connect('C:/Users/jacki/PycharmProjects/python122/database.db') as db:
        cursor = db.cursor()
        # חיפוש לפי שם או מספר קבלה
        cursor.execute("SELECT resit, name, house_number, dayp, money_, why FROM home WHERE name=? OR resit=?",
                       (search_resit, search_resit))
        rows = cursor.fetchall()

    # עדכון טבלת ה-Treeview עם תוצאות החיפוש (כל הנתונים הרלוונטיים)
    for row in rows:
        # כל שורה מכילה: resit, name, house_number, dayp, money_, why
        table.insert('', 'end', values=row)



def delete_selected_row():
    # קבלת ה-IDs של השורות שנבחרו בטבלה
    selected_items = table2.selection()

    # לולאה שמוחקת את כל השורות שנבחרו
    for selected_item in selected_items:
        table2.delete(selected_item)

def delete_all_rows():
    for row in table2.get_children():
        table2.delete(row)


# הגדרת frame חדש עבור הטבלה
frame_new_resit = tk.Frame(window, width=150, height=150, bg='yellow')
frame_new_resit.place(relx=0.5, rely=0.5, relwidth=0.5, relheight=0.5)

# יצירת טבלת Treeview בתוך frame_new_resit
table2 = ttk.Treeview(frame_new_resit, show='headings')

# הגדרת עמודות
table2['columns'] = ('Number', 'Name', 'House', 'Day', 'Money', 'Type')

# יצירת כותרות לעמודות
table2.heading('Number', text='קבלה')
table2.heading('Name', text='שם')
table2.heading('House', text='דירה')
table2.heading('Day', text='תאריך')
table2.heading('Money', text='שילם')
table2.heading('Type', text='עבור')

# יצירת עמודות עבור נתונים
table2.column('Number', anchor=tk.CENTER, width=50)
table2.column('Name', anchor=tk.CENTER, width=50)
table2.column('House', anchor=tk.CENTER, width=50)
table2.column('Day', anchor=tk.CENTER, width=50)
table2.column('Money', anchor=tk.CENTER, width=50)
table2.column('Type', anchor=tk.CENTER, width=50)

# הצגת הטבלה בתוך frame_new_resit
table2.pack(expand=tk.YES, fill=tk.BOTH)

# יצירת Scrollbar עבור ה-Treeview
scroll_pane = ttk.Scrollbar(frame_new_resit, command=table2.yview)
table2.configure(yscrollcommand=scroll_pane.set)
scroll_pane.pack(side=tk.RIGHT, fill=tk.Y)


def get_table_data():
    receipts_data = []

    # Define unique positions for each receipt (x, y) based on their index
    positions = [
        (160, 820),  # Position for receipt 0
        (460, 820),  # Position for receipt 1
        (160, 610),  # Position for receipt 2
        (460, 610),  # Position for receipt 3
        (160, 395),  # Position for receipt 4
        (460, 395),  # Position for receipt 4
        (160, 185),  # Position for receipt 4
        (460, 185),  # Position for receipt 4

    ]

    for index, row in enumerate(table2.get_children()):  # Iterate through the rows in the Treeview
        values = table2.item(row)['values']  # Get values of the current row

        # Get x, y position based on the index, defaulting to the last position if more receipts than positions
        x, y = positions[index] if index < len(positions) else (160, 820)  # Default position if out of bounds

        # Map the values to the fields in the receipts list
        receipt_dict = {
            'resit': values[0],  # Assuming the first column is 'resit' (Number)
            'house': values[2],  # Assuming the third column is 'house' (House)
            'name': values[1],  # Assuming the second column is 'name' (Name)
            'day': values[3],  # Assuming the fourth column is 'day' (Day)
            'money': values[4],  # Assuming the fifth column is 'money' (Money)
            'money_Hebrew': split_and_translate_digits(values[4]),  # הנחה שהעמודה החמישית היא 'money'
            'reason': values[5],  # Assuming the sixth column is 'reason' (Type)
            # Set specific 'x' and 'y' values from positions list
            'x': x,
            'y': y
        }
        receipts_data.append(receipt_dict)

    return receipts_data


def reverse_text(text):
    return text[::-1]


def save_receipts_to_pdf(receipts, output_pdf):
    c = canvas.Canvas(output_pdf, pagesize=A4)
    width, height = A4

    # Add background
    background_image_path = "C:/Users/jacki/PycharmProjects/python122/קבלה לדוגמא מספריים-1.png"  # Ensure the extension is correct
    c.drawImage(background_image_path, 0, 0, width=width, height=height)  # Adjust the image to fit the page

    for receipt in receipts:
        # Set position of the receipt
        x = receipt.get('x', 0)  # Default to 0 if not specified
        y = receipt.get('y', height - 100)  # Default to the height of the page if not specified

        # Set Hebrew font (change font size here if needed)
        c.setFont('Hebrew', 16)

        # Draw receipt details
        c.drawRightString(x + 30, y, f"{receipt['resit']}")  # Reverse text
        c.drawRightString(x + 90, y - 20, reverse_text(f"{receipt['name']}"))
        c.drawRightString(x + 90, y - 38, f"{receipt['house']}")
        c.drawRightString(x + 100, y - 56, reverse_text(f"{receipt['reason']}"))
        c.drawRightString(x + 115, y - 79, f"{receipt['money']}")
        # Assuming 'translated_money' should be defined or adjusted accordingly
        c.drawRightString(x + 20, y - 80, reverse_text(f"{receipt['money_Hebrew']}"))  # השתמש ב-money_Hebrew כאן

        # c.drawRightString(x + 20, y - 80, reverse_text(f"{receipt.get('translated_money', '')}"))
        c.drawRightString(x - 60, y - 105, reverse_text(f"העברה בנקאית"))
        c.drawRightString(x + 103, y - 138, f"{receipt['day']}")

    c.save()


def on_submit():
    new_receipts = get_table_data()  # Get data from the Treeview
    output_pdf = filedialog.asksaveasfilename(defaultextension=".pdf", filetypes=[("PDF files", "*.pdf")])  # Get save path for the PDF
    if output_pdf:  # Check if a path was selected
        save_receipts_to_pdf(new_receipts, output_pdf)  # Save the PDF with the extracted data


# Red
m_what = ttk.Label(frame_explor, text="חיפוש", font="Helvetica 28 bold")
k_resit = ttk.Combobox(frame_explor, values=items2)
btn_submit = ttk.Button(frame_explor,text="חיפוש", command=find_resit)
btn_understand = ttk.Button(frame_explor,text='שחזר', command=show_all_data)
btn_make_resit = ttk.Button(frame_explor,text='מחיקת שורה לחשבונית', command=delete_selected_row)
English = ttk.Button(frame_explor,text='לשלוח', command=on_submit)
btn_delete_all_rows = ttk.Button(frame_explor,text='מחיקה כל השורות', command=delete_all_rows)

# show_table
# מיקום
m_what.grid(row=0, column=1, sticky='w', padx=0, pady=10)
k_resit.grid(row=0, column=0, sticky='w', padx=150, pady=10)
btn_submit.grid(row=1, column=0, columnspan=1, sticky='n', padx=160, pady=10)
btn_understand.grid(row=2, column=0, columnspan=1, sticky='n', padx=160, pady=10)
btn_make_resit.grid(row=3, column=1, columnspan=1, sticky='n', padx=160, pady=10)
English.grid(row=4, column=1, columnspan=1, sticky='n', padx=160, pady=10)
btn_delete_all_rows.grid(row=5, column=1, columnspan=1, sticky='n', padx=160, pady=10)

# פונקציה שמופעלת כשלוחצים על כפתור


window.mainloop()

