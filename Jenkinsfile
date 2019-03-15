pipeline {
    agent {
        dockerfile {
            filename 'Dockerfile'
            additionalBuildArgs '--no-cache'
            args '-p 10081:10081 --security-opt apparmor=unconfined'
        }
    }

    environment {
        DATABASEURI = credentials('WXLOGINAPPID')
        WXLOGINAPPID = credentials('WXLOGINAPPID')
        WXLOGINSECRET = credentials('WXLOGINSECRET')
    }

    stages {
        stage('Initialize') {
            steps {
                sh 'gunicorn --chdir ./swagger_server app:app -b :81'
            }
        }
        stage('Deliver'){
            steps {
                input message: 'Start nginx? Click "proceed" to continue)'
                sh 'service nginx start'
                input message: 'Finished using the website? Click "proceed" to continue)'
            }
        }
    }
    post {
        always{
            cleanWs()
        }
    }
}