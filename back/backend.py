from flask import Flask

app = Flask(__name__)

@app.route('/')
def home():
    return "ברוכים הבאים למיקרוסרוויס של Flask!"

if __name__ == '__main__':
    app.run(debug=True)
