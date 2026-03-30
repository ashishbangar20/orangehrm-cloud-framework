pipeline {

    agent any

    parameters {
        string(name: 'WORKERS', defaultValue: '2', description: 'Number of parallel workers')
        choice(name: 'BROWSER', choices: ['chrome'], description: 'Select browser')
        choice(name: 'HEADLESS', choices: ['true', 'false'], description: 'Run in headless mode')
        choice(name: 'TEST_SUITE', choices: ['smoke', 'regression'], description: 'Select test suite')
    }

    environment {
        IMAGE_NAME     = "orangehrm-automation"
        CONTAINER_NAME = "orangehrm-container"
        REPORT_DIR     = "allure-results"
        BASE_URL       = "https://opensource-demo.orangehrmlive.com/"
    }

    options {
        timestamps()
        disableConcurrentBuilds()
        buildDiscarder(logRotator(numToKeepStr: '10'))
        timeout(time: 25, unit: 'MINUTES')
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

        stage('Remove Old Container (If Any)') {
            steps {
                sh 'docker rm -f $CONTAINER_NAME 2>/dev/null || true'
            }
        }

        stage('Build Docker Image') {
            steps {
                sh '''
                docker build --pull -t ${IMAGE_NAME}:${BUILD_NUMBER} .
                '''
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
                        mkdir -p ${WORKSPACE}/${REPORT_DIR}

                        docker run --rm \
                        --name ${CONTAINER_NAME} \
                        -u \$(id -u):\$(id -g) \
                        -e BASE_URL=${BASE_URL} \
                        -e USERNAME=\$ORANGE_USERNAME \
                        -e PASSWORD=\$ORANGE_PASSWORD \
                        -v ${WORKSPACE}/${REPORT_DIR}:/app/${REPORT_DIR} \
                        ${IMAGE_NAME}:${BUILD_NUMBER} \
                        pytest -n ${params.WORKERS} \
                        -m ${params.TEST_SUITE} \
                        --browser=${params.BROWSER} \
                        --headless=${params.HEADLESS} \
                        --alluredir=${REPORT_DIR} \
                        -v
                        """
                    }
                }
            }
        }

        stage('Publish Allure Report') {
            steps {
                allure includeProperties: false,
                       jdk: '',
                       results: [[path: "${REPORT_DIR}"]]
            }
        }
    }

    post {

        always {

            sh 'docker rm -f $CONTAINER_NAME 2>/dev/null || true'

            emailext(
                to: 'ashishbangar20@gmail.com',
                subject: "${currentBuild.currentResult}: ${env.JOB_NAME} #${env.BUILD_NUMBER}",
                body: """
Hello,

Automation Pipeline Result

Project: OrangeHRM Automation
Status: ${currentBuild.currentResult}

Job Name: ${env.JOB_NAME}
Build Number: ${env.BUILD_NUMBER}

Browser: ${params.BROWSER}
Headless: ${params.HEADLESS}
Workers: ${params.WORKERS}
Suite: ${params.TEST_SUITE}

Build URL:
${env.BUILD_URL}

Allure Report:
${env.BUILD_URL}allure

Regards
Jenkins CI
"""
            )
        }
    }
}