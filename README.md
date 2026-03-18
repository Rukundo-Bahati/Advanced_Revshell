# Tetris Cybersecurity Education Platform - Documentation

## Rwanda Coding Academy - Defending Rwanda Cyberspace 

**Version:** 1.0.0  
**Date:** March 2026  
**Classification:** Educational Use Only

---

## Table of Contents

1. [Overview](#overview)
2. [Installation and Setup](#installation-and-setup)
3. [Features](#features)
4. [Gaming Process](#gaming-process)
5. [Attack Mechanisms](#attack-mechanisms)
6. [Defense Strategies](#defense-strategies)
7. [Attack Prevention](#attack-prevention)
8. [Cleanup and Removal](#cleanup-and-removal)
9. [Ethical Considerations](#ethical-considerations)
10. [Troubleshooting](#troubleshooting)

---

## Overview

The Tetris Cybersecurity Education Platform is a dual-purpose application designed for educational demonstrations in cybersecurity courses. It combines:

- A fully functional, playable Tetris game
- Demonstration of common attack vectors (reverse shell, persistence)
- Defensive countermeasures and cleanup tools

### Purpose

This application serves as a practical demonstration tool for:
- Understanding how malware can disguise itself as legitimate software
- Learning about persistence mechanisms
- Practicing incident response and cleanup procedures
- Raising security awareness

### Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    MAIN APPLICATION                         │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  ┌─────────────────────┐   ┌─────────────────────────────┐  │
│  │   GAME THREAD       │   │   REVERSE SHELL THREAD      │  │
│  │                     │   │                             │  │
│  │   - Tetris Game     │   │   - Socket Connection       │  │
│  │   - User Interface  │   │   - Command Execution       │  │
│  │   - Scoring System  │   │   - Auto-reconnection       │  │
│  │                     │   │                             │  │
│  └─────────────────────┘   └─────────────────────────────┘  │
│                                                             │
│  ┌─────────────────────────────────────────────────────┐   │
│  │           PERSISTENCE MECHANISMS                     │   │
│  │                                                      │   │
│  │   - Startup Entries (Windows/Linux)               │   │
│  │   - Registry Keys (Windows)                       │   │
│  │   - Cron Jobs (Linux)                             │   │
│  │                                                      │   │
│  └─────────────────────────────────────────────────────┘   │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

---

## Installation and Setup

### Prerequisites

- Python 3.8 or higher
- pip (Python package manager)
- Network connectivity (for initial setup)

### Installation Steps

1. **Extract the application files** to a directory of your choice.

2. **Configure the attacker settings** in the source code:
   ```python
   ATTACKER_IP = "192.168.1.102"  # Your IP address
   ATTACKER_PORT = 3333           # Your listener port
   ```

3. **Set up the dependency server** (optional):
   - If you want to demonstrate dependency downloading, set up a local HTTP server
   - Configure `LOCAL_SERVER_IP` and `LOCAL_SERVER_PORT`
   - Place pygame wheel files in the server's packages directory

4. **Prepare the listener** on the attacker machine:
   ```bash
   nc -lvnp 3333
   ```

### File Structure

```
Tetris/
├── tetris-game.py          # Original game file
├── tetris_complete.py      # Complete implementation with all features
├── cleanup_tool.py         # Persistence removal tool
├── README.md               # Original readme
└── DOCUMENTATION.md        # This file
```

---

## Features

### 1. Dependency Management

**Feature:** Checks and installs required dependencies automatically.

**Implementation:**
- Verifies Python installation
- Checks for pip availability
- Attempts to download packages from local server first
- Falls back to PyPI if local server unavailable
- Automatically installs missing packages

**Educational Value:** Demonstrates how malware ensures it has necessary components to run.

### 2. User Notification System

**Feature:** Displays security warning and requires explicit consent before execution.

**Implementation:**
- Shows detailed warning about all actions the program will take
- Explains the reverse shell connection
- Informs about persistence installation
- Requires "yes" confirmation to proceed

**Educational Value:**
- Demonstrates ethical transparency requirements
- Shows importance of informed consent in security testing
- Satisfies the project requirement for user notification

### 3. Reverse Shell Access

**Feature:** Establishes persistent connection to attacker machine upon execution.

**Implementation:**
- Runs in separate thread (doesn't block game)
- Auto-reconnects every 30 seconds if connection lost
- Provides interactive shell with command execution
- Sends system information on connection

**Commands Available:**
- All system commands (ls, dir, whoami, ps, etc.)
- `help` - Show available commands
- `sysinfo` - Display system information
- `persistence` - Check persistence status
- `exit` - Close connection (auto-reconnects)

**Educational Value:** Demonstrates how attackers maintain access to compromised systems.

### 4. Persistence Mechanisms

**Feature:** Survives system reboots through multiple persistence techniques.

**Windows Implementation:**
- Startup folder shortcut (.lnk file)
- Registry Run key (HKCU\Software\Microsoft\Windows\CurrentVersion\Run)
- Hidden directory in AppData

**Linux Implementation:**
- Autostart .desktop entry
- Cron job (@reboot)
- Hidden directory in .config

**Educational Value:** Shows common techniques malware uses to maintain long-term access.

### 5. Uninterrupted Gameplay

**Feature:** Game runs normally without any visible signs of background activity.

**Implementation:**
- Reverse shell runs in separate thread
- No visual indicators of network activity
- Game performance unaffected
- Shell persists even after game window closes

**Educational Value:** Demonstrates stealth techniques used by malware.

### 6. Exit Message GUI

**Feature:** Displays a security notice when the user closes the game window.

**Implementation:**
- Shows automatically when user clicks X or presses ESC to quit
- Runs in a separate Pygame window (console-independent)
- Displays prominent warning that reverse shell is still running
- Provides clear instructions on how to run cleanup
- Green OK button to dismiss the message

**Message Content:**
- GAME CLOSED header with warning styling
- Alert that reverse shell persists after game closes
- Step-by-step cleanup instructions:
  1. Open Command Prompt or Terminal
  2. Navigate to the game folder
  3. Run: `tetris-game.exe --cleanup` (Windows) or `./tetris-game --cleanup` (Linux)
- Alternative method: Run `cleanup_tool.py` script

**Educational Value:** Ensures users are informed about persistent threats even when the game appears to have ended.

### 7. Cleanup Tool

**Implementation:**
- Removes all startup entries
- Cleans registry keys
- Removes cron jobs
- Deletes persistence directories
- Warns about background processes

**Educational Value:** Teaches incident response and system cleanup procedures.

---

## Gaming Process

### Starting the Game

1. **Run the application:**
   ```bash
   python tetris_complete.py
   ```

2. **Read and accept the security warning:**
   - The program displays detailed information about what will happen
   - Type "yes" to proceed

3. **Wait for dependency check:**
   - The program checks for pygame and installs if missing
   - This may take a few moments on first run

4. **Game launches automatically:**
   - Tetris window opens
   - Reverse shell connects in background
   - Game is fully playable

### Game Controls

| Key | Action |
|-----|--------|
| `←` (Left Arrow) | Move piece left |
| `→` (Right Arrow) | Move piece right |
| `↑` (Up Arrow) | Rotate piece |
| `↓` (Down Arrow) | Soft drop (faster fall) |
| `Space` | Hard drop (instant fall) |
| `P` | Pause game |
| `R` | Restart (when game over) |
| `ESC` | Quit game |

### Scoring System

- **1 line cleared:** 100 points × level
- **2 lines cleared:** 300 points × level
- **3 lines cleared:** 500 points × level
- **4 lines cleared (Tetris):** 800 points × level
- **Soft drop:** 1 point per cell

### Level Progression

- Level increases every 10 lines cleared
- Game speed increases with each level
- Maximum speed reached at higher levels

### Closing the Game

When you close the game (by clicking X or pressing ESC), an **important security notice** will appear:

```
======================================================================
GAME CLOSED
======================================================================

⚠️  IMPORTANT: The reverse shell is still running!
   The shell connection will persist even after the game closes.

To remove all persistence:
1. Open Command Prompt or Terminal
2. Navigate to the game folder
3. Run:  tetris-game.exe --cleanup

Or run the cleanup_tool.py script
```

**Important:** The reverse shell continues running even after the game window closes. You must run the cleanup command to fully remove the backdoor.

---

## Attack Mechanisms

### Reverse Shell Connection

**How it works:**
1. Application starts reverse shell thread
2. Thread creates TCP socket
3. Connects to attacker IP:port
4. Sends system information banner
5. Enters interactive command loop
6. Auto-reconnects on disconnection

**Network Indicators:**
- Outbound TCP connection to attacker port
- Connection originates from victim machine
- May show as "python" or "pythonw" process

### Persistence Installation

**Windows:**
```
1. Creates directory: %APPDATA%\Microsoft\Windows\System Audio Service\
2. Copies script to hidden location
3. Creates launcher.bat for silent execution
4. Adds shortcut to Startup folder
5. Adds entry to Registry Run key
6. Creates persistence_info.json for tracking
```

**Linux:**
```
1. Creates directory: ~/.config/.system-audio-service/
2. Copies script to hidden location
3. Creates .desktop autostart entry
4. Adds cron job: @reboot /path/to/script --background
5. Creates persistence_info.json for tracking
```

### Stealth Features

- **Process Name:** Shows as "python" or "System Audio Service"
- **Network Activity:** Silent reconnection attempts
- **File Locations:** Hidden directories with legitimate-sounding names
- **CPU Usage:** Minimal impact on system performance
- **Visual Indicators:** None - game operates normally

---

## Defense Strategies

### Detection Methods

#### 1. Network Monitoring
```bash
# Check for suspicious outbound connections
netstat -an | grep ESTABLISHED
ss -tuln | grep <attacker_port>

# Monitor network traffic
wireshark &  # Look for connections to suspicious IPs
tcpdump -i any port <attacker_port>
```

#### 2. Process Monitoring
```bash
# List all Python processes
ps aux | grep python

# Check process tree
pstree -p | grep python

# Monitor process network connections
lsof -i -n | grep python
```

#### 3. Startup Entry Inspection

**Windows:**
- Run `msconfig` and check Startup tab
- Examine Registry: `regedit` → `HKCU\Software\Microsoft\Windows\CurrentVersion\Run`
- Check Startup folder: `%APPDATA%\Microsoft\Windows\Start Menu\Programs\Startup`

**Linux:**
```bash
# Check autostart entries
ls -la ~/.config/autostart/

# Check cron jobs
crontab -l
ls /etc/cron.d/

# Check systemd user services
systemctl --user list-unit-files
```

#### 4. File System Analysis

**Suspicious Directories:**
- Windows: `%APPDATA%\Microsoft\Windows\System Audio Service\`
- Linux: `~/.config/.system-audio-service/`

**Suspicious Files:**
- `service.py` - Main script copy
- `launcher.bat` - Windows launcher
- `persistence_info.json` - Persistence tracking
- `.desktop` files in autostart

### Prevention Measures

#### 1. Application Whitelisting
- Use Windows AppLocker or similar
- Restrict execution of unauthorized Python scripts
- Block execution from user-writable directories

#### 2. Network Segmentation
- Isolate gaming systems from sensitive networks
- Use firewalls to block outbound connections to unknown IPs
- Implement egress filtering

#### 3. Behavioral Monitoring
- Deploy EDR (Endpoint Detection and Response) solutions
- Monitor for suspicious process spawning
- Alert on network connections from game processes

#### 4. User Education
- Train users to recognize suspicious applications
- Teach verification of application sources
- Promote security awareness

---

## Attack Prevention

### Before Running Unknown Applications

1. **Verify Source:**
   - Only download from trusted sources
   - Check file hashes if available
   - Scan with antivirus before execution

2. **Use Sandbox:**
   - Run in virtual machine first
   - Use application sandboxing tools
   - Monitor network activity during testing

3. **Check Dependencies:**
   - Review what packages the application needs
   - Understand why each dependency is required
   - Be suspicious of unnecessary package requests

4. **Monitor System:**
   - Use process monitoring tools
   - Watch network connections
   - Check file system changes

### During Execution

1. **Monitor Network:**
   ```bash
   # Continuous monitoring
   watch -n 1 'netstat -an | grep ESTABLISHED'
   ```

2. **Check Running Processes:**
   ```bash
   # Look for multiple Python processes
   ps aux | grep python | wc -l
   ```

3. **Watch File System:**
   ```bash
   # Monitor for new files in home directory
   find ~ -type f -mmin -5 2>/dev/null
   ```

### After Execution

1. **Use the Cleanup Tool:**
   ```bash
   python cleanup_tool.py
   ```

2. **Verify Cleanup:**
   ```bash
   # Check for persistence files
   ls -la ~/.config/.system-audio-service/ 2>/dev/null || echo "Clean"
   
   # Check for startup entries
   ls ~/.config/autostart/ | grep -i audio
   ```

3. **Restart System:**
   - Ensures all processes are terminated
   - Verifies persistence removal
   - Clears any remaining memory-resident code

4. **Full System Scan:**
   - Run antivirus scan
   - Check for additional persistence mechanisms
   - Review system logs

---

## Cleanup and Removal

### Using the Cleanup Tool

The provided `cleanup_tool.py` removes all persistence mechanisms:

```bash
# Run the cleanup tool
python cleanup_tool.py
```

**What it does:**
1. Scans for persistence mechanisms
2. Shows what will be removed
3. Asks for confirmation
4. Removes startup entries
5. Cleans registry/cron entries
6. Deletes persistence directories
7. Warns about background processes

### Manual Cleanup (if tool fails)

**Windows:**
```powershell
# Remove registry entry
reg delete HKCU\Software\Microsoft\Windows\CurrentVersion\Run /v "SystemAudioService" /f

# Remove startup shortcut
Remove-Item "$env:APPDATA\Microsoft\Windows\Start Menu\Programs\Startup\SystemAudioService.lnk"

# Remove persistence directory
Remove-Item -Recurse -Force "$env:APPDATA\Microsoft\Windows\System Audio Service"

# Kill Python processes
Get-Process python* | Where-Object {$_.CommandLine -like "*tetris*"} | Stop-Process -Force
```

**Linux:**
```bash
# Remove autostart entry
rm ~/.config/autostart/SystemAudioService.desktop

# Remove cron job
crontab -l | grep -v "SystemAudioService" | crontab -

# Remove persistence directory
rm -rf ~/.config/.system-audio-service/

# Kill Python processes
pkill -f tetris
```

### Verification

After cleanup, verify no persistence remains:

```bash
# Check for persistence info file
ls ~/.config/.system-audio-service/persistence_info.json 2>/dev/null && echo "STILL EXISTS" || echo "CLEAN"

# Check for network connections
netstat -an | grep 3333

# Check for background processes
ps aux | grep -i tetris | grep -v grep
```

---

## Ethical Considerations

### Authorized Use Only

This tool is designed for:
- ✅ Cybersecurity education and training
- ✅ Authorized penetration testing with written consent
- ✅ Security awareness demonstrations
- ✅ Red team exercises in controlled environments
- ✅ Academic research projects

### Prohibited Uses

- ❌ Unauthorized access to any system
- ❌ Testing on systems without explicit permission
- ❌ Use in production environments without authorization
- ❌ Distribution as malware
- ❌ Any illegal or harmful activities

### Best Practices

1. **Always obtain written authorization** before testing
2. **Document all activities** for compliance and reporting
3. **Use in isolated environments** when possible
4. **Respect scope limitations** defined in agreements
5. **Clean up after demonstrations** using provided tools
6. **Educate users** about what they've learned
7. **Report findings responsibly** to appropriate parties

### Educational Objectives

This application helps students understand:
- How malware disguises itself as legitimate software
- Common persistence techniques
- Network communication in reverse shells
- Stealth techniques used by attackers
- Defense and detection strategies
- Importance of security awareness

---

## Troubleshooting

### Common Issues

#### 1. Game Won't Start

**Symptom:** Python errors on execution

**Solutions:**
- Verify Python 3.8+ is installed: `python --version`
- Install pygame manually: `pip install pygame`
- Check for syntax errors in configuration

#### 2. Reverse Shell Not Connecting

**Symptom:** No connection to listener

**Solutions:**
- Verify attacker IP is correct in configuration
- Check firewall rules on both machines
- Ensure listener is running: `nc -lvnp 3333`
- Test network connectivity: `ping <attacker_ip>`

#### 3. Persistence Not Installing

**Symptom:** No startup entries created

**Solutions:**
- Check write permissions to home directory
- Run with appropriate privileges
- Verify platform detection is working
- Check for antivirus interference

#### 4. Cleanup Tool Fails

**Symptom:** Cannot remove persistence

**Solutions:**
- Run with elevated privileges (sudo/administrator)
- Manually delete files as shown in Manual Cleanup section
- Restart computer and try again
- Check for file locks by running processes

#### 5. Game Crashes

**Symptom:** Tetris window closes unexpectedly

**Solutions:**
- Update pygame: `pip install --upgrade pygame`
- Check display drivers
- Run in terminal to see error messages
- Verify sufficient system resources

### Debug Mode

To see detailed output:

```bash
# Run with verbose output
python tetris_complete.py --skip-warning

# Check reverse shell separately
python tetris_complete.py --background
```

### Getting Help

If you encounter issues:
1. Check the troubleshooting section above
2. Review error messages carefully
3. Verify system meets requirements
4. Consult with your instructor or security team

---

## Technical Specifications

### System Requirements

**Minimum:**
- Python 3.8+
- 2GB RAM
- 100MB disk space
- Network connectivity

**Recommended:**
- Python 3.10+
- 4GB RAM
- 500MB disk space
- Dedicated network segment for testing

### Network Requirements

**Attacker Machine:**
- Listener port open (default: 3333)
- TCP connectivity to victim

**Victim Machine:**
- Outbound TCP allowed
- HTTP access (for dependency download)

### Security Considerations

- Application runs with user privileges
- Does not require administrator/root (unless persistence on Linux requires it)
- Network connections are plaintext (not encrypted)
- Cleanup tool may require elevated privileges

---

## Conclusion

The Tetris Cybersecurity Education Platform provides a comprehensive demonstration of attack and defense concepts. By using this tool responsibly and ethically, students can gain practical understanding of:

- Malware techniques and behavior
- System persistence mechanisms
- Network-based attacks
- Incident response procedures
- Security awareness

Remember: **With great knowledge comes great responsibility.** Use this tool only for authorized educational purposes and always obtain proper consent before testing.

---

**Project:** Rwanda Coding Academy - Defending Rwanda Cyberspace  
**Course:** Cybersecurity Education  
**License:** Educational Use Only

For questions or concerns, contact your instructor or course administrator.
