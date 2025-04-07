###############################################################################
#
# (C) Copyright 2025 EVERYSK TECHNOLOGIES
#
# This is an unpublished work containing confidential and proprietary
# information of EVERYSK TECHNOLOGIES. Disclosure, use, or reproduction
# without authorization of EVERYSK TECHNOLOGIES is prohibited.
#
###############################################################################

import os
import sys
import subprocess

PWD = os.getcwd()
PYTHON = sys.executable

ENTRYPOINTS = {
    "create": f"{PWD}/scripts/create.py",
    "venv": f"{PWD}/scripts/venv.py",
    "deploy": f"{PWD}/scripts/deploy.py",
    "delete": f"{PWD}/scripts/delete.py",
    "debug": f"{PWD}/scripts/debug.py"
}

os.environ["PYTHONPATH"] = f"{PWD};{PWD}\\workers" if os.name == 'nt' else f"{PWD}:{PWD}/workers"

def check_python_version():
    required_version = (3, 11)

    if sys.version_info < required_version:
        print(f"Python {required_version[0]}.{required_version[1]} or higher is required.")
        sys.exit(1)

def run_python(command, params):
    entrypoint = ENTRYPOINTS.get(command)
    if entrypoint:
        subprocess.run([PYTHON, entrypoint] + params, check=True)
    else:
        print(f"Invalid command: {command}")

def main():
    if len(sys.argv) < 2:
        print("Option not found, please select one of the following options: deploy, delete, debug, tests, coverage")
        sys.exit(1)

    command = sys.argv[1]
    params = sys.argv[2:]

    if command == "create":
        "Creating a new worker folder structure."
        run_python(command, params)
    elif command == "venv":
        "Creating a virtual environment."
        run_python(command, params)
    elif command == "shell":
        subprocess.run(["/usr/local/bin/ipython"])
    elif command in ("deploy", "delete"):
        try:
            run_python(command, params)
        except subprocess.CalledProcessError:
            print(f"{command.capitalize()} failed.")
    elif command == "debug":
        print("Debugging...")
        print(params)
        run_python(command, params)
    elif command == "tests":
        print("Running tests...")
        tests = params if params else ["scripts.tests"]
        subprocess.run([PYTHON, "-W", "ignore", "-m", "unittest", "-f"] + tests)
    elif command == "coverage":
        print("Running coverage tests...")
        os.environ["PYTHONWARNINGS"] = "ignore"
        subprocess.run(["/usr/local/bin/coverage", "run", "-m", "unittest", "-f"] + params)
        subprocess.run(["/usr/local/bin/coverage", "report"])
    else:
        print("Option not found, please select one of the following options: deploy, delete, debug, tests, coverage")
        sys.exit(1)


if __name__ == "__main__":
    check_python_version()
    main()
