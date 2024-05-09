import re
import nltk
from nltk.corpus import wordnet as wn
from nlt import numlet as nl
from unidecode import unidecode
nltk.download('wordnet')
nltk.download('omw')

def convertir_fecha_texto(fecha):
    # Expresión regular para detectar fechas en el formato especificado
    regex_fecha = r'(\d+)\s*(a\.?\s*C\.?)'

    # Función para reemplazar la fecha encontrada por su equivalente en texto
    def reemplazar_fecha(match):
        numero = int(match.group(1))
        if numero == 1:
            return "un antes de cristo"
        elif numero < 10:
            unidades = ["uno", "dos", "tres", "cuatro", "cinco", "seis", "siete", "ocho", "nueve"]
            return unidades[numero - 1] + " antes de cristo"
        else:
            return str(numero) + " antes de cristo"

    # Reemplazar fechas en el texto utilizando la expresión regular y la función de reemplazo
    fecha_texto = re.sub(regex_fecha, reemplazar_fecha, fecha)

    return fecha_texto

def normalizar_fechas_en_texto(texto):
    # Expresión regular para encontrar todas las fechas en el texto
    regex_todas_fechas = r'\b\d+\s*a\.?\s*C\.?\b'

    # Encontrar todas las fechas en el texto
    fechas_encontradas = re.findall(regex_todas_fechas, texto)

    # Normalizar cada fecha encontrada en el texto
    for fecha in fechas_encontradas:
        texto = texto.replace(fecha, convertir_fecha_texto(fecha))

    return texto



def expandir_consulta(consulta):
    
    
    # Obtenemos los synsets (conjuntos de palabras con significados relacionados) de la consulta
    synsets = wn.synsets(consulta,lang='spa')
    
    # Verificamos si se encontraron synsets para la consulta
    if synsets:
        # Tomamos solo el primer synset para simplificar
        syns = []
        for synset in synsets:
            words=synset.lemma_names('spa')
            words= [unidecode(word.lower()) for word in words]
            words_ = [word.split('_') for word in words if "_" in word]
            #print(synset.definition())
            if len(words_) > 0:

                for w in words_:
                    for l in w:
                    
                        syns.append(l)
                
            syns+=words
        return syns
    else:
        return []
def num2let(num):
    return nl.Numero(num).a_letras

