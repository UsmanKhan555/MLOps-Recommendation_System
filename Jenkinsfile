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
                    try {
                        echo "🎯 Training model..."
                        sh 'python src/model.py | tee -a logs/train.log'  // Log output to file
                    } catch (Exception e) {
                        echo "❌ Model training failed!"
                        sh "echo 'Training failed at \$(date)' >> logs/error.log"
                        error "Stopping pipeline due to training failure"
                    }
                }
            }
        }

        stage('Evaluate Model') {
            steps {
                script {
                    try {
                        echo "🧪 Running model evaluation..."
                        sh 'pytest src/test.py --junitxml=results/test-results.xml | tee -a logs/test.log'
                    } catch (Exception e) {
                        echo "❌ Model evaluation failed!"
                        sh "echo 'Evaluation failed at \$(date)' >> logs/error.log"
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
                script {
                    echo "🐳 Building Docker image..."
                    dockerImage = docker.build("${DOCKERHUB_REPOSITORY}:latest")
                }
            }
        }

        stage('Push Docker Image') {
            steps {
                script {
                    echo "🚀 Pushing Docker image to registry..."
                    docker.withRegistry("${DOCKERHUB_REGISTRY}", "${DOCKER_HUB_CREDENTIAL_ID}") {
                        dockerImage.push('latest')
                    }
                }
            }
        }

        stage('Deploy') {
            steps {
                script {
                    echo "🚀 Deploying the application..."
                    withCredentials([string(credentialsId: 'render-deploy-mlops', variable: 'DEPLOY_HOOK_URL')]) {
                        sh 'curl -X POST $DEPLOY_HOOK_URL | tee -a logs/deploy.log'
                    }
                }
            }
        }
    }

    post {
        always {
            script {
                echo "📜 Saving logs & artifacts..."
                archiveArtifacts artifacts: 'logs/*.log, results/test-results.xml', fingerprint: true
            }
        }
        success {
            echo "✅ Pipeline completed successfully!"
        }
        failure {
            echo "❌ Pipeline failed! Check logs in Jenkins artifacts."
        }
    }
}
            