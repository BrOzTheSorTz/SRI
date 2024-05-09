import argparse
import csv
import json
import os
import time
from unidecode import unidecode

# Lista de caracteres permitidos
possible_values = [chr(c) for c in range(32, 127)] + ["á", "é", "í", "ó", "ú", "_", "-", "\n"]

# Función para eliminar caracteres especiales de una palabra
def remove_special_chars(word):
    return "".join([c if c in possible_values else "" for c in word])

# Función para transformar texto
def transform(content):
    word_list = [remove_special_chars(word.lower()) for word in content.split()]
    return word_list, []

# Función para cargar tokens en un archivo JSON
def load(token_list, file_name, tokens_path):
    with open(os.path.join(tokens_path, f"{file_name}.json"), "w") as file:
        json.dump(token_list, file)

# Función para procesar un archivo TSV y extraer tokens
def etl_tsv(path, tokens_path):
    data = {}
    with open(path, 'r') as tsv_file:
        tsv_reader = csv.reader(tsv_file, delimiter="\t")
        for row in tsv_reader:
            name_doc, content_doc = row[:2]
            tokens, _ = transform(unidecode(content_doc))
            data[name_doc] = tokens
        
    with open(tokens_path, 'w') as file:
        json.dump(data, file)

# Función principal
def main(config_file):
    inicio = time.time()
    
    with open(config_file) as f:
        config = json.load(f)
    
    doc_tsv = config["docs_path"]
    tokens_path = config["tokens_path"]
    etl_tsv(doc_tsv, tokens_path)

    fin = time.time()
    print("Execution time:", fin - inicio, "seconds")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="ETL process from TSV to JSON")
    parser.add_argument("config_file", help="Path to the configuration file")
    args = parser.parse_args()
    main(args.config_file)
