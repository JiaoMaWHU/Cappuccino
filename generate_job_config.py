# run in Python2 environment
from xml.etree.ElementTree import parse
import os
from generate_unit_tests import generate_unit_tests_from_json

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
    print("generate unit tests: y/n?")
    flag = raw_input()
    generate_unit_tests_activated = True if flag == "y" else False
    print("Enter your github repo URL, empty means using local files")
    github_url = raw_input()
    github_flag = True if github_url.find("/") != -1 else False 

    # generate unit tests from user json
    if generate_unit_tests_activated:
        generate_unit_tests_from_json(args.dir)

    # generate xml configuration
    dir = args.dir
    project_name = os.path.basename(os.path.normpath(dir))
    ENTER_WORKSPACE = "cd {}".format(dir)
    NOSETEST = "nosetests --with-coverage --cover-inclusive --cover-package={} > {}output 2>&1".format(project_name, dir)
    PYLINT = "pylint -f parseable -d I0011,R0801 {} | tee -a {}output".format(project_name, dir)
    raw_instructions = [ENTER_WORKSPACE]
    if nosetest_activated:
        raw_instructions.append(NOSETEST)
    if pylint_activated:
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
    else:
        root = tree.getroot()
        e = root.find("scm")
        root.remove(e)


    tree.write("config.xml")

    return job_name, dir
