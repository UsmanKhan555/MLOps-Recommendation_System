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

        stage ('Building plot') {
            agent any
            steps {
                plot csvFileName: 'plot-build-durations.csv', 
                    csvSeries: [[
                        width: 1600,
                        height: 1600,
                        displayTableFlag: false, 
                        exclusionValues: '', 
                        file: './build-durations.csv',  // Explicitly reference the file in root
                        inclusionFlag: 'OFF', 
                        url: ''
                    ]], 
                    group: 'BuildPerformanceMetrics', 
                    keepRecords: true,
                    numBuilds: '50', 
                    style: 'lineSimple', 
                    title: 'Build Durations Over Time',
                    yaxis: 'Build Duration (seconds)'
            }          
}

    // post {
    // always {
    //     script {
    //         // Calculate the total duration of the build
    //         def buildDuration = System.currentTimeMillis() - currentBuild.startTimeInMillis
    //         def formattedDuration = buildDuration / 1000  // Convert milliseconds to seconds

    //         // Write or append the duration to a CSV file
    //         def csvFile = 'build-durations.csv'
    //         def content = "${env.BUILD_NUMBER},${formattedDuration}\n"

    //         if (fileExists(csvFile)) {
    //             // Append to existing file
    //             writeFile file: csvFile, text: content, append: true
    //         } else {
    //             // Create new file and add headers
    //             writeFile file: csvFile, text: "Build Number,Duration (s)\n" + content
    //         }

    //         // Generate the plot
    //         plot csvFileName: csvFile, 
    //              group: 'Build Metrics', 
    //              title: 'Build Duration', 
    //              yaxis: 'Seconds',
    //              style: 'line'  // Change to 'line' to visualize the trend over builds
    //     }
    // }
}
}