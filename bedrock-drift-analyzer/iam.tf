resource "aws_iam_role" "lambda_role" {
  name = "bedrock-drift-lambda-role"

  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [{
      Effect = "Allow"
      Principal = {
        Service = "lambda.amazonaws.com"
      }
      Action = "sts:AssumeRole"
    }]
  })
}

resource "aws_iam_policy" "bedrock_policy" {
  name = "bedrock-invoke-policy"

  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Effect = "Allow"
        Action = [
          "bedrock:InvokeModel"
        ]
        Resource = "*"
      }
    ]
  })
}

resource "aws_iam_role_policy_attachment" "bedrock_attach" {
  role       = aws_iam_role.lambda_role.name
  policy_arn = aws_iam_policy.bedrock_policy.arn
}

resource "aws_iam_role_policy_attachment" "logs_attach" {
  role       = aws_iam_role.lambda_role.name
  policy_arn = "arn:aws:iam::aws:policy/service-role/AWSLambdaBasicExecutionRole"
}
