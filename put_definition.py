import boto3
from botocore.exceptions import ClientError
import yaml
import uuid

unique_id = uuid.uuid4()
unique_id_string = str(unique_id)

client = boto3.client('imagebuilder')

component_data = {
    'name': 'DnfInstalls',
    'schemaVersion': '1.0',
    'phases': [
        {
            'name': 'build',
            'steps': [
                {
                    'name': 'InstallPython',
                    'action': 'ExecuteBash',
                    'inputs': {
                        'commands': [
                            'dnf install python3.11 python3.11-pip',
                            'cd /usr/bin',
                            'ln -s python3.11 python'
                        ]
                    }
                }
            ]
        },
        {
            'name': 'test',
            'steps': [
                {
                    'name': 'TestDnfInstalls',
                    'action': 'ExecuteBash',
                    'inputs': {
                        'commands': [
                            'python --version'
                        ]
                    }
                }
            ]
        }
    ]
}

try:
    response = client.create_component(
        name='BagInstall',
        semanticVersion='1.1.1',
        platform='Linux',
        supportedOsVersions=['Amazon Linux 2'],
        data=yaml.dump(component_data),
        # kmsKeyId='arn:aws:kms:your-region:your-account-id:key/your-kms-key-id',  # Replace with your KMS key ID
        tags={'example': 'true'},
        clientToken=unique_id_string # Replace with a unique token
    )
    #print(yaml.dump(component_data))
    print(response)

except Exception as e:
    print(e)