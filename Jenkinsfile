pipeline {
    agent any

    environment {
        DOCKER_HUB_CREDENTIAL_ID = 'mlops-jenkins-dockerhub-token'
        DOCKERHUB_REGISTRY = 'https://registry.hub.docker.com'
        DOCKERHUB_REPOSITORY = 'usmankhan555/mlopsapp'    }

    stages {

        stage('Setup system Dependencies') {
            steps {
                echo 'Setting up system dependencies...'
                sh 'sudo apt-get update && sudo apt-get install -y libgl1-mesa-glx libglib2.0-0'

            }
        }


        stage('Cloning Git Repository') {
            steps {
                // Using the credentials to checkout the code
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
                echo 'Installing dependencies...'
                sh "python -m pip install --upgrade pip --break-system-packages"
                sh "python -m pip install --break-system-packages -r requirements.txt"
            }
        }


        stage('Train Model') {
            steps {
                echo 'Training model...'
                sh 'python src/model.py'
            }
        }


        stage('Evaluate Model') {
            steps {
                echo 'Testing the model...'
                sh 'python src/test.py'
            }
        }

        stage('Trivy Scan') {
            steps {
                script {
                    echo "Running Trivy Scan"
                    sh "trivy fs --format table -o trivy-fs-report.html"
                }
            }
        }

        stage('Docker Build') {
            steps {
                script {
                    echo 'Building Docker image'
                    dockerImage = docker.build("${DOCKERHUB_REPOSITORY}:latest")
                }
            }
        }

        stage('Trivy Docker Image scan') {
            steps {
                script {
                    echo "Running Trivy Docker Image Scan"
                    sh "trivy image --format table -o trivy-image-report.html ${DOCKERHUB_REPOSITORY}:latest"
                }
            }
        }

        stage('Push Docker Image') {
            steps {
                script {
                    echo 'Pushing Docker image to Docker Hub'
                    docker.withRegistry("${DOCKERHUB_REGISTRY}", "${DOCKER_HUB_CREDENTIAL_ID}") {
                        dockerImage.push('latest')
                    }
                }
            }
        }

        stage('Deploy') {
            steps {
                script {
                    echo 'Deploying the application'
                     // Fetch the deploy hook URL securely and use it to trigger a deploy
                    withCredentials([string(credentialsId: 'render-deploy-mlops', variable: 'DEPLOY_HOOK_URL')]) {
                        sh 'curl -X POST $DEPLOY_HOOK_URL'
                    }
                }
            }
        }
    }
}