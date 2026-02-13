import json
import boto3
import os

# Bedrock client
bedrock = boto3.client('bedrock', region_name='eu-north-1')

def lambda_handler(event, context):
    try:
        # Read input payload from Lambda invoke (your Jenkins drift-summary.json)
        if isinstance(event, str):
            event = json.loads(event)
        
        # Construct prompt text from drift summary
        drift_summary = json.dumps(event, indent=2)
        prompt_text = f"Analyze the following Terraform drift report and summarize the changes:\n{drift_summary}"

        # Bedrock invocation using an inference profile
        # Replace modelId with the inferenceProfileArn for Nova Micro
        response = bedrock.invoke_model(
            modelId="arn:aws:bedrock:eu-north-1:206716568967:inference-profile/eu.amazon.nova-micro-v1:0",
            body=json.dumps({"inputText": prompt_text}),
            contentType="application/json"
        )

        # Read response from Bedrock
        response_body = response['body'].read().decode('utf-8')
        result = json.loads(response_body)

        # Return structured output
        return {
            "statusCode": 200,
            "modelResponse": result
        }

    except Exception as e:
        return {
            "statusCode": 500,
            "errorType": type(e).__name__,
            "errorMessage": str(e)
        }
