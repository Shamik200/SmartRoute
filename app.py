from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/')
def home():
    return jsonify({"message": "Flask app deployed successfully!"})

@app.route('/predict', methods=['POST'])
def predict():
    data = request.json
    return jsonify({"prediction": "Your model result here", "input": data})

if __name__ == '__main__':
    app.run(debug=True)
