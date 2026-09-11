pipeline {
    agent any

    environment {
        ALLURE_RESULTS = 'allure-results'
        PYTHONIOENCODING = 'utf-8'
    }

    stages {
        stage('Setup Environment (Ubuntu)') {
            steps {
                // 修复点 1: 使用 bash -c 来支持 source 命令
                sh '''
                    bash -c '
                        python3 -m venv venv
                        source venv/bin/activate
                        pip install --upgrade pip
                        pip install -r requirements.txt
                        playwright install chromium
                        playwright install-deps chromium
                    '
                '''
            }
        }

        stage('Run Tests') {
            steps {
                withCredentials([usernamePassword(credentialsId: 'mdm-login-cred', usernameVariable: 'MDM_USER', passwordVariable: 'MDM_PASS')]) {
                    sh '''
                        bash -c '
                            source venv/bin/activate
                            export MDM_USERNAME=$MDM_USER
                            export MDM_PASSWORD=$MDM_PASS
                            pytest TestCase/ --alluredir=${ALLURE_RESULTS} -v --tb=short
                        '
                    '''
                }
            }
        }

        stage('Publish Allure Report') {
            steps {
                allure includeProperties: false, jdk: '', results: [[path: "${ALLURE_RESULTS}"]]
            }
        }
    }

    post {
        always {
            archiveArtifacts artifacts: '${ALLURE_RESULTS}/**/*', fingerprint: true
            
            // 修复点 2: 显式指定收件人邮箱
            emailext (
                to: 'll15225478665@gmail.com',
                subject: "🧪 [MDM自动化] 构建 #${env.BUILD_NUMBER} - ${currentBuild.result}",
                body: """
                    <h3>构建摘要</h3>
                    <ul>
                        <li><strong>状态:</strong> ${currentBuild.result}</li>
                        <li><strong>耗时:</strong> ${currentBuild.durationString}</li>
                    </ul>
                    <p>👉 <a href="${env.BUILD_URL}allure">点击查看详细 Allure 报告</a></p>
                """,
                attachLog: true,
                mimeType: 'text/html'
            )
        }
    }
}
