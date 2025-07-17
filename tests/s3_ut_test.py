from modules.s3_infrastructure import check_create_folder
from modules.s3_infrastructure import check_create_bucket
from modules.s3_infrastructure import check_folder_exists
from modules.s3_infrastructure import purge_bucket
import unittest
import os
import sys

print(os.getcwd())
print(sys.path)


class S3T:
    test_bucket_name = 'ltm-893-bag-test-bucket-4438'
    test_folder_name = 'test-folder'


class TestS3MethodsTest(unittest.TestCase):

    def test_check_create_bucket(self):
        Location = check_create_bucket(S3T.test_bucket_name)
        self.assertEqual(
            Location, 'http://' + str(S3T.test_bucket_name) + '.s3.amazonaws.com/')


    def test_check_create_folder(self):
        if check_folder_exists(S3T.test_bucket_name,S3T.test_folder_name):
            response =  check_create_folder(S3T.test_bucket_name,S3T.test_folder_name)
            self.assertEqual(response['Bucket'], S3T.test_bucket_name)
            self.assertEqual(response['Folder'], S3T.test_folder_name)

    
        
    def test_upper(self):
        self.assertEqual('foo'.upper(), 'FOO')


    def test_isupper(self):
        self.assertTrue('FOO'.isupper())
        self.assertFalse('Foo'.isupper())


    def test_split(self):
        s = 'hello world'
        self.assertEqual(s.split(), ['hello', 'world'])
        # check that s.split fails when the separator is not a string
        with self.assertRaises(TypeError):
            s.split(2)
            
    @classmethod
    def tearDownClass(cls):
        purge_bucket(S3T.test_bucket_name)


if __name__ == '__main__':
    unittest.main()
