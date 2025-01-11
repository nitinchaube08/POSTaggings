def word2features(sent, i):
    word = sent[i][0]
    features = {
        "bias": 1.0,
        "word.lower()": word.lower(),
        "word[-3:]": word[-3:],  # Last 3 characters
        "word[-2:]": word[-2:],  # Last 2 characters
        "word.isupper()": word.isupper(),
        "word.istitle()": word.istitle(),
        "word.isdigit()": word.isdigit(),
    }
    if i > 0:
        features.update({
            "-1:word.lower()": sent[i - 1][0].lower(),
            "-1:word.istitle()": sent[i - 1][0].istitle(),
            "-1:word.isupper()": sent[i - 1][0].isupper(),
        })
    else:
        features["BOS"] = True  # Beginning of Sentence

    if i < len(sent) - 1:
        features.update({
            "+1:word.lower()": sent[i + 1][0].lower(),
            "+1:word.istitle()": sent[i + 1][0].istitle(),
            "+1:word.isupper()": sent[i + 1][0].isupper(),
        })
    else:
        features["EOS"] = True  # End of Sentence

    return features

def sent2features(sent):
    return [word2features(sent, i) for i in range(len(sent))]

def sent2labels(sent):
    return [label for _, label in sent]

def sent2tokens(sent):
    return [token for token, _ in sent]
