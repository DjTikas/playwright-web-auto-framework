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
                echo "allure prepare"
                sh "rm -rf ${WORKSPACE}/reports"
                sh "rm -rf ${WORKSPACE}/allure-report"
                sh "cp -rf ${WORKSPACE}/../docker-demo-play/reports ${WORKSPACE}/reports"
                sh "allure generate ${WORKSPACE}/reports -o ${WORKSPACE}/allure-report --clean --lang zh"
                sh "rm -rf /opt/allure_latest_report/*"
                sh "cp -r ${WORKSPACE}/allure-report/* /opt/allure_latest_report/"
            }
        }
    }
}
