import unittest
import os
import sys

print(os.getcwd())
print(sys.path)

from infrastructure.create_s3 import check_create_bucket

class TestS3MethodsTest(unittest.TestCase):
    def test_create_bucket(self):
        Location = check_create_bucket('ltm-893-test-bucket-123')
        self.assertEqual(Location, 'http://ltm-893-test-bucket-123.s3.amazonaws.com/')

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

if __name__ == '__main__':
    unittest.main()