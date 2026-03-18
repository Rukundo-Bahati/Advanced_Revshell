#!/usr/bin/env python3
"""
Tetris Security Demo - Cleanup Tool
Rwanda Coding Academy - Defending Rwanda Cyberspace 

This tool removes all persistence mechanisms installed by the Tetris game.
Use this to clean up after the security demonstration.

FOR EDUCATIONAL AND AUTHORIZED TESTING ONLY
"""

import os
import sys
import json
import shutil
import platform
import subprocess
from pathlib import Path

# Platform detection
IS_WINDOWS = platform.system() == "Windows"
IS_LINUX = platform.system() == "Linux"

# Configuration - must match the main game
PERSISTENCE_NAME = "SystemAudioService"


def get_startup_path():
    """Get the appropriate startup/autostart directory for the current platform."""
    if IS_WINDOWS:
        startup_path = Path(os.environ.get("APPDATA", "")) / "Microsoft" / "Windows" / "Start Menu" / "Programs" / "Startup"
        return startup_path
    elif IS_LINUX:
        autostart_path = Path.home() / ".config" / "autostart"
        return autostart_path
    return None


def get_script_path():
    """Get the path where persistence files are stored."""
    if IS_WINDOWS:
        base_path = Path(os.environ.get("APPDATA", "")) / "Microsoft" / "Windows" / "System Audio Service"
    elif IS_LINUX:
        base_path = Path.home() / ".config" / ".system-audio-service"
    else:
        base_path = Path.home() / ".tetris-persistence"
    
    return base_path


def check_persistence_status():
    """Check if persistence is currently installed."""
    script_path = get_script_path()
    info_file = script_path / "persistence_info.json"
    
    if info_file.exists():
        return True, str(script_path)
    
    # Also check for any startup entries
    startup_path = get_startup_path()
    if startup_path:
        if IS_WINDOWS:
            startup_link = startup_path / f"{PERSISTENCE_NAME}.lnk"
            if startup_link.exists():
                return True, str(startup_link)
        elif IS_LINUX:
            desktop_file = startup_path / f"{PERSISTENCE_NAME}.desktop"
            if desktop_file.exists():
                return True, str(desktop_file)
    
    return False, None


def remove_persistence():
    """
    Remove all persistence mechanisms installed by the Tetris game.
    """
    print("=" * 70)
    print("TETRIS SECURITY DEMO - CLEANUP TOOL")
    print("Rwanda Coding Academy - Defending Rwanda Cyberspace")
    print("=" * 70)
    print()
    
    # Check if persistence exists
    is_persistent, location = check_persistence_status()
    
    if not is_persistent:
        print("[✓] No persistence mechanisms found.")
        print("    Your system is already clean.")
        print()
        return True
    
    print(f"[!] Persistence detected at: {location}")
    print()
    print("The following will be removed:")
    print("  - Startup/autostart entries")
    print("  - Registry entries (Windows)")
    print("  - Cron jobs (Linux)")
    print("  - Persistence directory and all files")
    print()
    
    # Get confirmation
    while True:
        response = input("Do you want to remove all persistence mechanisms? (yes/no): ").strip().lower()
        if response in ['yes', 'y']:
            break
        elif response in ['no', 'n']:
            print()
            print("Cleanup cancelled. Persistence remains active.")
            return False
        else:
            print("Please enter 'yes' or 'no'")
    
    print()
    print("[*] Starting cleanup process...")
    print()
    
    success = True
    removed_items = []
    
    try:
        script_path = get_script_path()
        info_file = script_path / "persistence_info.json"
        
        if info_file.exists():
            try:
                persistence_info = json.loads(info_file.read_text())
            except json.JSONDecodeError:
                print("[!] Warning: Could not parse persistence info file")
                persistence_info = {}
        else:
            persistence_info = {}
        
        # Remove Windows startup entries
        if IS_WINDOWS:
            startup_path = get_startup_path()
            startup_link = startup_path / f"{PERSISTENCE_NAME}.lnk"
            
            if startup_link.exists():
                try:
                    startup_link.unlink()
                    removed_items.append(f"Startup shortcut: {startup_link}")
                    print("[✓] Removed Windows startup shortcut")
                except Exception as e:
                    print(f"[!] Failed to remove startup shortcut: {e}")
                    success = False
            
            # Remove registry entry
            try:
                reg_command = f'reg delete HKCU\\Software\\Microsoft\\Windows\\CurrentVersion\\Run /v "{PERSISTENCE_NAME}" /f'
                result = subprocess.run(reg_command, shell=True, capture_output=True, text=True)
                if result.returncode == 0:
                    removed_items.append("Registry Run key")
                    print("[✓] Removed Windows registry entry")
            except Exception as e:
                print(f"[!] Failed to remove registry entry: {e}")
                # Don't mark as failed since registry entry might not exist
        
        # Remove Linux startup entries
        elif IS_LINUX:
            startup_path = get_startup_path()
            if startup_path:
                desktop_file = startup_path / f"{PERSISTENCE_NAME}.desktop"
                
                if desktop_file.exists():
                    try:
                        desktop_file.unlink()
                        removed_items.append(f"Autostart entry: {desktop_file}")
                        print("[✓] Removed Linux autostart entry")
                    except Exception as e:
                        print(f"[!] Failed to remove autostart entry: {e}")
                        success = False
            
            # Remove cron job
            try:
                # Remove any cron jobs containing the persistence name
                subprocess.run(
                    f'crontab -l 2>/dev/null | grep -v "{PERSISTENCE_NAME}" | crontab -',
                    shell=True,
                    check=True,
                    capture_output=True
                )
                removed_items.append("Cron job")
                print("[✓] Removed cron job")
            except subprocess.CalledProcessError:
                # Cron might not exist or already clean
                pass
            except Exception as e:
                print(f"[!] Note: Could not check/remove cron job: {e}")
        
        # Remove persistence directory
        if script_path.exists():
            try:
                shutil.rmtree(script_path)
                removed_items.append(f"Persistence directory: {script_path}")
                print("[✓] Removed persistence directory")
            except Exception as e:
                print(f"[!] Failed to remove persistence directory: {e}")
                success = False
        
        # Check for any remaining Python processes running the game in background
        print()
        print("[*] Checking for background processes...")
        try:
            if IS_WINDOWS:
                # Find and terminate python processes running tetris-game.py or tetris_complete.py
                ps_cmd = f'taskkill /F /FI "WINDOWTITLE eq Tetris*" 2>nul'
                subprocess.run(ps_cmd, shell=True, capture_output=True)
                
                # More aggressive: kill python processes with specific arguments
                ps_cmd = f'tasklist /FI "IMAGENAME eq python.exe" /FO CSV 2>nul'
                result = subprocess.run(ps_cmd, shell=True, capture_output=True, text=True)
                if "tetris" in result.stdout.lower():
                    print("[!] Warning: Python processes with 'tetris' in command line detected")
                    print("    Please close them manually or restart your computer")
            
            elif IS_LINUX:
                # Find python processes running tetris
                ps_cmd = f"ps aux | grep -i tetris | grep -v grep | grep -v {os.getpid()}"
                result = subprocess.run(ps_cmd, shell=True, capture_output=True, text=True)
                if result.stdout.strip():
                    print("[!] Warning: Tetris-related processes detected:")
                    print(result.stdout)
                    print("    These should be terminated if they're the background shell")
        except Exception as e:
            print(f"[!] Note: Could not check for background processes: {e}")
        
        print()
        print("=" * 70)
        print("CLEANUP SUMMARY")
        print("=" * 70)
        print()
        
        if removed_items:
            print("Removed the following items:")
            for item in removed_items:
                print(f"  ✓ {item}")
        else:
            print("No items were found to remove.")
        
        print()
        
        if success:
            print("[✓] Cleanup completed successfully!")
            print()
            print("Your system has been cleaned of all Tetris persistence mechanisms.")
            print()
            print("Additional recommendations:")
            print("  - Restart your computer to ensure all changes take effect")
            print("  - Check your startup programs if you're concerned about other persistence")
            print()
        else:
            print("[!] Cleanup completed with some errors.")
            print()
            print("Some items could not be removed automatically.")
            print("You may need to remove them manually or restart your computer.")
            print()
        
        return success
        
    except Exception as e:
        print(f"[!] Unexpected error during cleanup: {e}")
        return False


def show_help():
    """Display help information about the cleanup tool."""
    print("""
Tetris Security Demo - Cleanup Tool
====================================

This tool removes all persistence mechanisms installed by the Tetris
cybersecurity education demo.

USAGE:
    python cleanup_tool.py

WHAT IT DOES:
    1. Removes startup/autostart entries
    2. Removes Windows registry entries (if on Windows)
    3. Removes Linux cron jobs (if on Linux)
    4. Deletes the persistence directory and all files
    5. Checks for and warns about background processes

WHEN TO USE:
    - After completing the cybersecurity demonstration
    - If you want to remove all traces of the demo
    - Before uninstalling Python or removing the game files

SAFETY:
    - This tool only removes files created by the Tetris demo
    - It will not affect other programs or system settings
    - It asks for confirmation before making changes

For more information, see the project documentation.
""")


def main():
    """Main entry point for the cleanup tool."""
    # Check for help flag
    if len(sys.argv) > 1 and sys.argv[1] in ['-h', '--help', 'help']:
        show_help()
        return
    
    # Run cleanup
    success = remove_persistence()
    
    # Exit with appropriate code
    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()
