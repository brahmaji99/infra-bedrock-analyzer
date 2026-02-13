import boto3
import json
import os

bedrock = boto3.client('bedrock', region_name='eu-north-1')

def lambda_handler(event, context):
    # Step 1: List all inference profiles
    profiles = bedrock.list_inference_profiles()['inferenceProfileSummaries']
    
    # Step 2: Filter active profiles in eu-north-1
    active_profiles = [
        p for p in profiles 
        if p['status'] == 'ACTIVE' and p['inferenceProfileArn'].startswith('arn:aws:bedrock:eu-north-1:')
    ]
    
    if not active_profiles:
        return {"error": "No active inference profiles in eu-north-1"}

    # Pick the first active profile
    profile_arn = active_profiles[0]['inferenceProfileArn']

    # Step 3: Invoke the model via the inference profile
    drift_summary = event  # assuming drift-summary.json is passed as Lambda event

    response = bedrock.invoke_model(
        modelId=profile_arn,
        contentType='application/json',
        accept='application/json',
        body=json.dumps(drift_summary)
    )

    return response
