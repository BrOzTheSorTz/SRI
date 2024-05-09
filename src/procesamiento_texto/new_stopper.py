import argparse
import json
import os,sys
import time
from unidecode import unidecode
sys.path.append("../MEJORAS_SRI")
from src.indexacion.etl import load
from src.utils.ayuda import num2let

# Función para eliminar acentos de una lista de palabras
def remove_accents(stopwords):
    return [unidecode(word) for word in stopwords]

# Función para eliminar palabras vacías de una lista de tokens
def remove_empty_words(tokens, stopwords):
    stopwords = remove_accents(stopwords)
    return [token for token in tokens if token not in stopwords]

# Función para obtener las palabras vacías de un documento para un idioma específico
def obtain_stopwords_document(stopwords_path):
    with open(stopwords_path, "r", encoding="utf-8") as f:
        return f.read().split()

# Función principal para procesar archivos tokenizados, eliminar palabras vacías y calcular estadísticas
def main(config_file):
    ini = time.time()
    with open(config_file) as f:
        config = json.load(f)
    
    stopper_path = config["stopper_path"]
    tokens_path = config["tokens_path"]
    stopwords_path = config["stopwords_path"]
    
    with open(tokens_path, 'r') as file:
        content = json.load(file)

    stopwords = obtain_stopwords_document(stopwords_path)

    tokens_stopper = {}
    for doc, tokens in content.items():
        tokens = remove_empty_words(tokens, stopwords)
        tokens_stopper[doc] = tokens

    with open(stopper_path, 'w') as f:
        json.dump(tokens_stopper, f)
    
    fin = time.time()
    print("Execution time:", fin - ini, "seconds")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="ETL process from TSV to JSON")
    parser.add_argument("config_file", help="Path to the configuration file")
    args = parser.parse_args()
    main(args.config_file)
