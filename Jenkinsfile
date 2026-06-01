pipeline {

    agent any

    stages {

        stage('Checkout') {
            steps {
                checkout scm
            }
        }

        stage('Build Frontend') {
            steps {
                sh 'docker build -t student-frontend ./frontend'
            }
        }

        stage('Build Backend') {
            steps {
                sh 'docker build -t student-backend ./backend'
            }
        }

    }
}
