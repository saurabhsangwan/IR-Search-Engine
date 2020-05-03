import pickle
from collections import defaultdict
from django.conf import settings
with open('index.pickle', 'rb') as handle:
    b = pickle.load(handle)
inverted_index = b['inverted_index']
document_index = b['document_index']
def relevant_doc_weigts(doc_ids):
    result = defaultdict(int)

    for id in doc_ids:
        for key, value in document_index[id]['token_info'].items():
            result[key]+=value['tf']*value['idf']
            print(key, value)
    result = sorted(result.items(), key=lambda x: x[1], reverse=True)
    if len(result)>5:
        result = result[:5]
    return [i[0] for i in result]

def pseudo_relevance_feedback(doc_ids):
    if len(doc_ids)>settings.NUM_DOC_EXPANSION:
        doc_ids = doc_ids[:settings.NUM_DOC_EXPANSION]
    result = defaultdict(int)

    for id in doc_ids:
        for key, value in document_index[id]['token_info'].items():
            result[key] += value['tf'] * value['idf']
            print(key, value)
    result = sorted(result.items(), key=lambda x: x[1], reverse=True)
    if len(result)>5:
        result = result[:5]
    return [i[0] for i in result]