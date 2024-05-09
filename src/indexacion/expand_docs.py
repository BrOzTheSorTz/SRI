import json
from clize import run



def main(config_file):
    """Process tokenized files, remove stopwords, and calculate statistics.

    :param config_file: Path to the configuration json file.
    
    
    """
    with open(config_file) as f:
        config = json.load(f)  # Load configuration from JSON file
        
    stemmer_path = config["stemmer_path"]  # Get stopper path from configuration
    stemmer_expand_path = config["expand_docs"]  # Get tokens path from configuration
    
    with open(stemmer_path,'r') as file:
        content = json.load(file)
    
    
    
    new_stemmer = {}
    for id_doc,tokens in content.items():
        n_words = len(tokens)
        pos = 1
        new_stemmer[id_doc] = tokens
        new_token_list = []
        k = config["expand_factor"]
        for token in tokens:
            new_frequency = n_words / (pos * k)
            new_token_list.extend([token] * int(new_frequency))
            pos += 1
        
        new_stemmer[id_doc] += new_token_list
    
    with open(stemmer_expand_path,'w') as file:
        json.dump(new_stemmer,file)




if __name__ == "__main__":
    run(main)  # Run main function if script is executed directly
