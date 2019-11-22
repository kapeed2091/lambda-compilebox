import os
from shutil import copy, rmtree
import time


class Sandbox:
    def __init__(
            self, timeout_value, path, temp_folder, compiler_name,
            file_name, code, output_command, language_name, e_arguments,
            stdin_data
    ):
        self.timeout_value = timeout_value
        self.path = path
        self.temp_folder = temp_folder
        self.compiler_name = compiler_name
        self.file_name = file_name
        self.code = code
        self.output_command = output_command
        self.language_name = language_name
        self.e_arguments = e_arguments
        self.stdin_data = stdin_data

    def prepare(self):

        os.makedirs(self.temp_folder)

        src_payload_path = os.path.join(self.temp_folder, "Payload")
        os.makedirs(src_payload_path)

        code_file_path = os.path.join(src_payload_path, self.file_name)
        f = open(code_file_path, 'w')
        f.write(self.code)
        f.close()
        os.chmod(code_file_path, 0o777)
        self.code_file_path = code_file_path

        input_file_path = os.path.join(self.temp_folder, "inputFile")
        f = open(input_file_path, 'w')
        f.write(self.stdin_data)
        f.close()
        os.chmod(input_file_path, 0o777)

    def execute(self):
        logfile_path = os.path.join(self.temp_folder, "logfile.txt")
        completed_file_path = os.path.join(self.temp_folder, "completed")
        errors_file_path = os.path.join(self.temp_folder, "errors")

        script_path = os.path.join(self.path, 'Payload/script.sh')

        command_str = "sh {script_path} {temp_folder} {compiler_name} {code_file_path}".format(
            script_path=script_path, temp_folder=self.temp_folder,
            compiler_name=self.compiler_name,
            code_file_path=self.code_file_path)
        os.system(command_str)

        f = open(completed_file_path, 'r')
        completed_data = f.read()
        f.close()

        data = completed_data.split('*-COMPILEBOX::ENDOFOUTPUT-*')[0]
        exec_time = completed_data.split('*-COMPILEBOX::ENDOFOUTPUT-*')[1]

        if not os.path.exists(errors_file_path):
            errors_data = ""
        else:
            f = open(errors_file_path, 'r')
            errors_data = f.read()
            f.close()

        rmtree(self.temp_folder)
        return data, exec_time, errors_data

    def run(self):
        self.prepare()
        return self.execute()
