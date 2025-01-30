pipeline {
    agent any

    environment {
        DOCKER_HUB_CREDENTIAL_ID = 'mlops-jenkins-dockerhub-token'
        DOCKERHUB_REGISTRY = 'https://registry.hub.docker.com'
        DOCKERHUB_REPOSITORY = 'usmankhan555/mlopsapp'
    }

    stages {
        stage('Setup system Dependencies') {
            steps {
                echo 'Setting up system dependencies...'
                sh 'sudo apt-get update && sudo apt-get install -y libgl1-mesa-glx libglib2.0-0'
            }
        }

        stage('Cloning Git Repository') {
            steps {
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
                sh 'pytest src/test.py --junitxml=results/test-results.xml'
            }
            post {
                always {
                    junit 'results/test-results.xml'
                }
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
                    withCredentials([string(credentialsId: 'render-deploy-mlops', variable: 'DEPLOY_HOOK_URL')]) {
                        sh 'curl -X POST $DEPLOY_HOOK_URL'
                    }
                }
            }
        }
    }

    post {
        always {
            script {
                // Capture the end time
                def endTime = System.currentTimeMillis()

                // Calculate the duration
                def duration = endTime - currentBuild.startTimeInMillis

                // Write the duration to a CSV file
                writeFile file: 'build-duration.csv', text: "Build Duration (ms)\n${duration}"

                // Set correct permissions for the CSV file
                sh "chmod 644 build-duration.csv"

                // Debug: Print the CSV file content and permissions
                echo "CSV File Content:"
                sh "cat build-duration.csv"
                echo "CSV File Permissions:"
                sh "ls -l build-duration.csv"

                // Generate the plot
                plot csvFileName: 'build-duration.csv', 
                     group: 'Build Metrics', 
                     title: 'Build Duration', 
                     yaxis: 'Milliseconds',
                     style: 'line'
            }
        }
    }
}