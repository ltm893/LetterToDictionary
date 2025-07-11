

import logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


import boto3
from botocore.exceptions import ClientError
from boto3.dynamodb.conditions import Key

table_name = 'WashDict'

dynamodb = boto3.resource('dynamodb')
dynamodb_client = boto3.client("dynamodb")
dyn_table = dynamodb.Table(table_name)


def exists_table(client,table):
    try :
        response = client.list_tables()
        return table.name in response['TableNames']
     
    except dynamodb.exceptions.ResourceNotFoundException:
        print("The specified DynamoDB table or item does not exist.")
    except dynamodb.exceptions.ProvisionedThroughputExceededException:
        print("Provisioned throughput exceeded. Consider increasing throughput or implementing retries.")
    except ClientError as e:  # Catch any other ClientErrors
        print(f"An unexpected DynamoDB error occurred: {e}")
        
def exists_key(client,table,index,value): 
    try : 
        response = table.query(Select='COUNT',KeyConditionExpression=Key(index).eq(value))
        if response['Count'] > 0 :
            return True
        
    except ClientError as e:  # Catch any other ClientErrors
        print(f"An unexpected DynamoDB error occurred: {e}")
        
        

if __name__=="__main__":
    if exists_table(dynamodb_client,dyn_table):
        if(exists_key(dynamodb_client,dyn_table,'word','respectable'))