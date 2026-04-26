#!/usr/bin/env python3
"""
Script to create an AWS S3 bucket
"""

import boto3
from botocore.exceptions import ClientError
import uuid


def create_s3_bucket(bucket_name=None, region='us-east-1'):
    """Create an S3 bucket and return bucket details"""

    # Generate a unique bucket name if not provided
    if not bucket_name:
        bucket_name = f"my-bucket-{uuid.uuid4().hex[:8]}"

    try:
        s3_client = boto3.client('s3', region_name=region)

        # Create bucket
        if region == 'us-east-1':
            # us-east-1 doesn't need LocationConstraint
            s3_client.create_bucket(Bucket=bucket_name)
        else:
            # Other regions need LocationConstraint
            s3_client.create_bucket(
                Bucket=bucket_name,
                CreateBucketConfiguration={'LocationConstraint': region}
            )

        # Get bucket information
        response = s3_client.head_bucket(Bucket=bucket_name)
        creation_time = response['ResponseMetadata']['HTTPHeaders']['date']

        return {
            'success': True,
            'bucket_name': bucket_name,
            'region': region,
            'arn': f"arn:aws:s3:::{bucket_name}",
            'creation_time': creation_time
        }

    except ClientError as e:
        error_code = e.response['Error']['Code']
        if error_code == 'BucketAlreadyOwnedByYou':
            return {
                'success': False,
                'error': 'BucketAlreadyOwnedByYou',
                'message': f"Bucket already exists: {bucket_name}"
            }
        elif error_code == 'BucketAlreadyExists':
            return {
                'success': False,
                'error': 'BucketAlreadyExists',
                'message': f"Bucket name is taken globally: {bucket_name}"
            }
        else:
            return {
                'success': False,
                'error': error_code,
                'message': str(e)
            }
    except Exception as e:
        return {
            'success': False,
            'error': 'UnexpectedError',
            'message': str(e)
        }


if __name__ == "__main__":
    # You can specify bucket name and region, or use defaults
    result = create_s3_bucket()
    if result['success']:
        print(f"Creating S3 bucket: {result['bucket_name']}")
        print(f"Region: {result['region']}")
        print("-" * 80)
        print(f"\n[SUCCESS] S3 bucket created successfully!\n")
        print(f"Bucket Name: {result['bucket_name']}")
        print(f"Region: {result['region']}")
        print(f"ARN: {result['arn']}")
        print(f"Creation Time: {result['creation_time']}")
        print("\n" + "=" * 80)
        print("S3 BUCKET CREATED")
        print("=" * 80)
        print(f"You can now use this bucket to store objects.")
        print(f"Visit: https://s3.console.aws.amazon.com/s3")
        print("=" * 80)
    else:
        print(f"Error: {result['message']}")
    # Example with custom name:
    # create_s3_bucket(bucket_name='my-custom-bucket-name', region='us-west-2')
