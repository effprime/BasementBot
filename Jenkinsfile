pipeline {
    agent any
    stages {
        stage('Build') {
            steps {
                make dev
                make check-format
                make lint
                make prod
            }
        }
    }
}
