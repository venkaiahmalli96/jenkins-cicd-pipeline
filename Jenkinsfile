pipeline {
    agent any

    environment {
        IMAGE_NAME     = "flask-cicd-app"
        CONTAINER_NAME = "flask-app"
        APP_PORT       = "5000"
        APP_VERSION    = "${BUILD_NUMBER}"
    }

    stages {

        stage('Checkout') {
            steps {
                echo '============================================'
                echo 'Stage 1: Checkout — Pulling latest code'
                echo '============================================'
                checkout scm
                sh 'ls -la'
            }
        }

        stage('Build Docker Image') {
            steps {
                echo '============================================'
                echo 'Stage 2: Build — Building Docker image'
                echo '============================================'
                sh '''
                    cd app
                    docker build \
                        --build-arg APP_VERSION=${APP_VERSION} \
                        -t ${IMAGE_NAME}:${APP_VERSION} \
                        -t ${IMAGE_NAME}:latest \
                        .
                    docker images | grep ${IMAGE_NAME}
                '''
            }
        }

        stage('Test') {
            steps {
                echo '============================================'
                echo 'Stage 3: Test — Running health check'
                echo '============================================'
                sh '''
                    docker run -d --name test-container -p 5001:5000 ${IMAGE_NAME}:${APP_VERSION}
                    sleep 5
                    curl -f http://localhost:5001/health && echo "Health check PASSED"
                    docker stop test-container
                    docker rm test-container
                '''
            }
        }

        stage('Deploy') {
            steps {
                echo '============================================'
                echo 'Stage 4: Deploy — Deploying new container'
                echo '============================================'
                sh '''
                    docker stop ${CONTAINER_NAME} 2>/dev/null || echo "No existing container"
                    docker rm ${CONTAINER_NAME} 2>/dev/null || echo "No existing container"
                    docker run -d \
                        --name ${CONTAINER_NAME} \
                        --restart unless-stopped \
                        -p ${APP_PORT}:5000 \
                        -e APP_VERSION=${APP_VERSION} \
                        ${IMAGE_NAME}:${APP_VERSION}
                    docker ps | grep ${CONTAINER_NAME}
                '''
            }
        }

        stage('Verify') {
            steps {
                echo '============================================'
                echo 'Stage 5: Verify — Confirming deployment'
                echo '============================================'
                sh '''
                    sleep 5
                    curl -f http://localhost:${APP_PORT}/health && echo "Deployment verified!"
                    curl -s http://localhost:${APP_PORT}/sysinfo | python3 -m json.tool
                '''
            }
        }

    }

    post {
        success {
            echo "BUILD SUCCESS — Flask app v${BUILD_NUMBER} deployed!"
        }
        failure {
            echo "BUILD FAILED — Check logs above"
            sh '''
                docker stop test-container 2>/dev/null || true
                docker rm test-container 2>/dev/null || true
            '''
        }
        always {
            echo "Pipeline finished — Build #${BUILD_NUMBER}"
            sh 'docker ps'
        }
    }
}
