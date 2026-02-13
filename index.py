import json
import boto3

bedrock = boto3.client("bedrock-runtime", region_name="eu-north-1")

def lambda_handler(event, context):
    try:
        print("VERSION 3 - NOVA INPUTTEXT FORMAT")

        # Parse event safely
        if isinstance(event, dict):
            drift_summary = event
        else:
            drift_summary = json.loads(event)

        prompt_text = f"""
You are a Terraform drift analysis expert.

Analyze the following Terraform drift JSON and:
1. Classify risk level (LOW / MEDIUM / HIGH)
2. Explain what changed
3. Suggest remediation steps

Drift Data:
{json.dumps(drift_summary, indent=2)}
"""

        response = bedrock.invoke_model(
            modelId="arn:aws:bedrock:eu-north-1:206716568967:inference-profile/eu.amazon.nova-micro-v1:0",
            contentType="application/json",
            body=json.dumps({
                "messages": [
                    {
                        "role": "user",
                        "content": prompt_text
                    }
                ],
                "inferenceConfig": {
                    "maxTokens": 1000,
                    "temperature": 0.2
                }
            })
        )

        result = json.loads(response["body"].read().decode())

        print("Bedrock raw result:", result)

        return {
            "statusCode": 200,
            "analysis": result
        }

    except Exception as e:
        print("ERROR:", str(e))
        return {
            "statusCode": 500,
            "errorType": type(e).__name__,
            "errorMessage": str(e)
        }
