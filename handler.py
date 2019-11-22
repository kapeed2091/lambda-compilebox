import os
from sandbox import Sandbox
import string
import random
import uuid

compiler_dict = {
    'python': ["python", "file.py", "", "Python", ""],
    'C/C++': ["\'g++ -o /usercode/a.out\' ", "file.cpp", "/usercode/a.out",
              "C/C++", ""]
}


def handler(event, context):
    import base64
    language = event['language']
    code = base64.b64decode(event['code']).decode('utf8')
    stdin = event['stdin']
    return compile_code(language, code, stdin)


def compile_code(language, code, stdin):

    temp_folder = os.path.join('/tmp', str(uuid.uuid4()))
    timeout_value = 20
    path = os.getcwd()

    sandbox = Sandbox(
        timeout_value=timeout_value,
        path=path,
        temp_folder=temp_folder,
        compiler_name=compiler_dict[language][0],
        file_name=compiler_dict[language][1],
        code=code,
        output_command=compiler_dict[language][2],
        language_name=compiler_dict[language][3],
        e_arguments=compiler_dict[language][4],
        stdin_data=stdin
    )

    (data, exec_time, err) = sandbox.run()

    return {
        "output":data,
        "langid": language,
        "code":code,
        "errors":err,
        "time":exec_time
    }
