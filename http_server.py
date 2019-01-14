from flask import Flask, request, jsonify
from flask_cors import CORS

from server import server

app = Flask(__name__)
app.config['JSON_AS_ASCII'] = False
app.config['DEBUG'] = False
CORS(app)


@app.route("/single_tokenizer", methods=['GET'])
def single_tokenizer():
    message = request.args.get('message')

    segment_result = server(message)

    return jsonify(segment_result)


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
