pipeline {
    agent any

    environment {
        YOUTUBE_API_KEY = credentials('AIzaSyA-LJ5wh7JlVriUUGHXDyJcofOLrf7gpZc')
    }

    stages {
        stage('Cloning Git Repository') {
            steps {
                echo 'Cloning repository...'
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