import logging
logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

import boto3

from ..operations.db_ops import exists_table


def create_writer_dynamodb_table_if_not_exists(dynamo_client,dynamo_resource,table_name):
    logger.info("called")
    try:
        if not exists_table(dynamo_client,dynamo_resource,table_name) :
            logger.info(f"Creating Table {table_name}")
            table = dynamo_resource.create_table(
            TableName=table_name,
            KeySchema=[
                {
                    'AttributeName': 'word', 
                    'KeyType': 'HASH'
                },
                
                
            ],
            AttributeDefinitions=[
                {
                    'AttributeName': 'writer',
                    'AttributeType': 'S' 
                },
                {
                    'AttributeName': 'word',
                    'AttributeType': 'S' 
                }
            ],     
            # Define provisioned throughput (important for production environments)
            ProvisionedThroughput={
                'ReadCapacityUnits': 2,
                'WriteCapacityUnits': 2
            },
            GlobalSecondaryIndexes=[
            {
                'IndexName': 'word_index',
                'KeySchema': [
                    {
                        'AttributeName': 'writer',
                        'KeyType': 'HASH'
                    }
                ],
                'Projection': {
                    'ProjectionType': 'KEYS_ONLY',
                },
                'ProvisionedThroughput': {
                    'ReadCapacityUnits': 2,
                    'WriteCapacityUnits': 2
                }
            },
        ],
        )

        # Wait for the table to be created
            table.meta.client.get_waiter('table_exists').wait(TableName=table_name)
            logger.info(f"{table_name} created successfully.")

    except Exception as e:
        print(f"Error creating table: {e}")
        
if __name__=="__main__": 
    table_name = "YourTableName"
    print("ya")
    #f not exists_table(client,table_name):
        
        #create_dynamodb_table( table_name)
        #pass

