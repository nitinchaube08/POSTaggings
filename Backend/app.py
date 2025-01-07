from flask import Flask, jsonify, request
from flask_cors import CORS
from grammarChecker import *
from pos_tagger import *
import nltk

app = Flask(__name__)
CORS(app)

@app.route("/",methods=["GET"])
def home():
    return jsonify({"message" :"Backend is running!"})

@app.route("/api/tagging/rule-based", methods=['POST'])
def rule_based_tagging():
    try:
        data = request.get_json()
        text = data.get("text",'')
        #tokenize
        tokens = text.split()
        tagged_text = rule_based_pos_tag(tokens)
        # Perform grammar checking and correction
        grammar_result = check_and_correct_grammar(tagged_text)

        # Format response
        response = {
            "tagged_text": tagged_text,
            "method": "rule-based",
            "grammar_errors": grammar_result["errors"],
            "corrections": grammar_result["corrections"],
            "corrected_sentence": grammar_result["corrected_sentence"],
            "is_grammatically_correct": len(grammar_result["errors"]) == 0
        }
        return jsonify(response), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True)