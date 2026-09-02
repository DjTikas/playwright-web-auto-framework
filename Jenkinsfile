pipeline {
    agent any
    stages {
        stage("playwright‑demo") {
            agent {
                docker {
                    image 'mcr.microsoft.com/playwright/python:v1.48.0-focal'
                    customWorkspace "workspace/docker-demo-play"
                }
            }
            steps {
                // !!!重点：删掉原来脚本内部的git{...}整块代码，Jenkins页面SCM会自动拉取代码
                sh '''
                pip install -r requirement.txt \
                --index-url https://pypi.tuna.tsinghua.edu.cn/simple/ \
                --default-timeout=120
                '''
                sh 'python run.py'
            }
        }
    }
    post {
        always {
            script {
                echo "allure reports "
                sh 'cp -rf ./../docker-demo-play/reports ${WORKSPACE}/reports'
                allure includeProperties: false,
                       jdk: '',
                       resultPolicy: 'LEAVE_AS_IS',
                       results: [[path: 'reports']]
            }
        }
    }
}
