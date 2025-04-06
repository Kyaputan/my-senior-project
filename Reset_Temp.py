import os
import shutil
import time
from colorama import init, Fore, Style
from tqdm import tqdm

# Initialize Colorama
init(autoreset=True)

def display_header():
    """Display a beautiful header with animation"""
    os.system("cls" if os.name == "nt" else "clear")
    
    print(Fore.BLUE + Style.BRIGHT + "╔" + "═" * 48 + "╗")
    print(Fore.BLUE + Style.BRIGHT + "║" + " " * 48 + "║")
    print(Fore.BLUE + Style.BRIGHT + "║" + "  🚀 TEMPORARY FOLDER RESET UTILITY  ".center(47) + "║")
    print(Fore.BLUE + Style.BRIGHT + "║" + " " * 48 + "║")
    print(Fore.BLUE + Style.BRIGHT + "╚" + "═" * 48 + "╝")
    
    print("\n" + Fore.CYAN + Style.BRIGHT + "✦ " + Style.NORMAL + "This utility will clean and reset your temporary folders")
    print(Fore.CYAN + Style.BRIGHT + "✦ " + Style.NORMAL + "All existing data will be removed")
    print(Fore.CYAN + Style.BRIGHT + "✦ " + Style.NORMAL + "New empty folders will be created\n")

def display_warning():
    """Display an attention-grabbing warning"""
    print(Fore.RED + Style.BRIGHT + "⚠ WARNING " + "!" * 5)
    print(Fore.RED + "┌" + "─" * 62 + "┐")
    print(Fore.RED + "│" + " This action will delete all data in the temporary folders ".center(62) + "│")
    print(Fore.RED + "│" + " All existing snapshots, database files and logs will be lost ".center(48) + "│")
    print(Fore.RED + "└" + "─" * 62 + "┘\n")

def animate_progress(folder , progress , duration):
    """Show an animated progress bar for each folder reset"""
    for i in tqdm(range(progress), 
                 desc=f"{Fore.WHITE} Processing {folder}", 
                 bar_format="{l_bar}{bar}| {n_fmt}/{total_fmt}",
                 colour="green"):
        time.sleep(duration)

def reset_temp_folder():
    """Reset the temporary folders with visual feedback"""
    
    # Keep asking until a valid response is provided
    while True:
        warning_response = input(Fore.YELLOW + Style.BRIGHT + "❓ Do you want to proceed with the reset? (y/n): ")
        
        if warning_response.lower() in ['y', 'n']:
            break
        else:
            print(Fore.RED + "⚠ Invalid input! Please enter 'y' for yes or 'n' for no.")
    
    # Process the response
    if warning_response.lower() == "y":
        print(Fore.YELLOW + "\n⏳ Starting folder reset process...\n")
        
        folders = [
            ("Snapshots", Fore.MAGENTA, "📸" , 100 , 0.01),
            ("Database", Fore.CYAN, "🗃️" , 10 , 0.15),
            ("Logs", Fore.YELLOW, "📝" , 50 , 0.1)
        ]

        for folder, color, icon , progress , duration in folders:
            print(f"{color}{icon} Processing {folder}...")
            
            animate_progress(folder , progress , duration)
            
            if os.path.exists(folder):
                shutil.rmtree(folder)
            os.makedirs(folder)
            print(f"{color}✔ -{folder}- has been successfully reset.\n")

        print(Fore.GREEN + Style.BRIGHT + "┌" + "─" * 48 + "┐")
        print(Fore.GREEN + Style.BRIGHT + "│" + " ✅ ALL TEMPORARY FOLDERS HAVE BEEN RESET ".center(47) + "│")
        print(Fore.GREEN + Style.BRIGHT + "└" + "─" * 48 + "┘")
    else:
        print(Fore.RED + Style.BRIGHT + "❌ OPERATION CANCELLED")
        print(Fore.RED + "The temporary folders have not been reset.")

if __name__ == "__main__":
    display_header()
    display_warning()
    reset_temp_folder()  # No parameter needed as input is handled inside the function
    
    print(Fore.BLUE + Style.BRIGHT + "\n" + "═" * 50)
    print(Fore.BLUE + Style.BRIGHT + "Thank you for using the Folder Reset Utility".center(50))
    print(Fore.BLUE + Style.BRIGHT + "═" * 50)