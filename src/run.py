import uuid
from flask import Flask, jsonify, make_response, request
from flask_sqlalchemy import SQLAlchemy

# from flask_marshmallow import Marshmallow

app = Flask(__name__)
db = SQLAlchemy(app)
# ma = Marshmallow(app)

app.config['SQLALCHEMY_DATABASE_URI'] = "mysql://root:root@127.0.0.1:3306/mandir"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    code = db.Column(db.String(10), unique=True, nullable=False)
    info = db.Column(db.JSON, nullable=False)


# class UserSchema(ma.ModelSchema):
#     class Meta:
#         model = User

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
    info = request.form.get("info")
    user = User(code=code, info=info)
    db.session.add(user)
    db.session.commit()
    response = make_response(
        jsonify(
            {"message": "Customer created"}
        ),
        200,
    )
    # response.headers["Content-Type"] = "application/json"
    return response


@app.route("/get-customers", methods=["GET"])
def get_users():
    customers = User.query.all()
    # user_schema = UserSchema(many=True)
    # output = user_schema.dump(customers).data
    # return jsonify({'user': output})
    response = make_response(
        jsonify(
            {"customers": customers}
        ),
        200,
    )
    return response


if __name__ == '__main__':
    app.run(debug=True)
