#!/usr/bin/env python
import os
import generate_job_config
import argparse
from xml.etree.ElementTree import parse

def args_parse():
    parser = argparse.ArgumentParser(description='Cappuccino args parser')
    parser.add_argument('user', help='Jenkins user name')
    parser.add_argument('password', help='Jenkins user password')
    parser.add_argument('port', help='Jenkins running port')
    return parser.parse_args()

def execute_sudo_command(command):
    sudo_password = 'majinxin'
    os.system('echo %s|sudo -S %s' % (sudo_password, command))

def build(args):
    # output the banner for Cappuccino
    banner = open('banner.txt','r')
    lines = banner.read()
    print(lines)
    banner.close()
    prefix = 'sudo java -jar /var/cache/jenkins/war/WEB-INF/jenkins-cli.jar\
            -auth {}:{} -s http://localhost:{}'.format(args.user, args.password, args.port)

    print("=== Enter \"New\" to build a new job, \"List\" to build exisitng jobs ===")
    flag = raw_input()
    if flag != 'New':
        # list jobs
        print("=== Existing job list: ===")
        LIST_JOB = prefix + ' list-jobs'
        execute_sudo_command(LIST_JOB)
        print("=== Enter the job you want to build: ===")
        job_name = raw_input()
    else:
        # generate job config at current dir into  `config.xml`
        job_name, workspace = generate_job_config.generate_config_from_input()

        # set Jenkins privilege on given workspace
        execute_sudo_command("sudo chmod 777 {}".format(workspace))

        # create job
        CREATE_JOB = prefix + ' create-job {} < config.xml'.format(job_name)
        execute_sudo_command(CREATE_JOB)

    # get job output path
    JOB_INFO = prefix + ' get-job {} > getconfig.xml'.format(job_name)
    execute_sudo_command(JOB_INFO)
    tree = parse('getconfig.xml')
    e = tree.find("builders/hudson.tasks.Shell/command")
    path = e.text.split()[1]


    # build job
    print('=== Start building ===')
    BUILD_JOB = prefix + ' build {}'.format(job_name)
    execute_sudo_command(BUILD_JOB)
    print('=== Output is created in path: \"{}\" ===').format(path)
    print('=== Finish building, exit ===')

if __name__ == '__main__':
    args = args_parse()
    build(args)