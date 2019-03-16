pipeline {
    agent {
        dockerfile {
            filename 'Dockerfile'
            additionalBuildArgs '--no-cache'
            args '-p 10081:10081 --restart=always --security-opt apparmor=unconfined'
        }
    }

    environment {
        DATABASEURI = credentials('DATABASEURI')
        WXLOGINAPPID = credentials('WXLOGINAPPID')
        WXLOGINSECRET = credentials('WXLOGINSECRET')
    }

    stages {
        stage('Install') {
            steps { 
                sh 'pip3 install --no-cache-dir -r /var/jenkins_home/workspace/ProjectAgora-server/requirements.txt'
            }
        }
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