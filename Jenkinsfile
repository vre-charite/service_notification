pipeline {
    agent { label 'small' }
    environment {
      imagename_dev = "10.3.7.221:5000/notification"
      imagename_staging = "10.3.7.241:5000/notification"
      registryCredential = 'docker-registry'
      dockerImage = ''
    }

    stages {

    stage('Git clone for dev') {
        when {branch "k8s-dev"}
        steps{
          script {
          git branch: "k8s-dev",
              url: 'https://git.indocresearch.org/platform/service_notification.git',
              credentialsId: 'lzhao'
            }
        }
    }

    stage('DEV unit test') {
      when {branch "k8s-dev"}
      steps{
        sh "pip3 install -r requirements.txt"
        sh "pip3 install -r tests/test_requirements.txt"
        sh "pytest"
      }
    }

    stage('DEV Build and push image') {
      when {branch "k8s-dev"}
      steps{
        script {
            docker.withRegistry('http://10.3.7.221:5000', registryCredential) {
                customImage = docker.build("10.3.7.221:5000/notification:${env.BUILD_ID}")
                customImage.push()
            }
        }
      }
    }
    stage('DEV Remove image') {
      when {branch "k8s-dev"}
      steps{
        sh "docker rmi $imagename_dev:$BUILD_NUMBER"
      }
    }

    stage('DEV Deploy') {
      when {branch "k8s-dev"}
      steps{
        sh "sed -i 's/<VERSION>/${BUILD_NUMBER}/g' kubernetes/dev-deployment.yaml"
        sh "kubectl config use-context dev"
        sh "kubectl apply -f kubernetes/dev-deployment.yaml"
      }
    }

    stage('Git clone staging') {
        when {branch "k8s-staging"}
        steps{
          script {
          git branch: "k8s-staging",
              url: 'https://git.indocresearch.org/platform/service_notification.git',
              credentialsId: 'lzhao'
            }
        }
    }

    stage('STAGING Building and push image') {
      when {branch "k8s-staging"}
      steps{
        script {
            docker.withRegistry('http://10.3.7.241:5000', registryCredential) {
                customImage = docker.build("10.3.7.241:5000/notification:${env.BUILD_ID}")
                customImage.push()
            }
        }
      }
    }

    stage('STAGING Remove image') {
      when {branch "k8s-staging"}
      steps{
        sh "docker rmi $imagename_staging:$BUILD_NUMBER"
      }
    }

    stage('STAGING Deploy') {
      when {branch "k8s-staging"}
      steps{
        sh "sed -i 's/<VERSION>/${BUILD_NUMBER}/g' kubernetes/staging-deployment.yaml"
        sh "kubectl config use-context staging"
        sh "kubectl apply -f kubernetes/staging-deployment.yaml"
      }
    }
  }
}
