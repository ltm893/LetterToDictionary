from infrastructure.create_s3 import purge_bucket
from infrastructure.create_s3 import check_create_folder


bucket_name = 'ltm893-bag-writings-220259-test'


if __name__=="__main__":
    purge_bucket(bucket_name)
    