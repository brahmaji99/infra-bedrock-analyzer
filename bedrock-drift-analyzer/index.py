import json
import os
import boto3

bedrock = boto3.client("bedrock-runtime")

MODEL_ID = os.environ["BEDROCK_MODEL_ID"]

def lambda_handler(event, context):
    drift_json = json.dumps(event)

    prompt = f"""
You are a Terraform infrastructure risk analyst.

Analyze the following Terraform drift JSON and return ONLY valid JSON.

Rules:
- No markdown
- No explanations outside JSON

Return format:
{{
  "severity": "Low|Medium|High",
  "security_risk": "...",
  "cost_impact": "...",
  "operational_risk": "...",
  "recommended_action": "...",
  "auto_apply_safe": true|false
}}

Terraform Drift JSON:
{drift_json}
"""

    response = bedrock.invoke_model(
        modelId=MODEL_ID,
        contentType="application/json",
        accept="application/json",
        body=json.dumps({
            "messages": [
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            "max_tokens": 500
        })
    )

    result = json.loads(response["body"].read())

    return {
        "statusCode": 200,
        "analysis": result
    }
