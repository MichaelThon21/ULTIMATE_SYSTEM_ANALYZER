# 🚀 Ultimate System Analyzer

[![Python Version](https://img.shields.io/badge/python-3.7%2B-blue)](https://python.org)
[![Platform](https://img.shields.io/badge/platform-Windows-0078D6)](https://microsoft.com/windows)
[![License](https://img.shields.io/badge/license-MIT-green)](LICENSE)
[![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen)](../../pulls)

> **Professional Windows System Diagnostic & Reporting Tool**  
> Deep hardware analysis • Registry insights • Security audits • Benchmarks • Multi-format reports

---

## 📌 Overview

**Ultimate System Analyzer** is a powerful, all-in-one Windows diagnostic tool written in Python.  
It performs deep system inspection — from low-level hardware details to registry data and modern Windows security features — and generates professional multi-format reports.

Built for:

- 🖥 IT Professionals  
- 🔐 Security Analysts  
- 🧑‍💻 Developers  
- ⚙ Power Users  

---

## ✨ Features

### 🖥 System & Hardware Analysis
- OS edition, build, architecture
- Motherboard & BIOS details
- CPU (cores/threads, cache, per-core usage, temperature)
- GPU (dedicated/integrated, VRAM, driver info)
- RAM (modules, speed, usage, swap)
- Storage (physical disks, partitions, SMART status)
- Audio devices
- Power & battery health

### 🌐 Network Inspection
- Network interfaces (IP, MAC, DNS, DHCP)
- Wi-Fi profiles
- ARP table
- Firewall rules
- Public IP detection

### 🔐 Security & Modern Windows Features
- UAC status
- Secure Boot
- TPM status
- Windows Defender status
- LSA Protection
- Credential Guard
- WSL
- Hyper-V
- Windows Sandbox
- Containers support

### ⚙ Software & Registry
- Installed programs
- Running processes
- Services
- Startup entries
- Environment variables
- Windows Update history
- Registry analysis

### 🚀 Performance Benchmarks
- Multi-threaded CPU benchmark
- Memory performance test
- Disk I/O performance testing
- GPU scoring (if supported)

### 📊 Reporting
Export reports in:

- TXT
- JSON
- HTML
- PDF *(optional – requires `reportlab`)*
- CSV *(optional – requires `pandas`)*

---

## ⚙️ How It Works

1. **Auto-Installer**  
   Automatically checks and installs missing dependencies via `pip`.

2. **Privilege Detection**  
   Detects Administrator rights and offers UAC elevation for full system access.

3. **Deep System Scan**  
   Uses WMI, registry access, Windows APIs, and Python libraries to collect data.

4. **Professional Reporting**  
   Generates structured and formatted reports in multiple formats.

5. **Menu-Driven Interface**  
   Clean, user-friendly numbered menu with colored output.

---

## 🚀 Getting Started

### Requirements

- Windows 7 / 8 / 10 / 11
- Python 3.7+
- Internet connection (first run only for dependency installation)

Download Python:  
https://www.python.org/downloads/

---

## 🔧 Installation & Usage

### 🔹 Option 1 – Quick Run (Auto-Install Dependencies)

```bash
python ultimate_system_analyzer.py


