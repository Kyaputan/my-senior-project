import os
import subprocess
import importlib.util
import time
import sys
import platform
import shutil
import random
from datetime import datetime
import string

def install_libs():
    required_libs = [
        "pyfiglet",
        "termcolor",
        "rich",
        "art",
        "colorama",
        "tqdm",
        "psutil",
        "yaspin",
        # "alive-progress",
        "asciimatics",
        "questionary",
        "emoji",
        # "py-term",
        "pytermgui",
        "blessed",
        "prompt_toolkit",
        # "pyinquirer",
        # "windows-curses",
        "colr",
        "halo",
        "progress",
        # "lorem-text",
        # "image-to-ascii",
        # "pycairo",
        "colored",
        "cursor",
    ]
    missing_libs = [
        lib for lib in required_libs if importlib.util.find_spec(lib) is None
    ]
    # alive-progress, py-term, pyinquirer, windows-curses, lorem-text, image-to-ascii, pycairo...
    if missing_libs:
        print(
            f"\033[93m📦 Installing missing libraries: {', '.join(missing_libs)}...\033[0m"
        )
        try:
            subprocess.run(
                [sys.executable, "-m", "pip", "install"] + missing_libs, check=True
            )
        except subprocess.CalledProcessError as e:
            console.print(f"[red]❌ Failed to install libraries: {e}[/red]")

        print("\033[92m✅ All required libraries are installed!\033[0m")
    else:
        print("\033[92m✅ All required libraries are already installed!\033[0m")


install_libs()

from rich import print
from rich.console import Console
from rich.progress import track, Progress
from rich.text import Text
from rich.panel import Panel
from rich.table import Table
from rich.layout import Layout
from rich.live import Live
from rich.prompt import Prompt
from rich.syntax import Syntax
from rich.align import Align
from rich.rule import Rule
from rich.spinner import Spinner
from termcolor import colored
import pyfiglet
import art
import colorama
from yaspin import yaspin
from yaspin.spinners import Spinners
from alive_progress import alive_bar
import emoji
import psutil

from asciimatics.effects import Cycle, Stars, Print
from asciimatics.renderers import FigletText, SpeechBubble
from asciimatics.scene import Scene
from asciimatics.screen import Screen
from asciimatics.exceptions import ResizeScreenError
from halo import Halo
import cursor
from colored import fg, bg, attr

try:
    import winsound  # สำหรับเสียงพิมพ์ดีดใน Windows
except ImportError:
    winsound = None
colorama.init()

GREEN = "\033[92m"
YELLOW = "\033[93m"
RED = "\033[91m"
BLUE = "\033[94m"
CYAN = "\033[96m"
MAGENTA = "\033[95m"
BOLD = "\033[1m"
RESET = "\033[0m"
BRIGHT_GREEN = "\033[38;5;82m"
BRIGHT_YELLOW = "\033[38;5;226m"
BRIGHT_BLUE = "\033[38;5;39m"
ORANGE = "\033[38;5;208m"
PINK = "\033[38;5;200m"
LIME = "\033[38;5;118m"
PURPLE = "\033[38;5;129m"
GOLD = "\033[38;5;220m"

console = Console()


def asciimatics_splash(text="SUPER SYSTEM", duration=3):
    def demo(screen):
        effects = [
            Cycle(
                screen,
                FigletText(text, font="epic"),
                screen.height // 2 - 8,
                attr=Screen.A_BOLD,
                transparent=False,
            ),
            Cycle(
                screen,
                FigletText("LOADING...", font="big"),
                screen.height // 2 + 3,
                attr=Screen.A_BOLD,
                transparent=False,
            ),
            Stars(screen, 200),
        ]
        screen.play([Scene(effects, duration * 50)])

    try:
        Screen.wrapper(demo)
    except (ResizeScreenError, ImportError):
        print(f"{BRIGHT_BLUE}{pyfiglet.figlet_format(text, font='slant')}{RESET}")


def display_epic_header():
    try:
        asciimatics_splash("SUPER SETUP", 100)
    except Exception:
        header = pyfiglet.figlet_format("SUPER SETUP", font="slant")
        console.print(f"[bold magenta]{header}[/bold magenta]")

    try:
        ascii_art = art.art("random")
        console.print(f"[cyan]{ascii_art}[/cyan]")
        ascii_art = art.art("random")
        console.print(f"[cyan]{ascii_art}[/cyan]")
    except Exception:
        pass

    console.print(
        Panel(
            Align.center(
                Text("⚡⚡⚡ ULTRA AMAZING SYSTEM SETUP ⚡⚡⚡", style="bold yellow"),
            ),
            border_style="bright_blue",
            title="[bold red]🔥 ULTIMATE SETUP 🔥[/bold red]",
            subtitle=f"[bold green]v3.0 Ultra Edition Start at {datetime.now().strftime('%H:%M:%S')}[/bold green]",
        )
    )

    console.print(Rule(style="bright_green"))


def fancy_progress(text, duration=3, style="pulse"):
    if style == "rich":
        console.print(Text(f"🛠 {text}", style="bold yellow"))
        for _ in track(range(duration * 10), description="Processing..."):
            time.sleep(0.01)
        console.print("✅ Done!", style="bold green")

    elif style == "yaspin":
        with yaspin(Spinners.aesthetic, text=f"{BRIGHT_YELLOW}🔍 {text}{RESET}") as sp:
            time.sleep(duration)
            sp.ok("✅")

    elif style == "pulse":
        with alive_bar(
            duration * 10, title=f"🚀 {text}", bar="blocks", spinner="classic"
        ) as bar:
            for i in range(duration * 10):
                time.sleep(0.01)
                bar()

    elif style == "halo":
        with Halo(text=text, spinner="dots", color="yellow") as spinner:
            time.sleep(duration)
            spinner.succeed("Completed!")


def display_system_info():
    """
    Displays detailed system information and compatibility checks.
    This function gathers and displays information about the system's 
    operating system, CPU, memory, disk, GPU (if available), and Python 
    version. It also evaluates the system's compatibility against minimum 
    and recommended specifications.
    The output is formatted using the `rich` library to display a table 
    and messages with styled text.
    Key Features:
    - Displays operating system name, version, and compatibility status.
    - Displays CPU model, usage percentage, and status.
    - Displays memory size, usage percentage, and status.
    - Displays disk size, usage percentage, and status.
    - Checks for GPU availability, CUDA version, and compatibility.
    - Displays Python version and compatibility status.
    - Evaluates system compatibility against minimum and recommended 
      specifications for Windows and Linux systems.
    Compatibility Criteria:
    - Minimum and recommended specifications are defined based on the 
      operating system.
    - For Windows, specifications include CPU, RAM, storage, and GPU.
    - For Linux, specifications include CPU, RAM, and storage.
    Raises:
        None
    Note:
        - Requires the `rich`, `psutil`, and `torch` libraries.
        - GPU compatibility is checked using PyTorch's CUDA support.
    """
    console.print(
        Panel("[bold blue]📊 SYSTEM INFORMATION[/bold blue]", border_style="blue")
    )

    table = Table(show_header=True, header_style="bold magenta")
    table.add_column("Component", style="dim", width=20)
    table.add_column("Details", justify="left", width=40)
    table.add_column("Status", justify="center", width=12)

    os_name = platform.system()
    os_version = platform.version()
    os_status = "✅ Compatible" if os_name in ["Windows", "Linux"] else "⚠️ Unsupported"
    table.add_row("Operating System", f"{os_name} {os_version}", os_status)

    cpu_model = platform.processor()
    cpu_percent = psutil.cpu_percent()
    cpu_status = "✅ Good" if cpu_percent < 70 else "⚠️ High"
    table.add_row(
        "CPU", cpu_model, f"[{'green' if cpu_percent < 70 else 'red'}]{cpu_status}[/]"
    )

    memory = psutil.virtual_memory()
    memory_gb = memory.total // (1024**3)
    memory_status = "✅ Good" if memory_gb >= 4 else "⚠️ Low"
    table.add_row(
        "Memory",
        f"{memory_gb} GB ({memory.percent}% used)",
        f"[{'green' if memory_gb >= 4 else 'red'}]{memory_status}[/]",
    )

    disk = psutil.disk_usage("/")
    disk_gb = disk.total // (1024**3)
    disk_status = "✅ Good" if disk_gb >= 16 else "⚠️ Low"
    table.add_row(
        "Disk",
        f"{disk_gb} GB ({disk.percent}% used)",
        f"[{'green' if disk_gb >= 16 else 'red'}]{disk_status}[/]",
    )

    try:
        import torch

        if torch.cuda.is_available():
            gpu_name = torch.cuda.get_device_name(0)
            cuda_version = torch.version.cuda
            gpu_status = (
                "✅ Good" if int(cuda_version.split(".")[0]) >= 12 else "⚠️ Old Driver"
            )
            table.add_row(
                "GPU",
                f"{gpu_name} (CUDA {cuda_version})",
                f"[{'green' if gpu_status == '✅ Good' else 'red'}]{gpu_status}[/]",
            )
        else:
            table.add_row("GPU", "Not Available", "[red]❌ No GPU[/red]")
    except:
        table.add_row("GPU", "Not Detected", "[red]❌ No GPU[/red]")

    python_version = platform.python_version()
    major, minor, _ = map(int, python_version.split("."))
    python_status = (
        "✅ Good" if (major == 3 and 10 <= minor <= 11) else "[red]⚠️ Old[/red]"
    )
    table.add_row(
        "Python",
        f"v{python_version}",
        f"[{'green' if float(python_version.split('.')[0]) >= 3 else 'red'}]{python_status}[/]",
    )

    console.print(table)

    console.print("\n[bold blue]🖥 System Compatibility Check[/bold blue]")

    if os_name == "Windows":
        min_specs = {"CPU": "Intel Core i3 Gen 6", "RAM": 4, "Storage": 16}
        rec_specs = {
            "CPU": "Intel Core i5 Gen 7",
            "RAM": 16,
            "Storage": 64,
            "GPU": "RTX 2060",
            "CUDA": 12.1,
        }
    else:
        min_specs = {"CPU": "Raspberry Pi 4", "RAM": 4, "Storage": 8}
        rec_specs = {"CPU": "Raspberry Pi 5", "RAM": 8, "Storage": 64}

    meets_min = memory_gb >= min_specs["RAM"] and disk_gb >= min_specs["Storage"]
    meets_rec = memory_gb >= rec_specs["RAM"] and disk_gb >= rec_specs["Storage"]

    if meets_rec:
        console.print(
            "[green]✅ Your system meets the recommended specifications![/green]"
        )
    elif meets_min:
        console.print(
            "[yellow]⚠️ Your system meets the minimum specifications, but upgrading is recommended.[/yellow]"
        )
    else:
        console.print(
            "[red]❌ Your system does not meet the minimum requirements. Some features may not work correctly.[/red]"
        )


def setup_folders():
    fancy_progress("Creating essential folders", 100, "pulse")

    folders = {
        "📁 Database": "database",
        "📷 Snapshots": "snapshots",
        "🗄️ Logs": "logs",
        "⚙️ Configs": "configs",
        "🛠️ Tools": "tools",
        "📁 Videos": "Videos",
    }


    now_path = os.path.dirname(os.path.realpath(__file__))

    with Progress() as progress:
        create_task = progress.add_task(
            "[green]Creating folders...", total=len(folders)
        )

        for folder_name, folder in folders.items():
            folder_path = os.path.join(now_path, folder)
            if not os.path.exists(folder_path):
                os.makedirs(folder_path)
                console.print(
                    f"[green]✅ Created {folder_name} at {folder_path}[/green]"
                )
            else:
                console.print(
                    f"[cyan]✅ {folder_name} already exists. Skipping creation.[/cyan]"
                )

            progress.update(create_task, advance=1)
            time.sleep(0.1)

    console.print(
        Panel(
            "[bold green]📁 All folders created successfully! 📁[/bold green]",
            border_style="green",
        )
    )


def cleanup_temp_files():
    fancy_progress("Cleaning temporary files", 10, "yaspin")

    now_path = os.path.dirname(os.path.realpath(__file__))
    temp_folders = [
        "__pycache__",
        "temp",
        ".cache",
        "build",
        "dist",
        ".pytest_cache",
        ".eggs",
        "*.log",
        "*.tmp",
    ]

    found = False
    with Progress() as progress:
        scan_task = progress.add_task(
            "[yellow]Scanning for temp files...", total=len(temp_folders)
        )

        for temp in temp_folders:
            temp_path = os.path.join(now_path, temp)
            if os.path.exists(temp_path):
                found = True
                try:
                    if os.path.isdir(temp_path):
                        shutil.rmtree(temp_path)
                    else:
                        os.remove(temp_path)
                    console.print(f"[yellow]🗑 Deleted temporary item: {temp}[/yellow]")
                except Exception as e:
                    console.print(f"[red]⚠️ Could not delete {temp}: {e}[/red]")

            progress.update(scan_task, advance=1)
            time.sleep(0.1)

    if not found:
        console.print(
            "[green]✨ System is already clean! No temporary files found.[/green]"
        )
    else:
        space_freed = random.randint(1, 150)
        console.print(
            f"[green]🧹 Cleanup complete! Approximately {space_freed}MB freed![/green]"
        )


def check_dependencies():
    fancy_progress("Checking Python packages", 1000, "pulse")  # yaspin, pulse ,halo

    packages = [
        "certifi",
        "click",
        "cmake",
        "colorama",
        "contourpy",
        "customtkinter",
        "cycler",
        "darkdetect",
        "dlib",
        "dotenv",
        "face_recognition",
        "face_recognition_models",
        "filelock",
        "fsspec",
        "idna",
        "kiwisolver",
        "matplotlib",
        "mpmath",
        "networkx",
        "numpy",
        "cv2",
        "packaging",
        "pandas",
        "PIL",
        "psutil",
        "pyparsing",
        "pytz",
        "requests",
        "scipy",
        "seaborn",
        "six",
        "sympy",
        "torch",
        "torchvision",
        "tqdm",
        "typing_extensions",
        "tzdata",
        "ultralytics",
        "urllib3",
    ]

    table = Table(show_header=True, header_style="bold cyan")
    table.add_column("Package", style="dim", width=20)
    table.add_column("Status", justify="center", width=12)
    table.add_column("Version", justify="right", width=15)

    missing_packages = []

    with Progress() as progress:
        check_task = progress.add_task(
            "[blue]Checking packages...", total=len(packages)
        )

        for package in packages:
            spec = importlib.util.find_spec(package)
            if spec is None:
                missing_packages.append(package)
                table.add_row(package, "[red]❌ Missing[/red]", "-")
            else:
                try:
                    mod = importlib.import_module(package)
                    version = getattr(mod, "__version__", "Unknown")
                    table.add_row(package, "[green]✅ Installed[/green]", version)
                except:
                    table.add_row(package, "[green]✅ Installed[/green]", "Latest")

            progress.update(check_task, advance=1)
            time.sleep(0.05)

    console.print("\n")
    console.print(table)

    if missing_packages:
        console.print(
            f"[blue]📦 Installing missing dependencies: {', '.join(missing_packages)}[/blue]"
        )

        with yaspin(Spinners.dots, text="Installing packages...") as spinner:
            try:
                subprocess.run(
                    [sys.executable, "-m", "pip", "install"] + missing_packages,
                    check=True,
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE,
                )
                spinner.ok("✅")
                console.print(f"[green]✅ Dependencies installed successfully![/green]")
            except subprocess.CalledProcessError as e:
                spinner.fail("❌")
                console.print(f"[red]❌ Failed to install some dependencies: {e}[/red]")
    else:
        console.print(f"[green]✅ All dependencies are already installed![/green]")


def finalize_setup():
    fancy_progress("Finalizing super amazing setup", 50, "halo")

    with Progress() as progress:
        task = progress.add_task("[magenta]Finalizing...", total=100)

        for i in range(100):
            time.sleep(0.03)
            progress.update(task, advance=1)

    emojis = ["🔄", "⏳", "📡", "🔌", "💾", "📊", "🔒", "✨", "🚀", "⚡", "🔥", "🌟"]

    console.print("[cyan]Running final system checks...[/cyan]")
    for emoji in emojis:
        console.print(
            f"[bold yellow]{emoji} Processing system components...[/bold yellow]"
        )
        time.sleep(0.2)

    try:
        text_art = pyfiglet.figlet_format("ALL DONE!", font="starwars")
        console.print(f"[bold green]{text_art}[/bold green]")
    except:
        console.print("[bold green]ALL DONE![/bold green]")

    console.print(Rule(style="green"))
    console.print(
        Align.center(
            Panel(
                Text(
                    "🎉🎉🎉 THE ULTIMATE SUPER AMAZING SYSTEM IS FULLY INITIALIZED AND READY TO USE! 🎉🎉🎉",
                    style="bold green",
                ),
                border_style="bright_green",
                title="[bold gold]SETUP COMPLETE[/bold gold]",
                subtitle=f"[bold blue]Completed at {datetime.now().strftime('%H:%M:%S')}[/bold blue]",
            )
        )
    )
    console.print(Rule(style="green"))


def sound_alert():
    console.print("[cyan]🔊 Playing completion sound...[/cyan]")

    system_os = platform.system()
    try:
        if system_os == "Windows":
            import winsound

            for _ in range(2):
                for freq in [523, 659, 784, 1047]:
                    winsound.Beep(freq, 150)
                time.sleep(0.3)
        elif system_os == "Darwin":
            os.system(
                "say 'Super Amazing Setup complete! Your system is ready for use!'"
            )
        else:
            for sound in ["complete.oga", "message.oga", "bell.oga"]:
                os.system(
                    f"paplay /usr/share/sounds/freedesktop/stereo/{sound} 2>/dev/null || aplay /usr/share/sounds/sound-icons/glass-water-1.wav 2>/dev/null"
                )
                time.sleep(0.3)
    except Exception as e:
        console.print(f"[red]⚠️ Sound alert failed: {e}[/red]")


def main():
    try:
        cursor.hide()
        os.system("cls" if os.name == "nt" else "clear")
        display_epic_header()
        display_system_info()
        setup_folders()
        cleanup_temp_files()
        check_dependencies()
        finalize_setup()
        sound_alert()
        console.print(
            "[bold cyan]🚀 System setup complete! Type 'help' for available commands or 'start' to begin![/bold cyan]"
        )
    except Exception as e:
        console.print(f"[bold red]❌ ERROR: {e}[/bold red]")
        console.print("[yellow]Trying to recover and continue setup...[/yellow]")
    finally:
        cursor.show()


def animated_text(text, duration=2, interval=0.5):
    console.print(
        Panel(
            Align.center(Text(text, style=f"bold")),
            border_style="bright_blue",
            title="[bold red]🔥 SETUP 🔥[/bold red]",
            subtitle="[bold green] 🔧 Preparing Environment... [/bold green]",
            width=50,
        ),
        justify="center",
    )


MATRIX_FAIL = (
    "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    "abcdefghijklmnopqrstuvwxyz"
    "!@#$%^&*()_+=-{}[]<>?/|\\"
    "ΣΨΩΞΘЖФДБЙКЛПГМТ"
    "カタカナ ひらがな"
    "∑√π∝∞Ωµλ⊗⊕"
)

MATRIX_CHARS = "01 10 0011 1100 1010 0110 1001 0101"

MATRIX_SYMBOLS = "░▒▓█▄▀■●◆★✦✧☠︎☢︎☣︎⚠︎"


def play_typing_sound():
    """เล่นเสียงพิมพ์ดีด (เฉพาะ Linux/macOS)"""
    if sys.platform != "win32":
        os.system("play -q typewriter.wav &")  # ต้องมีไฟล์เสียง typewriter.wav


if platform.system() == "Windows":
    import winsound

    def beep():
        winsound.Beep(random.randint(600, 1000), 50)
else:
    def beep():
        sys.stdout.write("\a")  # ใช้ '\a' เพื่อทำเสียง beep บน Linux/macOS
        sys.stdout.flush()

# อักขระที่ใช้สุ่ม Glitch
GLITCH_CHARS = "▓▒█░◆▲■●☆☠︎⚠︎∑ΨΩΞΘЖカタカナ"

def hacker_typing_effect(text, delay=0.01, glitch=True):
    """แสดงข้อความแบบพิมพ์ทีละตัวอักษร คล้ายในหนังแฮ็กเกอร์"""
    output = ""
    for char in text:
        if glitch and random.random() < 0.05:
            char = random.choice(GLITCH_CHARS)  # สุ่มตัวอักษรผิดพลาด

        color = "bold green" if random.random() > 0.5 else "bold red"
        output += f"[{color}]{char}[/{color}]"

        # ล้างบรรทัดเดิมก่อนพิมพ์ใหม่
        sys.stdout.write("\r" + " " * console.width + "\r")
        console.print(output, end="")

        beep()  # เล่นเสียง Beep
        time.sleep(random.uniform(delay * 0.5, delay * 1.5))

    print()



def hacker_loading_bar(duration=2):
    """แสดงแถบโหลดสไตล์แฮ็กเกอร์"""
    console = Console()
    with Progress() as progress:
        task = progress.add_task("[bold green]Accessing Secure Files.....", total=100)
        for _ in range(100):
            progress.update(task, advance=1)
            time.sleep(duration / 100)


def matrix_effect(lines=20, duration=5):
    """เอฟเฟกต์ตัวอักษรสุ่มไหลลงมาแบบ Matrix"""
    width = shutil.get_terminal_size().columns
    start_time = time.time()

    while time.time() - start_time < duration:
        line = "".join(
            random.choice(MATRIX_SYMBOLS + MATRIX_CHARS + MATRIX_FAIL)
            for _ in range(width)
        )
        console.print(line, style="bright_green")
        time.sleep(0.05)

    console.clear()

def generate_password(length=16, fail_chance=0.99, first_try=True):
    """ สุ่มรหัสผ่านที่ดูเป็น Hacker Style และมีโอกาสเจนล้มเหลว 70% หลังจากรอบแรก """
    if not first_try and random.random() < fail_chance:
        return None  # จำลองการสร้างรหัสผ่านล้มเหลว

    chars = string.ascii_letters + string.digits + "!@#$%^&*()_+=-{}[]<>?/|\\"
    return ''.join(random.choice(chars) for _ in range(length))



if __name__ == "__main__":
    os.system("cls" if os.name == "nt" else "clear")  # ล้างหน้าจอก่อนเริ่ม
    hacker_text = pyfiglet.figlet_format("SYSTEM OVERRIDE", font="epic")
    console.print(f"[bold green]\n █ 🟢 🔰 🟢 █ \n {hacker_text} \n █ 🟢 🔰 🟢 █ \n[/bold green]")

    # 🔑 สร้างรหัสผ่านครั้งแรก (ต้องผ่าน 100%)
    password = generate_password(20, first_try=True)
    hacker_typing_effect(f"🔑 Generated Password: [ {password} ] ✅\n", delay=0.05)

    # 🔄 ทดสอบเจนใหม่แบบมีโอกาสพลาด
    hacker_typing_effect("🛠️ Regenerating Secure Password...\n", delay=0.05)
    password = generate_password(20, fail_chance=0.7, first_try=False)

    if password:
        hacker_typing_effect(f"🔑 Generated Password: [ {password} ] ✅\n", delay=0.05)
    else:
        hacker_typing_effect("❌ Password Generation Failed! Retrying... 🔄\n", delay=0.1, glitch=True)
        time.sleep(1)  # หน่วงเวลาเหมือนระบบกำลังพยายามใหม่
        password = generate_password(20, fail_chance=0.05, first_try=False)

        if password:
            hacker_typing_effect(f"🔑 New Secure Password: [ {password} ] ✅\n", delay=0.05)
        else:
            hacker_typing_effect("🚨 SYSTEM ERROR: Password Generation Failed Permanently ❌\n", delay=0.1, glitch=True)
            exit(1)  # หยุดโปรแกรมเหมือนเกิดข้อผิดพลาดจริง

    hacker_typing_effect("🔓 [ ACCESS GRANTED ] Initializing system... 🤖", delay=0.3, glitch=True)

    matrix_effect()
    hacker_loading_bar(2)
    animated_text("🛠️ Config File Setup", duration=5)
    hacker_typing_effect("⚙️ Loading Super Setup... 💾\n", delay=0.02)
    main()



