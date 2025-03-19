'''
repo : https://github.com/openmarmot/smol_aws_engineer
email : andrew@openmarmot.com
notes : tool functions for complex aws boto3 sdk actions
'''

import boto3
from botocore.exceptions import ClientError
from smolagents import tool
from typing import List, Dict

@tool
def get_aws_ec2_instances() -> List[Dict[str, str]]:
    '''
        Retrieve a list of EC2 instances from all AWS regions.
    
    Returns:
        List[Dict[str, str]]: A list of dictionaries, each containing 'instance_id' and 'instance_name'
    '''
    # Create EC2 client to get regions first
    ec2_client = boto3.client('ec2')
    
    # Get all regions
    regions = [region['RegionName'] for region in ec2_client.describe_regions()['Regions']]
    
    # List to store all instances
    all_instances = []
    
    # Iterate through each region
    for region in regions:
        try:
            # Create region-specific EC2 resource
            ec2_resource = boto3.resource('ec2', region_name=region)
            
            # Get all instances in this region
            instances = ec2_resource.instances.all()
            
            # Process each instance
            for instance in instances:
                # Get instance name from tags (if it exists)
                instance_name = 'Unnamed'
                if instance.tags:
                    for tag in instance.tags:
                        if tag['Key'] == 'Name':
                            instance_name = tag['Value']
                            break
                
                # Create dictionary for this instance
                instance_info = {
                    'instance_id': instance.id,
                    'instance_name': instance_name
                }
                
                all_instances.append(instance_info)
                
        except ClientError as e:
            print(f"Error accessing region {region}: {str(e)}")
            continue
    
    return all_instances

