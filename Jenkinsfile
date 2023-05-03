pipeline {
    agent any

    environment {
       //SONAR_TOKEN = credentials('SONAR_TOKEN')
       BIN_PATH = "/var/lib/jenkins/.local/bin"
       DOCKER_REGISTRY = "http://74.235.12.24:8070/repository/docker"
       DOCKER_REGISTRY_CREDENTIALS = credentials('NEXUS-CRED')
    }

    stages {
        stage('Checkout Branch') {
            steps {
                script {
                    sh "git checkout test"
                    sh "git pull origin test"
                }
            }
        }

        stage('Install Dependencies') {
            when {
                beforeAgent true
            }
            steps {
                sh "pip install -r requirements.txt"
            }
        }
        stage('increment version') {
            steps {
                script {
                    echo "incrementing app version..."
                    sh "$BIN_PATH/bumpversion --allow-dirty patch"
                    version = sh(returnStdout: true, script: "grep -o 'current_version = [0-9.]*' .bumpversion.cfg | cut -d ' ' -f 3").trim()
                    env.IMAGE_TAG = "$version-$BUILD_NUMBER"
                }
            }
        }
        stage('Build Artifact') {
            steps {
                script{
                    withCredentials([usernamePassword(credentialsId: 'GIT_CRED', usernameVariable: 'GIT_USER', passwordVariable: 'GIT_PASS')]) {
                        sh "rm -rf ./dist/"
                        sh "python3 setup.py sdist"
                        sh "git add . && git commit -m 'Bump version' || true"
                        sh "git push https://${GIT_USER}:${GIT_PASS}@github.com/KhaledBenfajria/DevSecOps-pipeline.git"

                    }
                }
            }
        }

        stage('Unit Tests') {
            steps {
                sh "$BIN_PATH/coverage run --source='.' manage.py test"
                sh "$BIN_PATH/coverage xml"

            }
        }

        stage('SonarQube - SAST') {
            steps {
                withSonarQubeEnv("SonarQube") {
                    sh "/var/lib/jenkins/.sonar/sonar-scanner-4.7.0.2747-linux/bin/sonar-scanner -Dsonar.projectKey=django-eco -Dsonar.host.url=https://9000-port-0d10cafb0e22450f.labs.kodekloud.com -Dsonar.login=sqp_7a9daad7224c0fa9d6702332665edb722c5e4c10"
                }
                timeout(time: 2, unit: 'MINUTES'){
                    script {
                        waitForQualityGate abortPipeline: true
                    }
                }
            }
        }

        stage('Vulerability Scan - Docker') {
            steps {
                parallel(
                    "DependencyCheck": {
                        sh "$BIN_PATH/safety check -r requirements.txt --continue-on-error " //--output json > report.json
                    },
                    "TrivyScan": {
                        sh "bash TrivyScan-docker-image.sh"
                    },
                    "OPA Conftest": {
                        sh "sudo docker run --rm  -v \$(pwd):/project openpolicyagent/conftest test --policy Dockerfile-security.rego Dockerfile"
                    }
                )
            }
        }

        stage('Publish Artifact to Nexus') {
            steps {
                nexusArtifactUploader (
                    nexusVersion: 'nexus3',
                    protocol: 'http',
                    nexusUrl: '74.235.12.24:8081/repository/Djecommerce-artifact/',
                    groupId: 'zed',
                    version: "${version}",
                    repository: 'Djecommerce-artifact',
                    credentialsId: 'NEXUS-CRED',
                    artifacts: [
                            [artifactId: 'Django-ecommerce',
                            classifier: 'file',
                            file: 'dist/Django-ecommerce-'+version+'.tar.gz',
                            type: 'tar.gz']
                     ]
                )
            }
        }

        stage('Build & Push Docker image to Nexus') {
            steps {
                script {
                  docker.withRegistry("${DOCKER_REGISTRY}", "NEXUS-CRED") {
                    sh "docker build -t my-django-ecommerce-image:${IMAGE_TAG} ."
                    sh "docker tag my-django-ecommerce-image:${IMAGE_TAG} 74.235.12.24:8070/repository/docker/my-django-ecommerce-image:${IMAGE_TAG}"
                    sh "docker push 74.235.12.24:8070/repository/docker/my-django-ecommerce-image:${IMAGE_TAG}"
                  }
                }
            }
        }
/*        stage('Vulerability Scan - kubernetes') {
            steps {
                parallel (
                    "OPA Conftest": {
                       sh "sudo docker run --rm  -v \$(pwd):/project openpolicyagent/conftest test --policy k8s-security.rego DJ-ecommerce-deploy.yaml"
                    },
                    "Kubesec - Scan": {
                        sh "bash kubesec-scan.sh"
                    }
                )
            }
        } */
        stage('Deploying Django E-commerce Application to Kubernetes') {
            steps {
                withKubeConfig([credentialsId: 'kubeconfig']) {
                    sh "sed -i 's#replace-image#74.235.12.24:8070/repository/docker/my-django-ecommerce-image:${IMAGE_TAG}#g' DJ-ecommerce-deploy.yaml"
                    sh "kubectl apply -f DJ-ecommerce-deploy.yaml"
                }
            }
        }
    }
}