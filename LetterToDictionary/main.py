from infrastructure.create_s3 import check_create_bucket
from infrastructure.create_s3 import check_create_folder


bucket_name = 'ltm893-bag-writings-220259-test'
writer_dir_name = 'Washington'

if __name__=="__main__":
    check_create_bucket(bucket_name)
    check_create_folder(bucket_name,writer_dir_name)