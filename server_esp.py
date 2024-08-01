from flask import Flask, request, jsonify

app = Flask(__name__)
data = {}
print("here")
@app.route('/data', methods=['POST'])
def receive_data():
    global data
    data = request.get_json()
    return jsonify(data), 200

@app.route('/latest', methods=['GET'])
def get_latest_data():
    print("hello")
    return jsonify(data), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)