from flask import Flask, jsonify

app = Flask(__name__)

@app.route('/')
def home():
    jsonify({'message': 'check backend'})
    return jsonify({'message': 'ברוכים הבאים למיקרוסרוויס של ה-Back!'})

if __name__ == '__main__':
    app.run(debug=True)
