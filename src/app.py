import json
import uuid
from flask_sqlalchemy import SQLAlchemy
from flask import Flask, jsonify, make_response, request

app = Flask(__name__)
db = SQLAlchemy(app)

app.config['SQLALCHEMY_DATABASE_URI'] = "mysql://root:root@127.0.0.1:3306/mandir"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    code = db.Column(db.String(10), unique=True, nullable=False)
    name = db.Column(db.TEXT, nullable=False)
    address = db.Column(db.TEXT, nullable=False)


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


@app.route("/create", methods=["POST"])
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


def insert_user(category: str, name: str, code: str, user_name: str, address: str, email: str, phone_number: str):
    if category:
        category = name
        category_dict = json.loads(category)
        plan = category_dict['name']
        price = category_dict['price']
        members = category_dict['members'] if category_dict['members'] else 0
        user = User(code=code, user_name=user_name, address=address, email=email,
                    phone_number=phone_number, category=category, plan=plan, price=price, members=members)
        print('q------>', db.session.add(user))
        db.session.commit()


@app.route("/get-customers", methods=["GET"])
def get_users():
    customers = User.query.all()
    customer_list = []
    for customer in customers:
        customer_list.append({
            'uuid': customer.code,
            'info': customer.info
        })
    response = make_response(
        jsonify(
            {"customers": customer_list}
        ),
        200,
    )
    return response


if __name__ == '__main__':
    app.run(debug=True)
