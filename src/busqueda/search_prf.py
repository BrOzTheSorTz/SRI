import heapq
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

    

    return similarities

def main(config_file):
    with open(config_file) as f:
        config = json.load(f)

    structure_path = config["structures_path"]
    stemmer_path_docs = config["stemmer_path"]
    relevant_docs = 5

    doc2id, term2id, id2doc, id2term, inverted_index = retrieve_structures(structure_path)

    with open(stemmer_path_docs,'r') as file:
        docs = json.load(file)

    with open(os.path.join(structure_path, 'tfidf_index.pkl'), 'rb') as f:
        tfidf_index = pickle.load(f)

    with open(os.path.join(structure_path, 'idf_term.pkl'), 'rb') as f:
        idf_term = pickle.load(f)

    with open(os.path.join(structure_path, 'term2id.json'), 'r') as f:
        term2id = json.load(f)
    
    with open(os.path.join(structure_path,'doc_freq.json'),'r') as f:
        doc_freq = json.load(f)

    queries = []
    with open(config["queries_path"], 'r') as f:
        queries_json = json.load(f)

    
    query_stemmer2 = {}
    for i in range(2):
        output = "ID,rel_docs\n"
        
        for id, query_stemmer in queries_json.items():
            
            
            if i > 0:
                query_stemmer += query_stemmer2[id]
                relevant_docs = 60
            
            print(id)
            returned_docs = cosine_similarity(query_stemmer, tfidf_index, idf_term, term2id)
            sorted_docs = heapq.nlargest(relevant_docs, returned_docs.items(), key=lambda x: x[1])
            line = str(id) + ","
            query_stemmer2 [id] = []
            if i == 0:
                for doc_id, sim in sorted_docs:
                    
                
                    doc = id2doc[doc_id]
                    tokens_doc = doc_freq[id2doc[doc_id]]
                
                    tokens_tf = heapq.nlargest(25, tokens_doc, key=tokens_doc.get)
                    query_stemmer2[id] += tokens_tf
            else:
                for doc_id, sim in sorted_docs:
                    line += id2doc[doc_id] + " "
                output += line + "\n"
            

    with open(config["result_path"], "w") as archivo:
        archivo.write(output)

if __name__ == "__main__":
    run(main)
