import json
import uuid
from flask_sqlalchemy import SQLAlchemy
from flask import Flask, jsonify, make_response, request
from flask import render_template
from flask_httpauth import HTTPBasicAuth
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
auth = HTTPBasicAuth()
db = SQLAlchemy(app)

users = {
    "admin": generate_password_hash("anjaradmin"),
    "test": generate_password_hash("testadmin")
}

app.config['SQLALCHEMY_DATABASE_URI'] = "mysql://root:@127.0.0.1:3306/mandir"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    code = db.Column(db.String(10), unique=True, nullable=False)
    name = db.Column(db.TEXT, nullable=False)
    address = db.Column(db.TEXT, nullable=False)
    phone_number = db.Column(db.String(64), nullable=False)
    email_id = db.Column(db.String(100), nullable=False)
    category = db.Column(db.String(45), nullable=False)
    plan = db.Column(db.String(45), nullable=False)
    price = db.Column(db.Numeric(10, 0), nullable=False)
    members = db.Column(db.Integer, nullable=False)


@app.route('/sample', methods=["GET", "POST"])
def hello():
    response = make_response(
        jsonify(
            {"message": "hello"}
        ),
        200,
    )
    response.headers["Content-Type"] = "application/json"
    return response


@app.route("/create-customer", methods=["POST"])
def add_user():
    code = str(uuid.uuid4())[:8]
    name = request.form.get('name')
    address = request.form.get('address')
    email = request.form.get('email_id')
    phone_number = request.form.get('phone_number')
    katha = request.form.get('katha').replace('\\','')
    insert_user(katha, 'Katha', code, name, address, email, phone_number)
    mahapuja = request.form.get('mahapuja').replace('\\','')
    insert_user(mahapuja, 'Mahapuja', code, name, address, email, phone_number)
    utsavo = request.form.get('utsavo').replace('\\','')
    insert_user(utsavo, 'Utsavo', code, name, address, email, phone_number)
    response = make_response(
        jsonify(
            {"message": "Customer created"}
        ),
        200,
    )
    return response


def insert_user(category: str, category_name: str, code: str, user_name: str, address: str, email: str,
                phone_number: str):
    if category:
        category_dict = json.loads(category)
        plan = category_dict['name']
        price = category_dict['price']
        if 'members' in category_dict:
            members = category_dict['members']
        else:
            members = 0    
        user = User(code=code, name=user_name, address=address, email_id=email, phone_number=phone_number,
                    category=category_name, plan=plan, price=price, members=members)
        db.session.add(user)
        db.session.commit()


@auth.verify_password
def verify_password(username, password):
    if username in users and \
            check_password_hash(users.get(username), password):
        return username


@app.route("/", methods=["GET"])
@auth.login_required
def get_users():
    customers = User.query.all()
    return render_template('index.html', items=customers)


if __name__ == '__main__':
    app.run(debug=True)
