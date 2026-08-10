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
import shutil
import sys

PWD = os.getcwd()
WORKERS_DIR = f"{PWD}/workers"
TEMPLATE_DIR = f"{PWD}/worker_template"

def create_folder_structure(worker_name):
    folder_name = f"wk_{worker_name}"
    worker_path = os.path.join(WORKERS_DIR, folder_name)

    os.makedirs(worker_path, exist_ok=True)

    if os.path.exists(TEMPLATE_DIR):
        for item in os.listdir(TEMPLATE_DIR):
            s = os.path.join(TEMPLATE_DIR, item)
            d = os.path.join(worker_path, item)
            if os.path.isdir(s):
                shutil.copytree(s, d, dirs_exist_ok=True)
            else:
                shutil.copy2(s, d)
        print(f"Folder '{folder_name}' created with config.json, form_inputs.json, and form_outputs.json files.")
    else:
        print("Error: Template directory does not exist.")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Invalid argument. Usage: run.py create <worker_name>")
    else:
        create_folder_structure(sys.argv[1])
