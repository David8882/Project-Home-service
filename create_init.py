import os

# נתיב התיקייה שבה תרצה ליצור את הקובץ
folder_path = 'back'  # עדכן את הנתיב לפי הצורך

# צור את התיקייה אם היא לא קיימת
os.makedirs(folder_path, exist_ok=True)

# יצירת קובץ __init__.py
init_file_path = os.path.join(folder_path, '__init__.py')
with open(init_file_path, 'w') as f:
    pass  # הקובץ יישאר ריק

print(f"Created: {init_file_path}")
