import sys

from botocore.exceptions import ClientError

import logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

import time


from modules.S3Exceptions import S3BucketAlreadyExists

def check_create_bucket(s3_client,bucket):
    message = {}
    try:
        s3_client.head_bucket(Bucket=bucket)
        logger.info(f"{bucket} s3 bucket found")
        raise  S3BucketAlreadyExists("S3 bucket exist",499)
        sys.exit(1)   
       
    except ClientError as e:
        error_code = e.response['Error']['Code']
        logger.info(f"Error Code {error_code}")
        
        if error_code == '400' or error_code == '404':
            logger.info(f"Bucket {bucket} not found or you don't have access to it")
            

            try: 
                logger.info(f"Creating {bucket}")
                response = s3_client.create_bucket(
                Bucket=bucket,
                CreateBucketConfiguration={'LocationConstraint': 'us-east-2' }
                )
                logger.debug(f"Calling bucket_exists waiter: " + str(int(time.time())))
                s3_bucket_exists_waiter = s3_client.get_waiter('bucket_exists')
                s3_bucket_exists_waiter.wait(Bucket=bucket) 
                logger.info(f"Bucket at {response['Location']} created")
                logger.debug(f"Response: {response}")
                return response['Location']
            
            except ClientError as e:
                logger.info("Exception occurred: %s", f"Bucket {bucket} not created" ,str(e))
        else:
            logger.info("Exception occurred:", str(e))
        
def check_create_folder(s3_client,bucket,writers_dir):
    writers_dir_path = writers_dir + '/'
    try: 
        s3_client.head_object(Bucket=bucket,Key=writers_dir)
        logger.info(f"{writers_dir} exists")
    except ClientError as e:
        error_code = e.response.get("Error", {}).get("Code")
        if error_code == '404':
            logger.info(f"Bucket '{writers_dir_path}' does not exist in {bucket}.")
            try:
                response =  s3_client.put_object(
                Bucket=bucket,
                Key=writers_dir_path
                )
                logger.info(f"Calling object_exists waiter: " + str(time.time()))
                s3_object_exists_waiter = s3_client.get_waiter('object_exists')
                s3_object_exists_waiter.wait(Bucket=bucket,Key=writers_dir_path) 
                logger.info("object_exists complete")
                logger.debug(f"Response: {response}")
                logger.info(f"{writers_dir_path} prefix created in {bucket} bucket")
                return {'Bucket': bucket,'Folder': writers_dir_path  }
             

            except ClientError as e:
                prefix_error_code = e.response.get("Error", {}).get("Code")
                logger.error(f"Creating prefix {writers_dir} in {bucket} failed: {prefix_error_code} - {e}")
        elif error_code == '403':
            logger.error(f"Access denied for bucket '{bucket}'. Check permissions.")
        else:
            logger.error(f"An unexpected error occurred when heading bucket '{bucket}': {error_code} - {e}")
    except Exception as e:
        logger.critical(f"A non-Boto3 error occurred: {e}")
        

    
            
def check_folder_exists(s3_client,bucket,folder):
    try:
        s3_client.head_object(Bucket=bucket, Key=folder)
        logger.info(f"Key {folder} found in {bucket}")
        return True
    except ClientError as e:
        error_code = e.response.get("Error", {}).get("Code")
        if error_code == '404':
               logger.info(f"Key {folder} not found in {bucket}")
        else:
            logger.error(f"An unexpected error occurred when heading bucket {bucket}: {error_code}")
            raise
 

def purge_bucket(s3_client,bucket_name):
    try: 
        response = s3_client.list_objects_v2(Bucket=bucket_name)
        if 'Contents' in response:
            try: 
                objects_to_delete = [{'Key': obj['Key']} for obj in response['Contents']]
                s3_client.delete_objects(Bucket=bucket_name, Delete={'Objects': objects_to_delete})
                logger.info(f"Emptied {bucket_name}")
            except ClientError as e:
                  logger.error(f"An unexpected error occurred when deleting objects in  {bucket_name}: {e}")
    except ClientError as e:
        logger.error(f"An unexpected error occurred when listing objects in  {bucket_name}: {e}")
        
    try:
        response = s3_client.delete_bucket(Bucket=bucket_name)
        logger.info(f"Purged {bucket_name}")
    except ClientError as e:
        logger.error(f"An unexpected error occurred when deleting {bucket_name}: {e}")
