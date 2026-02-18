# Ultimate System Analyzer – Professional GitHub Repository

Below you’ll find everything needed to create a **professional GitHub repository** for the Ultimate System Analyzer.  
The repository includes:

- **Main script** – `ultimate_system_analyzer.py` (the full tool)
- **`requirements.txt`** – lists all dependencies (including optional ones, commented out)
- **`README.md`** – detailed documentation with badges, features, usage, etc.
- **`LICENSE`** – MIT license

All files are ready to copy‑paste into your repository.  
Simply create a new GitHub repo, add these files, and push.

---

## 📁 Repository Structure

```
ULTIMATE_SYSTEM_ANALYZER/
├── ultimate_system_analyzer.py   # The main application
├── requirements.txt               # Python dependencies
├── README.md                      # Project documentation
├── LICENSE                        # MIT License
└── reports/                        # (created on first run) – output folder
```

---

## 📄 File Contents

### 1. `ultimate_system_analyzer.py`

Copy the entire script from the user's message.  
*(It is already provided in the conversation – ensure it is saved with this name.)*

> **Note:** The script is self‑contained and includes an auto‑installer for dependencies, but providing a `requirements.txt` makes it easier for users to pre‑install everything.

---

### 2. `requirements.txt`

```txt
# Core requirements (automatically installed by the script if missing)
psutil>=5.9.0
py-cpuinfo>=8.0.0
wmi>=1.5.1
GPUtil>=1.4.0
screeninfo>=0.6.7
colorama>=0.4.6

# Optional packages (for enhanced reports and features)
# pandas          # CSV export & data analysis
# numpy           # faster calculations (used by pandas)
# reportlab       # PDF report generation
# matplotlib      # charts (future use)
# py-cryptodome   # encryption (secure reports)
# netifaces       # advanced network info
# pywin32         # better Windows integration
# pystray         # system tray icon
# pillow          # image processing
# tqdm            # progress bars (optional)
```

---

### 3. `README.md`

```markdown
# 🚀 Ultimate System Analyzer

[![Python Version](https://img.shields.io/badge/python-3.7%2B-blue)](https://python.org)
[![License](https://img.shields.io/badge/license-MIT-green)](LICENSE)
[![Platform](https://img.shields.io/badge/platform-Windows-lightgrey)](https://microsoft.com)
[![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen)](https://github.com/yourusername/ULTIMATE_SYSTEM_ANALYZER/pulls)

**Ultimate System Analyzer** is a powerful, all‑in‑one system information and diagnostic tool for Windows. It automatically installs required dependencies, runs with or without administrator privileges, and generates professional reports in multiple formats (TXT, JSON, HTML, PDF, CSV).  
Inspired by tools like IObit System Information, it provides deep insight into every aspect of your machine – from hardware specs to security health and performance benchmarks.

---

## ✨ Features

| Category                 | Capabilities |
|--------------------------|--------------|
| **System Overview**      | Computer name, manufacturer, model, serial number, domain, uptime, install date |
| **Operating System**     | Edition, build number, service pack, locale, environment variables |
| **Processor (CPU)**      | Brand, cores/threads, clock speeds, cache sizes, temperature, per‑core usage |
| **Graphics (GPU)**       | Dedicated/integrated GPUs, VRAM, driver version, monitor resolutions, PPI |
| **Memory (RAM)**         | Total, used, available; physical modules (bank, speed, manufacturer); swap usage |
| **Storage (Disks)**      | Physical disks (model, interface, size, SMART status), logical drives, partitions, I/O stats |
| **Network**              | Interfaces (IP, MAC), DNS, DHCP, Wi‑Fi profiles, public IP, firewall rules |
| **Audio**                | Sound devices, drivers |
| **Motherboard / BIOS**   | Manufacturer, version, serial, release date, chassis info |
| **Power / Battery**      | Charge status, capacity, wear level, cycle count, estimated run time |
| **Security**             | UAC level, Secure Boot, TPM status, Windows Defender, installed security products |
| **Performance**          | Multi‑threaded CPU benchmark, memory speed test, disk sequential/random I/O, GPU score |
| **Software**             | Installed programs, running processes, Python packages |
| **Hardware Health**      | Temperature warnings, disk space alerts, battery health, SMART status |
| **Registry**             | Installed software keys, startup programs, environment variables |
| **Modern Windows**       | WSL, Hyper‑V, Sandbox, Containers, Credential Guard |
| **Windows Updates**      | Installed hotfixes, last check time |
| **Real‑time Monitoring** | CPU, memory, disk, and network usage with live progress bars |

---

## ⚙️ How It Works

1. **Auto‑installer** – On first run, the script checks for required Python packages and installs them automatically via `pip`.  
2. **Privilege detection** – Detects if running as Administrator and suggests elevation for full system access.  
3. **Comprehensive scanning** – Collects data using WMI, registry, command‑line tools, and the installed libraries.  
4. **Report generation** – Outputs professional reports in your chosen format (text, JSON, HTML, PDF, CSV).  
5. **Menu‑driven interface** – Simple numbered menus with coloured output.

---

## 🚀 Getting Started

### Prerequisites
- **Windows** (the tool is Windows‑specific)
- **Python 3.7 or higher** installed and added to PATH
- Internet connection (only for first‑run dependency installation)

### Installation & Usage

#### Option 1: Quick Run (auto‑install)
```bash
# Download the script
curl -O https://raw.githubusercontent.com/yourusername/ULTIMATE_SYSTEM_ANALYZER/main/ultimate_system_analyzer.py

# Run it – dependencies will be installed automatically
python ultimate_system_analyzer.py
```

#### Option 2: Using `requirements.txt` (recommended for reproducibility)
```bash
# Clone the repository
git clone https://github.com/yourusername/ULTIMATE_SYSTEM_ANALYZER.git
cd ULTIMATE_SYSTEM_ANALYZER

# (Optional) Create a virtual environment
python -m venv venv
venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run the analyzer
python ultimate_system_analyzer.py
```

> **Note:** The script will still ask about optional packages even if they are already installed. You can safely skip or install them later.

---

## 🧭 Usage

When launched, you’ll see the main menu:

```
╔══════════════════════════════════════════════════════════════════╗
║                          MAIN MENU                               ║
╠══════════════════════════════════════════════════════════════════╣
║   1. 🚀  Quick System Overview (Fast Style)                      ║
║   2. 🔍  Comprehensive Hardware Analysis                         ║
║   3. ⚙️   Full System Diagnostics (All Sections)                 ║
║   4. 📊  Performance Benchmark & Scoring                         ║
║   5. 🔒  Security & Health Check                                 ║
║   6. 💾  Export Professional Reports                             ║
║   7. 📈  Real-time Monitoring (Experimental)                     ║
║   8. ⚙️   Tools & Utilities                                      ║
║   0. ❌  Exit                                                    ║
╚══════════════════════════════════════════════════════════════════╝
```

- **Options 1–5** run specific analyses. After completion you can save reports.
- **Option 6** lets you export previously collected data (run a scan first).
- **Option 7** starts an experimental live monitor (press Ctrl+C to stop).
- **Option 8** provides utilities like reinstalling dependencies, cleaning temp files, opening system tools, etc.

---

## 📁 Output & Reports

All reports are saved in a `reports` folder (created automatically).  
The filename includes the computer name and timestamp, e.g.  
`SystemAnalysis_DESKTOP-ABC_20250219_143022.html`

Supported formats:
- **Text (.txt)** – Human‑readable comprehensive report.
- **JSON (.json)** – Full data structure for programmatic use.
- **HTML (.html)** – Styled web page with collapsible sections.
- **PDF (.pdf)** – (if `reportlab` installed) – Professional printable document.
- **CSV (.csv)** – (if `pandas` installed) – Tabular data for spreadsheets.

A `README.txt` inside the reports folder explains each file.

---

## 🔧 Customization & Extending

- **Configuration** – Edit the `Config` class in the script to change version, add/remove analysis sections, or tweak benchmark parameters.
- **Optional packages** – During installation you’ll be asked whether to install optional packages. Choose `y` for extra report formats.
- **Adding new analysis** – Create a new method in `ComprehensiveAnalyzer` (e.g., `analyze_my_feature`) and add it to the `sections` list in `full_diagnostics()`.

---

## 📦 Dependencies

| Required | Purpose |
|----------|---------|
| `psutil` | System and process utilities (CPU, memory, disks, network) |
| `py-cpuinfo` | Detailed CPU information |
| `wmi` | Windows Management Instrumentation (hardware details) |
| `GPUtil` | GPU real‑time stats (NVIDIA only) |
| `screeninfo` | Monitor resolutions and dimensions |
| `colorama` | Coloured console output |

Optional packages (for enhanced reports): `pandas`, `reportlab`, `matplotlib`, etc.  
All dependencies can be installed via `pip install -r requirements.txt`.

---

## 🛡️ Administrator vs. Standard User

Some features (SMART data, installed software list, Windows Update history, Wi‑Fi profiles, etc.) require **administrator privileges**.  
The tool will:
- Detect your current privilege level.
- Show which features will be limited.
- Offer to restart with elevation (UAC prompt).

You can still run without admin – you’ll get a useful subset of information.

---

## 🤝 Contributing

Contributions are welcome! If you’d like to improve the tool:

1. Fork the repository.
2. Create a feature branch (`git checkout -b feature/AmazingFeature`).
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`).
4. Push to the branch (`git push origin feature/AmazingFeature`).
5. Open a Pull Request.

Please ensure your code follows the existing style and includes comments where necessary.

---

## 📄 License

Distributed under the MIT License. See `LICENSE` for more information.

---

## 👤 Author

**MichaelThon21**  
- GitHub: [@MichaelThon21](https://github.com/MichaelThon21)

If you find this tool useful, please ⭐ star the repository!

---

## 🙌 Acknowledgements

- Uses many wonderful open‑source libraries (see dependencies)
- Thanks to the Python and Windows developer communities
```

---

### 4. `LICENSE`

```txt
MIT License

Copyright (c) 2026 MichaelThon21

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
```

---

## 🚀 Next Steps

1. **Create a new GitHub repository** named `ULTIMATE_SYSTEM_ANALYZER`.
2. **Add the files** above using the GitHub web interface or by cloning locally.
3. **Push the code** and watch the stars roll in! ⭐

Your repository will be professional, easy to use, and welcoming to contributors.  
Happy coding!
