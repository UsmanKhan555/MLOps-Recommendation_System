pipeline {
    agent any



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

        // stage('Deploy Application') {
        //     steps {
        //         // Add deployment commands here
        //         sh 'echo "Deploy application commands here"'
        //     }
        // }
    }
}