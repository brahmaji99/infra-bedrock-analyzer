resource "aws_lambda_function" "drift_analyzer" {
  function_name = "terraform-drift-bedrock-analyzer"
  role          = aws_iam_role.lambda_role.arn
  handler       = "index.lambda_handler"
  runtime       = "python3.11"
  timeout       = 60

  filename = "lambda.zip"

  environment {
    variables = {
      BEDROCK_MODEL_ID = var.bedrock_model_id
    }
  }
}
