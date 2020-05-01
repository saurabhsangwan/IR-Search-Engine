from html.parser import HTMLParser
from os import walk, path
import re
from nltk.tokenize import word_tokenize
from nltk.stem import PorterStemmer
from nltk.corpus import stopwords
import nltk
from collections import Counter, defaultdict
import string
from math import sqrt, log2
from crawler.models import TextData
import pickle

# porter stemmer being initialised
ps = PorterStemmer()
nltk.download('stopwords')
stop_words = set(stopwords.words('english'))
nltk.download('punkt')


#function to tokenise any string and return a list of tokens
def tokenize(s):
    s = s.lower()
    s.translate(str.maketrans('', '', string.punctuation))
    s = re.sub(r'\d+', '', s)
    s.translate(str.maketrans('', '', string.punctuation))
    tokenizer = word_tokenize(s)
    tokens = tokenizer
    tokens = [i for i in tokens if len(i) > 2]
    tokens = [ps.stem(i.lower()).lower() for i in tokens]
    tokens = [i.lower() for i in tokens if i.lower() not in stop_words]
    tokens = [i.translate(str.maketrans('', '', string.punctuation)) for i in tokens if i not in stop_words]
    tokens = [ps.stem(i.lower()).lower() for i in tokens]
    tokens = [i for i in tokens if i not in stop_words]
    tokens = [i for i in tokens if len(i) > 2]
    return tokens



#retrieving results for a query
def retrieve_documents(query):
    query_tokens = tokenize(query)
    query_tf = Counter(query_tokens)
    with open('index.pickle', 'rb') as handle:
        b = pickle.load(handle)
    inverted_index = b['inverted_index']
    document_index = b['document_index']
    document_dict = {}
    for qt in query_tf.keys():
        for doc in inverted_index[qt]:
            document_dict[doc] = 0

    for key, value in document_dict.items():
        dot_product = 0
        mod_query = 0
        for qt, qt_tf in query_tf.items():
            if qt in document_index[key]['token_info']:
                dot_product += (qt_tf * document_index[key]['token_info'][qt]['idf']) * document_index[key]['token_info'][qt]['idf'] * \
                               document_index[key]['token_info'][qt]['tf']
            mod_query += (qt_tf) ** 2

        mod_query = sqrt(mod_query)
        mod_document = document_index[key]['length']
        cosine_similarity = dot_product/(mod_query*mod_document)
        document_dict[key]=cosine_similarity
    sorted_document_list = sorted(document_dict.items(), key=lambda kv: kv[1], reverse=True)
    return [i[0] for i in sorted_document_list]


def create_index():
    inverted_index = defaultdict(list)
    document_index = {}


    file_info = {}
    tds = TextData.objects.all()
    # file data being parsed into a dict
    # inverted index being created
    for td in tds:
        tokens = tokenize(td.text)
        if len(tokens)==0:
            continue
        token_counts = dict(Counter(tokens))
        token_info = {}
        max_freq = max([i[1] for i in token_counts.items()])
        for key, value in token_counts.items():
            token_info[key] = {
                'tf': value / max_freq
            }
        document_index[td.id] = {'token_info': token_info}
        for token in tokens:
            if td.id not in inverted_index[token]:
                inverted_index[token].append(td.id)


    # idf and length of each document being calculated
    for td in tds:
        if td.text=='':
           continue
        weight = 0
        for token, token_value in document_index[td.id]['token_info'].items():
            document_index[td.id]['token_info'][token]['idf'] = 1 + log2(len(tds) / len(inverted_index[token]))
            document_index[td.id]['token_info'][token]['weight'] = (document_index[td.id]['token_info'][token]['tf'] * document_index[td.id]['token_info'][token][
                'idf']) ** 2
            weight += document_index[td.id]['token_info'][token]['weight']
        document_index[td.id]['length'] = sqrt(weight)

    a={'inverted_index': inverted_index,
       'document_index': document_index}

    with open('index.pickle', 'wb') as handle:
        pickle.dump(a, handle, protocol=pickle.HIGHEST_PROTOCOL)