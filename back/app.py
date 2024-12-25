import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from flask import Flask, jsonify, request
from flask_cors import CORS
from find_n import my_directory

app = Flask(__name__)
CORS(app)
# הגדרת חיבור למסד הנתונים של MySQL

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:yekw88Xfu!@localhost/mydatabase'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

from db.models import DataHome, db

db.init_app(app)

# יצירת הטבלאות במסד הנתונים (ניתן להריץ פעם אחת בלבד כדי ליצור את המבנה)
with app.app_context():
    db.create_all()


def show_user(data):
    data = request.get_json()
    home = data.get('home', '')
    user = my_directory.get(home)
    return user


@app.route('/send', methods=['POST'])
def main_route():
    data = request.get_json()  # מקבל את הנתונים שנשלחו מה-Frontend
    resit = data.get('resit', '')
    money = data.get('money', '')
    home = data.get('home', '')
    day = data.get('day', '')
    user = my_directory.get(home)
    why = data.get('why', '')
    username = data.get('username', '')  # שולף את שם המשתמש
    age = data.get('age', '')  # שולף את הגיל

    # עיבוד הנתונים (לדוגמה: החזרת הודעה מותאמת אישית).


@app.route('/control', methods=['POST'])
def post_info():
    data = request.get_json()
    user = show_user(data)
    if not user:
        user = ''
    new_commit = DataHome(resit=data['resit'], money=data['money'], home=data['home'], day=data['day'],
                          user=user, why=data['why'])
    db.session.add(new_commit)
    db.session.commit()
    return jsonify({'message': 'קבלה חדשה נרשמה'}), 201




@app.route('/control', methods=['GET'])
def get_all():
    infos = DataHome.query.all()
    return jsonify([{
        'resit': info.resit,
        'money': info.money,
        'home': info.home,
        'day': info.day,
        'user': info.user,
        'why': info.why
    }for info in infos])


@app.route('/home/<string:home>', methods=['GET'])
def get_home(home):
    home_data = DataHome.query.filter_by(home=home).all()

    if not home_data:
        return jsonify({'message': 'Home not found'})  # אם לא נמצא, החזר הודעת שגיאה


    # הפיכת הרשומות למבנה JSON
    result = [{
        'resit': record.resit,
        'money': record.money,
        'home': record.home,
        'day': record.day,
        'user': record.user,
        'why': record.why
    } for record in home_data]

    return jsonify(result)  # החזר רשימה של כל הרשומות


@app.route('/resit/<int:resit>', methods=['DELETE'])
def delite_resit(resit):
    # שליפת הרשומה לפי מפתח ראשי
    resit_data = DataHome.query.get(resit)
    if not resit_data:
        # החזרת הודעת שגיאה אם הרשומה לא נמצאה
        return jsonify({'message': 'resit not found'}), 404

    # מחיקת הרשומה מהמסד
    db.session.delete(resit_data)
    db.session.commit()

    # החזרת הודעה על הצלחה
    return jsonify({'message': f"Resit deleted successfully!"})



if __name__ == '__main__':
    app.run(debug=True)
