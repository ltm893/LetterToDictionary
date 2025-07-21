from .db_ops import put_obj

import requests
import time
import json
 
text_file = './input/Series3Sub3E.txt'
text_file = './input/test_input.txt'
word_dict = {}
#exclude_file = 'config/exclude_words.txt'
#print(exclude_file)

free_word_dictionary_url ='https://api.dictionaryapi.dev/api/v2/entries/en/'

def load_exclude_set(exclude_file):
    exclude_set = set()
    with open(exclude_file, 'r') as file:
        for line in file:
            clean_line = line.strip()
            exclude_set.add(clean_line.lower())

    return exclude_set

def get_alphabet_characters(input_string):
    result = ""
    for char in input_string:
        if char.isalpha():
            result += char
    return result

def call_free_dict_url(word):
    url = free_word_dictionary_url  + word
    print(url)
    response = requests.get(url) 
    time.sleep(5)
    if response.status_code == 200:
        return json.loads(response.text)
    else:
        return None

def load_words_text(text_file,exclude_set,writer,dynamo_resource, table_name,):
    with open(text_file, 'r') as file:
        for line in file:
            clean_line = line.strip()
            
            for item in clean_line.split() :
                word = item.lower()
                word = get_alphabet_characters(word)
                if word not in exclude_set and len(word) > 1:
                    word_dict = call_free_dict_url(word) 
                    if word_dict is not None : 
                        
                        for w in word_dict:
                            wr = {"writer": writer}
                            w.update(wr)
                            for k in ('sourceUrls','license','phonetic','phonetics'):
                                if k in w :
                                    del w[k]
                            obj = (w)
                            json_obj = json.dumps(obj, indent=4)
                            print(json_obj)  
                            put_obj(dynamo_resource, table_name, w)
    



if __name__=="__main__":
    load_exclude_set()
    load_words_text()

  