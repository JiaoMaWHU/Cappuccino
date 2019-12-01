import json
import os
import shutil

def generate_unit_tests_from_json(dir):
    # directory to store unit test file
    folder = os.path.exists(dir + "tests")
    if folder:
        shutil.rmtree("{}tests".format(dir))
    os.mkdir("{}tests".format(dir))

    with open("{}test_cases.json".format(dir), 'r') as f:
        data = f.read()

    desps = json.loads(data)
    #print(len(desps))

    f = open("{}tests/unit_test.py".format(dir), "w")
    f.write("import unittest\n")
    for i in range(len(desps)):
        desp = desps[i]
        dir = desp["dir"]
        #print(dir)
        f.write("import {}\n".format(dir))

    class_counter = 0   # generate 1 class for every python file
    method_counter = 0  # generate 1 test method for every method with given different input
    f.write("\n\n")

    for i in range(len(desps)):
        desp = desps[i]
        dir = desp["dir"]
        f.write("class Test{}(unittest.TestCase):\n".format(class_counter))
        class_counter += 1
        method_counter = 0

        methods = desp["methods"]
        for j in range(len(methods)):
            method = methods[j]
            method_name = method["name"]
            inputs = eval(str(method["input"]))
            outputs = eval(str(method["output"]))
            #print(method_name, inputs, outputs)

            for k in range(len(inputs)):
                f.write("\tdef test{}(self):\n".format(method_counter))
                method_counter += 1
                assertion = "self.assertEqual({}({}), {})\n".format(dir + "." + method_name, inputs[k], outputs[k])
                f.write("\t\t" + assertion)
                f.write("\n")


