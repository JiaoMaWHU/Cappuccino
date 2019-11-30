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

    # generate xml configuration
    dir = args.dir
    project_name = os.path.basename(os.path.normpath(dir))
    ENTER_WORKSPACE = "cd {}../".format(dir)
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
    tree.write("config.xml")

    return job_name, dir