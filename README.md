# Oh My USB 🔌🦆

A stealthy Python-powered BadUSB payload generator designed for penetration testers, red teamers, and hardware hackers.

**Oh My USB** lets you craft DuckyScript payloads for USB Rubber Ducky, Digispark, or any HID-based device. It includes built-in presets, custom scripting, stealth mode, payload stats, and safety checks.

---

## 🚀 Features

* 🧠 Preset payloads (Reverse Shell, Keylogger, Wi-Fi Reconfig, Self-Destruct, etc.)
* ✍️ Write your own custom DuckyScript from scratch
* 🕵️ Stealth Mode — adds random delays to simulate human typing
* 📊 Payload Stats — line count, string/delay count, execution time
* 🔐 Detects dangerous commands like `Remove-Item` or `shutdown`
* 📡 Suggests reverse shell listener if applicable (`nc -lvnp 4444`)

---

## 📦 Payload Types Supported

* Rubber Ducky (`.txt` format)
* Digispark / Arduino HID output *(planned)*
* Multi-device formatting *(future upgrade)*

---

## 📂 Installation

```bash
git clone https://github.com/yourusername/oh-my-usb.git
cd oh-my-usb
python3 oh_my_usb.py
```

> Requires Python 3.x

---

## 📁 Example Usage

```bash
$ python3 oh_my_usb.py

Evil USB Payload Generator
[1] Use preset payload
[2] Write custom payload
Choose an option (1 or 2): 1

Available Payloads:
[1] Reverse Shell
[2] Keylogger
[3] Open Website
[4] Wifi Reconfig
[5] Self Destruct

Select a payload number to generate: 1
Enable stealth mode? (y/n): y

--- Payload Stats ---
Total lines: 6
STRING commands: 1
DELAY commands: 3
Estimated time (ms): 1350
----------------------

[!] This looks like a reverse shell payload. Example listener:
    nc -lvnp 4444
```

---

## 🛡 Disclaimer

This tool is intended **for educational and authorized testing only**.
Do **not** use on targets you don’t have explicit permission to test.

You are responsible for your actions.

---

## 🙌 Credits

* Built by \[mqz]
* Inspired by Hak5 Rubber Ducky ecosystem

---

## 📄 License

MIT License – see [LICENSE](./LICENSE)
