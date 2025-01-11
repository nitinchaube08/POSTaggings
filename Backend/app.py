from flask import Flask, jsonify, request
from flask_cors import CORS
from grammarChecker import *
from pos_tagger import *
import nltk
from hmm_tagger import hmm_train_tagger, Viterbi
from crf_taggger import sent2features, sent2labels, sent2tokens
import joblib


app = Flask(__name__)
CORS(app)
initial_probs, transitional_probs, emission_probs = hmm_train_tagger()


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
    
@app.route("/api/tagging/hmm-pos-tagging", methods=['POST'])
def hmm_pos_tagging():
    try:    
        data = request.get_json()
        sentence = data.get("text", "")
        
        if not sentence:
            return jsonify({"error": "No text provided"}), 400

        # Tokenize the sentence
        tokens = nltk.word_tokenize(sentence)

        # Perform POS tagging using HMM
        tagged_sentence = Viterbi(tokens, transitional_probs, emission_probs, initial_probs)

        grammar_result = check_and_correct_grammar(tagged_sentence)

        return jsonify({
            "tagged_text": tagged_sentence,
            "method": "HMM based",
            "grammar_errors": grammar_result["errors"],
            "corrections": grammar_result["corrections"],
            "corrected_sentence": grammar_result["corrected_sentence"],
            "is_grammatically_correct": len(grammar_result["errors"]) == 0
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Load the trained CRF model
crf = joblib.load("crf_model.pkl")
@app.route("/api/tagging/crf-based-tagging", methods=['POST'])
def crf_pos_tagging():
    try:
        # Get input sentence
        data = request.get_json()
        sentence = data.get("text", "")

        if not sentence:
            return jsonify({"error": "No text provided"}), 400

        # Tokenize the sentence
        tokens = nltk.word_tokenize(sentence)
        input_data = [(token, "") for token in tokens]

        # Extract features and predict POS tags
        features = sent2features(input_data)
        tags = crf.predict_single(features)
        tagged_text = [(word, tag) for word, tag in zip(tokens, tags)]

        # Perform grammar checking
        grammar_result = check_and_correct_grammar(tagged_text)

        # Construct the response
        response = {
            "tagged_text": tagged_text,
            "method": "CRF-based",
            "grammar_errors": grammar_result["errors"],
            "corrections": grammar_result["corrections"],
            "corrected_sentence": grammar_result["corrected_sentence"],
            "is_grammatically_correct": len(grammar_result["errors"]) == 0
        }

        return jsonify(response)
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
if __name__ == "__main__":
    app.run(debug=True)