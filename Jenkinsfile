pipeline {
    agent any
    stages {
        stage('Build') {
            steps {
                sh 'sudo make dev'
                sh 'sudo make check-format'
                sh 'sudo make lint'
                sh 'sudo make prod'
            }
        }
    }
}
