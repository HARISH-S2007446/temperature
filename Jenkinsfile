pipeline {
    agent any

    environment {
        DOCKER_IMAGE = "harishs2007446/temperature"
        IMAGE_TAG = "${env.GIT_COMMIT.take(12)}"
        DOCKER_CREDENTIALS = credentials('dockerhub-creds')
        KUBE_CONFIG = credentials('kubeconfig-creds')
    }

    stages {
        stage('Source Code') {
            steps {
                echo "Cloning repository and preparing source code"
                checkout scm
            }
        }

        stage('Version Control') {
            steps {
                echo "Current commit: ${env.GIT_COMMIT}"
                sh 'git --no-pager log -1 --oneline'
            }
        }

        stage('Continuous Integration') {
            steps {
                echo "Installing dependencies and running tests"
                sh '''
                    python3 -m venv .venv
                    . .venv/bin/activate
                    python -m pip install --upgrade pip
                    pip install -r requirements.txt
                    pytest -q
                '''
            }
        }

        stage('Build') {
            steps {
                echo "Building Docker image for commit ${IMAGE_TAG}"
                sh """
                    docker login -u ${DOCKER_CREDENTIALS_USR} -p ${DOCKER_CREDENTIALS_PSW}
                    docker build -t ${DOCKER_IMAGE}:${IMAGE_TAG} .
                    docker push ${DOCKER_IMAGE}:${IMAGE_TAG}
                """
            }
        }

        stage('Deployment') {
            steps {
                echo "Deploying Docker image to Kubernetes"
                sh '''
                    export KUBECONFIG=$WORKSPACE/kubeconfig
                    echo "$KUBE_CONFIG" > $WORKSPACE/kubeconfig
                    chmod 600 $WORKSPACE/kubeconfig

                    kubectl apply -f k8s/deployment.yaml
                    kubectl apply -f k8s/service.yaml
                    kubectl set image deployment/temperature-converter temperature-converter=${DOCKER_IMAGE}:${IMAGE_TAG}
                    kubectl rollout status deployment/temperature-converter
                '''
            }
        }
    }

    post {
        always {
            echo "Pipeline finished."
        }
    }
}