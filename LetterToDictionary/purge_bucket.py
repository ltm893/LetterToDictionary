from modules.s3_infrastructure import purge_bucket
#from modules.s3_infrastructure import check_create_folder

import boto3
bucket_name = 'ltm893-bag-writings-220259-test'
s3_client = boto3.client('s3')

if __name__=="__main__":
    purge_bucket(s3_client,bucket_name)
    