# run in Python2 environment
from xml.etree.ElementTree import parse
import os

def generate_config_from_input():
    # generate xml configuration
    print("=== Enter the path for test repo ===")
    dir = raw_input()
    project_name = os.path.basename(os.path.normpath(dir))
    ENTER_WORKSPACE = "cd {}../".format(dir)
    NOSETEST = "nosetests --cover-package={} --cover-inclusive ".format(project_name)
    # fixme: problem here, only support cover package here 
    PYLINT = "pylint -f parseable -d I0011,R0801 {} | tee -a {}output".format(project_name, dir)
    raw_instructions = [ENTER_WORKSPACE]

    # configuration for testing job
    print("=== Enter the github URL, leave empty for local repo ===")
    github_url = raw_input()
    github_flag = True if github_url else False 

    print("=== Enter the name for your job: ===")
    job_name = raw_input()

    print("** Include code coverage? y/n")
    flag = raw_input()
    if flag == "y":
        NOSETEST += '--with-coverage '
    print("** Clean previous statistics? y/n")
    flag = raw_input()
    if flag == "y":
        NOSETEST += '--cover-erase '
    print("** Be more verbose? y/n")
    flag = raw_input()
    if flag == "y":
        NOSETEST += '-v '
    print("** Traverse through all path entries of a namespace package? y/n")
    flag = raw_input()
    if flag == "y":
        NOSETEST += '--traverse-namespace '
    print("** Include code style check? y/n")
    flag = raw_input()
    if flag == "n":
        PYLINT = ''

    NOSETEST += '> {}output 2>&1'.format(dir)
    raw_instructions.append(NOSETEST)
    raw_instructions.append(PYLINT)
    instructions = "\n".join(raw_instructions)

    # create xml file
    tree = parse("config_template.xml")
    e = tree.find("builders/hudson.tasks.Shell/command")
    e.text = instructions
    # set github repo
    if github_flag:
        e = tree.find("scm/userRemoteConfigs/hudson.plugins.git.UserRemoteConfig/url")
        e.text = github_url
    else:
        e = tree.find("scm")
        for child in list(e):
            e.remove(child)
        e.attrib.pop("plugin", None)
        e.set("class", "hudson.scm.NullSCM")

    tree.write("config.xml")

    return job_name, dir
