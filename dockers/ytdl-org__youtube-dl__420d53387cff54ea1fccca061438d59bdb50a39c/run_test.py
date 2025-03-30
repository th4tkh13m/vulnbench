import subprocess
import sys
import os
# from ...utils.log_parser import parse_log_django


def run_test():
    os.chdir("/app")  # Ensure we are in the correct directory
    # Construct the correct shell command
    cmd = "coverage run -m nose test --verbose $test_set $multiprocess_args"
    
    # Run the command in a shell so environment variables are expanded
    proc = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True, env=os.environ)
    
    # Capture output and errors
    out, err = proc.communicate()
    
    return out.decode("utf-8"), err.decode("utf-8"), proc.returncode  # Decode bytes to string

if __name__ == "__main__":
    out, err, returncode = run_test()
    # print("Output")
    sys.stdout.write(out)
    # print("Error")
    sys.stderr.write(err)
    
    # print(parse_log_django(out))
    
    # print("Return code:", returncode)
    # print(parse_log_django(err))
    sys.exit(returncode)
    
