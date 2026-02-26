pipeline {

    agent any

    parameters {
        choice(
            name: 'TEST_SUITE',
            choices: ['smoke', 'regression'],
            description: 'Select test suite to execute'
        )
    }

    environment {
        IMAGE_NAME = "orangehrm-automation"
        CONTAINER_NAME = "orangehrm-container"
        REPORT_DIR = "reports"
    }

    options {
        timestamps()
        buildDiscarder(logRotator(numToKeepStr: '10'))
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
                sh '''
                docker build --no-cache -t $IMAGE_NAME .
                '''
            }
        }

        stage('Run Tests (Headless - Free Tier Safe)') {
            steps {
                sh '''
                docker rm -f $CONTAINER_NAME 2>/dev/null || true
                mkdir -p $REPORT_DIR

                docker run --name $CONTAINER_NAME \
                -v $(pwd)/$REPORT_DIR:/app/reports \
                $IMAGE_NAME \
                pytest -v \
                -m ${TEST_SUITE} \
                --browser=chrome \
                --headless=true \
                --html=reports/report.html \
                --self-contained-html
                '''
            }
        }
    }

    post {

        always {
            echo "Cleaning up container..."
            sh 'docker rm -f $CONTAINER_NAME 2>/dev/null || true'
            archiveArtifacts artifacts: 'reports/*.html', allowEmptyArchive: true
            echo 'Pipeline Finished'
        }

        success {
            echo "Build Successful ✅"
        }

        failure {
            echo "Build Failed ❌"
        }
    }
}