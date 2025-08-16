from flask import Flask, request, jsonify
from flask_cors import CORS
import google.generativeai as genai
import os
from dotenv import load_dotenv

load_dotenv()
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

app = Flask(__name__)
CORS(app)

def categorize_prompt(prompt: str):
    travel_keywords = ["trip", "travel", "tour", "vacation", "places", "temple", "visit", "itinerary"]
    expense_keywords = ["expense", "spend", "spent", "transaction", "cost", "summary"]
    budget_keywords = ["budget", "plan", "allocation", "saving"]

    text = prompt.lower()
    if any(word in text for word in expense_keywords):
        return "expense"
    elif any(word in text for word in budget_keywords):
        return "budget"
    elif any(word in text for word in travel_keywords):
        return "travel"
    else:
        return "unknown"

def get_ai_response(category, prompt):
    if category == "unknown":
        return "I cannot answer this question. Please ask about travel, expenses, or budget planning."

    model = genai.GenerativeModel("gemini-1.5-flash")
    response = model.generate_content(f"You are an AI assistant for {category}. User prompt: {prompt}")
    return response.text.strip() if response and response.text else "No response generated."

@app.route("/agent", methods=["POST"])
def agent():
    data = request.json
    prompt = data.get("prompt", "")

    category = categorize_prompt(prompt)
    reply = get_ai_response(category, prompt)

    return jsonify({"category": category, "response": reply})

if __name__ == "__main__":
    app.run(debug=True)