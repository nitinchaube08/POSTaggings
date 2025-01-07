def check_and_correct_grammar(tagged_text):
    
    errors = []
    corrections = []
    corrected_words = []
    auxiliary_verbs = {"is", "are", "was", "were", "am", "be", "being", "been"}

    # Subject-Verb Agreement
    for i, (word, tag) in enumerate(tagged_text):
        if tag in ["NN", "NNP"] and i + 1 < len(tagged_text):
            next_word, next_tag = tagged_text[i + 1]
            
            # Skip auxiliary verbs
            if next_word.lower() in auxiliary_verbs:
                corrected_words.append(word)
                continue

            # Plural verb after singular noun
            if next_tag == "VBP":
                errors.append(f"Subject-verb agreement error: '{word} {next_word}'")
                corrections.append(f"{word} {next_word}s")  # Suggest correction
                corrected_words.append(f"{word} {next_word}s")
                continue

        # Determiner-Noun Agreement
        if tag == "DT" and i + 1 < len(tagged_text):
            next_word, next_tag = tagged_text[i + 1]
            if next_tag not in ["NN", "NNS"]:
                errors.append(f"Determiner-noun agreement error: '{word} {next_word}'")
                corrected_words.append(f"{word} <noun>")
                continue

        # Punctuation Errors
        if tag == "PUNCT" and i == len(tagged_text) - 1:
            if word not in [".", "?", "!"]:
                errors.append("Sentence does not end with valid punctuation.")
                corrected_words.append(".")
                continue

        # Default: Add the word as is
        corrected_words.append(word)

    # Build corrected sentence
    corrected_sentence = " ".join(corrected_words)

    return {
        "errors": errors,
        "corrections": corrections,
        "corrected_sentence": corrected_sentence
    }
