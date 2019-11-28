# <project>
# <builders>
#     <hudson.tasks.Shell>
#       <command>

from xml.etree.ElementTree import parse
# f = open("./config_template.xml")
doc = parse("../config_template.xml")
print(doc.getroot().tag)

# for item in doc.iterfind('project/builders/hudson.tasks.Shell'):
#
#     print(item.findtext('command'))





general_config = "cd /home/chen/workspace/sample\
sudo /home/chen/.local/bin/nosetests --with-coverage --cover-inclusive\
sudo /home/chen/.local/bin/coverage xml\
sudo /home/chen/.local/bin/pylint -f parseable -d I0011,R0801 sample | tee pylint.out"

job_name = ""
dir = "/home/chen/workspace/sample2"

PYTHON_PATH = "/home/chen/.local/bin/"

ENTER_WORKSPACE = "cd {}".format(dir)

NOSETEST = "sudo {}nosetests --with-coverage --cover-inclusive".format(PYTHON_PATH)
COVERAGE_REPORT = "sudo {}coverage xml".format(PYTHON_PATH)
PYLINT = "sudo {}pylint -f parseable -d I0011,R0801 sample | tee pylint.out".format(PYTHON_PATH)

nosetest_activated = True
coverage_activated = True
pylint_activated = True

raw_instructions = [ENTER_WORKSPACE]
if nosetest_activated:
    raw_instructions.append(NOSETEST)
if coverage_activated:
    raw_instructions.append(COVERAGE_REPORT)
if pylint_activated:
    raw_instructions.append(PYLINT)

instructions = "\n".join(raw_instructions)
# print(instructions)


e = doc.find("builders/hudson.tasks.Shell/command")
# e = doc.find("actions")
print(e.text)
e.text = instructions
print(e.text)

doc.write("./config.xml")