from xml.etree.ElementTree import parse

print("please enter your job name: ")
job_name = input()

print("please enter your workspace directory: ")
dir = input()
dir = dir if dir else "/home/chen/workspace/sample2"
print("please enter your test tasks: (tap yes to activate)")
print("nosetest: y/n?")
flag = input()
nosetest_activated = True if flag == "y" else False
print("coverage: y/n?")
flag = input()
coverage_activated = True if flag == "y" else False
print("pylint: y/n?")
flag = input()
pylint_activated = True if flag == "y" else False

PYTHON_PATH = "/home/chen/.local/bin/"

ENTER_WORKSPACE = "cd {}".format(dir)   # TODO 需给workspace添加写权限
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