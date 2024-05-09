import csv
import json
import os
import time
from clize import run
from bs4 import BeautifulSoup
from unidecode import unidecode
from etl import transform

# Lista de caracteres permitidos
possible_values = [chr(c) for c in range(32, 127)] + ["á", "é", "í", "ó", "ú", "_", "-", "\n"]

# Función para eliminar caracteres especiales de una palabra
def remove_special_chars(word):
    return "".join([c if c in possible_values else "" for c in word])

# Función para procesar un archivo CSV de consultas y extraer tokens
def etl_queries(csv_path, tokens_path):
    queries = {}
    with open(csv_path, 'r', encoding='utf-8') as csv_file:
        csv_reader = csv.reader(csv_file)
        for id, row in enumerate(csv_reader):
            cleaned_row = unidecode(row[0].replace('"', ''))
            tokens, _ = transform(cleaned_row)
            queries[str(id)] = tokens
    
    with open(tokens_path, 'w') as file:
        json.dump(queries, file)

# Función principal
def main(config_file):
    with open(config_file) as f:
        config = json.load(f)
    
    queries_csv = config["queries_path"]
    tokens_path = config["tokens_path"]
    etl_queries(queries_csv, tokens_path)

if __name__ == "__main__":
    run(main)
