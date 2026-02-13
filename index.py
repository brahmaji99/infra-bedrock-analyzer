import json
import boto3

# Correct client for invoking models
bedrock = boto3.client('bedrock-runtime', region_name='eu-north-1')

def lambda_handler(event, context):
    """
    Lambda handler to send Terraform drift summary to Bedrock (Nova Micro)
    """
    try:
        # Load event payload
        if isinstance(event, dict):
            drift_summary = event
        else:
            drift_summary = json.loads(event)

        prompt_text = json.dumps(drift_summary, indent=2)

        # Bedrock now requires 'messages' key
        body_payload = {
            "messages": [
                {
                    "role": "user",
                    "content": [
                        {"type": "text", "text": prompt_text}
                    ]
                }
            ]
        }

        # Invoke model
        response = bedrock.invoke_model(
            modelId="arn:aws:bedrock:eu-north-1:206716568967:inference-profile/eu.amazon.nova-micro-v1:0",
            body=json.dumps(body_payload),
            contentType="application/json"
        )

        # Decode model response
        result = json.loads(response['body'].read().decode())

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
