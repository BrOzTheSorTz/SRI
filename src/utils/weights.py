import os
import math
import pickle
import sys
import time
import json
from clize import run

# Función para recuperar las estructuras utilizadas para indexar
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

# Función principal para calcular los pesos TF-IDF para los términos en el índice invertido y guardar los resultados en archivos
def main(config_file):
    start = time.time()  # Registrar el tiempo de inicio

    with open(config_file) as f:
        config = json.load(f)  # Cargar la configuración desde el archivo JSON
    structures_path = config["structures_path"]  # Obtener la ruta de las estructuras desde la configuración
    doc2id, term2id, id2doc, id2term, inverted_index = retrieve_structures(structures_path)

    num_archivos = len(doc2id)

    document_index = {}  # Inicializar el diccionario de índice de documentos
    idf_terms = {}  # Inicializar el diccionario de IDF (Frecuencia Inversa de Documento)
    max_tf_ij = -1  # Inicializar el valor máximo de TF (Frecuencia del Término)

    # Calcular la frecuencia inversa de documento para cada término
    for term_id, postings_list in inverted_index.items():
        idf_terms[term_id] = math.log(float(num_archivos / len(postings_list)), 2)  # Calcular IDF
        for doc_id, frequency in postings_list.items():
            if doc_id not in document_index:
                document_index[doc_id] = {}
            document_index[doc_id][term_id] = frequency  # Almacenar la frecuencia del término en el índice del documento

    # Normalizar las frecuencias
    for doc_id, terms in document_index.items():
        max_tf_ij = max(terms.values())  # Calcular el valor máximo de TF
        for term_id, frequency in terms.items():
            document_index[doc_id][term_id] = float(frequency / max_tf_ij)  # Normalizar TF

    # Obtener los pesos de los términos en un documento usando la fórmula TF-IDF
    for doc_id, terms in document_index.items():
        sum_weights = 0
        for term_id, frequency in terms.items():
            weight = frequency * idf_terms[term_id]  # Calcular el peso TF-IDF
            document_index[doc_id][term_id] = weight  # Actualizar el peso del término en el índice del documento
            sum_weights += weight * weight  # Acumular los pesos al cuadrado

        norm = math.sqrt(sum_weights)  # Calcular la norma L2
        for term_id, frequency in terms.items():
            document_index[doc_id][term_id] = float(document_index[doc_id][term_id] / norm)  # Normalizar por la norma L2

    end = time.time()  # Registrar el tiempo de finalización
    print("Tiempo de ejecución: ", (end - start), " segundos")  # Imprimir el tiempo de ejecución
    print("Tamaño del nuevo índice invertido: ", sys.getsizeof(document_index), " bytes.")  # Imprimir el tamaño del índice invertido

    # Guardar el índice TF-IDF en un archivo
    with open(os.path.join(structures_path, 'tfidf_index.pkl'), 'wb') as f:
        pickle.dump(document_index, f)

    # Guardar el IDF de cada término en un archivo
    with open(os.path.join(structures_path, 'idf_term.pkl'), 'wb') as f:
        pickle.dump(idf_terms, f)

if __name__ == "__main__":
    run(main)  # Ejecutar la función principal si el script es ejecutado directamente
