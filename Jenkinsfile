node {
    def app

    stage('Clone repository') {
        /* Cloning the Repository to our Workspace */
        checkout scm
    }

    stage('Build image') {
        /* This builds the actual image */
        app = docker.build("chaimaelhadraoui/python_data")
    }

    stage('Test image') {
        
        app.inside {
            echo "Tests passed"
        }
    }

    stage('Test code') {
        
        app.inside {
            sh("pytest")
        }
    }

    stage('Push image') {
        /* 
		You would need to first register with DockerHub before you can push images to your account	
	*/
	docker.withRegistry('https://registry.hub.docker.com', 'docker-hub') {
		app.push("${env.BUILD_NUMBER}")
		app.push("latest")
	} 
        
                echo "Trying to Push Docker Build to DockerHub"
    }
	stage('Deploy image') {
                sh("docker run -d -p 5000:5000 -p 8000:8000 chaimaelhadraoui/python_data:latest")
    }
}
