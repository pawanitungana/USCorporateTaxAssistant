from flask import Flask, request, jsonify, render_template
from tax_utils import fetch_tax_data, build_system_prompt, get_tax_response
import os
import json
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

# Load tax data once on startup
df = fetch_tax_data()
system_prompt = build_system_prompt(df)

# Load your OpenAI API key
OPENAI_API_KEY = os.environ.get('OPENAI_API_KEY')

USER_QUERY_FILE = "user_queries.json"
RESPONSE_FILE = "responses.json"

def save_user_query(user_query):
    user_data = {"user_query": user_query}
    if os.path.exists(USER_QUERY_FILE):
        with open(USER_QUERY_FILE, "r") as file:
            data = json.load(file)
    else:
        data = []
    data.append(user_data)
    with open(USER_QUERY_FILE, "w") as file:
        json.dump(data, file, indent=4)

def save_response(response_data):
    response_entry = {"response": response_data}
    if os.path.exists(RESPONSE_FILE):
        with open(RESPONSE_FILE, "r") as file:
            data = json.load(file)
    else:
        data = []
    data.append(response_entry)
    with open(RESPONSE_FILE, "w") as file:
        json.dump(data, file, indent=4)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/api/get_tax_info", methods=["POST"])
def get_tax_info():
    data = request.get_json()
    print("[DEBUG] Request received:", data)

    if not data or 'user_query' not in data:
        return jsonify({"error": "Missing user query"}), 400

    user_query = data['user_query']
    print("[DEBUG] User Query:", user_query)

    try:
        response = get_tax_response(user_query, system_prompt, OPENAI_API_KEY)
        print("[DEBUG] Response from OpenAI:", response)

        # Uncomment if you want to store these:
        # save_user_query(user_query)
        # save_response(response)

        return jsonify({"response": response})
    except Exception as e:
        import traceback
        print("[EXCEPTION]")
        traceback.print_exc()
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True)
