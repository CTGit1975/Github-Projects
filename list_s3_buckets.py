#!/usr/bin/env python3
"""
Script to list all AWS S3 buckets
"""

import boto3
from botocore.exceptions import ClientError


def list_s3_buckets():
    """List all S3 buckets in the AWS account"""

    try:
        s3_client = boto3.client('s3')

        print("Listing all S3 buckets...")
        print("=" * 80)

        # List all buckets
        response = s3_client.list_buckets()
        buckets = response['Buckets']

        if not buckets:
            print("No S3 buckets found in your account.")
            return

        print(f"Found {len(buckets)} bucket(s):\n")

        for bucket in buckets:
            bucket_name = bucket['Name']
            creation_date = bucket['CreationDate']

            print(f"Bucket Name: {bucket_name}")
            print(f"Created: {creation_date}")

            # Get bucket location
            try:
                location_response = s3_client.get_bucket_location(Bucket=bucket_name)
                region = location_response['LocationConstraint'] or 'us-east-1'
                print(f"Region: {region}")
            except ClientError as e:
                print(f"Region: Unable to determine ({e})")

            # Get bucket size (count of objects)
            try:
                objects_response = s3_client.list_objects_v2(Bucket=bucket_name)
                object_count = objects_response.get('KeyCount', 0)
                print(f"Objects: {object_count}")
            except ClientError:
                print(f"Objects: Unable to count")

            print("-" * 80)

        print(f"\nTotal buckets: {len(buckets)}")

    except ClientError as e:
        print(f"Error: {e}")
    except Exception as e:
        print(f"Unexpected error: {e}")


if __name__ == "__main__":
    list_s3_buckets()
