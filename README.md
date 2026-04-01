# Simple Python Port Scanner 🚀

A high-performance, multi-threaded TCP port scanner written in Python. This tool is designed for security researchers and network administrators to quickly identify open ports, enumerate services (banner grabbing), and export findings for further analysis.

## ✨ Features

* **Multi-Threaded:** Uses `ThreadPoolExecutor` to scan ports concurrently, making it significantly faster than sequential scanners.
* **Banner Grabbing:** Attempts to retrieve service information (headers/banners) from open ports to identify running software.
* **Multiple Export Formats:** Automatically saves scan results to both `CSV` and `JSON` files.
* **Error Handling:** Robust handling for hostname resolution, timeouts, and user interruptions (Ctrl+C).

## 🛠️ Installation

1. Clone the repository:
   ```bash
   git clone [https://github.com/ngwingallah/A-Simple-Python-Port-Scanner.git](https://github.com/ngwingallah/A-Simple-Python-Port-Scanner.git)
   cd A-Simple-Python-Port-Scanner
   
2. Ensure you have Python 3.x installed:
    ```bash
   python3 --version

## 🚀 Usage
- Run the script by providing a target IP address or hostname:
   ```bash
   python3 portscanner.py <target_ip>

## 📊 Output

Upon completion, the tool generates two files in the project directory:
* **scan_results.csv:** Best for viewing in Excel/Google Sheets.
* **scan_results.json:** Best for integration with other web tools or scripts.

## 🔍 How It Works

The scanner performs a TCP Connect Scan. It attempts to complete the three-way handshake with the target. If successful, it sends a small probe to "grab" the service banner before closing the connection.

## ⚠️ Disclaimer

This tool is for educational and ethical testing purposes only. Scanning targets without prior authorization is illegal and unethical. The developer assumes no liability for misuse of this tool.
