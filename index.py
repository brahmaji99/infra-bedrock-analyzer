import json
import boto3

# ✅ Use the correct Bedrock client for runtime model invocation
bedrock = boto3.client('bedrock-runtime', region_name='eu-north-1')

def lambda_handler(event, context):
    """
    Lambda handler to send Terraform drift summary to Bedrock using Nova Micro.
    Returns the model's analysis of the drift.
    """
    try:
        # Load the JSON payload
        if isinstance(event, dict):
            drift_summary = event
        else:
            drift_summary = json.loads(event)

        # Convert the drift JSON to a readable string for the model
        prompt_text = json.dumps(drift_summary, indent=2)

        # Invoke Bedrock model (Nova Micro inference profile)
        response = bedrock.invoke_model(
            modelId="arn:aws:bedrock:eu-north-1:206716568967:inference-profile/eu.amazon.nova-micro-v1:0",
            body=json.dumps({"inputText": prompt_text}),  # only inputText is allowed
            contentType="application/json"
        )

        # Decode model response
        result = json.loads(response['body'].read().decode())

        # Return successful response
        return {
            "statusCode": 200,
            "body": result
        }

    except Exception as e:
        # Return error info so Jenkins can read it
        return {
            "statusCode": 500,
            "errorType": type(e).__name__,
            "errorMessage": str(e)
        }
