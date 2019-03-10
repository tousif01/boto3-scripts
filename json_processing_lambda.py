import json
import boto3

""" Refer the example.json for json format-
    {
        "Name": "Tousi",
        "RollNo": 3332,
        "Place": "Pune"
    }
    DynamoDB table was created with key = rollno
    the json file was uploaded to s3 using s3upload.py script
    permissions were granted to lambda using role json-processing-lambda-role
    cloudwatch logs contain all lambda execution logs
    use boto3 docs and json functions to load the data
    event is another imp aspect, you can print the event and see what all data does it contain
    also, the bucket name and json file name are taken from even and then the actual object is read using s3.get_object
    Region : us-east-2 (Ohio)
"""
def lambda_handler(event, context):
    s3 = boto3.client('s3')
    ddb = boto3.resource('dynamodb')
    bucket_name = event['Records'][0]['s3']['bucket']['name']
    file_name = event['Records'][0]['s3']['object']['key']
    print(bucket_name)
    print(file_name)
    json_object = s3.get_object(Bucket=bucket_name, Key=file_name)
    json_dict = json.loads(json_object['Body'].read())
    table = ddb.Table('employee')
    table.put_item(Item=json_dict)
    print("json successfully imported into db")
