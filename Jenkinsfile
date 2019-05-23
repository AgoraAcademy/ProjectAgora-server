pipeline {
    agent {
        dockerfile {
            filename 'Dockerfile'
            additionalBuildArgs '--no-cache'
            args '-p 10081:10081 -v ProjectAgora-storage:/var/ProjectAgora-storage --restart=always --security-opt apparmor=unconfined'
        }
    }

    environment {
        DATABASEURI = credentials('DATABASEURI')
        WXLOGINAPPID = credentials('WXLOGINAPPID')
        WXLOGINSECRET = credentials('WXLOGINSECRET')
        STORAGEURL = credentials('STORAGEURL')
        EWS_admin_password = credentials('EWS_admin_password')
        EWS_admin_email = credentials('EWS_admin_email')
    }

    stages {
        stage('Install') {
            steps { 
                sh 'pip3 install --no-cache-dir -r /var/jenkins_home/workspace/ProjectAgora-server/requirements.txt'
            }
        }
        stage('Initialize') {
            steps {
                sh 'gunicorn --chdir ./swagger_server --certfile /etc/agora/cert.pem --keyfile /etc/agora/cert.pem app:app -b :10081'
            }
        }
        // stage('Deliver'){
        //     steps {
        //         input message: 'Start nginx? Click "proceed" to continue)'
        //         sh 'service nginx start'
        //         input message: 'Finished using the website? Click "proceed" to continue)'
        //     }
        // }
    }
    post {
        always{
            cleanWs()
        }
    }
}