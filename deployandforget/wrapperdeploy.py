import json
import os
import boto3

def updateCFStack(payload: str, stack_name: str) -> None:
    client = boto3.client('cloudformation')
    try:
        response = client.update_stack(
            StackName=stack_name,
            UsePreviousTemplate=True,
            Parameters=[
                {
                    'ParameterKey': 'ParamS3Key',
                    'ParameterValue': payload,
                    'UsePreviousValue': False,
                },
                {
                    'ParameterKey': 'ParamS3Bucket',
                    'UsePreviousValue': True,
                },
                {
                    'ParameterKey': 'cronexpression',
                    'UsePreviousValue': True,
                },
            ]
        )
        print(response['StackId'])
    except CloudFormation.Client.exceptions.InsufficientCapabilitiesException:
        print("Please check parameters passed")
    


def lambda_handler(event, context):
    STACK_NAME = os.environ['STACK_NAME']
    try:
        payload = event['Records']['s3']['key']
        if ".zip" in payload:
            updateCFStack(payload, STACK_NAME)
    except Exception as e:
        print("Issuse with s3 event", str(e))