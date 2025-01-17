pipeline {
    agent any



    stages {
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


        // stage('Install Dependencies') {
        //     steps {
        //         echo 'Installing dependencies...'
        //         // sh 'pip install -r requirements.txt'
        //     }
        // }

        // stage('Run Tests') {
        //     steps {
        //         // Add your test commands here
        //         sh 'echo "Run tests here"'
        //     }
        // }

        // stage('Train Model') {
        //     steps {
        //         sh 'python src/model.py'
        //     }
        // }

        // stage('Deploy Application') {
        //     steps {
        //         // Add deployment commands here
        //         sh 'echo "Deploy application commands here"'
        //     }
        // }
    }
}