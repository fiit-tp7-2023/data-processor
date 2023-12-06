import nltk
from src.models.neo4j_models import NFT
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer
from nltk.corpus import wordnet as wn

class TokenizationService:
    lemmatizer: WordNetLemmatizer
    englishStopword: list[str]
    def __init__(self) -> None:
        self.lemmatizer = WordNetLemmatizer()
        self.englishStopword = stopwords.words('english')
        pass
    
    def remove_verbs(self, text: tuple[str, str]) -> list[str] | None:
        return [word for word, pos in text if pos in ['NN', 'NNS', 'NNPS', 'NNP']]

    def nounify(self, verb_word: str) -> str:
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
    
    def _tokenize(self, tokenizable_string: str) -> dict[str, int]:
        # Tokenization
        
        if(tokenizable_string == ''):
            return dict()
        
        tokens = word_tokenize(tokenizable_string.lower())

        # Remove stop words
        filtered_tokens = [word for word in tokens if not word in self.englishStopword]


        filtered_tags = nltk.pos_tag(filtered_tokens)

        #give me list of adjetives

        adjs = [word for word, pos in filtered_tags if pos == 'JJ']

        nouns = [self.nounify(word) for word in adjs]

        filtered_tokens = self.remove_verbs(filtered_tags)
        
        if filtered_tokens is None:
            filtered_tokens = []

        #add nouns to filtered_tokens
        filtered_tokens.extend(nouns)
        filtered_tokens = [word for word in filtered_tokens if word is not None]

        filtered_tokens = [word for word in filtered_tokens if word.isalpha()]

        # Lemmatization
        lemmatized_tokens = [self.lemmatizer.lemmatize(word) for word in filtered_tokens]

        return nltk.FreqDist(lemmatized_tokens)
    
    
    def _parseAttributes(self, attributes: list[dict[str, str]]) -> str:
        tokenizable_string = ''
        for attribute in attributes:
            if(attribute['trait_type']):
                tokenizable_string += attribute['trait_type'] + ': '
            if(attribute['value']):
                tokenizable_string += attribute['value'] + '. '
        return tokenizable_string

        
    def tokenize(self, nft: NFT) -> dict[str, int]:
        tokenizable_string = ''
        # Check if there is a description
        if(nft.description):
            tokenizable_string += nft.description + '. '
            
        # Check if there is a name
        if(nft.name):
            tokenizable_string += nft.name + '. '
            
        # Check if there are attributes
        if(nft.attributes):
            tokenizable_string += self._parseAttributes(nft.attributes)
            
        return self._tokenize(tokenizable_string)
        