from flask import Flask, request, jsonify, send_from_directory
import os
import http.client
import json

app = Flask(__name__, static_folder='static')

# 🔹 Serve frontend (index.html)
@app.route('/')
def home():
    return send_from_directory('static', 'index.html')


# 🔹 Example API route (resume analysis)
@app.route('/analyze', methods=['POST'])
def analyze():
    data = request.get_json()
    resume_text = data.get("resume", "")
    job_desc = data.get("job_description", "")

    # 🔐 API key from environment
    api_key = os.environ.get("ANTHROPIC_API_KEY")

    conn = http.client.HTTPSConnection("api.anthropic.com")

    payload = json.dumps({
        "model": "claude-3-sonnet-20240229",
        "max_tokens": 800,
        "messages": [
            {
                "role": "user",
                "content": f"Analyze this resume:\n{resume_text}\n\nJob Description:\n{job_desc}"
            }
        ]
    })

    headers = {
        'Content-Type': 'application/json',
        'x-api-key': api_key,
        'anthropic-version': '2023-06-01'
    }

    conn.request("POST", "/v1/messages", payload, headers)
    res = conn.getresponse()
    response_data = res.read()

    return jsonify(json.loads(response_data))


# 🔹 Run app (Render compatible)
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)