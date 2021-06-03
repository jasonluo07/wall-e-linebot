from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://Admin:123456@127.0.0.1:5432/testdb'
db = SQLAlchemy(app)


class events(db.Model):
    __tablename__ = 'students'
    sid = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    img = db.Column(db.String(50))
    date = db.Column(db.String(50))
    time = db.Column(db.String(50))
    type = db.Column(db.String(50))
    link = db.Column(db.String(50))
    host = db.Column(db.String(50))
    location = db.Column(db.String(50))
    explanation = db.Column(db.String(50))

    def __init__(self, name, img, date, time, type, link, host, location, explanation):
        self.name = name
        self.img = img
        self.date = date
        self.time = time
        self.type = type
        self.link = link
        self.host = host
        self.location = location
        self.explanation = explanation


@app.route('/')
def index():
    db.create_all()
    return '資料庫連線成功！'


if __name__ == '__main__':
    app.run()
