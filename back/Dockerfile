# בסיס: Python
FROM python:3.10-slim

# תיקיית עבודה
WORKDIR /app

# התקנת התלויות
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# העתקת כל הקבצים
COPY . .

# פתיחת פורט Flask
EXPOSE 5000

# הפעלת Flask
CMD ["python", "app.py"]
