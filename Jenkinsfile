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

        stage('Generate CSV') {
            steps {
                script {
                    // Calculate the total duration of the build
                    def buildDuration = System.currentTimeMillis() - currentBuild.startTimeInMillis
                    def formattedDuration = buildDuration / 1000  // Convert milliseconds to seconds

                    // Write or append the duration to a CSV file
                    def csvFile = 'build-durations.csv'
                    def content = "${env.BUILD_NUMBER},${formattedDuration}\n"

                    if (fileExists(csvFile)) {
                        // Append to existing file using shell command
                        sh "echo '${content}' >> ${csvFile}"
                    } else {
                        // Create new file and add headers
                        writeFile file: csvFile, text: "Build Number,Duration (s)\n" + content
                    }
                }
            }
        }


        stage('Building plot') {
            steps {
                plot csvFileName: 'build-durations.csv', 
                     group: 'Build Metrics', 
                     title: 'Build Duration Over Time', 
                     yaxis: 'Duration (s)',
                     style: 'line',  // Use 'line' for a line chart
                     csvSeries: [[
                         file: 'build-durations.csv',
                         inclusionFlag: 'OFF'
                     ]]
            }
        }
    }

    stages {
        stage('Generate CSV - Build Duration') {
            steps {
                script {
                    // Calculate build duration in seconds
                    def buildDuration = (System.currentTimeMillis() - currentBuild.startTimeInMillis) / 1000
                    def durationFile = 'build-durations.csv'

                    if (fileExists(durationFile)) {
                        sh "echo '${buildDuration}' >> ${durationFile}"
                    } else {
                        writeFile file: durationFile, text: "Duration (s)\n${buildDuration}\n"
                    }

                    // Debugging: Show CSV content
                    sh "cat ${durationFile}"
                }
            }
        }
    }

    post {
        always {
            script {
                // ✅ Capture build success (1) or failure (0)
                def buildStatus = currentBuild.result == null || currentBuild.result == 'SUCCESS' ? 1 : 0
                def successFile = 'build-success-rate.csv'

                if (fileExists(successFile)) {
                    sh "echo '${buildStatus}' >> ${successFile}"
                } else {
                    writeFile file: successFile, text: "Success (1=pass, 0=fail)\n${buildStatus}\n"
                }

                // Debugging: Show CSV content
                sh "cat ${successFile}"
            }
        }
    }

    stages {
        stage('Visualize Build Duration') {
            steps {
                plot csvFileName: 'build-durations.csv', 
                     group: 'Build Metrics', 
                     title: 'Build Duration Over Time', 
                     yaxis: 'Duration (s)',
                     style: 'line',
                     csvSeries: [[file: 'build-durations.csv', inclusionFlag: 'OFF']]
            }
        }

        stage('Visualize Success Rate') {
            steps {
                plot csvFileName: 'build-success-rate.csv', 
                     group: 'Build Metrics', 
                     title: 'Build Success Rate Over Time', 
                     yaxis: 'Success (1=pass, 0=fail)',
                     style: 'bar',
                     csvSeries: [[file: 'build-success-rate.csv', inclusionFlag: 'OFF']]
            }
        }
    }
}