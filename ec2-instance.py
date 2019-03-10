import boto3
from botocore.exceptions import ClientError
import logging

def describe_ec2_instance(instance_id):
    ec2 = boto3.client('ec2')
    response = ec2.describe_instances()
    return response

def create_ec2_instance(image_id, instance_type, keypair_name):
    ec2_client = boto3.client('ec2',region_name='us-east-1')
    try:
        response = ec2_client.run_instances(ImageId=image_id, InstanceType=instance_type, KeyName=keypair_name, MinCount=1, MaxCount=1)

    except ClientError as e:
        logging.error(e)
        return None

    return response['Instances'][0]


def main():
    image_id = "ami-02da3a138888ced85"
    instance_type = "t2.micro"
    keypair_name = "virginia-boto3"


    # Set up logging
    logging.basicConfig(level=logging.DEBUG,format='%(levelname)s: %(asctime)s: %(message)s')

    instance_created = create_ec2_instance(image_id, instance_type, keypair_name)
    if instance_created is not None:
        logging.info('Launched EC2 Instance: ' + str({instance_created["InstanceId"]}))
        logging.info('    VPC ID: ' + str({instance_created["VpcId"]}))
        logging.info('    Private IP Address: '+str({instance_created["PrivateIpAddress"]}))
        logging.info('    Current State: ' + str({instance_created["State"]["Name"]}))


if __name__ == '__main__':
    main()

