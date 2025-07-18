

import boto3
resource = boto3.resource('dynamodb', region_name='us-east-2')
client = boto3.client("dynamodb")

from ..operations.db_ops import exists_table


# from db_ops import exists_table

def create_dynamodb_table(table_name):
    try:
        table = resource.create_table(
            TableName=table_name,
            KeySchema=[
                {
                    'AttributeName': 'writer', 
                    'KeyType': 'HASH'
                }
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
                        'AttributeName': 'word',
                        'KeyType': 'HASH'
                    },
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
        print(f"Table '{table_name}' created successfully.")

    except Exception as e:
        print(f"Error creating table: {e}")
        
if __name__=="__main__": 
    table_name = "YourTableName"
    print("ya")
    #f not exists_table(client,table_name):
        
        #create_dynamodb_table( table_name)
        #pass

