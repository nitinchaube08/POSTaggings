from rules import LEXICAL_RULES, SUFFIX_RULES, COMMON_ADVERBS, PUNCTUATION_RULES

def rule_based_pos_tag(tokens):
    tags = []

    for i, word in enumerate(tokens):
        lower_word = word.lower()

        # Rule 1: Punctuation
        if word in PUNCTUATION_RULES:
            tags.append((word, PUNCTUATION_RULES[word]))
            continue

        # Rule 2: Lexical lookup
        if lower_word in LEXICAL_RULES:
            tags.append((word, LEXICAL_RULES[lower_word]))
            continue

        # Rule 3: Common adverbs
        if lower_word in COMMON_ADVERBS:
            tags.append((word, "RB"))
            continue

        # Rule 4: Suffix-based tagging
        matched_suffix = False
        for suffix, tag in SUFFIX_RULES.items():
            if lower_word.endswith(suffix):
                tags.append((word, tag))
                matched_suffix = True
                break
        if matched_suffix:
            continue

        # Rule 5: Proper Nouns (Capitalized, Not First Word)
        if word[0].isupper() and i > 0:
            tags.append((word, "NNP"))
            continue

        # Rule 6: Fallback Rule: Default to noun
        tags.append((word, "NN"))

        # Rule 7: Context-aware adjustments
        if i > 0:
            prev_word, prev_tag = tags[i - 1]
            # Adverbs modifying adjectives or other adverbs
            if prev_tag in ["JJ", "RB"]:
                tags[-1] = (word, "RB")  

    return tags
