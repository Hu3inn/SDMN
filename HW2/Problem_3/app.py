from flask import Flask, request, jsonify

app = Flask(__name__)
status = {"status": "OK"}

@app.route("/api/v1/status", methods=["GET", "POST"])
def handle_status():
    global status
    if request.method == "GET":
        return jsonify(status), 200
    elif request.method == "POST":
        new_status = request.get_json()
        if "status" in new_status:
            status["status"] = new_status["status"]
            return jsonify(status), 201
        else:
            return jsonify({"error": "Missing 'status' key"}), 400

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)