from modules.infrastructure.s3 import check_create_bucket
from modules.infrastructure.s3 import check_create_folder
from modules.operations.s3_ops import put_file
from modules.operations.person_letter_dictionary import load_exclude_set
from modules.operations.person_letter_dictionary import load_words_text
from modules.infrastructure.dynamodb_ops import create_writer_dynamodb_table_if_not_exists

from pathlib import Path
import boto3

region_name = 'us-east-2'
s3_client = boto3.client('s3')
dynamo_client = boto3.client("dynamodb",region_name)
dynamo_resource = boto3.resource('dynamodb', region_name)

base_dir_path = Path(__file__).resolve().parent.parent
data_dir_path = base_dir_path / "data"
data_file_path = data_dir_path / "input" / "Series3Sub3E.txt"

config_dir_path = data_dir_path / "config"
exclude_file_path = config_dir_path / "exclude_words.txt"


bucket_name = 'ltm893-bag-writings-220259-test'
writer = 'Washington'
s3_file_name = writer + '_writings'
writer_dir_name =  writer
table_name = writer + '_table'


if __name__ == "__main__":
    check_create_bucket(s3_client, bucket_name)
    check_create_folder(s3_client,bucket_name,writer_dir_name)
    create_writer_dynamodb_table_if_not_exists(dynamo_client,dynamo_resource,table_name)
    put_file(s3_client,bucket_name,writer_dir_name,data_file_path,s3_file_name)
    exclude_set = load_exclude_set(exclude_file_path)
    load_words_text(data_file_path, exclude_set,writer,dynamo_resource, table_name)
    
   
