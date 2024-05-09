import heapq
import os
import math
import collections
import pickle
import time
import json
from clize import run

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
def search(query,global_avg,docs,doc_freq,config):
    
    stemmer_path = config["stemmer_path"]
    structure_path = config["structures_path"]
    k = config["k_bm25"]
    b = config["b_bm25"]

    doc2id, term2id, id2doc, id2term, inverted_index = retrieve_structures(structure_path)
    
    total_docs = 200000
    docs_and_rsv = {}
    

    list_tokens = query
    # Weights
    weights_terms = {}
    token_counts = collections.Counter(list_tokens)
    

    
    for doc,content in docs.items():
        id_doc = doc2id[doc]
        sum = 0
    
        long_doc = len(content)
        
        for token,f in token_counts.items():
            if token in content:
                id_token = term2id[token]

                n_token = len(inverted_index[id_token])
                f_in_doc = doc_freq[doc][token]
                idf = calculateIDF(total_docs,n_token)

                sum = sum + bm25(f_in_doc,idf,k,b,long_doc,global_avg)


        docs_and_rsv[id_doc] = sum
    
    
    return docs_and_rsv

    
def bm25(f,idf,k,b,long_doc,global_avg):

    division = (f*(k+1))/(f+k*(1-b+b*(long_doc/global_avg)))

    return idf*division



def calculateIDF(total_docs,n_token):
    return math.log((total_docs-n_token+0.5)/(n_token+0.5))
"""
    We obtain the global mean length of all the docs

"""

def obtain_global_average(stemmer_path):
    with open(os.path.join(stemmer_path),"r") as f:
        docs = json.load(f)

    global_avg = 0
    for content in docs.values():
        global_avg += len(content)
    
    return global_avg/len(docs)

"""
Retrieve relevant documents based on queries using TF-IDF weighted index.
@param[in] config_file: Path to the configuration file.
@param[in] summarize_format: Boolean indicating whether to print results in summary format or not.
"""
def main(config_file,*,summarize_format = False):
    """Retrieve relevant documents based on queries in a doc, using TF-IDF weighted index.

    :param config_file: Path to the configuration json file.
    """
    inicio = time.time()

    with open(config_file) as f:
        config = json.load(f)

    relevant_docs= 10
    structure_path = config["structures_path"]
    
    queries = []
    with open(config["queries_path"], 'r') as f:
        queries_json = json.load(f)

    output = "ID,rel_docs\n"
    doc2id, term2id, id2doc, id2term, inverted_index = retrieve_structures(structure_path)
    
    stemmer_path = config["stemmer_path"]
    global_avg = obtain_global_average(stemmer_path)
    with open(stemmer_path,'r') as file:
        docs = json.load(file)
    with open(os.path.join(structure_path, 'doc_freq.json'), 'r') as file:
        doc_freq = json.load(file)
    
    for id, query_stemmer in queries_json.items():
        print(id)
        returned_docs = search(query_stemmer,global_avg,docs,doc_freq, config)
    
        sorted_docs = heapq.nlargest(relevant_docs, returned_docs.items(), key=lambda x: x[1])
        
            
        line = str(id) + ","
        for doc_id, sim in sorted_docs:
        
            doc = id2doc[doc_id]
            line += doc + " "
        line += "\n"
        print(line)
        output += line
        
        

    with open(config["result_path"], "w") as archivo:
        archivo.write(output)

    

    fin = time.time()
    print("Tiempo: ", fin - inicio, " segundos")

if __name__ == "__main__":
    run(main)