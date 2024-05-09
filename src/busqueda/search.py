import os
import math
import pickle
import json
from clize import run
import numpy as np
import collections

def retrieve_structures(path):
    with open(os.path.join(path, 'doc2id.json'), 'r') as file:
        doc2id = json.load(file)

    with open(os.path.join(path, 'term2id.json'), 'r') as file:
        term2id = json.load(file)

    with open(os.path.join(path, 'id2doc.json'), 'r') as file:
        id2doc = json.load(file)

    with open(os.path.join(path, 'id2term.json'), 'r') as file:
        id2term = json.load(file)

    with open(os.path.join(path, 'inverted_index.pkl'), 'rb') as file:
        inverted_index = pickle.load(file)

    return doc2id, term2id, id2doc, id2term, inverted_index

def cosine_similarity(query, tfidf_index, idf_term, term2id):
    weights_terms = {}
    token_counts = collections.Counter(query)
    suma = 0
    for token, f in token_counts.items():
        if token in term2id:
            tid = term2id[token]
            idf = idf_term[tid]
            tf = f
            weight = idf * tf
            weights_terms[tid] = weight
            suma = suma + weight * weight
    norm = math.sqrt(suma)
            
    if norm > 0:
        for key, value in weights_terms.items():
            weights_terms[key] = float(value / norm)


    similarities = {}
    for doc_id, terms in tfidf_index.items():
        sum = 0
        for term_id,weight in weights_terms.items():
            #If the term of the query is on the doc
            if term_id in terms:
                weight_doc = terms[term_id]
                sum += weight * weight_doc
        similarities[doc_id] = sum

    #query_vector = np.zeros(len(term2id))

    

    # for term_id, weight in weights_terms.items():
    #     query_vector[term_id] = weight
    
    # similarities = {}
    # for doc_id, docs in tfidf_index.items():
    #     doc_vector = np.zeros(len(term2id))
    #     for term_id,weight in docs.items():
    #         doc_vector[term_id] = weight
    #     similarities[doc_id] = np.dot(query_vector, doc_vector) 

    return similarities

def main(config_file):
    with open(config_file) as f:
        config = json.load(f)

    structure_path = config["structures_path"]
    relevant_docs = 32

    doc2id, term2id, id2doc, id2term, inverted_index = retrieve_structures(structure_path)

    with open(os.path.join(structure_path, 'tfidf_index.pkl'), 'rb') as f:
        tfidf_index = pickle.load(f)

    with open(os.path.join(structure_path, 'idf_term.pkl'), 'rb') as f:
        idf_term = pickle.load(f)

    with open(os.path.join(structure_path, 'term2id.json'), 'r') as f:
        term2id = json.load(f)

    queries = []
    with open(config["queries_path"], 'r') as f:
        queries_json = json.load(f)

    output = "ID,rel_docs\n"
    
    for id, query_stemmer in queries_json.items():
        print(id)
        returned_docs = cosine_similarity(query_stemmer, tfidf_index, idf_term, term2id)
        sorted_docs = sorted(returned_docs.items(), key=lambda x: x[1], reverse=True)[:relevant_docs]
        
        line = str(id) + ","
        for doc_id, sim in sorted_docs:
        
            doc = id2doc[doc_id]
            line += doc + " "
        line += "\n"
        output += line
        
        

    with open(config["result_path"], "w") as archivo:
        archivo.write(output)

if __name__ == "__main__":
    run(main)
