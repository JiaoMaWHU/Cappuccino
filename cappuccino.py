#!/usr/bin/env python
# use ' instead of "
import os
import generate_job_config
import argparse

def args_parse():
    parser = argparse.ArgumentParser(description='Cappuccino args parser')
    parser.add_argument('user', help='Jenkins user name')
    parser.add_argument('password', help='Jenkins user password')
    parser.add_argument('port', help='Jenkins running port')
    parser.add_argument('dir', help='Test code and  directory, end with slash')
    return parser.parse_args()

def execute_sudo_command(command):
    sudo_password = '296019'
    os.system('echo %s|sudo -S %s' % (sudo_password, command))

def build(args):
    # generate job config at current dir into  `config.xml`
    job_name, workspace = generate_job_config.generate_config_from_input(args)
    # job_name = "sample2"
    # workspace = "/home/chen/workspace/sample2"

    # set Jenkins privilege on given workspace
    execute_sudo_command("sudo chmod 777 {}".format(workspace))

    # create job
    prefix = 'sudo java -jar /var/cache/jenkins/war/WEB-INF/jenkins-cli.jar\
            -auth {}:{} -s http://localhost:{}'.format(args.user, args.password, args.port)
    CREATE_JOB = prefix + ' create-job {} < config.xml'.format(job_name)
    execute_sudo_command(CREATE_JOB)



    # build job
    BUILD_JOB = prefix + ' build {}'.format(job_name)
    execute_sudo_command(BUILD_JOB)

if __name__ == '__main__':
    args = args_parse()
    build(args)
