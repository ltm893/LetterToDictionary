import sys
import boto3
from botocore.exceptions import ClientError

import logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

import requests
import time


from infrastructure.S3Exceptions import S3BucketAlreadyExists


# text_file = './input/Series3Sub3E.txt'
# text_file = './input/test_input.txt'
word_dict = {}
# exclude_file = 'config/exclude_words.txt'

exclude_set = set()
free_word_dictionary_url ='https://api.dictionaryapi.dev/api/v2/entries/en/'


client = boto3.client('s3')
# resource  = boto3.resource('s3')
# bucket_name = 'ltm893-bag-writings-999'
# writer_dir_name = 'Washington'



def check_create_bucket(bucket):
    message = {}
    try:
        client.head_bucket(Bucket=bucket)
        logger.info(f"{bucket} s3 bucket found")
        raise  S3BucketAlreadyExists("S3 bucket exist",499)
        sys.exit(1)   
       
    except ClientError as e:
        if e.response['Error']['Code'] == '404':
            logger.info(f"Bucket {bucket} not found or you don't have access. Created {bucket}")

            try: 
                response = client.create_bucket(
                Bucket=bucket,
                CreateBucketConfiguration={'LocationConstraint': 'us-east-2' }
                )
                logger.info(f"Calling bucket_exists waiter: " + str(time.time()))
                s3_bucket_exists_waiter = client.get_waiter('bucket_exists')
                s3_bucket_exists_waiter.wait(Bucket=bucket) 
                logger.info("Bucket_exists complete")
                logger.info(response['Location'])
                logger.debug(f"Response: {response}")
                return response['Location']
            
            except ClientError as e:
                logger.info("Exception occurred: %s", f"Bucket {bucket} not created" ,str(e))
        else:
            logger.info("Exception occurred:", str(e))
        
def check_create_folder(bucket,writers_dir):
    try: 
        client.head_object(Bucket=bucket,Key=writers_dir)
        logger.info(f"{writers_dir} exists")
    except ClientError as e:
        error_code = e.response.get("Error", {}).get("Code")
        if error_code == '404':
            logger.info(f"Bucket '{writers_dir}' does not exist in {bucket}.")
            try:
                response =  client.put_object(
                Bucket=bucket,
                Key=writers_dir
                )
                logger.info(f"Calling object_exists waiter: " + str(time.time()))
                s3_object_exists_waiter = client.get_waiter('object_exists')
                s3_object_exists_waiter.wait(Bucket=bucket,Key=writers_dir) 
                logger.info("object_exists complete")
                logger.debug(f"Response: {response}")
                logger.info(f"{writers_dir} prefix created in {bucket} bucket")
                return {'Bucket': bucket,'Folder': writers_dir  }
             

            except ClientError as e:
                prefix_error_code = e.response.get("Error", {}).get("Code")
                logger.error(f"Creating prefix {writers_dir} in {bucket} failed: {prefix_error_code} - {e}")
        elif error_code == '403':
            logger.error(f"Access denied for bucket '{bucket}'. Check permissions.")
        else:
            logger.error(f"An unexpected error occurred when heading bucket '{bucket}': {error_code} - {e}")
    except Exception as e:
        logger.critical(f"A non-Boto3 error occurred: {e}")
        
        
def check_folder_exists(bucket,folder):
    try:
        client.head_object(Bucket=bucket, Key=folder)
        logger.info(f"Key {folder} found in {bucket}")
        return True
    except ClientError as e:
        error_code = e.response.get("Error", {}).get("Code")
        if error_code == '404':
               logger.info(f"Key {folder} not found in {bucket}")
        else:
            logger.error(f"An unexpected error occurred when heading bucket {bucket}: {error_code}")
            raise
 

def purge_bucket(bucket_name):
    try: 
        response = client.list_objects_v2(Bucket=bucket_name)
        if 'Contents' in response:
            try: 
                objects_to_delete = [{'Key': obj['Key']} for obj in response['Contents']]
                client.delete_objects(Bucket=bucket_name, Delete={'Objects': objects_to_delete})
                logger.info(f"Emptied {bucket_name}")
            except ClientError as e:
                  logger.error(f"An unexpected error occurred when deleting objects in  {bucket_name}: {e}")
    except ClientError as e:
        logger.error(f"An unexpected error occurred when listing objects in  {bucket_name}: {e}")
        
    try:
        response = client.delete_bucket(Bucket=bucket_name)
        logger.info(f"Purged {bucket_name}")
    except ClientError as e:
        logger.error(f"An unexpected error occurred when deleting {bucket_name}: {e}")
