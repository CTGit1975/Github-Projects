#!/usr/bin/env python3
"""
Script to list all AWS EC2 instances across all regions
"""

import boto3
from botocore.exceptions import ClientError


def list_ec2_instances():
    """List all EC2 instances across all AWS regions"""

    # Create EC2 client
    ec2 = boto3.client('ec2')

    try:
        # Get all regions
        regions_response = ec2.describe_regions()
        regions = [region['RegionName'] for region in regions_response['Regions']]

        print(f"Checking {len(regions)} AWS regions for EC2 instances...\n")

        total_instances = 0

        # Iterate through each region
        for region in regions:
            print(f"Region: {region}")
            print("-" * 80)

            # Create EC2 resource for this region
            ec2_region = boto3.resource('ec2', region_name=region)

            # Get all instances
            instances = ec2_region.instances.all()

            region_count = 0
            for instance in instances:
                region_count += 1
                total_instances += 1

                print(f"  Instance ID: {instance.id}")
                print(f"  Instance Type: {instance.instance_type}")
                print(f"  State: {instance.state['Name']}")
                print(f"  Launch Time: {instance.launch_time}")

                # Get instance name from tags if available
                if instance.tags:
                    for tag in instance.tags:
                        if tag['Key'] == 'Name':
                            print(f"  Name: {tag['Value']}")

                # Get public and private IPs
                if instance.public_ip_address:
                    print(f"  Public IP: {instance.public_ip_address}")
                if instance.private_ip_address:
                    print(f"  Private IP: {instance.private_ip_address}")

                print()

            if region_count == 0:
                print("  No instances found\n")
            else:
                print(f"  Total in {region}: {region_count}\n")

        print("=" * 80)
        print(f"Total EC2 instances found: {total_instances}")

    except ClientError as e:
        print(f"Error: {e}")
    except Exception as e:
        print(f"Unexpected error: {e}")


if __name__ == "__main__":
    list_ec2_instances()
