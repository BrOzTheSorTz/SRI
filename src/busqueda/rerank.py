import heapq
from clize import run
from sentence_transformers.cross_encoder import CrossEncoder
import json,csv

def main(config_file):
    model = CrossEncoder("cross-encoder/ms-marco-MiniLM-L-6-v2")
    #cross-encoder/nli-deberta-base
    with open(config_file) as f:
        config = json.load(f)
    
    json_docs = config["json_docs"]
    with open(json_docs,'r' ) as file:
        docs = json.load(file)
    json_queries = config["json_queries"]
    with open(json_queries,'r') as file:
        queries = json.load(file)

    results_csv = config["result_path"]
    with open(results_csv,newline='') as file:
        reader = csv.reader(file,delimiter=',')
        next(reader) # Skip header
        output = "ID,rel_docs\n"
        for row in reader:
            
            query_id = row[0]
            print(query_id)
            docs_id = row[1].split(" ")
            query = queries[query_id]
            
            linea = f"{query_id},"

            result = {}
            for doc_id in docs_id:
                if doc_id != "":
                    doc = docs[doc_id]
                    score = model.predict([(query, doc)])
                    result[doc_id] = score

            # Ordenar los scores de mayor a menor
            
            sorted_result = sorted(result.items(), key=lambda x: x[1], reverse=True)[:10]
            

            # Obtener los ID de los documentos ordenados por relevancia
            sorted_docs_id = [doc_id for doc_id, _ in sorted_result]

            # Concatenar los ID de los documentos ordenados por relevancia separados por espacios
            sorted_docs_id_str = " ".join(sorted_docs_id)

            # Añadir los ID de los documentos por relevancia a la línea
            linea += sorted_docs_id_str

            # Añadir la línea al output
            output += linea + "\n"
        
    with open(config["result_path"], "w") as archivo:
        archivo.write(output)



if __name__ == "__main__":
    run(main)