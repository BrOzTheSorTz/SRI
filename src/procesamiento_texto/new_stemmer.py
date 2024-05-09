import json,sys
from nltk.stem import PorterStemmer, SnowballStemmer
sys.path.append("../MEJORAS_SRI")
from src.indexacion.etl import load
from clize import run

# Función para aplicar stemming a una lista de tokens
def apply_stemmer(tokens, algorithm, language):
    new_tokens = []  # Inicializa lista para los tokens stem
    if algorithm == "porter":  # Si se selecciona el algoritmo porter
        stemmer = PorterStemmer()  # Inicializa Porter stemmer
    elif algorithm == "snowball":  # Si se selecciona el algoritmo snowball
        language = "spanish" if language == "es" else "english"  # Convertir código de idioma a snowball language code
        stemmer = SnowballStemmer(language=language)  # Inicializa Snowball stemmer
    
    # Aplica stemming a cada token y añade el token stem a la lista
    for token in tokens:
        if token and token[0] != "&":  # Si el token no está vacío y no es una entidad especial
            new_tokens.append(stemmer.stem(token))  # Aplica stemming al token y añádelo a la lista
        else:
            new_tokens.append(token)  # Conserva las entidades especiales sin stemming
    
    return new_tokens  # Retorna lista de tokens stem

# Función principal para procesar archivos tokenizados, aplicar stemming y guardar los resultados
def main(config_file):
    with open(config_file) as f:
        config = json.load(f)  # Carga la configuración desde el archivo JSON
    
    algorithm = config["algorithm_stemmer"]  # Obtiene el algoritmo de stemming de la configuración
    language = "es"  # Define el idioma (puedes cambiarlo según sea necesario)
    stopper_path = config["stopper_path"]  # Obtiene la ruta de los tokens después del stopper desde la configuración
    stemmer_path = config["stemmer_path"]  # Obtiene la ruta para guardar los tokens después del stemming desde la configuración
    
    with open(stopper_path, 'r') as file:
        content = json.load(file)  # Carga los tokens después del stopper
    
    result = {}  # Inicializa el diccionario para los tokens después del stemming
    
    for doc, tokens in content.items():
        tokens = apply_stemmer(tokens, algorithm, language)  # Aplica stemming a los tokens
        result[doc] = tokens  # Agrega los tokens después del stemming al diccionario
    
    # Guarda los resultados en un archivo JSON
    with open(stemmer_path, 'w') as file:
        json.dump(result, file)

if __name__ == "__main__":
    run(main)  # Ejecuta la función principal si el script es ejecutado directamente
