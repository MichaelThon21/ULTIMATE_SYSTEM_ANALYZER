# Ultimate System Analyzer

**Professional Windows System Diagnostic Tool** – Auto‑installing, comprehensive hardware/software analysis with registry insights, security audits, performance benchmarks, and multi‑format reporting.

[![Python 3.7+](https://img.shields.io/badge/python-3.7+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Windows](https://img.shields.io/badge/platform-Windows-0078D6)](https://www.microsoft.com/windows)

---

## 📌 Overview

**Ultimate System Analyzer** is a powerful Python script that collects **every possible detail** about a Windows machine – from CPU and RAM to registry entries and modern Windows features (WSL, Hyper‑V, Secure Boot). It features an **auto‑installation** engine that downloads and sets up all required packages, so you can run it immediately without manual dependency handling.

After scanning, the tool generates professional reports in **TXT, JSON, HTML, PDF, and CSV** formats, giving you a complete picture of your system’s health, security, and performance.

---

## ✨ Key Features

- **Auto‑installer** – Checks and installs required Python packages on first run.
- **Privilege management** – Detects admin rights and offers UAC elevation for full access.
- **Comprehensive analysis** – 20+ sections including:
  - System Overview, OS details, Motherboard, BIOS
  - CPU (including temperature and per‑core usage)
  - GPU (dedicated/integrated, VRAM, driver info)
  - Memory (physical modules, virtual/swap)
  - Storage (physical disks, SMART data, partitions)
  - Network (interfaces, Wi‑Fi profiles, DNS cache, ARP table, firewall rules)
  - Audio devices
  - Power & Battery (cycle count, wear level)
  - Security (UAC, LSA protection, TPM, Secure Boot, Defender)
  - Performance benchmarks (multi‑threaded CPU, memory, disk I/O)
  - Software inventory (installed programs, services, processes)
  - Hardware health (temperatures, disk usage, battery health)
  - **Registry analysis** (installed software, startup programs, environment variables)
  - **Modern Windows features** (WSL, Hyper‑V, Sandbox, Containers, Credential Guard)
  - **Windows Update history**
- **Real‑time monitoring** (experimental) – CPU, memory, disk, and network usage.
- **Professional reports** – Export data as TXT, JSON, HTML, PDF, CSV.
- **Tools & Utilities** – Reinstall dependencies, clean temp files, open system configuration tools, basic registry explorer.

---

## 🚀 Installation & Usage

### Requirements
- Windows 7/8/10/11 (64‑bit recommended)
- Python 3.7 or higher ([download](https://www.python.org/downloads/))

### Quick Start

1. **Download the script**  
   Save `ultimate_system_analyzer.py` to a folder of your choice.

2. **Run as Administrator** (recommended for full data collection)  
   Right‑click the script and select “Run with Python” or open a terminal and execute:
