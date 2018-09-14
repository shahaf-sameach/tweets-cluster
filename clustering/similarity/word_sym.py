from nltk import word_tokenize, pos_tag
from nltk.corpus import wordnet as wn


def penn_to_wn(tag):
    """ Convert between a Penn Treebank tag to a simplified Wordnet tag """
    if tag.startswith('N'):
        return 'n'

    if tag.startswith('V'):
        return 'v'

    if tag.startswith('J'):
        return 'a'

    if tag.startswith('R'):
        return 'r'

    return None


def tagged_to_synset(word, tag):
    wn_tag = penn_to_wn(tag)
    if wn_tag is None:
        return None

    try:
        return wn.synsets(word, wn_tag)[0]
    except:
        return None


def sentence_similarity(sentence1, sentence2):
    """ compute the sentence similarity using Wordnet """
    # Tokenize and tag
    v1 = (sentence1 + '.')[:-1]
    v2 = (sentence2 + '.')[:-1]
    sentence1 = pos_tag(word_tokenize(sentence1))
    sentence2 = pos_tag(word_tokenize(sentence2))

    # Get the synsets for the tagged words
    synsets1 = [tagged_to_synset(*tagged_word) for tagged_word in sentence1]
    synsets2 = [tagged_to_synset(*tagged_word) for tagged_word in sentence2]

    # Filter out the Nones
    synsets1 = [ss for ss in synsets1 if ss]
    synsets2 = [ss for ss in synsets2 if ss]

    score, count = 0.0, 0

    # For each word in the first sentence
    for synset in synsets1:
        # Get the similarity value of the most similar word in the other sentence
        path_similarity = [synset.path_similarity(ss) for ss in synsets2]

        best_score = None
        if path_similarity:
            best_score = max(path_similarity)

        # Check that the similarity could have been computed
        if best_score is not None:
            score += best_score
            count += 1

    # Average the values
    if count > 0:
        score /= count
    return score


def symmetric_sentence_similarity(sentence1, sentence2):
    """ compute the sentence similarity using Wordnet """
    # Tokenize and tag
    sentence1 = pos_tag(word_tokenize(sentence1))
    sentence2 = pos_tag(word_tokenize(sentence2))

    # Get the synsets for the tagged words
    synsets1 = [tagged_to_synset(*tagged_word) for tagged_word in sentence1]
    synsets2 = [tagged_to_synset(*tagged_word) for tagged_word in sentence2]

    # Filter out the Nones
    synsets1 = [ss for ss in synsets1 if ss]
    synsets2 = [ss for ss in synsets2 if ss]

    score, count = 0.0, 0

    # For each word in the first sentence
    for synset in synsets1:
        # Get the similarity value of the most similar word in the other sentence
        path_similarity = [synset.path_similarity(ss) for ss in synsets2]

        best_score = None
        if path_similarity:
            best_score = max(path_similarity)

        # Check that the similarity could have been computed
        if best_score is not None:
            score += best_score
            count += 1

    sentence1_score = score / count if count > 0 else score

    score, count = 0.0, 0
    for synset in synsets2:
        # Get the similarity value of the most similar word in the other sentence
        path_similarity = [synset.path_similarity(ss) for ss in synsets1]

        best_score = None
        if path_similarity:
            best_score = max(path_similarity)

        # Check that the similarity could have been computed
        if best_score is not None:
            score += best_score
            count += 1

    sentence2_score = score / count if count > 0 else score

    return (sentence1_score + sentence2_score) / 2.0


if __name__ == "__main__":

    sentences = [
        "Dogs are awesome.",
        "Some gorgeous creatures are felines.",
        "Dolphins are swimming mammals.",
        "Cats are beautiful animals.",
    ]

    focus_sentence = "Cats are beautiful animals."

    for sentence in sentences:
        print "Similarity(\"%s\", \"%s\") = %s" % (focus_sentence, sentence, sentence_similarity(focus_sentence, sentence))
        print "Similarity(\"%s\", \"%s\") = %s" % (sentence, focus_sentence, sentence_similarity(sentence, focus_sentence))
        print "Symm Similarity(\"%s\", \"%s\") = %s" % (sentence, focus_sentence, symmetric_sentence_similarity(sentence, focus_sentence))
        print

    # Similarity("Cats are beautiful animals.", "Dogs are awesome.") = 0.511111111111
    # Similarity("Dogs are awesome.", "Cats are beautiful animals.") = 0.666666666667
    # Similarity("Cats are beautiful animals.", "Some gorgeous creatures are felines.") = 0.833333333333
    # Similarity("Some gorgeous creatures are felines.", "Cats are beautiful animals.") = 0.833333333333
    # Similarity("Cats are beautiful animals.", "Dolphins are swimming mammals.") = 0.483333333333
    # Similarity("Dolphins are swimming mammals.", "Cats are beautiful animals.") = 0.4
    # Similarity("Cats are beautiful animals.", "Cats are beautiful animals.") = 1.0
    # Similarity("Cats are beautiful animals.", "Cats are beautiful animals.") = 1.0
