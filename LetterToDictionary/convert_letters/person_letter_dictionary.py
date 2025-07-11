import requests

text_file = './input/Series3Sub3E.txt'
text_file = './input/test_input.txt'
word_dict = {}
exclude_file = 'config/exclude_words.txt'
#print(exclude_file)
exclude_set = set()
free_word_dictionary_url ='https://api.dictionaryapi.dev/api/v2/entries/en/'

def load_exclude_set(exclude_set):
    
    with open(exclude_file, 'r') as file:
        for line in file:
            clean_line = line.strip()
            exclude_set.add(clean_line.lower())


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
    print(response.status_code) 
    print(response.text)

def load_words_text():
    with open(text_file, 'r') as file:
        for line in file:
            clean_line = line.strip()
            
            for item in clean_line.split() :
                word = item.lower()
                word = get_alphabet_characters(word)
                if word not in exclude_set:
                    word_dict[word] = call_free_dict_url(word) 

    words = word_dict.keys()
    print(len(words))
    string_representation = ", ".join(str(item) for item in sorted(words))
    print(string_representation)



if __name__=="__main__":
    load_exclude_set()
    load_words_text()

  