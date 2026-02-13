import json
import boto3

# Initialize Bedrock client
bedrock = boto3.client("bedrock", region_name="eu-north-1")

def lambda_handler(event, context):
    """
    Lambda handler to send Terraform drift summary to Bedrock using Nova Micro.
    Cleans the payload to avoid any invalid keys (like max_tokens).
    """
    try:
        # Parse event payload
        if isinstance(event, dict):
            drift_summary = event
        else:
            drift_summary = json.loads(event)

        # Convert JSON to string for model prompt
        prompt_text = json.dumps(drift_summary, indent=2)

        # Construct a clean payload — only allowed keys
        payload = {
            "inputText": prompt_text
        }

        # Invoke Bedrock model (Nova Micro inference profile)
        response = bedrock.invoke_model(
            modelId="arn:aws:bedrock:eu-north-1:206716568967:inference-profile/eu.amazon.nova-micro-v1:0",
            body=json.dumps(payload),
            contentType="application/json"
        )

        # Read and decode the model response
        result = json.loads(response["body"].read().decode())

        return {
            "statusCode": 200,
            "body": result
        }

    except Exception as e:
        # Catch and return any errors
        return {
            "statusCode": 500,
            "errorType": type(e).__name__,
            "errorMessage": str(e)
        }
