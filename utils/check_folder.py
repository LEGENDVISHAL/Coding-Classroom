import multiprocessing
import os

from .check_file import CheckFile

FORMAT = "utf-8"
ALLOWED_FILE_TYPES = ["py", "c", "java"]
COMPILED_FILES = ["out", "class"]

# Helper Functions
def is_number(number):
    try:
        float(number)
        return True
    except ValueError:
        return False

def string_from_test_case(test_input):
    input_string = ""
    for digits in test_input:
        input_string += " ".join(map(str, digits))
        input_string += "\n"
    return input_string.encode(FORMAT)

def verify_output(stdout, program_output):
    digits = []
    for line in stdout.split("\n"):
        if not line:
            continue
        for number in line.split(" "):
            if is_number(number):
                digits.append(float(number))
            else:
                digits.append(number)

    for digit, expected_digit  in zip(digits, program_output):
        if digit != float(expected_digit):
            return False
    return True

def replace(array, elem, new_elem):
    try:
        index = array.index(elem)
    except ValueError:
        return array
    array[index] = new_elem
    return array

class CheckFolder:
    '''
    CheckFolder
    '''
    def __init__(self):
        self.dir_name = None
        self.test_input = None
        self.test_output = None
        self.file_types = None
        super().__init__()

    def set_folder(self, dir_name):
        self.dir_name = dir_name
    def get_folder(self):
        return self.dir_name

    def set_test_cases(self, test_input, test_output):
        self.test_input = test_input
        self.test_output = test_output
    def get_test_cases(self):
        return self.test_input, self.test_output

    def set_file_types(self, file_types):
        self.file_types = file_types
    def get_file_types(self):
        return self.file_types


    def run_test(self):
        results = []
        # number_test_case = len(self.test_input)
        compile_folder = os.path.join(self.dir_name, "compiled")

        if not os.path.exists(compile_folder):
            os.mkdir(compile_folder)

        files_to_be_checked = []
        for file_name in os.listdir(self.dir_name):
            if file_name == __file__:
                continue

            extension = file_name.split(".")[-1].lower()
            if extension in self.file_types:
                files_to_be_checked.append(file_name)
        with multiprocessing.Pool(processes=10) as pool:
            results = pool.map(self.run_test_parallel, files_to_be_checked)

        for file_name in os.listdir(compile_folder):
            extension = file_name.split(".")[-1].lower()
            if extension in COMPILED_FILES:
                os.remove(os.path.join(compile_folder, file_name))
        os.rmdir(compile_folder)

        return results

    def run_test_parallel(self, file_name):
        file_checker = CheckFile()
        file_checker.set_file_name(file_name)
        file_checker.set_folder(self.dir_name)
        file_checker.set_test_cases(self.test_input, self.test_output)
        result = file_checker.run_test()
        return result
