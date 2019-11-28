# run in Python2 environment
import os
import generate_job_config

def execute_sudo_command(command):
    sudo_password = "296019"
    os.system('echo %s|sudo -S %s' % (sudo_password, command))

# generate job config at current dir into  `config.xml`
job_name, workspace = generate_job_config.generate_config_from_input()
# job_name = "sample2"
# workspace = "/home/chen/workspace/sample2"

# set Jenkins privilege on given workspace
execute_sudo_command("sudo chmod 777 {}".format(workspace))

# create job
prefix = "sudo java -jar /var/cache/jenkins/war/WEB-INF/jenkins-cli.jar -auth chen:296019 -s http://localhost:8080 "
CREATE_JOB = prefix + " create-job {} < config.xml".format(job_name)
execute_sudo_command(CREATE_JOB)

# build job
BUILD_JOB = prefix + " build {}".format(job_name)
execute_sudo_command(BUILD_JOB)
