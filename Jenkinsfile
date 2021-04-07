pipeline {
    agent any
    stages {
        stage('Build') {
            steps {
                sh 'make dev'
                sh 'make check-format'
                sh 'make lint'
                sh 'make prod'
            }
        }
    }
}
