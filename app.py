from flask import Flask, request, jsonify

app = Flask(__name__)

# Hardcoded user details
FULL_NAME = "Rajeev Joshi"
DOB = "22/07/2005"  # ddmmyyyy format
EMAIL = "rajeev22joshi@gmail.com"
ROLL_NUMBER = "22BCS11920"

# Generate user_id dynamically
USER_ID = f"{FULL_NAME.lower().replace(' ', '_')}_{DOB}"

@app.route("/bfhl", methods=["GET"])
def get_operation_code():
    return jsonify({"operation_code": 1}), 200

@app.route("/bfhl", methods=["POST"])
def process_data():
    try:
        # Ensure request has JSON and "data" key
        request_data = request.get_json()
        if not request_data or "data" not in request_data:
            return jsonify({"is_success": False, "error": "Missing 'data' field in request"}), 400
        
        data = request_data["data"]

        if not isinstance(data, list):
            return jsonify({"is_success": False, "error": "Invalid input format, 'data' must be a list"}), 400

        # Extract numbers and alphabets while preserving order
        numbers = [item for item in data if isinstance(item, str) and item.isdigit()]
        alphabets = [item for item in data if isinstance(item, str) and item.isalpha()]

        # Find highest alphabet (case insensitive)
        highest_alphabet = [max(alphabets, key=str.lower)] if alphabets else []

        response = {
            "is_success": True,
            "user_id": USER_ID,
            "email": EMAIL,
            "roll_number": ROLL_NUMBER,
            "numbers": numbers,
            "alphabets": alphabets,
            "highest_alphabet": highest_alphabet
        }

        return jsonify(response), 200

    except Exception as e:
        return jsonify({"is_success": False, "error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True, port=5000)