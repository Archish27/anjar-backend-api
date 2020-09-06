import json
import uuid
from flask_sqlalchemy import SQLAlchemy
from flask import Flask, jsonify, make_response, request
from flask import render_template

app = Flask(__name__)
db = SQLAlchemy(app)

app.config['SQLALCHEMY_DATABASE_URI'] = "mysql://root:root@127.0.0.1:3306/mandir"
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
    email = request.form.get('email')
    phone_number = request.form.get('phone_number')
    katha = request.form.get('katha')
    insert_user(katha, 'Katha', code, name, address, email, phone_number)
    mahapuja = request.form.get('mahapuja')
    insert_user(mahapuja, 'Mahapuja', code, name, address, email, phone_number)
    utsavo = request.form.get('utsavo')
    insert_user(utsavo, 'Utsavo', code, name, address, email, phone_number)
    response = make_response(
        jsonify(
            {"message": "Customer created"}
        ),
        200,
    )
    return response


def insert_user(category: str, category_name: str, code: str, user_name: str, address: str, email: str, phone_number: str):
    if category:
        category_dict = json.loads(category)
        print('json---------------', type(category_dict))
        plan = category_dict['name']
        price = category_dict['price']
        members = category_dict['members'] if category_dict['members'] else 0
        user = User(code=code, user_name=user_name, address=address, email_id=email, phone_number=phone_number,
                    category=category_name, plan=plan, price=price, members=members)
        db.session.add(user)
        db.session.commit()


@app.route("/get-customers", methods=["GET"])
def get_users():
    customers = User.query.all()
    return render_template('index.html', items=customers)


# @app.route("/data", methods=["GET"])
# def get_data():
#     return render_template('index.html', items=get_users())


if __name__ == '__main__':
    app.run(debug=True)
