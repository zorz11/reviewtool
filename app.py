
from flask import Flask, request, jsonify
import openai
import os

app = Flask(__name__)

openai.api_key = os.getenv("OPENAI_API_KEY")

SYSTEM_PROMPT = """
You are an English teacher assistant.
Given a transcript of a lesson between a student and a teacher, generate a structured lesson review including:
1. A summary of the lesson
2. Vocabulary list (word, definition, example)
3. Grammar mistakes with corrections
4. Sentence improvements (optional or awkward sentences improved)
5. Two suggested practice activities
"""

@app.route('/generate-review', methods=['POST'])
def generate_review():
    data = request.get_json()
    transcript = data.get("transcript", "")

    if not transcript:
        return jsonify({"error": "No transcript provided."}), 400

    try:
        response = openai.ChatCompletion.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": transcript}
            ],
            temperature=0.4
        )

        content = response["choices"][0]["message"]["content"]
        return jsonify({"review": content})

    except Exception as e:
        return jsonify({"error": str(e)}), 500

import os
port = int(os.environ.get("PORT", 5000))
app.run(host="0.0.0.0", port=port)


