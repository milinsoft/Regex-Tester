from flask import Flask, render_template, request, url_for, Response
from flask_sqlalchemy import SQLAlchemy
import sys

import re

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


@app.route('/', methods=['GET', 'POST'])
def main_page():
    if request.method == 'POST':
        # add info to db without redirection
        regex, text = request.form.get('regex'), request.form.get('text')  # using .get method allows to handle keyerror.
        regex_result = bool(re.match(regex, text))
        regex_enty = RegexModel(regex=regex, text=text, result=regex_result)
        db.session.add(regex_enty)
        db.session.commit()
        return str(regex_result)
    else:
        return render_template('index.html')


@app.route('/history/')
def history():
    all_info = RegexModel.query.all()
    return render_template('history.html', data=all_info)


# don't change the following way to run flask:
if __name__ == '__main__':
    if len(sys.argv) > 1:
        arg_host, arg_port = sys.argv[1].split(':')
        app.run(host=arg_host, port=arg_port, debug=True)
    else:
        app.run(debug=True)
