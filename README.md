# Sistema de Recuperación de Información (SRI) en Python

Este proyecto implementa un Sistema de Recuperación de Información (SRI) en Python, que indexa documentos y permite realizar consultas eficientes sobre ellos. El SRI utiliza técnicas como tokenización, normalización, pesado de términos y construcción de índices invertidos para lograr una recuperación de información precisa y rápida.

## Características Principales

* Para ejecutar cada parte debe seguirse el orden habitual de procesado de documentos y consultas en un sistema de recuperación de información. Necesario es por tanto unas nociones básicas.

* Se divide por módulos, cada módulo puede hacer una determinada acción que explicaremos más adelante. Lo que hagas en un módulo puede depender en el módulo siguiente.

## Requisitos del Sistema

- Python 3.x
- Bibliotecas Python: `bs4`, `json`, `pandas`, `unidecode`, `queue`, `clize`, `scipy`, `nltk`

## Instalación y Uso

1. **Clonar el Repositorio**: Clona este repositorio en tu máquina local utilizando el siguiente comando:

    ```
    git clone https://github.com/tu_usuario/sistema-recuperacion-informacion.git
    ```

2. **Instalar Dependencias**: Instala las dependencias del proyecto ejecutando el siguiente comando en la raíz del proyecto:

    ```
    pip install -r requirements.txt
    ```

3. **Configuración**: Antes de ejecutar el sistema, asegúrate de configurar los archivos de configuración según tus necesidades. Estos archivos incluyen configuraciones como las rutas de los documentos a indexar, las palabras vacías (stop words), etc.
Claro, en el README puedes incluir una sección que explique el propósito de los archivos de configuración `config.json` y `config_queries.json`, así como la información que contienen. Aquí tienes un ejemplo de cómo podrías hacerlo:

---

## Archivos de Configuración

El proyecto utiliza archivos de configuración en formato JSON para especificar diversas opciones y rutas de los datos necesarios para el funcionamiento del sistema. A continuación se describen los principales archivos de configuración utilizados:

### `config.json`

Este archivo contiene las configuraciones principales para el procesamiento de documentos en el corpus. Aquí está la información detallada de cada clave:

- `"docs_path"`: Ruta al archivo TSV que contiene los documentos del corpus.
- `"tokens_path"`: Ruta donde se guardarán los tokens procesados de los documentos en formato JSON.
- `"stopper_path"`: Ruta donde se guardarán los resultados del proceso de eliminación de stop words en formato JSON.
- `"stopwords_path"`: Ruta al archivo de palabras vacías (stop words) en el idioma especificado.
- `"algorithm_stemmer"`: Algoritmo de stemmer utilizado para reducir las palabras a su raíz. Puede ser `"porter"` o `"snowball"`.
- `"stemmer_path"`: Ruta donde se guardarán los resultados del proceso de stemming en formato JSON. En este lugar se guardaran los tokens que queremos usar realmente en la indexación y el pesado por lo que si hacemos expansión de consultas debemos especificar aquí su ruta para hacer el indexado y el pesado.
- `"expand_docs"`: Ruta donde se guardarán los resultados del proceso de expansión de documentos en formato JSON.
- `"expand_factor"`: Factor de expansión para el proceso de expansión de documentos.
- `"structures_path"`: Ruta donde se guardarán las estructuras de datos utilizadas por el sistema.
- `"queries_path"`: Ruta al archivo CSV que contiene las consultas a procesar.
- `"json_docs"`: Ruta donde se guardarán los documentos en formato JSON.
- `"json_queries"`: Ruta donde se guardarán las consultas en formato JSON.
- `"k_bm25"`: Parámetro K para el algoritmo BM25.
- `"b_bm25"`: Parámetro B para el algoritmo BM25.
- `"result_path"`: Ruta donde se guardará el archivo CSV con los resultados de las consultas.

### `config_queries.json`

Este archivo contiene las configuraciones específicas para el procesamiento de consultas. Aquí está la información detallada de cada clave:

- `"queries_path"`: Ruta al archivo CSV que contiene las consultas a procesar.
- `"tokens_path"`: Ruta donde se guardarán los tokens procesados de las consultas en formato JSON.
- `"stopper_path"`: Ruta donde se guardarán los resultados del proceso de eliminación de stop words en formato JSON.
- `"stopwords_path"`: Ruta al archivo de palabras vacías (stop words) en el idioma especificado.
- `"algorithm_stemmer"`: Algoritmo de stemmer utilizado para reducir las palabras a su raíz. Puede ser `"porter"` o `"snowball"`.
- `"stemmer_path"`: Ruta donde se guardarán los resultados del proceso de stemming en formato JSON.


4. **Ejecución del Sistema**: Ejecuta el sistema utilizando el siguiente comando:

    ```
    python ruta_a/{nombre_archivo}.py config/config{_queries}.json
    ```

    Donde `config{_queries}.json` es el archivo de configuración que deseas utilizar.
    Y donde `nombre_archivo.py` será aquel del módulo que queramos ejecutar.

5. **Consulta de Documentos**: Una vez que el sistema haya indexado los documentos, podrás realizar consultas utilizando el siguiente comando:

    ```
    python search.py config/config.json
    ```

    El archivo de búsqueda puede ser **search\.py**, **search_prf\.py**, **bm25\.py** o **rerank\.py**.

## Estructura del Proyecto

- `config/`: Archivos de configuración en formato JSON.
- `data/`: Datos del corpus y las consultas.
- `structures/`: Estructuras de datos utilizadas por el sistema (índices invertidos, diccionarios, etc.).
- `src/`: Código fuente del proyecto.
- `README.md`: Este archivo README que estás leyendo.

## Contribuciones

¡Las contribuciones son bienvenidas! Si deseas contribuir al proyecto, por favor abre un nuevo issue o envía una solicitud de extracción con tus mejoras las recibo con los brazos abiertos :\)
