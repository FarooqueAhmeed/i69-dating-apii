pipeline {
    agent any

    parameters {
        string(defaultValue: 'production', description: 'enter the branch name to deploy', name: 'branch')
        string(description: 'enter the rev_ver', name: 'REV_VER')
    }

    stages {
        stage('Prepare environment'){
          steps {
                script {
                    env.BRANCH_PARAM_COPY = "${branch}"
                    env.REV_VER_PARAM_COPY = "${REV_VER}"
                }
            }
    }
        stage("Backup code") {
        steps {
            script {
                // Save the current branch and commit hash
                def branch = params.branch
                def commit = sh(returnStdout: true, script: 'git rev-parse HEAD').trim()

                // Connect to the server and backup the code
                withCredentials([sshUserPrivateKey(credentialsId: 'mainserverkey', keyFileVariable: 'MAIN_SSH_KEY')]) {
                    sh """
                        ssh -o StrictHostKeyChecking=no -i $MAIN_SSH_KEY i69admin@188.34.154.165 -p 2289 '
                        cd fixes &&
                        rm -rf /mnt/HC_Volume_32770002/backups/i69-apibackup.tar.gz &&
                        tar -czvf /mnt/HC_Volume_32770002/backups/i69-apibackup.tar.gz i69-api
                        '
                    """
                }
            }
        }
    }
    
        stage("Deploy code to main server") {
            steps {
                script {
                    // Save the current branch and commit hash
                    def branchs = params.branch
                    def rev_ver = params.branch

                    // Connect to the server and deploy the code
                    withCredentials([sshUserPrivateKey(credentialsId: 'mainserverkey', keyFileVariable: 'MAIN_SSH_KEY')]) {
                        sh """
                            ssh -o StrictHostKeyChecking=no -i $MAIN_SSH_KEY i69admin@188.34.154.165 -p 2289 '
                            cd fixes &&
                            cd i69-api &&
                            git fetch && git pull &&
                            git checkout ${params.branch} &&
                            git reset --hard ${params.REV_VER} &&
                            docker-compose -f docker-compose.prod.yml down &&
                            rm -vf supervisor.sock &&
                            docker-compose -f docker-compose.prod.yml build &&
                            docker-compose -f docker-compose.prod.yml up -d
                            '
                        """
                    }
                }
            }
        }

       
    }

    post {
        always{
             cleanWs()
        }
        failure {
            script {
                // Trigger the rollback job if the build fails
                def previousBuild = currentBuild.previousSuccessfulBuild
                    def branch = previousBuild.buildVariables["BRANCH_PARAM_COPY"]
                    def rev_ver = previousBuild.buildVariables["REV_VER_PARAM_COPY"]
                    echo "branch value: ${branch}"
                    echo "rev ver value: ${rev_ver}"
                    build job:  env.JOB_NAME ,parameters: [[$class: 'StringParameterValue', name: 'branch', value: "${branch}"], [$class: 'StringParameterValue', name: 'REV_VER', value: "${rev_ver}"]]
                    
            }
        }
    }
}
