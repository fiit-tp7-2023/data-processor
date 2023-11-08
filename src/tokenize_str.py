import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer
from nltk.corpus import wordnet as wn
from typing import Dict, List, Tuple



def remove_verbs(text: Tuple[str, str]) -> List[str] | None:
    return [word for word, pos in text if pos in ['NN', 'NNS', 'NNPS', 'NNP']]

def nounify(verb_word: str) -> str:
    """ Transform a verb to the closest noun: die -> death """
    verb_synsets = wn.synsets(verb_word)

    # Word not found
    if not verb_synsets:
        return None

    # Get all verb lemmas of the word
    verb_lemmas = [l for s in verb_synsets \
                   for l in s.lemmas() if s.name().split('.')[1] == 'v']

    # Get related forms
    derivationally_related_forms = [(l, l.derivationally_related_forms()) \
                                    for l in    verb_lemmas]

    # filter only the nouns
    related_noun_lemmas = [l for drf in derivationally_related_forms \
                           for l in drf[1] if l.synset().name().split('.')[1] == 'n']

    # Extract the words from the lemmas
    words = [l.name() for l in related_noun_lemmas]
    len_words = len(words)

    # Build the result in the form of a list containing tuples (word, probability)
    result = [(w, float(words.count(w))/len_words) for w in set(words)]
    result.sort(key=lambda w: -w[1])


    
    # return all the possibilities sorted by probability
    return result[0][0] if result else None

    
def tokenize(description: str) -> Dict[str, int]:
    # Tokenization
    tokens = word_tokenize(description.lower())

    # Remove stop words
    filtered_tokens = [word for word in tokens if not word in stopwords.words('english')]


    filtered_tags = nltk.pos_tag(filtered_tokens)

    #give me list of adjetives

    adjs = [word for word, pos in filtered_tags if pos == 'JJ']

    nouns = [nounify(word) for word in adjs]

    filtered_tokens = remove_verbs(filtered_tags)
    
    if filtered_tokens is None:
        filtered_tokens = []

    #add nouns to filtered_tokens
    filtered_tokens.extend(nouns)
    filtered_tokens = [word for word in filtered_tokens if word is not None]

    filtered_tokens = [word for word in filtered_tokens if word.isalpha()]

    # Lemmatization
    lemmatizer = WordNetLemmatizer()
    lemmatized_tokens = [lemmatizer.lemmatize(word) for word in filtered_tokens]

    freq_dist = nltk.FreqDist(lemmatized_tokens)

    return freq_dist
       

