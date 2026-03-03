pipeline {

    agent any

    parameters {
        string(name: 'WORKERS', defaultValue: '2', description: 'Number of parallel workers')
        choice(name: 'BROWSER', choices: ['chrome', 'firefox'], description: 'Select browser')
        choice(name: 'HEADLESS', choices: ['true', 'false'], description: 'Run in headless mode')
        choice(name: 'TEST_SUITE', choices: ['smoke', 'regression'], description: 'Select test suite to run')
    }

    environment {
        IMAGE_NAME     = "orangehrm-automation"
        CONTAINER_NAME = "orangehrm-container"
        REPORT_DIR     = "reports"
        BASE_URL       = "https://opensource-demo.orangehrmlive.com/"
    }

    options {
        timestamps()
        disableConcurrentBuilds()
        buildDiscarder(logRotator(numToKeepStr: '10'))
        timeout(time: 20, unit: 'MINUTES')
    }

    stages {

        stage('Clean Workspace') {
            steps {
                deleteDir()
            }
        }

        stage('Checkout Code') {
            steps {
                git branch: 'main',
                    url: 'https://github.com/ashishbangar20/orangehrm-cloud-framework.git'
            }
        }

        stage('Remove Old Container') {
            steps {
                sh 'docker rm -f $CONTAINER_NAME 2>/dev/null || true'
            }
        }

        stage('Build Docker Image') {
            steps {
                sh 'docker build -t ${IMAGE_NAME}:${BUILD_NUMBER} .'
            }
        }

        stage('Run Tests in Docker') {
            steps {
                script {
                    withCredentials([usernamePassword(
                        credentialsId: 'orangehrm-creds',
                        usernameVariable: 'ORANGE_USERNAME',
                        passwordVariable: 'ORANGE_PASSWORD'
                    )]) {

                        sh """
                        mkdir -p $REPORT_DIR

                        docker run --rm \
                        --name $CONTAINER_NAME \
                        -e BASE_URL=${BASE_URL} \
                        -e USERNAME=\$ORANGE_USERNAME \
                        -e PASSWORD=\$ORANGE_PASSWORD \
                        -v \$(pwd)/$REPORT_DIR:/app/$REPORT_DIR \
                        ${IMAGE_NAME}:${BUILD_NUMBER} \
                        pytest -n ${params.WORKERS} \
                        -m ${params.TEST_SUITE} \
                        --browser=${params.BROWSER} \
                        --headless=${params.HEADLESS} \
                        --html=$REPORT_DIR/report.html \
                        --self-contained-html \
                        -v
                        """
                    }
                }
            }
        }

        stage('Publish HTML Report') {
            steps {
                publishHTML([
                    allowMissing: true,
                    alwaysLinkToLastBuild: true,
                    keepAll: true,
                    reportDir: 'reports',
                    reportFiles: 'report.html',
                    reportName: 'OrangeHRM Automation Report'
                ])
            }
        }
    }

    post {

        always {
            sh 'docker rm -f $CONTAINER_NAME 2>/dev/null || true'
        }

        success {
            echo "🎉 Build Successful!"
        }

        failure {
            echo "❌ Build Failed!"
        }
    }
}