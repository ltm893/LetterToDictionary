from modules.s3_infrastructure import check_create_bucket
from modules.s3_infrastructure import check_create_folder
from modules.s3_ops import put_file
from modules.person_letter_dictionary import load_exclude_set
from modules.person_letter_dictionary import load_words_text

from pathlib import Path
import boto3
s3_client = boto3.client('s3')


base_dir_path = Path(__file__).resolve().parent.parent
data_dir_path = base_dir_path / "data"
data_file_path = data_dir_path / "input" / "Series3Sub3E.txt"

config_dir_path = data_dir_path / "config"
exclude_file_path = config_dir_path / "exclude_words.txt"

s3_file_name = 'Washington1'
bucket_name = 'ltm893-bag-writings-220259-test'
writer_dir_name = 'Washington'
table_name = writer_dir_name + '_table'


if __name__ == "__main__":
    check_create_bucket(s3_client, bucket_name)
    # check_create_folder(bucket_name,writer_dir_name)
    # put_file(bucket_name,writer_dir_name,data_file_path,s3_file_name)
    # load_exclude_set(exclude_file_path)
    # load_words_text(data_file_path)
