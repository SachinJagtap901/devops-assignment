pipeline {
    agent any

    environment {
        IMAGE_NAME = "devops-api"
        IMAGE_TAG = "${BUILD_NUMBER}"
    }

    stages {

        stage('Build') {
            steps {
                echo 'Building application...'

                sh '''
                    python3 -m venv venv
                    . venv/bin/activate
                    pip install -r requirements.txt
                '''
            }
        }

        stage('Unit Test') {
            steps {
                echo 'Running unit tests...'

                sh '''
                    . venv/bin/activate
                    pytest
                '''
            }
        }

        stage('Docker Build') {
            steps {
                echo 'Building Docker image...'

                sh '''
                    docker build -t ${IMAGE_NAME}:${IMAGE_TAG} .
                '''
            }
        }

        stage('Push to Registry') {
            steps {
                echo 'ACR push will be configured next.'
            }
        }

        stage('Deploy to Kubernetes') {
            steps {
                echo 'AKS deployment will be configured next.'
            }
        }
    }

    post {
        success {
            echo 'Pipeline completed successfully!'
        }

        failure {
            echo 'Pipeline failed!'
        }
    }
}