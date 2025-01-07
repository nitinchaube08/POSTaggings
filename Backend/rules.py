# Lexical rules for direct word-to-POS mapping
LEXICAL_RULES = {
    "the": "DT",
    "a": "DT",
    "an": "DT",
    "and": "CC",
    "but": "CC",
    "he": "PRP",
    "she": "PRP",
    "it": "PRP",
    "they": "PRP",
    "is": "VBZ",
    "are": "VBP",
    "was": "VBD",
    "were": "VBD",
    "run": "VB",
    "runs": "VBZ",
    "running": "VBG",
    "ran": "VBD",
    "walk": "VB",
    "walking": "VBG",
    "walked": "VBD"
}

# Suffix rules for pattern-based tagging
SUFFIX_RULES = {
    "ing": "VBG",  # Gerund or Present Participle
    "ed": "VBD",   # Past Tense
    "ly": "RB",    # Adverb
    "ion": "NN",   # Noun
    "s": "NNS"     # Plural Noun
}

# Punctuation rules
PUNCTUATION_RULES = {
    ".": "PUNCT",
    "?": "PUNCT-Q",
    "!": "PUNCT-E",
    ",": "PUNCT-C",
    ":": "PUNCT-S",
    ";": "PUNCT-S",
    "\"": "PUNCT-QT",
    "'": "PUNCT-QT",
    "(": "PUNCT-P",
    ")": "PUNCT-P"
}
# Common adverbs
COMMON_ADVERBS = {
    "always", "never", "sometimes", "often", "rarely", "soon",
    "here", "there", "now", "yesterday", "tomorrow", "quickly", "slowly"
}