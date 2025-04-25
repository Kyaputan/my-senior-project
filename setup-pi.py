import os
import subprocess
import sys
import platform

folder_1 = "Database"
folder_2 = "Snapshots"
folder_3 = "Logs"
folder_4 = "Videos"

now_path = os.path.dirname(os.path.realpath(__file__))

folder_1_path = os.path.join(now_path, folder_1)
folder_2_path = os.path.join(now_path, folder_2)
folder_3_path = os.path.join(now_path, folder_3)
folder_4_path = os.path.join(now_path, folder_4)


def print_styled(message, style="bold"):
    style_dict = {
        "bold": "\033[1m",  
        "blue": "\033[34m",  
        "green": "\033[32m",  
        "red": "\033[31m",  
        "underline": "\033[4m",  
        "reset": "\033[0m",  
        "yellow": "\033[33m",  
        "cyan": "\033[36m"  
    }
    styled_message = f"{style_dict.get(style, style_dict['reset'])}{message}{style_dict['reset']}"
    print(styled_message)

   
if not os.path.exists(folder_1_path):
    os.makedirs(folder_1_path)
    print_styled(f"CREATED FOLDER: {folder_1} AT {now_path}", "green")
else:
    print_styled(f"FOLDER {folder_1_path} ALREADY EXISTS. SKIPPING CREATION.", "blue")

if not os.path.exists(folder_2_path):
    os.makedirs(folder_2_path)
    print_styled(f"CREATED FOLDER: {folder_2} AT {now_path}", "green")
else:
    print_styled(f"FOLDER {folder_2_path} ALREADY EXISTS. SKIPPING CREATION.", "blue")

if not os.path.exists(folder_3_path):
    os.makedirs(folder_3_path)
    print_styled(f"CREATED FOLDER: {folder_3} AT {now_path}", "green")
else:
    print_styled(f"FOLDER {folder_3_path} ALREADY EXISTS. SKIPPING CREATION.", "blue")

if not os.path.exists(folder_4_path):
    os.makedirs(folder_4_path)
    print_styled(f"CREATED FOLDER: {folder_4} AT {now_path}", "green")
else:
    print_styled(f"FOLDER {folder_4_path} ALREADY EXISTS. SKIPPING CREATION.", "blue")

