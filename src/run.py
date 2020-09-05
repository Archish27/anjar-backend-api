from flask import Flask, jsonify, make_response

app = Flask(__name__)


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


if __name__ == '__main__':
    app.run(debug=True)
