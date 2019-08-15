pipeline {
    agent {
        dockerfile {
            filename 'Dockerfile'
            additionalBuildArgs '--no-cache'
            args '-p 10081:80 -v ProjectAgora-storage:/var/ProjectAgora-storage --restart=always --security-opt apparmor=unconfined'
        }
    }
    environment {
        DEV_DATABASEURI = credentials('DEV_DATABASEURI')
        DATABASEURI = credentials('DATABASEURI')
        WXLOGINAPPID = credentials('WXLOGINAPPID')
        WXLOGINSECRET = credentials('WXLOGINSECRET')
        STORAGEURL = credentials('STORAGEURL')
        EWS_admin_password = credentials('EWS_admin_password')
        EWS_admin_email = credentials('EWS_admin_email')
        SSL_CERT_KEY_PROD = credentials('SSL_CERT_KEY_PROD')
        SSL_CERT_CRT_PROD = credentials('SSL_CERT_CRT_PROD')
        MINIPROGRAM_APPID = credentials('MINIPROGRAM_APPID')
        MINIPROGRAM_APPSECRET = credentials('MINIPROGRAM_APPSECRET')
        MICROSOFT_CLIENT_ID = credentials('MICROSOFT_CLIENT_ID')
        MICROSOFT_CLIENT_SECRET = credentials('MICROSOFT_CLIENT_SECRET')
    }

    stages {
        stage('Install') {
            steps { 
                sh 'pip3 install --no-cache-dir -r /var/jenkins_home/workspace/ProjectAgora-server/requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple'
            }
        }
        stage('Serve') {
            steps {
                sh 'gunicorn --chdir ./swagger_server --certfile $SSL_CERT_CRT_PROD --keyfile $SSL_CERT_KEY_PROD --log-level=debug app:app -b :80'
            }
        }
    }
    post {
        always{
            cleanWs()
        }
    }
}