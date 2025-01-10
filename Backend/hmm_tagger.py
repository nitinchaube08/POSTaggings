from nltk.corpus import treebank
from nltk.probability import ConditionalFreqDist, ConditionalProbDist, LidstoneProbDist

def hmm_train_tagger():
    start = "<s>"
    end = "</s>"
    tagged_sentences = treebank.tagged_sents()
    sentence_with_boundaries = [
        [(start, start)] + sentence + [(end, end)] for sentence in tagged_sentences
    ]

    # Transition probabilities
    transitional_freqs = ConditionalFreqDist()
    for sentence in sentence_with_boundaries:
        for i in range(len(sentence) - 1):
            _, current_tag = sentence[i]
            _, next_tag = sentence[i + 1]
            transitional_freqs[current_tag][next_tag] += 1
    transitional_probs = ConditionalProbDist(transitional_freqs, LidstoneProbDist, 0.1)

    # Emission probabilities
    emission_freqs = ConditionalFreqDist()
    for sentence in sentence_with_boundaries:
        for word, tag in sentence:
            emission_freqs[tag][word] += 1
    emission_probs = ConditionalProbDist(emission_freqs, LidstoneProbDist, 0.1)

    # Initial probabilities
    initial_freqs = ConditionalFreqDist()
    for sentence in sentence_with_boundaries:
        _, first_tag = sentence[1]
        initial_freqs[start][first_tag] += 1
    initial_probs = ConditionalProbDist(initial_freqs, LidstoneProbDist, 0.1)

    return initial_probs, transitional_probs, emission_probs

def Viterbi(sentence, transitional_probs, emission_probs, initial_probs):
    states = list(transitional_probs.keys())
    V = [{}]
    path = {}

    for state in states:
        if state in emission_probs:
            prob = emission_probs[state].prob(sentence[0]) if sentence[0] in emission_probs[state].samples() else 0.01
            V[0][state] = initial_probs["<s>"].prob(state) * prob
            path[state] = [state]

    for t in range(1, len(sentence)):
        V.append({})
        new_path = {}
        for state in states:
            if state not in emission_probs:
                continue
            emission_prob = emission_probs[state].prob(sentence[t]) if sentence[t] in emission_probs[state].samples() else 0.01
            prob, prev_state = max(
                (V[t - 1][prev_state] * transitional_probs[prev_state].prob(state) * emission_prob, prev_state)
                for prev_state in states if prev_state in V[t - 1]
            )
            V[t][state] = prob
            new_path[state] = path[prev_state] + [state]
        path = new_path

    final_state = max(V[-1], key=V[-1].get)
    return [(word, tag) for word, tag in zip(sentence, path[final_state])]
