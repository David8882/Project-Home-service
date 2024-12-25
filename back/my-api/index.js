// טוען את Express
const express = require('express');
const cors = require('cors'); // ייבוא CORS
const jwt = require('jsonwebtoken');


// פורט שבו השרת ירוץ
const app = express();
const PORT = 3000;

app.use(cors()); // הפעלת CORS

let table = [];


// רוט בסיסי - נקודת התחלה
app.get('/', (req, res) => {
    res.send('Welcome to my basic API!');
});

// רוט שמחזיר רשימת משתמשים
app.get('/users', (req, res) => {
    const users = [
        { id: 1, name: 'David' },
        { id: 2, name: 'Sarah' },
        { id: 3, name: 'Michael' }
    ];
    res.json(users);
});



// הפעלת השרת
app.listen(PORT, () => {
    console.log(`Server is running on http://localhost:${PORT}`);
});
