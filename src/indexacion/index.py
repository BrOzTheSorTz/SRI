import os
import json
import time
import collections
import pickle
from clize import run
from scipy.sparse import lil_matrix

# Función para guardar las estructuras de datos en formato JSON
def save_structures(path, term2id, doc2id, id2term, id2doc, inverted_index):
    with open(os.path.join(path, 'doc2id.json'), 'w') as file:
        json.dump(doc2id, file)
    with open(os.path.join(path, 'term2id.json'), 'w') as file:
        json.dump(term2id, file)
    with open(os.path.join(path, 'id2doc.json'), 'w') as file:
        json.dump(id2doc, file)
    with open(os.path.join(path, 'id2term.json'), 'w') as file:
        json.dump(id2term, file)
    with open(os.path.join(path, 'inverted_index.pkl'), 'wb') as file:
        pickle.dump(inverted_index, file)

# Función para visualizar el índice invertido en la consola
def visualize_index(index, id2term, id2doc):
    for term_id, postings_list in index.items():
        print("Term: ", id2term[term_id])
        for doc_id, frequency in postings_list.items():
            print("[ {}, {} ]\t".format(id2doc[doc_id], frequency))
        print("")

# Función para escribir el índice invertido en un archivo de texto
def visualize_index_txt(index, id2term, id2doc):
    with open("index.txt", 'w') as file:
        for term_id, postings_list in index.items():
            file.write("Term: {}\n".format(id2term[term_id]))
            for doc_id, frequency in postings_list.items():
                file.write("{}-{}\t".format(id2doc[doc_id], frequency))
            file.write("\n")

# Función principal para procesar archivos XML, construir un índice invertido y guardar las estructuras de datos
def main(config_file):
    start = time.time()
    with open(config_file) as f:
        config = json.load(f)

    stemmer_path = config["stemmer_path"]
    structures_path = config["structures_path"]

    with open(stemmer_path, 'r') as f:
        data = json.load(f)
    
    docs = list(data.keys())
    doc2id = {}
    id2doc = []
    term2id = {}
    id2term = []

    i = 0
    total_tokens = []
    for doc, tokens in data.items():
        doc2id[doc] = i
        id2doc.append(doc)
        i += 1
        total_tokens += tokens
    
    total_tokens = set(total_tokens)
    
    n_docs = len(doc2id)
    n_tokens = len(total_tokens)
    inverted_index = lil_matrix((n_tokens, n_docs), dtype=int)
    index = {}

    i = 0
    token_freq = {}
    for token in total_tokens:
        term2id[token] = i
        id2term.append(token)
        i += 1

    for doc, tokens in data.items():
        term_freq = collections.Counter(tokens)
        token_freq[doc] = term_freq
        for term, freq in term_freq.items():
            term_id = term2id[term]
            doc_id = doc2id[doc]
            if term_id not in index:
                index[term_id] = {}
            index[term_id][doc_id] = freq
    
    with open(os.path.join(structures_path, 'doc_freq.json'), 'w') as file:
        json.dump(token_freq, file)
    
    save_structures(structures_path, term2id, doc2id, id2term, id2doc, index)

    end = time.time()
    print("Time (s): ", end - start)

# Ejecuta la función principal si el script es ejecutado directamente
if __name__ == "__main__":
    run(main)
