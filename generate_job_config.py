# run in Python2 environment
from xml.etree.ElementTree import parse

def generate_config_from_input():
    print("please enter your job name: ")
    job_name = raw_input()

    print("please enter your workspace directory: ")
    dir = raw_input()
    dir = dir if dir else "/home/chen/workspace/sample2"
    print("please enter your test tasks: (tap y to activate)")
    print("nosetest: y/n?")
    flag = raw_input()
    nosetest_activated = True if flag == "y" else False
    print("coverage: y/n?")
    flag = raw_input()
    coverage_activated = True if flag == "y" else False
    print("pylint: y/n?")
    flag = raw_input()
    pylint_activated = True if flag == "y" else False

    PYTHON_PATH = "/home/chen/.local/bin/"

    ENTER_WORKSPACE = "cd {}".format(dir)   
    NOSETEST = "sudo {}nosetests --with-coverage --cover-inclusive".format(PYTHON_PATH)
    COVERAGE_REPORT = "sudo {}coverage xml".format(PYTHON_PATH)
    PYLINT = "sudo {}pylint -f parseable -d I0011,R0801 sample | tee pylint.out".format(PYTHON_PATH)


    raw_instructions = [ENTER_WORKSPACE]
    if nosetest_activated:
        raw_instructions.append(NOSETEST)
    if coverage_activated:
        raw_instructions.append(COVERAGE_REPORT)
    if pylint_activated:
        raw_instructions.append(PYLINT)

    instructions = "\n".join(raw_instructions)
    print("command shell:")
    print(instructions)

    tree = parse("./config_template.xml")
    e = tree.find("builders/hudson.tasks.Shell/command")
    # e = doc.find("actions")
    e.text = instructions

    tree.write("./config.xml")

    return job_name, dir
