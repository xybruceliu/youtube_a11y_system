import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import os, sys
from sklearn.model_selection import train_test_split
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import PorterStemmer
from collections import Counter
from num2words import num2words
from nltk.stem import WordNetLemmatizer 
from sklearn.pipeline import Pipeline
from sklearn.ensemble import ExtraTreesClassifier
from sklearn.model_selection import cross_validate
from sklearn import svm
from sklearn.naive_bayes import GaussianNB
from sklearn.feature_extraction.text import TfidfVectorizer
from collections import Counter, defaultdict
from sklearn.metrics import accuracy_score
from sklearn.metrics import confusion_matrix
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.linear_model import LogisticRegression
import optunity
import optunity.metrics
from nltk.tokenize import sent_tokenize, word_tokenize
import gensim
from gensim.test.utils import common_texts, get_tmpfile
from scipy.stats import entropy

def convert_lower_case(data):
    return np.char.lower(data)

def remove_stop_words(data):
    stop_words = stopwords.words('english')
    words = word_tokenize(str(data))
    new_text = ""
    for w in words:
        if w not in stop_words and len(w) > 1:
            new_text = new_text + " " + w
    return new_text

def remove_punctuation(data):
    symbols = "!\"#$%&()*+-./:;<=>?@[\]^_`{|}~\n"
    for i in range(len(symbols)):
        data = np.char.replace(data, symbols[i], ' ')
        data = np.char.replace(data, "  ", " ")
    data = np.char.replace(data, ',', '')
    return data

def remove_apostrophe(data):
    return np.char.replace(data, "'", "")

def stemming(data):
    lemmatizer = WordNetLemmatizer()
    
    tokens = word_tokenize(str(data))
    new_text = ""
    for w in tokens:
        new_text = new_text + " " + lemmatizer.lemmatize(w)
    return new_text

def convert_numbers(data):
    tokens = word_tokenize(str(data))
    new_text = ""
    for w in tokens:
        try:
            w = num2words(int(w))
        except:
            a = 0
        new_text = new_text + " " + w
    new_text = np.char.replace(new_text, "-", " ")
    return new_text

def preprocess(data):
    data = convert_lower_case(data)
    data = remove_punctuation(data) #remove comma seperately
    data = remove_apostrophe(data)
    #data = remove_stop_words(data)
    data = convert_numbers(data)
    data = stemming(data)
    data = remove_punctuation(data)
    data = convert_numbers(data)
    data = stemming(data) #needed again as we need to stem the words
    data = remove_punctuation(data) #needed again as num2word is giving few hypens and commas fourty-one
    #data = remove_stop_words(data) #needed again as num2word is giving stop words 101 - one hundred and one
    return data


def word_count(captions):
    data = str(preprocess(captions)).split()
    return len(data)

# compute text entropy
# entropy of text distribution over the set of words
# ref: https://www.aclweb.org/anthology/P19-1101.pdf
def entropy1(captions, base=None):
    data = str(preprocess(captions)).split()
    value, counts = np.unique(data, return_counts=True)
    return entropy(counts, base=base)

# compute lexical density
# measure of the number of lexical/content words as a proportion of the total number of words
# lexical word tokens (nouns, adjectives, verbs, adverbs)
# ref: https://en.wikipedia.org/wiki/Lexical_density
def lexical_density(captions):
    tokens = word_tokenize(captions.lower())
    text = nltk.Text(tokens)
    tags = nltk.pos_tag(text)
    counts = Counter(tag for word,tag in tags)
    density = (counts['NN']+counts['NNS']+counts['NNP']+counts['NNPS']+
              counts['JJ']+counts['JJR']+counts['JJS']+
              counts['VB']+counts['VBD']+counts['VBG']+counts['VBN']+counts['VBP']+counts['VBZ']+
              counts['RB']+counts['RBR']+counts['RBS']) / len(tokens)
              
    return density
