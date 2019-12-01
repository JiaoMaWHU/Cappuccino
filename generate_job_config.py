# run in Python2 environment
from xml.etree.ElementTree import parse
import os

def generate_config_from_input(args):
    # output the banner for Cappuccino
    banner = open('banner.txt','r')
    lines = banner.read()
    print(lines)
    banner.close()

    # configuration for testing job
    print("Enter the name for your testing job: ")
    job_name = raw_input()
    print("Use nosetest: y/n?")
    flag = raw_input()
    nosetest_activated = True if flag == "y" else False
    print("Use pylint: y/n?")
    flag = raw_input()
    pylint_activated = True if flag == "y" else False
    print("Enter your github repo URL, empty means using local files")
    github_url = raw_input()
    github_flag = True if github_url else False 

    # generate xml configuration
    dir = args.dir
    project_name = os.path.basename(os.path.normpath(dir))
    ENTER_WORKSPACE = "cd {}../".format(dir)
    NOSETEST = "nosetests --cover-package={} ".format(project_name)
    # --with-coverage --cover-inclusive --cover-erase 
    # > {}output 2>&1 dir
    PYLINT = "pylint -f parseable -d I0011,R0801 {} | tee -a {}output".format(project_name, dir)
    raw_instructions = [ENTER_WORKSPACE]

    # configuration for testing job
    print("Enter the name for your job: ")
    job_name = raw_input()
    print("Include code coverage? y/n")
    flag = raw_input()
    if flag == "y":
        NOSETEST += ''
    raw_instructions.append(NOSETEST)
    raw_instructions.append(PYLINT)
    instructions = "\n".join(raw_instructions)

    print("Your testing configuration:")

    # create xml file
    tree = parse("config_template.xml")
    e = tree.find("builders/hudson.tasks.Shell/command")
    e.text = instructions
    # set github repo
    if github_flag:
        e = tree.find("scm/userRemoteConfigs/hudson.plugins.git.UserRemoteConfig/url")
        e.text = github_url

    tree.write("config.xml")

    return job_name, dir
