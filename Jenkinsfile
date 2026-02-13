pipeline {
    agent any

    environment {
        TF_IN_AUTOMATION = "true"
        TF_INPUT         = "false"
        AWS_REGION       = "eu-north-1"
    }

    options {
        timestamps()
    }

    stages {

        stage('Checkout') {
            steps {
                checkout scm
            }
        }

        stage('Package Lambda') {
            steps {
                sh '''
                echo "📦 Packaging Lambda function"
                zip -r lambda.zip index.py
                '''
            }
        }

        stage('Terraform Init') {
            steps {
                sh '''
                terraform init -upgrade
                '''
            }
        }

        stage('Terraform Validate') {
            steps {
                sh '''
                terraform validate
                '''
            }
        }

        stage('Terraform Plan') {
            steps {
                sh '''
                terraform plan \
                  -out=tfplan \
                  -var="region=${AWS_REGION}"
                '''
            }
        }

        stage('Terraform Apply') {
            
            steps {
                
                sh '''
                terraform apply -auto-approve tfplan
                '''
            }
        }
    }

    post {
        success {
            echo "✅ Bedrock drift analyzer deployed successfully"
        }
        failure {
            echo "❌ Terraform deployment failed"
        }
    }
}
