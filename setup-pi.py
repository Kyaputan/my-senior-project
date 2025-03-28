import os
import subprocess
import sys
import platform

# Folder names
folder_1 = "database"
folder_2 = "snapshots"
folder_3 = "logs"
folder_4 = "Videos"

# Get the current path
now_path = os.path.dirname(os.path.realpath(__file__))

# Paths for the folders
folder_1_path = os.path.join(now_path, folder_1)
folder_2_path = os.path.join(now_path, folder_2)

# Function to print styled messages with bigger, bolder, colorful text
def print_styled(message, style="bold"):
    style_dict = {
        "bold": "\033[1m",  # Bold text
        "blue": "\033[34m",  # Blue text
        "green": "\033[32m",  # Green text
        "red": "\033[31m",  # Red text
        "underline": "\033[4m",  # Underlined text
        "reset": "\033[0m",  # Reset text styling
        "yellow": "\033[33m",  # Yellow text
        "cyan": "\033[36m"  # Cyan text
    }
    styled_message = f"{style_dict.get(style, style_dict['reset'])}{message}{style_dict['reset']}"
    print(styled_message)

# Creating folders with bigger bold and colored text
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

# Installing dependencies from requirements.txt with more emphasis
def install_requirements():
    if os.path.exists('requirements.txt'):
        print_styled("INSTALLING DEPENDENCIES FROM requirements.txt", "yellow")
        
        # Check the operating system
        current_platform = platform.system().lower()
        
        try:
            if current_platform == 'windows':
                subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
                print_styled("INSTALLATION SUCCESSFUL ON WINDOWS!", "cyan")
            elif current_platform == 'linux':
                # Assuming Raspberry Pi uses Linux-based OS (like Raspbian or Raspberry Pi OS)
                subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
                print_styled("INSTALLATION SUCCESSFUL ON RASPBERRY PI!", "cyan")
            else:
                print_styled("UNSUPPORTED PLATFORM. INSTALLATION MAY FAIL.", "red")
        except subprocess.CalledProcessError as e:
            print_styled(f"AN ERROR OCCURRED WHILE INSTALLING DEPENDENCIES: {e}", "red")
    else:
        print_styled("NO requirements.txt FILE FOUND.", "red")

# Run the installation
install_requirements()
