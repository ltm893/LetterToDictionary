import boto3
from botocore.exceptions import ClientError

import logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

import time


#from modules.S3Exceptions import S3BucketAlreadyExists
from .s3_infrastructure import check_folder_exists



def put_file(s3_client,bucket,writers_dir,local_file,s3_file_name):
    if check_folder_exists(bucket,writers_dir + '/') :
        try:
            with open(local_file, 'rb') as f:
                response = s3_client.put_object(
                Bucket=bucket,
                Body=f,
                Key=writers_dir + '/' + s3_file_name,
                ServerSideEncryption='AES256'
                )
                logger.info(response)
        except ClientError as e:
                prefix_error_code = e.response.get("Error", {}).get("Code")
                logger.error(f"Uploading {s3_file_name} in {bucket} failed: {prefix_error_code} - {e}")
        
        
    else :
        logger.info("Folder path does not exist, create path")