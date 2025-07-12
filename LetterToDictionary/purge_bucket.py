from infrastructure.s3_ops import purge_bucket
from infrastructure.s3_ops import check_create_folder


bucket_name = 'ltm893-bag-writings-220259-test'


if __name__=="__main__":
    purge_bucket(bucket_name)
    