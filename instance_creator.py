import argparse
import os
import time


import googleapiclient.discovery
from six.moves import input

compute = googleapiclient.discovery.build('compute', 'v1')


def list_instances(compute, project, zone):
    result = compute.instances().list(project=project, zone=zone).execute()
    return result['items'] if 'items' in result else None

x = list_instances(compute,'newcloudproject-353304' ,'europe-west2-a')
print(x)

def create_instance(compute, project, zone, name, bucket):
    # Get the latest Debian Jessie image.
    image_response = compute.images().getFromFamily(
        project='debian-cloud', family='debian-9').execute()
    source_disk_image = image_response['selfLink']

    machine_type = "zones/%s/machineTypes/n1-standard-1" % zone

    config = {
        'name': name,
        'machineType': machine_type,


        'disks': [
            {
                'boot': True,
                'autoDelete': True,
                'initializeParams': {
                    'sourceImage': source_disk_image,
                }
            }
        ],


        'networkInterfaces': [{
            'network': 'global/networks/default',
            'accessConfigs': [
                {'type': 'ONE_TO_ONE_NAT', 'name': 'External NAT'}
            ]
        }],


        'serviceAccounts': [{
            'email': 'default',
            'scopes': [
                'https://www.googleapis.com/auth/devstorage.read_write',
                'https://www.googleapis.com/auth/logging.write'
            ]
        }],

        # Metadata is readable from the instance and allows you to
        # pass configuration from deployment scripts to instances.
        'metadata': {

        }
    }

    return compute.instances().insert(
        project=project,
        zone=zone,
        body=config).execute()

create_instance(compute,'newcloudproject-353304' ,'europe-west2-a', 'pyvm','pybucket')