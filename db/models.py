from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class DataHome(db.Model):
    __tablename__ = 'info'

    resit = db.Column(db.Integer, primary_key=True)
    money = db.Column(db.Integer, nullable=False)
    home = db.Column(db.String(50), nullable=False)
    user = db.Column(db.String(50), nullable=False)
    day = db.Column(db.String(50), nullable=False)
    why = db.Column(db.String(50), nullable=False)
