def run_cmd(cmd):
    import subprocess
    try:
        proc = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE,
                                stderr=subprocess.PIPE)
        r = proc.communicate()
        print('Executing run_cmd with:', cmd)
        print('Response of run_cmd:', r)
        return proc.returncode, r
    except Exception as e:
        print('run_cmd, Exception:', e)
        return 1, None
