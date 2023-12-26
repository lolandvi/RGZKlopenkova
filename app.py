from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_jsonrpc import JSONRPC
from flask import redirect, url_for

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///api_database.db'
db = SQLAlchemy(app)
jsonrpc = JSONRPC(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)

with app.app_context():
    db.create_all()

@jsonrpc.method("user.get_user_by_id", authenticated=False)
def get_user_by_id(user_id: int) -> dict:
    user = User.query.get(user_id)
    if user:
        return {'username': user.username, 'id': user.id}
    else:
        return {'error': 'User not found'}

@app.route("/mainpage")
def mainpage():
    return render_template('mainpage.html')

@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/register')
def register():
    return render_template('register.html')

if __name__ == '__main__':
    app.run(debug=True)