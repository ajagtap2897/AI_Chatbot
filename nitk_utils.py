import nltk
import numpy as np
#nltk.download('punkt')
#nltk.download('punkt_tab')
from nltk.stem.porter import PorterStemmer
stemer= PorterStemmer()

def tokenize(sentence):
    return nltk.word_tokenize(sentence)

def stem(word):
    return stemer.stem(word.lower())

def bag_of_words(tokenized_sentenced, all_words):
    tokenized_sentenced = [stem(w) for w in tokenized_sentenced]

    bag = np.zeros(len(all_words), dtype=np.float32)
    for idx, w in enumerate(all_words):
        if w in tokenized_sentenced:
            bag[idx] = 1.0
            
    return bag

