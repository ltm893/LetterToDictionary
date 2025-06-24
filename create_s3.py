
import boto3
from botocore.exceptions import ClientError

import logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


client = boto3.client('s3')
bucket = 'ltm893-bag-writings'


def check_create_bucket(bucket):
    message = {}
    try:
        client.head_bucket(Bucket=bucket)
        logger.info(f"{bucket} s3 bucket found")
           
       
    except ClientError as e:
        if e.response['Error']['Code'] == '404':
            logger.info(f"Bucket {bucket} not found or you don't have access. Creattin {bucket}")

            try: 
                client.create_bucket(
                Bucket=bucket,
                CreateBucketConfiguration={'LocationConstraint': 'us-east-2' }
                )
                logger.info(f"{bucket} created")
            except ClientError as e:
                logger.info("Exception occurred: %s", f"Bucket {bucket} not created" ,str(e))
        else:
            logger.info("Exception occurred:", str(e))
        
def check_create_prefix(bucket,writers_dir):
    try: 
        client.head_object(Bucket=bucket,Key=writers_dir)
        logger.info(f"{writers_dir} exists")
    except ClientError as e:
        if e.response['Error']['Code'] == '404':
           # logging.exception(f"An error occurred during division: {e}")
            logger.info(f"{e}")


               


if __name__=="__main__":
    check_create_bucket(bucket)
    check_create_prefix(bucket,'Washington')