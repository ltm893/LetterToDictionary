
import boto3
from botocore.exceptions import ClientError

client = boto3.client('s3')
bucket = 'ltm893-bag-writings'


try:
    client.head_bucket(Bucket=bucket)
except ClientError as e:
    if e.response['Error']['Code'] == '404':
        print("Bucket not found or you don't have access.")
        try: 
            client.create_bucket(
            Bucket=bucket,
            CreateBucketConfiguration={
            'LocationConstraint': 'us-east-2',
            }
        except ClientError as e:
            print(e)
)
    else:
        # Handle other potential ClientError exceptions
        print(f"An error occurred: {e}")