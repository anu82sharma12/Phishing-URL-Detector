from flask import Flask, request, jsonify
from detector import predict

app = Flask(__name__)

@app.route("/detect", methods=["POST"])
def detect():
    url = request.json["url"]
    label, prob = predict(url)
    return jsonify({"url": url, "label": label, "confidence": prob})

if __name__ == "__main__":
    app.run(port=5000)
