pipeline {
    agent any
    stages {
        stage('Build dev image') {
            steps {
                sh 'make dev'
            }
        }
        stage('Linting') {
            steps {
                sh 'make check-format'
                sh 'make lint'
            }
        }
        stage('Build prod image') {
            steps {
                sh 'make prod'
            }
        }
    }
}
