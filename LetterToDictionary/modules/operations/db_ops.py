

from boto3.dynamodb.conditions import Key
from botocore.exceptions import ClientError
import boto3
import logging
logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


def exists_table(dynamo_client, dynamo_resource, table_name):
    logger.info(f"Checking for {table_name} table existence")
    try:
        response = dynamo_client.list_tables()
        print(response)
        if not response['TableNames']:
            logger.info('No Tables found')
            return False
        if table_name in response['TableNames']:
            logger.info(f"Table {table_name} exists")
            return True
     

    except dynamo_resource.exceptions.ResourceNotFoundException:
        logger.info(f"DynamoDB {table_name} table does not exist.")
        return False
    except dynamo_resource.exceptions.ProvisionedThroughputExceededException:
        logger.warn(
            "Provisioned throughput exceeded. Consider increasing throughput or implementing retries.")
    except ClientError as e:  # Catch any other ClientErrors
        logger.error(f"An unexpected DynamoDB error occurred: {e}")
        
def put_obj(dynamo_resource, table_name, word_dict):
    logger.info(f"Putting json object into {table_name} table")
    
    try:
        table = dynamo_resource.Table(table_name)
        response = table.put_item(Item=word_dict)
    except ClientError as e:  # Catch  ClientErrors
        logger.error(f"Put Item error occurred: {e}")





