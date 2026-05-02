from flask import Flask, request, jsonify, send_from_directory
import http.client
import json
import os

app = Flask(__name__, static_folder="static")

ANTHROPIC_API_KEY = os.environ.get("ANTHROPIC_API_KEY", "")

def call_claude(prompt):
    payload = json.dumps({
        "model": "claude-sonnet-4-20250514",
        "max_tokens": 1500,
        "messages": [{"role": "user", "content": prompt}]
    })
    headers = {
        "Content-Type": "application/json",
        "x-api-key": ANTHROPIC_API_KEY,
        "anthropic-version": "2023-06-01"
    }
    conn = http.client.HTTPSConnection("api.anthropic.com")
    conn.request("POST", "/v1/messages", payload, headers)
    res = conn.getresponse()
    data = json.loads(res.read().decode("utf-8"))
    conn.close()
    if "error" in data:
        raise Exception(data["error"].get("message", "API error"))
    return "".join(b.get("text","") for b in data.get("content",[]))

@app.route("/")
def index():
    return send_from_directory("static", "index.html")

@app.route("/analyze", methods=["POST"])
def analyze():
    body = request.get_json(force=True)
    resume = (body.get("resume") or "").strip()
    job    = (body.get("job") or "").strip()

    if not resume:
        return jsonify({"error": "Resume text is required"}), 400

    prompt = f"""You are a senior career coach and ATS expert. Analyze the resume below{' against the provided job description' if job else ''}.
Respond ONLY with a valid JSON object — no markdown fences, no extra text.

Resume:
{resume[:3500]}
{"Job Description:" + chr(10) + job[:1500] if job else ""}

Return exactly this JSON structure:
{{
  "overallScore": <integer 0-100>,
  "atsScore": <integer 0-100>,
  "roleTitle": "<detected role, max 5 words>",
  "experienceLevel": "<e.g. Senior · ~7 yrs>",
  "verdict": "<strong | moderate | weak>",
  "verdictLabel": "<e.g. Strong Candidate>",
  "sections": [
    {{"name": "Contact Info",  "score": <0-100>, "note": "<one short tip>"}},
    {{"name": "Work History",  "score": <0-100>, "note": "<one short tip>"}},
    {{"name": "Skills",        "score": <0-100>, "note": "<one short tip>"}},
    {{"name": "Education",     "score": <0-100>, "note": "<one short tip>"}},
    {{"name": "Achievements",  "score": <0-100>, "note": "<one short tip>"}},
    {{"name": "Formatting",    "score": <0-100>, "note": "<one short tip>"}}
  ],
  "skillsFound": ["skill1","skill2","skill3","skill4","skill5","skill6","skill7","skill8"],
  "skillsGap": ["missing1","missing2","missing3","missing4"],
  "keywords": {{"matched": ["kw1","kw2","kw3"], "missing": ["kw4","kw5"]}},
  "summary": "<3 sentences: strengths, weaknesses, overall impression>",
  "topStrength": "<single best thing about this resume>",
  "suggestions": [
    "<specific improvement 1>",
    "<specific improvement 2>",
    "<specific improvement 3>",
    "<specific improvement 4>",
    "<specific improvement 5>"
  ]
}}"""

    try:
        raw = call_claude(prompt)
        raw = raw.strip().lstrip("```json").lstrip("```").rstrip("```").strip()
        result = json.loads(raw)
        return jsonify(result)
    except json.JSONDecodeError as e:
        return jsonify({"error": f"Could not parse AI response: {e}"}), 500
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True, port=5050)
