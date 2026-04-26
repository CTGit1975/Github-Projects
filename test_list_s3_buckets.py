import boto3
import pytest

def list_s3_buckets():
    s3 = boto3.client('s3')
    response = s3.list_buckets()
    return [bucket['Name'] for bucket in response['Buckets']]

def test_list_s3_buckets():
    buckets = list_s3_buckets()
    assert isinstance(buckets, list)
    for bucket in buckets:
        assert isinstance(bucket, str)