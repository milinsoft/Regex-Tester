from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import sys

DB_NAME = 'db.sqlite3'
app = Flask(__name__)

app.config.update(
    {'SQLALCHEMY_DATABASE_URI': f'sqlite:///{DB_NAME}'}
)

# write your code here
db = SQLAlchemy(app)


class RegexModel(db.Model):
    __tablename__ = 'record'
    id = db.Column(db.Integer, primary_key=True)
    regex = db.Column(db.String(50))
    text = db.Column(db.String(1024), nullable=False)
    result = db.Column(db.Boolean, nullable=False)


db.create_all()


# don't change the following way to run flask:
if __name__ == '__main__':
    if len(sys.argv) > 1:
        arg_host, arg_port = sys.argv[1].split(':')
        app.run(host=arg_host, port=arg_port)
    else:
        app.run()