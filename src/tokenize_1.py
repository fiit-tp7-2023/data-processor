import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer
from nltk.corpus import wordnet as wn



def remove_verbs(text):
    return [word for word, pos in text if pos in ['NN', 'NNS', 'NNPS', 'NNP']]

def nounify(verb_word):
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

    
def main():
    # Example NFT description of monkey business
    description = "Introducing the 'Celestial Legends' collection, an exclusive series of NFTs that bring the constellations to life. Each NFT in this collection is a unique digital tapestry depicting a zodiac sign transformed into a majestic creature. From the daring Aries Ram, adorned with rubies and wrapped in wisps of white clouds, to the mysterious Pisces Fish, glimmering with scales of sapphire blue and emerald green, swimming in the cosmic ocean. The collection features 12 main pieces, each animated with subtle movements that make the stars twinkle and the creatures breathe. Holders of these NFTs will also receive an augmented reality version, allowing them to project their celestial companions into the real world. The 'Celestial Legends' are not just collectibles; they are interactive pieces of art that offer a gateway to the stars."

    # Tokenization
    tokens = word_tokenize(description.lower())

    # Remove stop words
    filtered_tokens = [word for word in tokens if not word in stopwords.words('english')]


    filtered_tags = nltk.pos_tag(filtered_tokens)

    #give me list of adjetives

    adjs = [word for word, pos in filtered_tags if pos == 'JJ']

    nouns = [nounify(word) for word in adjs]

    filtered_tokens = remove_verbs(filtered_tags)

    #add nouns to filtered_tokens
    filtered_tokens.extend(nouns)
    filtered_tokens = [word for word in filtered_tokens if word is not None]

    filtered_tokens = [word for word in filtered_tokens if word.isalpha()]

    # Lemmatization
    lemmatizer = WordNetLemmatizer()
    lemmatized_tokens = [lemmatizer.lemmatize(word) for word in filtered_tokens]

    freq_dist = nltk.FreqDist(lemmatized_tokens)

    # order by frequency
    freq_dist = {k: v for k, v in sorted(freq_dist.items(), key=lambda item: item[1], reverse=True)}

    # Print the entire frequency distribution
    print("Frequency Distribution of Lemmatized Tokens:")
    for word, freq in freq_dist.items():
        print(word, ":", freq)
       



main()





# Generate tags (using the lemmatized tokens)
#tags = list(set(lemmatized_tokens))

#print(tags)
