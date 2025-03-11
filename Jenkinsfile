pipeline {
    agent any

    environment {
        DOCKER_HUB_CREDENTIAL_ID = 'mlops-jenkins-dockerhub-token'
        DOCKERHUB_REGISTRY = 'https://registry.hub.docker.com'
        DOCKERHUB_REPOSITORY = 'usmankhan555/mlopsapp'
    }

    stages {
        stage('Setup System Dependencies') {
            steps {
                echo "🔧 Setting up system dependencies..."
                sh 'sudo apt-get update && sudo apt-get install -y libgl1-mesa-glx libglib2.0-0'
            }
        }

        stage('Cloning Git Repository') {
            steps {
                echo "📥 Cloning repository..."
                checkout([
                    $class: 'GitSCM', 
                    branches: [[name: '*/main']], 
                    userRemoteConfigs: [[
                        url: 'https://github.com/UsmanKhan555/MLOps-Recommendation_System.git',  
                        credentialsId: 'mlops-git-token'
                    ]]
                ])
            }
        }

        stage('Install Dependencies') {
            steps {
                echo "📦 Installing dependencies..."
                sh "python -m pip install --upgrade pip --break-system-packages"
                sh "python -m pip install --break-system-packages -r requirements.txt"
            }
        }

        stage('Train Model') {
            steps {
                script {
                    echo "🎯 Training model..."
                    try {
                        sh 'python src/model.py'
                        echo "✅ Model training completed successfully!"
                    } catch (Exception e) {
                        echo "❌ Model training failed!"
                        error "Stopping pipeline due to training failure"
                    }
                }
            }
        }

        stage('Evaluate Model') {
            steps {
                script {
                    echo "🧪 Running model evaluation..."
                    try {
                        sh 'pytest src/test.py --junitxml=results/test-results.xml'
                        echo "✅ Model evaluation completed successfully!"
                    } catch (Exception e) {
                        echo "❌ Model evaluation failed!"
                        error "Stopping pipeline due to evaluation failure"
                    }
                }
            }
            post {
                always {
                    junit 'results/test-results.xml'
                }
            }
        }

        stage('Docker Build') {
            steps {
                echo "🐳 Building Docker image..."
                script {
                    dockerImage = docker.build("${DOCKERHUB_REPOSITORY}:latest")
                }
            }
        }

        stage('Push Docker Image') {
            steps {
                echo "🚀 Pushing Docker image to registry..."
                script {
                    docker.withRegistry("${DOCKERHUB_REGISTRY}", "${DOCKER_HUB_CREDENTIAL_ID}") {
                        dockerImage.push('latest')
                    }
                }
            }
        }

        stage('Deploy') {
            steps {
                echo "🚀 Deploying the application..."
                script {
                    withCredentials([string(credentialsId: 'render-deploy-mlops', variable: 'DEPLOY_HOOK_URL')]) {
                        sh 'curl -X POST $DEPLOY_HOOK_URL'
                        echo "✅ Deployment trigger sent!"
                    }
                }
            }
        }
    }

    post {
        always {
            echo "📜 Pipeline execution completed!"
        }
        success {
            echo "✅ Pipeline finished successfully!"
        }
        failure {
            echo "❌ Pipeline failed! Check logs in Jenkins console."
        }
    }
}
