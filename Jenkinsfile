pipeline {
    agent any

    environment {
        IMAGE_NAME = "orangehrm-automation"
        CONTAINER_NAME = "orangehrm-container"
    }

    stages {

        stage('Checkout Code') {
            steps {
                git branch: 'main',
                    url: 'https://github.com/ashishbangar20/orangehrm-cloud-framework.git'
            }
        }

        stage('Build Docker Image') {
            steps {
                sh 'docker build --no-cache -t $IMAGE_NAME .'
            }
        }

        stage('Run Tests in Container') {
            steps {
                sh '''
                docker run --name $CONTAINER_NAME $IMAGE_NAME
                '''
            }
        }

        stage('Copy Test Reports') {
            steps {
                sh '''
                docker cp $CONTAINER_NAME:/app/reports ./reports || true
                docker rm $CONTAINER_NAME || true
                '''
            }
        }
    }

    post {
        always {
            archiveArtifacts artifacts: 'reports/*.html', allowEmptyArchive: true
            echo 'Pipeline Finished'
        }
    }
}