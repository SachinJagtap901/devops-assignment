pipeline {
    agent any

    environment {
        DOCKERHUB_USERNAME = "sachinj6277"

        DEVOPS_IMAGE = "devops-api"
        HOROSCOPE_IMAGE = "horoscope-api"

        IMAGE_TAG = "${BUILD_NUMBER}"
    }

    stages {

        stage('Build DevOps API') {
            steps {
                echo 'Building DevOps API...'

                sh '''
                    python3 -m venv venv
                    . venv/bin/activate
                    pip install -r requirements.txt
                '''
            }
        }

        stage('Unit Test DevOps API') {
            steps {
                echo 'Running DevOps API unit tests...'

                sh '''
                    . venv/bin/activate
                    pytest
                '''
            }
        }

        stage('Build DevOps Docker Image') {
            steps {
                echo 'Building DevOps API Docker image...'

                sh '''
                    docker build \
                        -t ${DOCKERHUB_USERNAME}/${DEVOPS_IMAGE}:${IMAGE_TAG} \
                        .
                '''
            }
        }

        stage('Build Horoscope API') {
            steps {
                echo 'Building Horoscope API...'

                sh '''
                    python3 -m venv horoscope-venv
                    . horoscope-venv/bin/activate
                    pip install -r horoscope-api/requirements.txt
                '''
            }
        }

        stage('Unit Test Horoscope API') {
            steps {
                echo 'Running Horoscope API unit tests...'

                sh '''
                    . horoscope-venv/bin/activate
                    pytest horoscope-api/test_app.py
                '''
            }
        }

        stage('Build Horoscope Docker Image') {
            steps {
                echo 'Building Horoscope API Docker image...'

                sh '''
                    docker build \
                        -t ${DOCKERHUB_USERNAME}/${HOROSCOPE_IMAGE}:${IMAGE_TAG} \
                        horoscope-api
                '''
            }
        }

        stage('Push Images to Docker Hub') {
            steps {
                echo 'Pushing both images to Docker Hub...'

                withCredentials([
                    usernamePassword(
                        credentialsId: 'dockerhub',
                        usernameVariable: 'DOCKER_USERNAME',
                        passwordVariable: 'DOCKER_PASSWORD'
                    )
                ]) {
                    sh '''
                        echo "$DOCKER_PASSWORD" | docker login \
                            --username "$DOCKER_USERNAME" \
                            --password-stdin

                        docker push \
                            ${DOCKERHUB_USERNAME}/${DEVOPS_IMAGE}:${IMAGE_TAG}

                        docker push \
                            ${DOCKERHUB_USERNAME}/${HOROSCOPE_IMAGE}:${IMAGE_TAG}

                        docker logout
                    '''
                }
            }
        }

        stage('Deploy DevOps API') {
            steps {
                echo 'Deploying DevOps API to Kubernetes...'

                sh '''
                    kubectl set image deployment/devops-api \
                        devops-api=${DOCKERHUB_USERNAME}/${DEVOPS_IMAGE}:${IMAGE_TAG}

                    kubectl rollout status deployment/devops-api \
                        --timeout=120s
                '''
            }
        }

        stage('Deploy Horoscope API') {
            steps {
                echo 'Deploying Horoscope API to Kubernetes...'

                sh '''
                    kubectl set image deployment/horoscope-api \
                        horoscope-api=${DOCKERHUB_USERNAME}/${HOROSCOPE_IMAGE}:${IMAGE_TAG}

                    kubectl rollout status deployment/horoscope-api \
                        --timeout=120s
                '''
            }
        }

        stage('Verify Kubernetes') {
            steps {
                echo 'Verifying Kubernetes deployments...'

                sh '''
                    kubectl get deployments
                    kubectl get pods
                    kubectl get services

                    echo "DevOps API image:"
                    kubectl get deployment devops-api \
                        -o jsonpath='{.spec.template.spec.containers[0].image}'
                    echo

                    echo "Horoscope API image:"
                    kubectl get deployment horoscope-api \
                        -o jsonpath='{.spec.template.spec.containers[0].image}'
                    echo
                '''
            }
        }
    }

    post {
        success {
            echo 'Both applications built, tested, pushed, and deployed successfully!'
        }

        failure {
            echo 'Pipeline failed!'
        }
    }
}