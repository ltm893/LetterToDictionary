
import boto3
from botocore.exceptions import ClientError

import logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

import requests

text_file = './input/Series3Sub3E.txt'
text_file = './input/test_input.txt'
word_dict = {}
exclude_file = 'config/exclude_words.txt'

exclude_set = set()
free_word_dictionary_url ='https://api.dictionaryapi.dev/api/v2/entries/en/'


client = boto3.client('s3')
bucket_name = 'ltm893-bag-writings'
writer_dir_name = 'Washington'


def check_create_bucket(bucket):
    message = {}
    try:
        client.head_bucket(Bucket=bucket)
        logger.info(f"{bucket} s3 bucket found")
           
       
    except ClientError as e:
        if e.response['Error']['Code'] == '404':
            logger.info(f"Bucket {bucket} not found or you don't have access. Creattin {bucket}")

            try: 
                response = client.create_bucket(
                Bucket=bucket,
                CreateBucketConfiguration={'LocationConstraint': 'us-east-2' }
                )
                print(response['Location'])
                logger.info(f"Response: {response}")
                return response['Location']
            
            except ClientError as e:
                logger.info("Exception occurred: %s", f"Bucket {bucket} not created" ,str(e))
        else:
            logger.info("Exception occurred:", str(e))
        
def check_create_prefix(bucket,writers_dir):
    try: 
        client.head_object(Bucket=bucket,Key=writers_dir)
        logger.info(f"{writers_dir} exists")
    except ClientError as e:
        error_code = e.response.get("Error", {}).get("Code")
        if error_code == '404':
            logger.info(f"Bucket '{writers_dir}' does not exist.")
            try:
                client.put_object(
                Bucket=bucket,
                Key=writers_dir
            )
            except ClientError as e:
                prefix_error_code = e.response.get("Error", {}).get("Code")
                logger.error(f"Creating prefix {writers_dir} in {bucket} failed: {prefix_error_code} - {e}")
        elif error_code == '403':
            logger.error(f"Access denied for bucket '{bucket}'. Check permissions.")
        else:
            logger.error(f"An unexpected error occurred when heading bucket '{bucket}': {error_code} - {e}")
    except Exception as e:
        logger.critical(f"A non-Boto3 error occurred: {e}")


def load_exlude_set():
    
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
    check_create_bucket(bucket_name)
    check_create_prefix(bucket_name,writer_dir_name)
    load_exlude_set()
    load_words_text()