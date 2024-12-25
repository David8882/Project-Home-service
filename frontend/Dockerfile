# בסיס: Node.js
FROM node:18

# תיקיית עבודה
WORKDIR /app

# התקנת התלויות
COPY package*.json ./
RUN npm install

# העתקת כל הקבצים
COPY . .

# פתיחת פורט Angular
EXPOSE 4200

# הפעלת Angular
CMD ["ng", "serve", "--host", "0.0.0.0"]
