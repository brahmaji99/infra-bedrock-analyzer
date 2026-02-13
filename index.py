import json
import boto3
import os

# Initialize Bedrock client
bedrock = boto3.client('bedrock', region_name='eu-north-1')

def lambda_handler(event, context):
    """
    Lambda handler to send Terraform drift summary to Bedrock using Nova Micro.
    """
    try:
        # Read the drift JSON from Lambda payload
        if isinstance(event, dict):
            drift_summary = event
        else:
            drift_summary = json.loads(event)

        # Convert JSON to a readable string for the model
        prompt_text = json.dumps(drift_summary, indent=2)

        # Bedrock invocation
        response = bedrock.invoke_model(
            modelId="arn:aws:bedrock:eu-north-1:206716568967:inference-profile/eu.amazon.nova-micro-v1:0",
            body=json.dumps({"inputText": prompt_text}),
            contentType="application/json"
        )

        # Read and decode the model response
        result = json.loads(response['body'].read().decode())

        # Return the result
        return {
            "statusCode": 200,
            "body": result
        }

    except Exception as e:
        return {
            "statusCode": 500,
            "errorType": type(e).__name__,
            "errorMessage": str(e)
        }
