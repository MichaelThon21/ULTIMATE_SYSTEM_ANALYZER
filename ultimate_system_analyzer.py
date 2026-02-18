# ==================== ULTIMATE AUTO-INSTALLING SYSTEM ANALYZER ====================
import sys
import subprocess
import importlib
import os
import platform
import socket
import json
import ctypes
import uuid
import re
import math
import hashlib
import time
import threading
import traceback
import itertools
import statistics
import textwrap
import webbrowser
from datetime import datetime, timedelta
from pathlib import Path
from collections import OrderedDict, defaultdict
from typing import Dict, List, Any, Optional, Tuple
import xml.etree.ElementTree as ET


# ==================== CONFIGURATION & CONSTANTS ====================
class Config:
    """Configuration settings for the analyzer"""

    VERSION = "3.0"

    REQUIRED_PACKAGES = {
        "psutil": {"import_as": "psutil", "min_version": "5.9.0"},
        "py-cpuinfo": {"import_as": "cpuinfo", "min_version": "8.0.0"},
        "wmi": {"import_as": "wmi", "min_version": "1.5.1"},
        "GPUtil": {"import_as": "GPUtil", "min_version": "1.4.0"},
        "screeninfo": {"import_as": "screeninfo", "min_version": "0.6.7"},
        "python-dateutil": {
            "import_as": "dateutil",
            "min_version": "2.8.2",
            "optional": True,
        },
        "colorama": {"import_as": "colorama", "min_version": "0.4.6"},
        "tqdm": {"import_as": "tqdm", "min_version": "4.65.0", "optional": True},
    }

    OPTIONAL_PACKAGES = {
        "pandas": "Data analysis and export (enhanced reports)",
        "numpy": "Numerical operations (faster calculations)",
        "py-cryptodome": "Encryption utilities (secure reports)",
        "netifaces": "Advanced network interface detection",
        "pywin32": "Better Windows integration (if not installed via wmi)",
        "pystray": "System tray integration",
        "pillow": "Image processing for reports",
        "matplotlib": "Performance charts and graphs",
        "reportlab": "PDF report generation",
    }

    ANALYSIS_SECTIONS = [
        "System Overview",
        "Operating System",
        "Processor (CPU)",
        "Graphics (GPU)",
        "Memory (RAM)",
        "Storage (Disks)",
        "Network",
        "Display",
        "Audio",
        "Motherboard",
        "Bios/UEFI",
        "Power/Battery",
        "Security",
        "Performance",
        "Software",
        "Hardware Health",
        "Registry",
        "Modern Windows Features",
        "Windows Updates",
        "Benchmarks",
    ]

    @staticmethod
    def get_banner():
        """Get the application banner"""
        return r"""
╔══════════════════════════════════════════════════════════════════════════════╗
║                                                                              ║
║   ██╗   ██╗██╗     ████████╗██╗███╗   ███╗ █████╗ ████████╗███████╗          ║
║   ██║   ██║██║     ╚══██╔══╝██║████╗ ████║██╔══██╗╚══██╔══╝██╔════╝          ║
║   ██║   ██║██║        ██║   ██║██╔████╔██║███████║   ██║   █████╗            ║
║   ██║   ██║██║        ██║   ██║██║╚██╔╝██║██╔══██║   ██║   ██╔══╝            ║
║   ╚██████╔╝███████╗   ██║   ██║██║ ╚═╝ ██║██║  ██║   ██║   ███████╗          ║
║    ╚═════╝ ╚══════╝   ╚═╝   ╚═╝╚═╝     ╚═╝╚═╝  ╚═╝   ╚═╝   ╚══════╝          ║
║                                                                              ║
║                     ULTIMATE SYSTEM ANALYZER                                 ║
║               Professional System Diagnostic Tool                            ║
║                                                                              ║
║   ▸ Author(s) : https://github.com/MichaelThon21                             ║
║   ▸ Tool     : ULTIMATE SYSTEM ANALYZER                                      ║
║   ▸ Version  : 3.0                                                           ║
║   ▸ Status   : Auto-Installing • System Scan Ready                           ║
║                                                                              ║
╚══════════════════════════════════════════════════════════════════════════════╝

"""


# ==================== PRIVILEGE MANAGER ====================
class PrivilegeManager:
    """Manage administrator privileges and elevation"""

    @staticmethod
    def is_admin():
        """Check if running as administrator"""
        try:
            return ctypes.windll.shell32.IsUserAnAdmin() != 0
        except:
            return False

    @staticmethod
    def request_admin_privileges():
        """Request administrator privileges by re-launching with UAC prompt"""
        try:
            import sys
            import ctypes

            if not PrivilegeManager.is_admin():
                print(
                    "\n⚠️  This tool requires Administrator privileges for full system analysis."
                )
                print("   Some features will be limited without admin rights.")
                print("   Would you like to restart as Administrator?")

                choice = input("\nRestart as Administrator? [Y/n]: ").strip().lower()
                if choice in ["", "y", "yes"]:
                    print("\n🔒 Requesting administrator privileges...")

                    # Re-run with admin rights
                    ctypes.windll.shell32.ShellExecuteW(
                        None, "runas", sys.executable, " ".join(sys.argv), None, 1
                    )
                    return True  # Original instance should exit
            return False
        except Exception as e:
            print(f"\n❌ Failed to elevate privileges: {e}")
            return False

    @staticmethod
    def check_privilege_requirements():
        """Check what features require admin privileges"""
        requirements = {
            "full": [
                "All disk information (SMART)",
                "Network connection details",
                "Installed software list (registry)",
                "Windows Update information",
                "Event log access",
                "System restore points",
                "Driver details",
                "Service status",
                "Process details",
                "Security audit (UAC, Defender)",
                "Wi-Fi profiles",
                "Windows features (Hyper-V, WSL)",
            ],
            "limited": [
                "Basic system info",
                "CPU information",
                "Memory usage",
                "Basic disk space",
                "Display information",
                "Battery status (basic)",
                "User information",
                "Performance benchmarks",
            ],
        }

        is_admin = PrivilegeManager.is_admin()

        print("\n" + "=" * 60)
        print("PRIVILEGE ANALYSIS")
        print("=" * 60)

        if is_admin:
            print("✅ Running as Administrator")
            print("\n  All features available")
        else:
            print("⚠️  Running as Standard User")
            print("\n   Limited features only:")
            for feature in requirements["limited"]:
                print(f"   • {feature}")

            print("\nRequires Administrator:")
            for feature in requirements["full"]:
                print(f"   • {feature}")

        print("\n" + "=" * 60)
        return is_admin


# ==================== AUTO-INSTALLATION ENGINE ====================
class DependencyInstaller:
    """Handles automatic installation of required dependencies"""

    @staticmethod
    def check_python_version():
        """Check if Python version is compatible"""
        required = (3, 7)
        current = sys.version_info[:2]
        if current < required:
            print(
                f"❌ Python {required[0]}.{required[1]}+ required. You have {current[0]}.{current[1]}"
            )
            return False
        return True

    @staticmethod
    def install_package(package_name, version=None, upgrade=True, silent=False):
        """Install a Python package with progress indication (fixed: removed invalid --progress-bar)"""
        try:
            cmd = [sys.executable, "-m", "pip", "install"]
            if upgrade:
                cmd.append("--upgrade")
            if silent:
                cmd.append("--quiet")

            if version:
                cmd.append(f"{package_name}=={version}")
            else:
                cmd.append(package_name)

            if not silent:
                print(f"   Installing {package_name}...", end="", flush=True)

            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                timeout=120,
                creationflags=(
                    subprocess.CREATE_NO_WINDOW
                    if hasattr(subprocess, "CREATE_NO_WINDOW")
                    else 0
                ),
            )

            if result.returncode == 0:
                if not silent:
                    print(" ✓")
                return True
            else:
                if not silent:
                    print(" ✗")
                    if "ERROR" in result.stderr:
                        print(f"     Error: {result.stderr[:200]}...")
                return False
        except subprocess.TimeoutExpired:
            if not silent:
                print(" ✗ (Timeout)")
            return False
        except Exception as e:
            if not silent:
                print(f" ✗ ({str(e)[:50]}...)")
            return False

    @staticmethod
    def check_import(package_name, import_name=None):
        """Check if a package can be imported"""
        try:
            importlib.import_module(import_name or package_name)
            return True
        except ImportError:
            return False

    @staticmethod
    def install_all_dependencies(ask_for_optional=True, silent=False):
        """Install all required and optional dependencies"""
        if not silent:
            print("\n" + "=" * 60)
            print("DEPENDENCY INSTALLATION")
            print("=" * 60)

        # Check pip availability
        try:
            subprocess.run(
                [sys.executable, "-m", "pip", "--version"],
                capture_output=True,
                check=True,
                timeout=10,
            )
        except:
            if not silent:
                print("❌ pip not available. Please install pip first.")
            return None, ["pip"]

        installed = {}
        failed = []

        # Install required packages
        if not silent:
            print("\n📦 Required Packages:")

        for pkg, info in Config.REQUIRED_PACKAGES.items():
            import_name = info.get("import_as", pkg)

            if DependencyInstaller.check_import(pkg, import_name):
                if not silent:
                    print(f"   ✓ {pkg} already installed")
                installed[import_name] = importlib.import_module(import_name)
            else:
                if not silent:
                    print(f"   - {pkg} needs installation")
                if DependencyInstaller.install_package(
                    pkg, info.get("min_version"), silent=silent
                ):
                    try:
                        installed[import_name] = importlib.import_module(import_name)
                        if not silent:
                            print(f"   ✓ {pkg} installed successfully")
                    except ImportError:
                        if not silent:
                            print(f"   ✗ {pkg} failed to import after installation")
                        failed.append(pkg)
                else:
                    if not silent:
                        print(f"   ✗ Failed to install {pkg}")
                    if not info.get("optional", False):
                        failed.append(pkg)

        # Ask about optional packages
        if ask_for_optional and Config.OPTIONAL_PACKAGES and not silent:
            print("\n🔧 Optional Packages (enhanced features):")
            for pkg, description in Config.OPTIONAL_PACKAGES.items():
                response = (
                    input(f"   Install {pkg}? ({description}) [Y/n]: ").strip().lower()
                )
                if response in ["", "y", "yes"]:
                    if DependencyInstaller.install_package(pkg, silent=False):
                        try:
                            installed[pkg] = importlib.import_module(pkg)
                            print(f"   ✓ {pkg} installed")
                        except:
                            print(f"   ✗ {pkg} failed to import")

        # Summary
        if not silent:
            print("\n" + "=" * 60)
            print("INSTALLATION SUMMARY")
            print("=" * 60)
            print(f"✅ Installed: {len(installed)} packages")
            if failed:
                print(f"❌ Failed: {len(failed)} packages: {', '.join(failed)}")
                print("\nFor manual installation, run:")
                for pkg in failed:
                    print(f"   pip install {pkg}")
            else:
                print("🎉 All dependencies installed successfully!")

        return installed, failed


# ==================== ENHANCED USER INTERFACE ====================
class EnhancedUI:
    """Enhanced user interface with colors and better UX"""

    # Initialize colorama if available
    try:
        import colorama

        colorama.init()
        COLORS = {
            "HEADER": colorama.Fore.CYAN + colorama.Style.BRIGHT,
            "OKBLUE": colorama.Fore.BLUE,
            "OKGREEN": colorama.Fore.GREEN,
            "WARNING": colorama.Fore.YELLOW,
            "FAIL": colorama.Fore.RED,
            "ENDC": colorama.Style.RESET_ALL,
            "BOLD": colorama.Style.BRIGHT,
            "UNDERLINE": colorama.Style.NORMAL,
        }
    except:
        COLORS = {
            k: ""
            for k in [
                "HEADER",
                "OKBLUE",
                "OKGREEN",
                "WARNING",
                "FAIL",
                "ENDC",
                "BOLD",
                "UNDERLINE",
            ]
        }

    @staticmethod
    def color_text(text, color_type):
        """Color text using colorama if available"""
        return f"{EnhancedUI.COLORS.get(color_type, '')}{text}{EnhancedUI.COLORS.get('ENDC', '')}"

    @staticmethod
    def clear_screen():
        """Clear the console screen"""
        os.system("cls" if os.name == "nt" else "clear")

    @staticmethod
    def show_menu():
        """Display enhanced main menu"""
        EnhancedUI.clear_screen()
        print(EnhancedUI.color_text(Config.get_banner(), "HEADER"))

        menu = f"""
{EnhancedUI.color_text('╔══════════════════════════════════════════════════════════════════╗', 'OKBLUE')}
{EnhancedUI.color_text('║                          MAIN MENU                               ║', 'OKBLUE')}
{EnhancedUI.color_text('╠══════════════════════════════════════════════════════════════════╣', 'OKBLUE')}
{EnhancedUI.color_text('║   1. 🚀  Quick System Overview (Fast Style)                      ║', 'OKGREEN')}
{EnhancedUI.color_text('║   2. 🔍  Comprehensive Hardware Analysis                         ║', 'OKGREEN')}
{EnhancedUI.color_text('║   3. ⚙️   Full System Diagnostics (All Sections)                 ║', 'OKGREEN')}
{EnhancedUI.color_text('║   4. 📊  Performance Benchmark & Scoring                         ║', 'OKGREEN')}
{EnhancedUI.color_text('║   5. 🔒  Security & Health Check                                 ║', 'OKGREEN')}
{EnhancedUI.color_text('║   6. 💾  Export Professional Reports                             ║', 'OKGREEN')}
{EnhancedUI.color_text('║   7. 📈  Real-time Monitoring (Experimental)                     ║', 'OKGREEN')}
{EnhancedUI.color_text('║   8. ⚙️   Tools & Utilities                                      ║', 'OKGREEN')}
{EnhancedUI.color_text('║   0. ❌  Exit                                                    ║', 'FAIL')}
{EnhancedUI.color_text('╚══════════════════════════════════════════════════════════════════╝', 'OKBLUE')}

{EnhancedUI.color_text('System:', 'BOLD')} {socket.gethostname()} | {EnhancedUI.color_text('Privileges:', 'BOLD')} {'Admin' if PrivilegeManager.is_admin() else 'User'}
"""

        print(menu)

        while True:
            choice = input(
                f"\n{EnhancedUI.color_text('Select option', 'BOLD')} [0-8]: "
            ).strip()
            if choice in ["0", "1", "2", "3", "4", "5", "6", "7", "8"]:
                return int(choice)
            print(
                f"{EnhancedUI.color_text('Invalid choice. Please enter 0-8.', 'WARNING')}"
            )

    @staticmethod
    def ask_yes_no(question, default=True):
        """Ask a yes/no question with colored prompts"""
        default_str = "Y/n" if default else "y/N"
        while True:
            response = (
                input(f"{EnhancedUI.color_text(question, 'BOLD')} [{default_str}]: ")
                .strip()
                .lower()
            )
            if response == "":
                return default
            elif response in ["y", "yes"]:
                return True
            elif response in ["n", "no"]:
                return False
            else:
                print(
                    f"{EnhancedUI.color_text('Please answer yes/no (y/n)', 'WARNING')}"
                )

    @staticmethod
    def show_progress(step, total, message, current_item=""):
        """Show animated progress bar"""
        bar_length = 50
        percent = step / total
        filled_length = int(bar_length * percent)
        bar = "█" * filled_length + "░" * (bar_length - filled_length)

        # Animation characters
        anim = ["⠋", "⠙", "⠹", "⠸", "⠼", "⠴", "⠦", "⠧", "⠇", "⠏"]
        anim_char = anim[step % len(anim)]

        sys.stdout.write(
            f'\r  {EnhancedUI.color_text(anim_char, "OKBLUE")} [{bar}] {percent*100:5.1f}% - {message} {current_item}'
        )
        sys.stdout.flush()

        if step == total:
            print(
                f"\r  {EnhancedUI.color_text('✓', 'OKGREEN')} {' ' * (bar_length + 30)}"
            )

    @staticmethod
    def print_section_header(title):
        """Print a section header"""
        print(f"\n{EnhancedUI.color_text('═' * 60, 'OKBLUE')}")
        print(f"{EnhancedUI.color_text(f'  {title}', 'HEADER')}")
        print(f"{EnhancedUI.color_text('═' * 60, 'OKBLUE')}")


# ==================== COMPREHENSIVE SYSTEM ANALYZER ====================
class ComprehensiveAnalyzer:
    """Comprehensive system analyzer collecting all possible information"""

    def __init__(self, dependencies, is_admin=False):
        self.deps = dependencies
        self.is_admin = is_admin
        self.data = OrderedDict()
        self.errors = []
        self.warnings = []
        self.scan_start_time = None

        # Initialize modules
        self.wmi = None
        if "wmi" in self.deps:
            try:
                self.wmi = self.deps["wmi"].WMI()
            except:
                self.errors.append("Failed to initialize WMI")

        self.cache = {}

    def safe_execute(self, func, section, default=None, *args, **kwargs):
        """Safely execute a function and log errors"""
        try:
            result = func(*args, **kwargs)
            return result if result not in [None, ""] else default
        except Exception as e:
            error_msg = f"{section}: {func.__name__} - {str(e)[:100]}"
            self.errors.append(error_msg)
            return default

    def format_size(self, bytes_size):
        """Format bytes to human readable size"""
        if bytes_size == 0 or bytes_size is None:
            return "0 Bytes"
        for unit in ["Bytes", "KB", "MB", "GB", "TB"]:
            if bytes_size < 1024.0:
                return f"{bytes_size:.2f} {unit}"
            bytes_size /= 1024.0
        return f"{bytes_size:.2f} PB"

    # ==================== ANALYSIS SECTIONS ====================

    def analyze_system_overview(self):
        """Collect high-level system overview"""
        EnhancedUI.print_section_header("System Overview")

        overview = {
            "computer_name": socket.gethostname(),
            "manufacturer": "Unknown",
            "model": "Unknown",
            "system_type": "Unknown",
            "serial_number": "Unknown",
            "domain": "Unknown",
            "username": os.environ.get("USERNAME", "Unknown"),
            "logon_server": os.environ.get("LOGONSERVER", "Unknown"),
            "system_up_time": "Unknown",
            "install_date": "Unknown",
        }

        # Get computer system info from WMI
        if self.wmi:
            try:
                for cs in self.wmi.Win32_ComputerSystem():
                    overview["manufacturer"] = self.safe_execute(
                        lambda: cs.Manufacturer, "System", "Unknown"
                    )
                    overview["model"] = self.safe_execute(
                        lambda: cs.Model, "System", "Unknown"
                    )
                    overview["system_type"] = self.safe_execute(
                        lambda: cs.SystemType, "System", "Unknown"
                    )
                    overview["total_physical_memory"] = (
                        self.format_size(int(cs.TotalPhysicalMemory))
                        if cs.TotalPhysicalMemory
                        else "Unknown"
                    )
                    overview["domain"] = self.safe_execute(
                        lambda: cs.Domain, "System", "Unknown"
                    )
                    overview["part_of_domain"] = "Yes" if cs.PartOfDomain else "No"
                    break
            except:
                pass

            # Get system enclosure (chassis)
            try:
                for se in self.wmi.Win32_SystemEnclosure():
                    overview["chassis_type"] = self.safe_execute(
                        lambda: se.ChassisTypes[0], "System", "Unknown"
                    )
                    overview["serial_number"] = self.safe_execute(
                        lambda: se.SerialNumber, "System", "Unknown"
                    )
                    break
            except:
                pass

            # Get operating system info for uptime
            try:
                for os_info in self.wmi.Win32_OperatingSystem():
                    if os_info.LastBootUpTime:
                        try:
                            boot_time = datetime.strptime(
                                os_info.LastBootUpTime.split(".")[0], "%Y%m%d%H%M%S"
                            )
                            uptime = datetime.now() - boot_time
                            days = uptime.days
                            hours = uptime.seconds // 3600
                            minutes = (uptime.seconds % 3600) // 60
                            overview["system_up_time"] = f"{days}d {hours}h {minutes}m"
                        except:
                            overview["system_up_time"] = "Unknown"

                    if os_info.InstallDate:
                        try:
                            install_date = datetime.strptime(
                                os_info.InstallDate.split(".")[0], "%Y%m%d%H%M%S"
                            )
                            overview["install_date"] = install_date.strftime("%Y-%m-%d")
                        except:
                            overview["install_date"] = "Unknown"
                    break
            except:
                pass

        # Get username and domain
        try:
            import getpass

            overview["username"] = getpass.getuser()
        except:
            pass

        # Get Windows product key (partial)
        try:
            import winreg

            key = winreg.OpenKey(
                winreg.HKEY_LOCAL_MACHINE,
                r"SOFTWARE\Microsoft\Windows NT\CurrentVersion",
            )
            product_id, _ = winreg.QueryValueEx(key, "ProductId")
            overview["product_id"] = product_id
            winreg.CloseKey(key)
        except:
            overview["product_id"] = "Unknown"

        self.data["System Overview"] = overview
        return overview

    def analyze_operating_system(self):
        """Collect detailed OS information"""
        EnhancedUI.print_section_header("Operating System")

        os_info = {
            "name": platform.system(),
            "version": platform.version(),
            "release": platform.release(),
            "platform": platform.platform(),
            "architecture": platform.architecture()[0],
            "machine": platform.machine(),
            "processor": platform.processor(),
            "node": platform.node(),
            "windows_details": {},
        }

        # Get detailed Windows information
        if platform.system() == "Windows":
            try:
                import winreg

                key_paths = {
                    "current_version": r"SOFTWARE\Microsoft\Windows NT\CurrentVersion",
                    "windows_update": r"SOFTWARE\Microsoft\Windows\CurrentVersion\WindowsUpdate",
                }

                for key_name, path in key_paths.items():
                    try:
                        with winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, path) as key:
                            os_info["windows_details"][key_name] = {}
                            i = 0
                            while True:
                                try:
                                    value_name, value_data, value_type = (
                                        winreg.EnumValue(key, i)
                                    )
                                    if isinstance(value_data, (str, int)):
                                        os_info["windows_details"][key_name][
                                            value_name
                                        ] = str(value_data)
                                    i += 1
                                except OSError:
                                    break
                    except:
                        pass
            except:
                pass

            # Get Windows edition from registry
            try:
                import winreg

                key = winreg.OpenKey(
                    winreg.HKEY_LOCAL_MACHINE,
                    r"SOFTWARE\Microsoft\Windows NT\CurrentVersion",
                )
                os_info["windows_edition"] = self.safe_execute(
                    winreg.QueryValueEx, "OS", "Unknown", key, "ProductName"
                )[0]
                os_info["build_number"] = self.safe_execute(
                    winreg.QueryValueEx, "OS", "Unknown", key, "CurrentBuildNumber"
                )[0]
                os_info["display_version"] = self.safe_execute(
                    winreg.QueryValueEx, "OS", "Unknown", key, "DisplayVersion"
                )[0]
                winreg.CloseKey(key)
            except:
                os_info["windows_edition"] = "Unknown"
                os_info["build_number"] = "Unknown"

        # Get Windows version via WMI for more details
        if self.wmi:
            try:
                for win_os in self.wmi.Win32_OperatingSystem():
                    os_info["caption"] = self.safe_execute(
                        lambda: win_os.Caption, "OS", "Unknown"
                    )
                    os_info["build_type"] = self.safe_execute(
                        lambda: win_os.BuildType, "OS", "Unknown"
                    )
                    os_info["country_code"] = self.safe_execute(
                        lambda: win_os.CountryCode, "OS", "Unknown"
                    )
                    os_info["csd_version"] = self.safe_execute(
                        lambda: win_os.CSDVersion, "OS", "Unknown"
                    )
                    os_info["locale"] = self.safe_execute(
                        lambda: win_os.Locale, "OS", "Unknown"
                    )
                    os_info["os_language"] = self.safe_execute(
                        lambda: win_os.OSLanguage, "OS", "Unknown"
                    )
                    os_info["os_architecture"] = self.safe_execute(
                        lambda: win_os.OSArchitecture, "OS", "Unknown"
                    )
                    os_info["service_pack_major"] = self.safe_execute(
                        lambda: win_os.ServicePackMajorVersion, "OS", "Unknown"
                    )
                    os_info["service_pack_minor"] = self.safe_execute(
                        lambda: win_os.ServicePackMinorVersion, "OS", "Unknown"
                    )
                    os_info["windows_directory"] = self.safe_execute(
                        lambda: win_os.WindowsDirectory, "OS", "Unknown"
                    )
                    break
            except:
                pass

        # Get system directories
        os_info["system_directories"] = {
            "windows_dir": os.environ.get("WINDIR", "Unknown"),
            "system_dir": os.environ.get("SYSTEMROOT", "Unknown"),
            "program_files": os.environ.get("ProgramFiles", "Unknown"),
            "program_files_x86": os.environ.get("ProgramFiles(x86)", "Unknown"),
            "user_profile": os.environ.get("USERPROFILE", "Unknown"),
            "temp_dir": os.environ.get("TEMP", "Unknown"),
        }

        # Get system locale
        try:
            import locale

            os_info["system_locale"] = locale.getlocale()
            os_info["default_encoding"] = locale.getpreferredencoding()
        except:
            pass

        self.data["Operating System"] = os_info
        return os_info

    def analyze_processor(self):
        """Collect detailed CPU information"""
        EnhancedUI.print_section_header("Processor (CPU)")

        cpu_info = {
            "basic_info": {},
            "detailed_info": {},
            "performance": {},
            "cache": {},
            "features": [],
            "temperatures": {},
        }

        # Get basic CPU info from cpuinfo
        if "cpuinfo" in self.deps:
            try:
                cpu_data = self.deps["cpuinfo"].get_cpu_info()

                cpu_info["basic_info"] = {
                    "brand": cpu_data.get("brand_raw", "Unknown"),
                    "hz_advertised": cpu_data.get("hz_advertised_friendly", "Unknown"),
                    "hz_actual": cpu_data.get("hz_actual_friendly", "Unknown"),
                    "cores": cpu_data.get("count", 1),
                    "architecture": cpu_data.get("arch", "Unknown"),
                    "bits": cpu_data.get("bits", "Unknown"),
                    "vendor": cpu_data.get("vendor_id", "Unknown"),
                }

                # Cache information
                cache_keys = [
                    "l1_data_cache_size",
                    "l1_instruction_cache_size",
                    "l2_cache_size",
                    "l3_cache_size",
                    "l4_cache_size",
                ]
                for key in cache_keys:
                    if key in cpu_data and cpu_data[key]:
                        friendly_name = key.replace("_", " ").title()
                        cpu_info["cache"][friendly_name] = str(cpu_data[key])

                # CPU features/flags
                if "flags" in cpu_data:
                    cpu_info["features"] = cpu_data["flags"]
            except Exception as e:
                self.errors.append(f"CPUInfo error: {str(e)}")

        # Get detailed CPU info from WMI
        if self.wmi:
            try:
                for processor in self.wmi.Win32_Processor():
                    cpu_info["detailed_info"] = {
                        "name": self.safe_execute(
                            lambda: processor.Name, "CPU", "Unknown"
                        ),
                        "description": self.safe_execute(
                            lambda: processor.Description, "CPU", "Unknown"
                        ),
                        "manufacturer": self.safe_execute(
                            lambda: processor.Manufacturer, "CPU", "Unknown"
                        ),
                        "processor_id": self.safe_execute(
                            lambda: processor.ProcessorId, "CPU", "Unknown"
                        ),
                        "socket_designation": self.safe_execute(
                            lambda: processor.SocketDesignation, "CPU", "Unknown"
                        ),
                        "family": self.safe_execute(
                            lambda: processor.Family, "CPU", "Unknown"
                        ),
                        "stepping": self.safe_execute(
                            lambda: processor.Stepping, "CPU", "Unknown"
                        ),
                        "revision": self.safe_execute(
                            lambda: processor.Revision, "CPU", "Unknown"
                        ),
                        "address_width": self.safe_execute(
                            lambda: processor.AddressWidth, "CPU", "Unknown"
                        ),
                        "data_width": self.safe_execute(
                            lambda: processor.DataWidth, "CPU", "Unknown"
                        ),
                        "cpu_status": self.safe_execute(
                            lambda: processor.CpuStatus, "CPU", "Unknown"
                        ),
                        "current_clock_speed": f"{processor.CurrentClockSpeed} MHz",
                        "max_clock_speed": f"{processor.MaxClockSpeed} MHz",
                        "ext_clock": (
                            f"{processor.ExtClock} MHz"
                            if processor.ExtClock
                            else "Unknown"
                        ),
                        "l2_cache_size": (
                            f"{processor.L2CacheSize} KB"
                            if processor.L2CacheSize
                            else "Unknown"
                        ),
                        "l3_cache_size": (
                            f"{processor.L3CacheSize} KB"
                            if processor.L3CacheSize
                            else "Unknown"
                        ),
                        "number_of_cores": processor.NumberOfCores,
                        "number_of_logical_processors": processor.NumberOfLogicalProcessors,
                        "thread_count": (
                            processor.ThreadCount
                            if hasattr(processor, "ThreadCount")
                            else "Unknown"
                        ),
                    }
                    break
            except Exception as e:
                self.errors.append(f"WMI CPU error: {str(e)}")

        # Get CPU performance metrics
        if "psutil" in self.deps:
            try:
                # CPU usage
                cpu_percent = self.deps["psutil"].cpu_percent(interval=0.5, percpu=True)
                cpu_info["performance"]["usage_per_core"] = [
                    {"core": i, "percent": percent}
                    for i, percent in enumerate(cpu_percent)
                ]
                cpu_info["performance"]["usage_total"] = sum(cpu_percent) / len(
                    cpu_percent
                )

                # CPU frequency
                cpu_freq = self.deps["psutil"].cpu_freq()
                if cpu_freq:
                    cpu_info["performance"]["frequency"] = {
                        "current": f"{cpu_freq.current:.2f} MHz",
                        "min": f"{cpu_freq.min:.2f} MHz" if cpu_freq.min else "Unknown",
                        "max": f"{cpu_freq.max:.2f} MHz",
                    }

                # CPU times
                cpu_times = self.deps["psutil"].cpu_times()
                cpu_info["performance"]["times"] = {
                    "user": cpu_times.user,
                    "system": cpu_times.system,
                    "idle": cpu_times.idle,
                }

                # CPU stats
                cpu_stats = self.deps["psutil"].cpu_stats()
                cpu_info["performance"]["stats"] = {
                    "ctx_switches": cpu_stats.ctx_switches,
                    "interrupts": cpu_stats.interrupts,
                    "soft_interrupts": cpu_stats.soft_interrupts,
                }
            except Exception as e:
                self.errors.append(f"Psutil CPU error: {str(e)}")

        # Try to get CPU temperature
        if "psutil" in self.deps:
            try:
                sensors = self.deps["psutil"].sensors_temperatures()
                if sensors:
                    for name, entries in sensors.items():
                        if any(x in name.lower() for x in ["core", "cpu", "package"]):
                            for entry in entries:
                                cpu_info["temperatures"][name] = {
                                    "current": f"{entry.current}°C",
                                    "high": (
                                        f"{entry.high}°C" if entry.high else "Unknown"
                                    ),
                                    "critical": (
                                        f"{entry.critical}°C"
                                        if entry.critical
                                        else "Unknown"
                                    ),
                                }
                                break
            except:
                pass

        self.data["Processor"] = cpu_info
        return cpu_info

    def analyze_graphics(self):
        """Collect detailed GPU information"""
        EnhancedUI.print_section_header("Graphics (GPU)")

        gpu_info = {"gpus": [], "displays": [], "driver_info": {}, "performance": {}}

        # Get GPU info from WMI
        if self.wmi:
            try:
                for i, gpu in enumerate(self.wmi.Win32_VideoController()):
                    gpu_data = {
                        "index": i,
                        "name": self.safe_execute(lambda: gpu.Name, "GPU", "Unknown"),
                        "adapter_compatibility": self.safe_execute(
                            lambda: gpu.AdapterCompatibility, "GPU", "Unknown"
                        ),
                        "adapter_ram": (
                            self.format_size(int(gpu.AdapterRAM))
                            if gpu.AdapterRAM
                            else "Unknown"
                        ),
                        "adapter_dac_type": self.safe_execute(
                            lambda: gpu.AdapterDACType, "GPU", "Unknown"
                        ),
                        "driver_version": self.safe_execute(
                            lambda: gpu.DriverVersion, "GPU", "Unknown"
                        ),
                        "driver_date": self.safe_execute(
                            lambda: gpu.DriverDate, "GPU", "Unknown"
                        ),
                        "video_architecture": self.safe_execute(
                            lambda: gpu.VideoArchitecture, "GPU", "Unknown"
                        ),
                        "video_memory_type": self.safe_execute(
                            lambda: gpu.VideoMemoryType, "GPU", "Unknown"
                        ),
                        "video_processor": self.safe_execute(
                            lambda: gpu.VideoProcessor, "GPU", "Unknown"
                        ),
                        "current_resolution": f"{gpu.CurrentHorizontalResolution}x{gpu.CurrentVerticalResolution}",
                        "current_refresh_rate": f"{gpu.CurrentRefreshRate} Hz",
                        "current_bits_per_pixel": f"{gpu.CurrentBitsPerPixel} bit",
                        "current_number_of_colors": f"{gpu.CurrentNumberOfColors:,}",
                        "max_refresh_rate": (
                            f"{gpu.MaxRefreshRate} Hz"
                            if gpu.MaxRefreshRate
                            else "Unknown"
                        ),
                        "min_refresh_rate": (
                            f"{gpu.MinRefreshRate} Hz"
                            if gpu.MinRefreshRate
                            else "Unknown"
                        ),
                        "pnp_device_id": self.safe_execute(
                            lambda: gpu.PNPDeviceID, "GPU", "Unknown"
                        ),
                        "status": self.safe_execute(
                            lambda: gpu.Status, "GPU", "Unknown"
                        ),
                        "inf_filename": self.safe_execute(
                            lambda: gpu.InfFilename, "GPU", "Unknown"
                        ),
                        "installed_display_drivers": self.safe_execute(
                            lambda: gpu.InstalledDisplayDrivers, "GPU", "Unknown"
                        ),
                    }

                    # Determine GPU type
                    gpu_name = gpu_data["name"].upper()
                    if "NVIDIA" in gpu_name:
                        gpu_data["type"] = "Dedicated (NVIDIA)"
                        gpu_data["vendor"] = "NVIDIA"
                    elif "AMD" in gpu_name or "RADEON" in gpu_name:
                        gpu_data["type"] = "Dedicated (AMD)"
                        gpu_data["vendor"] = "AMD"
                    elif (
                        "INTEL" in gpu_name
                        or "HD GRAPHICS" in gpu_name
                        or "UHD" in gpu_name
                    ):
                        gpu_data["type"] = "Integrated (Intel)"
                        gpu_data["vendor"] = "Intel"
                    else:
                        gpu_data["type"] = "Unknown"
                        gpu_data["vendor"] = "Unknown"

                    gpu_info["gpus"].append(gpu_data)
            except Exception as e:
                self.errors.append(f"WMI GPU error: {str(e)}")

        # Get additional GPU info from GPUtil
        if "GPUtil" in self.deps and gpu_info["gpus"]:
            try:
                gpus = self.deps["GPUtil"].getGPUs()
                for i, gpu in enumerate(gpus):
                    if i < len(gpu_info["gpus"]):
                        gpu_info["gpus"][i].update(
                            {
                                "real_time_memory_total": f"{gpu.memoryTotal} MB",
                                "real_time_memory_used": f"{gpu.memoryUsed} MB",
                                "real_time_memory_free": f"{gpu.memoryFree} MB",
                                "real_time_memory_utilization": f"{gpu.memoryUtil * 100:.1f}%",
                                "real_time_gpu_utilization": f"{gpu.load * 100:.1f}%",
                                "real_time_temperature": (
                                    f"{gpu.temperature}°C"
                                    if hasattr(gpu, "temperature")
                                    else "Unknown"
                                ),
                                "uuid": gpu.uuid if hasattr(gpu, "uuid") else "Unknown",
                                "display_mode": (
                                    gpu.display_mode
                                    if hasattr(gpu, "display_mode")
                                    else "Unknown"
                                ),
                            }
                        )
            except:
                pass

        # Get display information
        if "screeninfo" in self.deps:
            try:
                monitors = self.deps["screeninfo"].get_monitors()
                for i, monitor in enumerate(monitors):
                    display_info = {
                        "index": i,
                        "name": (
                            monitor.name
                            if hasattr(monitor, "name")
                            else f"Display {i+1}"
                        ),
                        "resolution": f"{monitor.width}x{monitor.height}",
                        "position": f"({monitor.x}, {monitor.y})",
                        "is_primary": (
                            monitor.is_primary
                            if hasattr(monitor, "is_primary")
                            else False
                        ),
                        "width_mm": (
                            monitor.width_mm if hasattr(monitor, "width_mm") else 0
                        ),
                        "height_mm": (
                            monitor.height_mm if hasattr(monitor, "height_mm") else 0
                        ),
                    }

                    # Calculate PPI
                    if display_info["width_mm"] > 0 and display_info["height_mm"] > 0:
                        diagonal_pixels = math.sqrt(
                            monitor.width**2 + monitor.height**2
                        )
                        diagonal_mm = math.sqrt(
                            monitor.width_mm**2 + monitor.height_mm**2
                        )
                        diagonal_inches = diagonal_mm / 25.4
                        display_info["diagonal_inches"] = round(diagonal_inches, 1)
                        display_info["ppi"] = (
                            round(diagonal_pixels / diagonal_inches, 1)
                            if diagonal_inches > 0
                            else 0
                        )

                    gpu_info["displays"].append(display_info)
            except Exception as e:
                self.errors.append(f"Screeninfo error: {str(e)}")

        # Get DirectX info from registry
        try:
            import winreg

            dx_versions = {}
            for dx in ["DirectX", "DirectX 10", "DirectX 11", "DirectX 12"]:
                try:
                    key = winreg.OpenKey(
                        winreg.HKEY_LOCAL_MACHINE, rf"SOFTWARE\Microsoft\{dx}"
                    )
                    dx_versions[dx] = "Installed"
                    winreg.CloseKey(key)
                except:
                    dx_versions[dx] = "Not found"
            gpu_info["directx_versions"] = dx_versions
        except:
            pass

        self.data["Graphics"] = gpu_info
        return gpu_info

    def analyze_memory(self):
        """Collect detailed memory information"""
        EnhancedUI.print_section_header("Memory (RAM)")

        memory_info = {
            "virtual_memory": {},
            "swap_memory": {},
            "physical_modules": [],
            "performance": {},
        }

        # Get virtual memory info
        if "psutil" in self.deps:
            try:
                vm = self.deps["psutil"].virtual_memory()
                memory_info["virtual_memory"] = {
                    "total": self.format_size(vm.total),
                    "available": self.format_size(vm.available),
                    "used": self.format_size(vm.used),
                    "free": self.format_size(vm.free),
                    "percent": f"{vm.percent}%",
                    "active": self.format_size(getattr(vm, "active", 0)),
                    "inactive": self.format_size(getattr(vm, "inactive", 0)),
                    "buffers": self.format_size(getattr(vm, "buffers", 0)),
                    "cached": self.format_size(getattr(vm, "cached", 0)),
                    "shared": self.format_size(getattr(vm, "shared", 0)),
                }

                # Get swap memory
                swap = self.deps["psutil"].swap_memory()
                memory_info["swap_memory"] = {
                    "total": self.format_size(swap.total),
                    "used": self.format_size(swap.used),
                    "free": self.format_size(swap.free),
                    "percent": f"{swap.percent}%",
                    "sin": self.format_size(swap.sin),
                    "sout": self.format_size(swap.sout),
                }
            except Exception as e:
                self.errors.append(f"Psutil memory error: {str(e)}")

        # Get physical memory modules
        if self.wmi:
            try:
                for i, mem in enumerate(self.wmi.Win32_PhysicalMemory()):
                    module = {
                        "bank": mem.BankLabel if mem.BankLabel else f"Bank {i}",
                        "capacity": (
                            self.format_size(int(mem.Capacity))
                            if mem.Capacity
                            else "Unknown"
                        ),
                        "speed": f"{mem.Speed} MHz" if mem.Speed else "Unknown",
                        "manufacturer": (
                            mem.Manufacturer if mem.Manufacturer else "Unknown"
                        ),
                        "serial": mem.SerialNumber if mem.SerialNumber else "Unknown",
                        "part_number": mem.PartNumber if mem.PartNumber else "Unknown",
                        "form_factor": self.safe_execute(
                            lambda: mem.FormFactor, "Memory", "Unknown"
                        ),
                        "memory_type": self.safe_execute(
                            lambda: mem.MemoryType, "Memory", "Unknown"
                        ),
                        "data_width": (
                            f"{mem.DataWidth} bits" if mem.DataWidth else "Unknown"
                        ),
                        "total_width": (
                            f"{mem.TotalWidth} bits" if mem.TotalWidth else "Unknown"
                        ),
                        "device_locator": (
                            mem.DeviceLocator if mem.DeviceLocator else "Unknown"
                        ),
                    }
                    memory_info["physical_modules"].append(module)
            except Exception as e:
                self.errors.append(f"WMI memory error: {str(e)}")

            # Get memory array info
            try:
                for array in self.wmi.Win32_PhysicalMemoryArray()[:1]:
                    memory_info["memory_array"] = {
                        "memory_devices": array.MemoryDevices,
                        "max_capacity": (
                            self.format_size(int(array.MaxCapacity) * 1024)
                            if array.MaxCapacity
                            else "Unknown"
                        ),
                        "memory_error_correction": self.safe_execute(
                            lambda: array.MemoryErrorCorrection, "Memory", "Unknown"
                        ),
                    }
                    break
            except:
                pass

        # Memory performance from WMI
        if self.wmi:
            try:
                for perf in self.wmi.Win32_PerfRawData_PerfOS_Memory()[:1]:
                    memory_info["performance"] = {
                        "available_bytes": self.format_size(int(perf.AvailableBytes)),
                        "cache_bytes": self.format_size(int(perf.CacheBytes)),
                        "cache_bytes_peak": self.format_size(int(perf.CacheBytesPeak)),
                        "committed_bytes": self.format_size(int(perf.CommittedBytes)),
                        "page_faults_per_sec": f"{int(perf.PageFaultsPersec):,}",
                        "pages_per_sec": f"{int(perf.PagesPersec):,}",
                        "pool_nonpaged_bytes": self.format_size(
                            int(perf.PoolNonpagedBytes)
                        ),
                        "pool_paged_bytes": self.format_size(int(perf.PoolPagedBytes)),
                    }
                    break
            except:
                pass

        self.data["Memory"] = memory_info
        return memory_info

    def analyze_storage(self):
        """Collect detailed storage information including SMART data"""
        EnhancedUI.print_section_header("Storage (Disks)")

        storage_info = {
            "physical_disks": [],
            "logical_disks": [],
            "partitions": [],
            "volumes": [],
            "performance": {},
            "smart_data": [],
        }

        # Get physical disks from WMI
        if self.wmi:
            try:
                for disk in self.wmi.Win32_DiskDrive():
                    disk_info = {
                        "index": disk.Index,
                        "model": disk.Model.strip() if disk.Model else "Unknown",
                        "manufacturer": (
                            disk.Manufacturer.strip()
                            if disk.Manufacturer
                            else "Unknown"
                        ),
                        "interface_type": (
                            disk.InterfaceType if disk.InterfaceType else "Unknown"
                        ),
                        "media_type": disk.MediaType if disk.MediaType else "Unknown",
                        "size": (
                            self.format_size(int(disk.Size)) if disk.Size else "Unknown"
                        ),
                        "serial_number": (
                            disk.SerialNumber.strip()
                            if disk.SerialNumber
                            else "Unknown"
                        ),
                        "firmware_revision": (
                            disk.FirmwareRevision
                            if disk.FirmwareRevision
                            else "Unknown"
                        ),
                        "partitions": disk.Partitions,
                        "bytes_per_sector": (
                            f"{disk.BytesPerSector} bytes"
                            if disk.BytesPerSector
                            else "Unknown"
                        ),
                        "total_cylinders": (
                            f"{disk.TotalCylinders:,}"
                            if disk.TotalCylinders
                            else "Unknown"
                        ),
                        "total_heads": (
                            disk.TotalHeads if disk.TotalHeads else "Unknown"
                        ),
                        "total_sectors": (
                            f"{disk.TotalSectors:,}" if disk.TotalSectors else "Unknown"
                        ),
                        "total_tracks": (
                            f"{disk.TotalTracks:,}" if disk.TotalTracks else "Unknown"
                        ),
                        "tracks_per_cylinder": (
                            disk.TracksPerCylinder
                            if disk.TracksPerCylinder
                            else "Unknown"
                        ),
                        "sectors_per_track": (
                            disk.SectorsPerTrack if disk.SectorsPerTrack else "Unknown"
                        ),
                        "pnp_device_id": (
                            disk.PNPDeviceID if disk.PNPDeviceID else "Unknown"
                        ),
                        "status": disk.Status if disk.Status else "Unknown",
                    }

                    # Determine disk type
                    model_upper = disk_info["model"].upper()
                    if "SSD" in model_upper:
                        disk_info["type"] = "SSD"
                    elif "NVME" in model_upper or "M.2" in model_upper:
                        disk_info["type"] = "NVMe SSD"
                    elif "HDD" in model_upper or "HARD DISK" in model_upper:
                        disk_info["type"] = "HDD"
                    elif disk_info["media_type"] == "Fixed hard disk media":
                        disk_info["type"] = "HDD"
                    else:
                        disk_info["type"] = "Unknown"

                    storage_info["physical_disks"].append(disk_info)

                    # Try to get SMART data
                    if self.is_admin:
                        smart = self._get_smart_data(disk.Index)
                        if smart:
                            storage_info["smart_data"].append(
                                {"disk": disk.Index, "data": smart}
                            )
            except Exception as e:
                self.errors.append(f"WMI disk error: {str(e)}")

        # Get logical disks (drive letters)
        if self.wmi:
            try:
                for logical in self.wmi.Win32_LogicalDisk():
                    disk_data = {
                        "device_id": logical.DeviceID,
                        "volume_name": logical.VolumeName if logical.VolumeName else "",
                        "file_system": (
                            logical.FileSystem if logical.FileSystem else "Unknown"
                        ),
                        "size": (
                            self.format_size(int(logical.Size))
                            if logical.Size
                            else "Unknown"
                        ),
                        "free_space": (
                            self.format_size(int(logical.FreeSpace))
                            if logical.FreeSpace
                            else "Unknown"
                        ),
                        "drive_type": logical.DriveType,
                        "drive_type_name": {
                            0: "Unknown",
                            1: "No Root Directory",
                            2: "Removable Disk",
                            3: "Local Disk",
                            4: "Network Drive",
                            5: "CD-ROM",
                            6: "RAM Disk",
                        }.get(int(logical.DriveType), "Unknown"),
                        "compressed": "Yes" if logical.Compressed else "No",
                        "serial_number": (
                            logical.VolumeSerialNumber
                            if logical.VolumeSerialNumber
                            else "Unknown"
                        ),
                    }

                    # Calculate usage percentage
                    if logical.Size and logical.FreeSpace:
                        used = int(logical.Size) - int(logical.FreeSpace)
                        disk_data["used_space"] = self.format_size(used)
                        disk_data["percent_used"] = (
                            f"{(used / int(logical.Size)) * 100:.1f}%"
                        )

                    storage_info["logical_disks"].append(disk_data)
            except Exception as e:
                self.errors.append(f"WMI logical disk error: {str(e)}")

        # Get disk partitions
        if self.wmi:
            try:
                for partition in self.wmi.Win32_DiskPartition():
                    part_info = {
                        "device_id": partition.DeviceID,
                        "disk_index": partition.DiskIndex,
                        "index": partition.Index,
                        "size": (
                            self.format_size(int(partition.Size))
                            if partition.Size
                            else "Unknown"
                        ),
                        "starting_offset": (
                            self.format_size(int(partition.StartingOffset))
                            if partition.StartingOffset
                            else "Unknown"
                        ),
                        "type": partition.Type if partition.Type else "Unknown",
                        "bootable": "Yes" if partition.Bootable else "No",
                        "boot_partition": "Yes" if partition.BootPartition else "No",
                        "primary_partition": (
                            "Yes" if partition.PrimaryPartition else "No"
                        ),
                        "hidden_sectors": (
                            partition.HiddenSectors
                            if partition.HiddenSectors
                            else "Unknown"
                        ),
                    }
                    storage_info["partitions"].append(part_info)
            except:
                pass

        # Get disk usage from psutil
        if "psutil" in self.deps:
            try:
                partitions = self.deps["psutil"].disk_partitions(all=False)
                for partition in partitions:
                    try:
                        usage = self.deps["psutil"].disk_usage(partition.mountpoint)
                        volume_info = {
                            "device": partition.device,
                            "mountpoint": partition.mountpoint,
                            "fstype": partition.fstype,
                            "opts": partition.opts,
                            "total": self.format_size(usage.total),
                            "used": self.format_size(usage.used),
                            "free": self.format_size(usage.free),
                            "percent": f"{usage.percent}%",
                        }
                        storage_info["volumes"].append(volume_info)
                    except:
                        continue
            except Exception as e:
                self.errors.append(f"Psutil disk error: {str(e)}")

            # Get disk I/O statistics
            try:
                io_counters = self.deps["psutil"].disk_io_counters(perdisk=False)
                if io_counters:
                    storage_info["performance"] = {
                        "read_count": f"{io_counters.read_count:,}",
                        "write_count": f"{io_counters.write_count:,}",
                        "read_bytes": self.format_size(io_counters.read_bytes),
                        "write_bytes": self.format_size(io_counters.write_bytes),
                        "read_time": f"{io_counters.read_time} ms",
                        "write_time": f"{io_counters.write_time} ms",
                    }
            except:
                pass

        self.data["Storage"] = storage_info
        return storage_info

    def _get_smart_data(self, disk_index):
        """Retrieve SMART data for a physical disk (admin required)"""
        smart = {}
        try:
            # Use wmic to get SMART status (limited)
            result = subprocess.run(
                ["wmic", "diskdrive", f"where index={disk_index}", "get", "status"],
                capture_output=True,
                text=True,
                shell=True,
                timeout=5,
            )
            if result.returncode == 0:
                lines = result.stdout.strip().split("\n")
                if len(lines) >= 2:
                    smart["status"] = lines[1].strip()
        except:
            smart["status"] = "Unknown"

        # Try to get more detailed SMART via PowerShell (if available)
        try:
            ps_cmd = f"Get-PhysicalDisk -DeviceNumber {disk_index} | Select-Object HealthStatus, OperationalStatus, MediaType, SpindleSpeed | ConvertTo-Json"
            result = subprocess.run(
                ["powershell", "-Command", ps_cmd],
                capture_output=True,
                text=True,
                shell=True,
                timeout=5,
            )
            if result.returncode == 0 and result.stdout.strip():
                data = json.loads(result.stdout)
                smart.update(data)
        except:
            pass

        return smart

    def analyze_network(self):
        """Collect detailed network information"""
        EnhancedUI.print_section_header("Network")

        network_info = {
            "interfaces": [],
            "connections": [],
            "configuration": {},
            "statistics": {},
            "wireless": {},
            "dns_cache": [],
            "arp_table": [],
            "firewall_rules": [],
            "proxy_settings": {},
        }

        # Get network interfaces from psutil
        if "psutil" in self.deps:
            try:
                addrs = self.deps["psutil"].net_if_addrs()
                stats = self.deps["psutil"].net_if_stats()

                for iface, addr_list in addrs.items():
                    iface_info = {"name": iface, "addresses": [], "statistics": {}}

                    for addr in addr_list:
                        addr_data = {
                            "family": str(addr.family),
                            "address": addr.address,
                            "netmask": addr.netmask if addr.netmask else None,
                            "broadcast": addr.broadcast if addr.broadcast else None,
                            "ptp": addr.ptp if addr.ptp else None,
                        }
                        iface_info["addresses"].append(addr_data)

                    # Interface statistics
                    if iface in stats:
                        stat = stats[iface]
                        iface_info["statistics"] = {
                            "is_up": "Yes" if stat.isup else "No",
                            "duplex": {0: "Unknown", 1: "Half", 2: "Full"}.get(
                                stat.duplex, "Unknown"
                            ),
                            "speed": f"{stat.speed} Mbps",
                            "mtu": stat.mtu,
                        }

                    network_info["interfaces"].append(iface_info)
            except Exception as e:
                self.errors.append(f"Psutil network error: {str(e)}")

        # Get network configuration from WMI
        if self.wmi:
            try:
                adapters = []
                for adapter in self.wmi.Win32_NetworkAdapterConfiguration(
                    IPEnabled=True
                ):
                    adapter_info = {
                        "description": adapter.Description,
                        "mac_address": adapter.MACAddress,
                        "ip_addresses": (
                            list(adapter.IPAddress) if adapter.IPAddress else []
                        ),
                        "subnet_masks": (
                            list(adapter.IPSubnet) if adapter.IPSubnet else []
                        ),
                        "default_gateways": (
                            list(adapter.DefaultIPGateway)
                            if adapter.DefaultIPGateway
                            else []
                        ),
                        "dhcp_enabled": "Yes" if adapter.DHCPEnabled else "No",
                        "dhcp_server": adapter.DHCPServer if adapter.DHCPServer else "",
                        "dns_servers": (
                            list(adapter.DNSServerSearchOrder)
                            if adapter.DNSServerSearchOrder
                            else []
                        ),
                        "dns_domain": adapter.DNSDomain if adapter.DNSDomain else "",
                        "wins_primary": (
                            adapter.WINSPrimaryServer
                            if adapter.WINSPrimaryServer
                            else ""
                        ),
                        "wins_secondary": (
                            adapter.WINSSecondaryServer
                            if adapter.WINSSecondaryServer
                            else ""
                        ),
                        "mtu": adapter.MTU if adapter.MTU else "Unknown",
                    }
                    adapters.append(adapter_info)

                network_info["configuration"] = {
                    "adapters": adapters,
                    "hostname": socket.gethostname(),
                    "fqdn": socket.getfqdn(),
                    "domain": os.environ.get("USERDOMAIN", "Unknown"),
                }
            except Exception as e:
                self.errors.append(f"WMI network error: {str(e)}")

        # Get network statistics
        if "psutil" in self.deps:
            try:
                io_counters = self.deps["psutil"].net_io_counters()
                network_info["statistics"] = {
                    "bytes_sent": self.format_size(io_counters.bytes_sent),
                    "bytes_recv": self.format_size(io_counters.bytes_recv),
                    "packets_sent": f"{io_counters.packets_sent:,}",
                    "packets_recv": f"{io_counters.packets_recv:,}",
                    "errin": f"{io_counters.errin:,}",
                    "errout": f"{io_counters.errout:,}",
                    "dropin": f"{io_counters.dropin:,}",
                    "dropout": f"{io_counters.dropout:,}",
                }
            except:
                pass

        # Get wireless network info (if available)
        if self.is_admin:
            try:
                import subprocess

                result = subprocess.run(
                    ["netsh", "wlan", "show", "interfaces"],
                    capture_output=True,
                    text=True,
                    shell=True,
                )
                if result.returncode == 0:
                    lines = result.stdout.split("\n")
                    wireless_info = {}
                    for line in lines:
                        if ":" in line:
                            key, value = line.split(":", 1)
                            wireless_info[key.strip()] = value.strip()

                    if wireless_info:
                        network_info["wireless"]["current"] = wireless_info

                # Get saved Wi-Fi profiles
                result = subprocess.run(
                    ["netsh", "wlan", "show", "profiles"],
                    capture_output=True,
                    text=True,
                    shell=True,
                )
                if result.returncode == 0:
                    profiles = []
                    for line in result.stdout.split("\n"):
                        if "All User Profile" in line:
                            ssid = line.split(":")[1].strip()
                            profiles.append(ssid)
                    network_info["wireless"]["saved_profiles"] = profiles
            except:
                pass

        # Get DNS cache
        if self.is_admin:
            try:
                result = subprocess.run(
                    ["ipconfig", "/displaydns"],
                    capture_output=True,
                    text=True,
                    shell=True,
                )
                if result.returncode == 0:
                    # Basic parsing, could be improved
                    network_info["dns_cache"] = result.stdout[:500]
            except:
                pass

        # Get ARP table
        try:
            result = subprocess.run(
                ["arp", "-a"], capture_output=True, text=True, shell=True
            )
            if result.returncode == 0:
                network_info["arp_table"] = result.stdout[:500]
        except:
            pass

        # Get proxy settings from registry
        try:
            import winreg

            key = winreg.OpenKey(
                winreg.HKEY_CURRENT_USER,
                r"Software\Microsoft\Windows\CurrentVersion\Internet Settings",
            )
            proxy_enable, _ = winreg.QueryValueEx(key, "ProxyEnable")
            proxy_server, _ = winreg.QueryValueEx(key, "ProxyServer")
            network_info["proxy_settings"] = {
                "enabled": "Yes" if proxy_enable else "No",
                "server": proxy_server if proxy_server else "",
            }
            winreg.CloseKey(key)
        except:
            pass

        # Get Windows Firewall rules
        if self.is_admin:
            try:
                result = subprocess.run(
                    ["netsh", "advfirewall", "firewall", "show", "rule", "name=all"],
                    capture_output=True,
                    text=True,
                    shell=True,
                )
                if result.returncode == 0:
                    # Truncate for brevity
                    network_info["firewall_rules"] = result.stdout[:1000]
            except:
                pass

        # Get public IP (external)
        try:
            import urllib.request

            with urllib.request.urlopen("https://api.ipify.org", timeout=5) as response:
                network_info["public_ip"] = response.read().decode("utf-8")
        except:
            network_info["public_ip"] = "Not available"

        self.data["Network"] = network_info
        return network_info

    def analyze_audio(self):
        """Collect audio device information"""
        EnhancedUI.print_section_header("Audio Devices")

        audio_info = {"devices": [], "drivers": [], "configuration": {}}

        # Get audio devices from WMI
        if self.wmi:
            try:
                for sound in self.wmi.Win32_SoundDevice():
                    device = {
                        "name": sound.ProductName if sound.ProductName else "Unknown",
                        "manufacturer": (
                            sound.Manufacturer if sound.Manufacturer else "Unknown"
                        ),
                        "status": sound.Status if sound.Status else "Unknown",
                        "pnp_device_id": (
                            sound.PNPDeviceID if sound.PNPDeviceID else "Unknown"
                        ),
                    }
                    audio_info["devices"].append(device)
            except Exception as e:
                self.errors.append(f"WMI audio error: {str(e)}")

        # Try to get audio information from registry
        try:
            import winreg

            audio_registry = {}

            # Check for audio devices in registry
            try:
                key = winreg.OpenKey(
                    winreg.HKEY_LOCAL_MACHINE,
                    r"SYSTEM\CurrentControlSet\Control\Class\{4d36e96c-e325-11ce-bfc1-08002be10318}",
                )

                i = 0
                while True:
                    try:
                        subkey_name = winreg.EnumKey(key, i)
                        subkey = winreg.OpenKey(key, subkey_name)

                        try:
                            driver_desc, _ = winreg.QueryValueEx(subkey, "DriverDesc")
                            audio_registry[subkey_name] = driver_desc
                        except:
                            pass

                        winreg.CloseKey(subkey)
                        i += 1
                    except OSError:
                        break

                winreg.CloseKey(key)
            except:
                pass

            if audio_registry:
                audio_info["registry_devices"] = audio_registry
        except:
            pass

        self.data["Audio"] = audio_info
        return audio_info

    def analyze_motherboard(self):
        """Collect motherboard information"""
        EnhancedUI.print_section_header("Motherboard")

        mb_info = {"baseboard": {}, "bios": {}, "chassis": {}}

        # Get baseboard (motherboard) info
        if self.wmi:
            try:
                for baseboard in self.wmi.Win32_BaseBoard():
                    mb_info["baseboard"] = {
                        "manufacturer": (
                            baseboard.Manufacturer
                            if baseboard.Manufacturer
                            else "Unknown"
                        ),
                        "product": (
                            baseboard.Product if baseboard.Product else "Unknown"
                        ),
                        "version": (
                            baseboard.Version if baseboard.Version else "Unknown"
                        ),
                        "serial_number": (
                            baseboard.SerialNumber
                            if baseboard.SerialNumber
                            else "Unknown"
                        ),
                        "part_number": (
                            baseboard.PartNumber if baseboard.PartNumber else "Unknown"
                        ),
                        "hosting_board": "Yes" if baseboard.HostingBoard else "No",
                        "hot_swappable": (
                            "Yes"
                            if hasattr(baseboard, "HotSwappable")
                            and baseboard.HotSwappable
                            else "No"
                        ),
                        "removable": "Yes" if baseboard.Removable else "No",
                        "replaceable": "Yes" if baseboard.Replaceable else "No",
                    }
                    break
            except Exception as e:
                self.errors.append(f"WMI baseboard error: {str(e)}")

        # Get BIOS info
        if self.wmi:
            try:
                for bios in self.wmi.Win32_BIOS():
                    mb_info["bios"] = {
                        "manufacturer": (
                            bios.Manufacturer if bios.Manufacturer else "Unknown"
                        ),
                        "name": bios.Name if bios.Name else "Unknown",
                        "serial_number": (
                            bios.SerialNumber if bios.SerialNumber else "Unknown"
                        ),
                        "version": (
                            bios.SMBIOSBIOSVersion
                            if bios.SMBIOSBIOSVersion
                            else "Unknown"
                        ),
                        "release_date": (
                            bios.ReleaseDate.split("T")[0]
                            if bios.ReleaseDate
                            else "Unknown"
                        ),
                        "smbios_version": f"{bios.SMBIOSMajorVersion}.{bios.SMBIOSMinorVersion}",
                        "bios_version": bios.Version if bios.Version else "Unknown",
                    }
                    break
            except Exception as e:
                self.errors.append(f"WMI BIOS error: {str(e)}")

        # Get chassis info
        if self.wmi:
            try:
                for chassis in self.wmi.Win32_SystemEnclosure():
                    mb_info["chassis"] = {
                        "manufacturer": (
                            chassis.Manufacturer if chassis.Manufacturer else "Unknown"
                        ),
                        "serial_number": (
                            chassis.SerialNumber if chassis.SerialNumber else "Unknown"
                        ),
                        "chassis_types": (
                            [str(t) for t in chassis.ChassisTypes]
                            if chassis.ChassisTypes
                            else []
                        ),
                        "security_status": (
                            chassis.SecurityStatus
                            if chassis.SecurityStatus
                            else "Unknown"
                        ),
                        "sku": (
                            chassis.SMBIOSAssetTag
                            if chassis.SMBIOSAssetTag
                            else "Unknown"
                        ),
                    }
                    break
            except Exception as e:
                self.errors.append(f"WMI chassis error: {str(e)}")

        self.data["Motherboard"] = mb_info
        return mb_info

    def analyze_power(self):
        """Collect power and battery information including cycle count and wear"""
        EnhancedUI.print_section_header("Power & Battery")

        power_info = {"battery": {}, "power_supply": {}, "settings": {}}

        # Get battery info from psutil
        if "psutil" in self.deps:
            try:
                battery = self.deps["psutil"].sensors_battery()
                if battery:
                    power_info["battery"]["psutil"] = {
                        "percent": f"{battery.percent}%",
                        "plugged": "Yes" if battery.power_plugged else "No",
                        "secs_left": (
                            battery.secsleft
                            if battery.secsleft
                            != self.deps["psutil"].POWER_TIME_UNKNOWN
                            else "Unknown"
                        ),
                        "time_left": self._format_battery_time(battery.secsleft),
                    }
            except:
                pass

        # Get detailed battery info from WMI
        if self.wmi:
            try:
                batteries = []
                for batt in self.wmi.Win32_Battery():
                    battery_data = {
                        "name": batt.Name if batt.Name else "Unknown",
                        "device_id": batt.DeviceID if batt.DeviceID else "Unknown",
                        "battery_status": batt.BatteryStatus,
                        "battery_status_description": self._get_battery_status(
                            batt.BatteryStatus
                        ),
                        "chemistry": batt.Chemistry if batt.Chemistry else "Unknown",
                        "design_capacity": (
                            f"{batt.DesignCapacity} mWh"
                            if batt.DesignCapacity
                            else "Unknown"
                        ),
                        "full_charge_capacity": (
                            f"{batt.FullChargeCapacity} mWh"
                            if batt.FullChargeCapacity
                            else "Unknown"
                        ),
                        "estimated_charge_remaining": (
                            f"{batt.EstimatedChargeRemaining}%"
                            if batt.EstimatedChargeRemaining
                            else "Unknown"
                        ),
                        "estimated_run_time": (
                            f"{batt.EstimatedRunTime} minutes"
                            if batt.EstimatedRunTime
                            else "Unknown"
                        ),
                        "expected_battery_life": (
                            f"{batt.ExpectedBatteryLife} minutes"
                            if batt.ExpectedBatteryLife
                            else "Unknown"
                        ),
                        "time_on_battery": (
                            f"{batt.TimeOnBattery} seconds"
                            if batt.TimeOnBattery
                            else "Unknown"
                        ),
                        "time_to_full_charge": (
                            f"{batt.TimeToFullCharge} minutes"
                            if batt.TimeToFullCharge
                            else "Unknown"
                        ),
                        "manufacturer": (
                            batt.Manufacturer if batt.Manufacturer else "Unknown"
                        ),
                        "manufacture_date": (
                            batt.ManufactureDate if batt.ManufactureDate else "Unknown"
                        ),
                        "serial_number": (
                            batt.SerialNumber if batt.SerialNumber else "Unknown"
                        ),
                    }

                    # Calculate battery health and wear
                    if batt.DesignCapacity and batt.FullChargeCapacity:
                        health = (
                            int(batt.FullChargeCapacity) / int(batt.DesignCapacity)
                        ) * 100
                        battery_data["health_percent"] = f"{health:.1f}%"
                        battery_data["health_status"] = self._get_battery_health(health)
                        battery_data["wear_level"] = f"{100 - health:.1f}%"

                    # Try to get cycle count (may not be available in all batteries)
                    # This is often in the registry
                    cycle_count = self._get_battery_cycle_count(batt.DeviceID)
                    if cycle_count:
                        battery_data["cycle_count"] = cycle_count

                    batteries.append(battery_data)

                if batteries:
                    power_info["battery"]["wmi"] = batteries
            except Exception as e:
                self.errors.append(f"WMI battery error: {str(e)}")

        # Get power supply info
        if self.wmi:
            try:
                for ps in self.wmi.Win32_PowerSupply()[:1]:
                    power_info["power_supply"] = {
                        "name": ps.Name if ps.Name else "Unknown",
                        "device_id": ps.DeviceID if ps.DeviceID else "Unknown",
                        "battery_installed": "Yes" if ps.BatteryInstalled else "No",
                        "can_power_off": "Yes" if ps.CanPowerOff else "No",
                        "current_voltage": (
                            f"{ps.CurrentVoltage} V" if ps.CurrentVoltage else "Unknown"
                        ),
                        "design_voltage": (
                            f"{ps.DesignVoltage} V" if ps.DesignVoltage else "Unknown"
                        ),
                        "max_voltage": (
                            f"{ps.MaxVoltage} V" if ps.MaxVoltage else "Unknown"
                        ),
                        "min_voltage": (
                            f"{ps.MinVoltage} V" if ps.MinVoltage else "Unknown"
                        ),
                        "output_voltage": (
                            f"{ps.OutputVoltage} V" if ps.OutputVoltage else "Unknown"
                        ),
                        "power_capacity": (
                            f"{ps.PowerCapacity} W" if ps.PowerCapacity else "Unknown"
                        ),
                    }
                    break
            except:
                pass

        # Get power settings
        try:
            import subprocess

            result = subprocess.run(
                ["powercfg", "/list"], capture_output=True, text=True, shell=True
            )
            if result.returncode == 0:
                power_info["settings"]["power_schemes"] = result.stdout[:500]
        except:
            pass

        self.data["Power"] = power_info
        return power_info

    def _get_battery_cycle_count(self, device_id):
        """Attempt to retrieve battery cycle count from registry"""
        try:
            import winreg

            # Try common registry location for battery cycle count
            key_path = f"SYSTEM\\CurrentControlSet\\Enum\\{device_id}\\Device Parameters"
            key = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, key_path)
            cycle_count, _ = winreg.QueryValueEx(key, "CycleCount")
            return str(cycle_count)
        except:
            return None

    def _format_battery_time(self, seconds):
        """Format battery time remaining"""
        if seconds == getattr(self.deps["psutil"], "POWER_TIME_UNLIMITED", -1):
            return "Unlimited"
        elif seconds == getattr(self.deps["psutil"], "POWER_TIME_UNKNOWN", -2):
            return "Unknown"
        elif seconds < 0:
            return "Unknown"
        else:
            hours = seconds // 3600
            minutes = (seconds % 3600) // 60
            return f"{hours}h {minutes}m"

    def _get_battery_status(self, status_code):
        """Get battery status description"""
        status_map = {
            1: "Other",
            2: "Unknown",
            3: "Fully Charged",
            4: "Low",
            5: "Critical",
            6: "Charging",
            7: "Charging and High",
            8: "Charging and Low",
            9: "Charging and Critical",
            10: "Undefined",
            11: "Partially Charged",
        }
        return status_map.get(status_code, "Unknown")

    def _get_battery_health(self, health_percent):
        """Get battery health description"""
        if health_percent >= 80:
            return "Excellent"
        elif health_percent >= 60:
            return "Good"
        elif health_percent >= 40:
            return "Fair"
        elif health_percent >= 20:
            return "Poor"
        else:
            return "Critical"

    def analyze_security(self):
        """Collect security information"""
        EnhancedUI.print_section_header("Security")

        security_info = {
            "user_accounts": [],
            "security_products": [],
            "firewall": {},
            "windows_defender": {},
            "bitlocker": [],
            "uefi_secure_boot": "Unknown",
            "tpm": {},
            "uac_level": "Unknown",
            "lsa_protection": "Unknown",
            "installed_certificates": [],
            "recommendations": [],
        }

        # Get user accounts
        if self.wmi:
            try:
                for user in self.wmi.Win32_UserAccount()[:10]:  # Limit to 10
                    user_info = {
                        "name": user.Name,
                        "full_name": user.FullName if user.FullName else "",
                        "disabled": "Yes" if user.Disabled else "No",
                        "domain": user.Domain,
                        "sid": user.SID,
                        "password_changeable": (
                            "Yes" if user.PasswordChangeable else "No"
                        ),
                        "password_expires": "Yes" if user.PasswordExpires else "No",
                        "password_required": "Yes" if user.PasswordRequired else "No",
                    }
                    security_info["user_accounts"].append(user_info)
            except:
                pass

        # Check admin privileges
        security_info["running_as_admin"] = "Yes" if self.is_admin else "No"

        # Get security products
        if self.wmi:
            try:
                # Antivirus
                for product in self.wmi.Win32_Product():
                    name = product.Name.lower()
                    if any(
                        term in name
                        for term in [
                            "antivirus",
                            "security",
                            "defender",
                            "norton",
                            "mcafee",
                            "kaspersky",
                            "avast",
                            "avg",
                        ]
                    ):
                        security_info["security_products"].append(
                            {
                                "name": product.Name,
                                "vendor": product.Vendor,
                                "version": product.Version,
                                "type": "Antivirus",
                            }
                        )
            except:
                pass

        # Check Windows Defender
        try:
            import winreg

            try:
                key = winreg.OpenKey(
                    winreg.HKEY_LOCAL_MACHINE, r"SOFTWARE\Microsoft\Windows Defender"
                )
                security_info["windows_defender"]["installed"] = "Yes"
                winreg.CloseKey(key)
            except:
                security_info["windows_defender"]["installed"] = "No"
        except:
            pass

        # Check UEFI Secure Boot
        try:
            import subprocess

            result = subprocess.run(
                ["powershell", "-Command", "Confirm-SecureBootUEFI"],
                capture_output=True,
                text=True,
                shell=True,
            )
            if "True" in result.stdout:
                security_info["uefi_secure_boot"] = "Enabled"
            elif "False" in result.stdout:
                security_info["uefi_secure_boot"] = "Disabled"
            else:
                security_info["uefi_secure_boot"] = "Unknown"
        except:
            pass

        # Get TPM status
        if self.wmi:
            try:
                for tpm in self.wmi.Win32_TPM()[:1]:
                    security_info["tpm"] = {
                        "is_activated": "Yes" if tpm.IsActivated_InitialValue else "No",
                        "is_enabled": "Yes" if tpm.IsEnabled_InitialValue else "No",
                        "is_owned": "Yes" if tpm.IsOwned_InitialValue else "No",
                        "manufacturer_version": (
                            tpm.ManufacturerVersion
                            if tpm.ManufacturerVersion
                            else "Unknown"
                        ),
                        "spec_version": (
                            tpm.SpecVersion if tpm.SpecVersion else "Unknown"
                        ),
                    }
                    break
            except:
                pass

        # Check UAC level from registry
        try:
            import winreg

            key = winreg.OpenKey(
                winreg.HKEY_LOCAL_MACHINE,
                r"SOFTWARE\Microsoft\Windows\CurrentVersion\Policies\System",
            )
            enable_lua, _ = winreg.QueryValueEx(key, "EnableLUA")
            if enable_lua == 1:
                consent_prompt, _ = winreg.QueryValueEx(key, "ConsentPromptBehaviorAdmin")
                uac_levels = {
                    0: "Never notify",
                    1: "Always notify (secure desktop)",
                    2: "Notify me only when apps try to make changes to my computer (default)",
                    3: "Notify me only when apps try to make changes to my computer (do not dim my desktop)",
                    4: "Never notify (disable UAC prompts)",
                    5: "Always notify (default for high security)",
                }
                security_info["uac_level"] = uac_levels.get(consent_prompt, str(consent_prompt))
            else:
                security_info["uac_level"] = "Disabled"
            winreg.CloseKey(key)
        except:
            pass

        # Check LSA protection (RunAsPPL)
        try:
            import winreg

            key = winreg.OpenKey(
                winreg.HKEY_LOCAL_MACHINE,
                r"SYSTEM\CurrentControlSet\Control\LSA",
            )
            runasppl, _ = winreg.QueryValueEx(key, "RunAsPPL")
            security_info["lsa_protection"] = "Enabled" if runasppl == 1 else "Disabled"
        except:
            pass

        # Get installed certificates (basic)
        try:
            import subprocess

            result = subprocess.run(
                ["certutil", "-store", "Root"],
                capture_output=True,
                text=True,
                shell=True,
            )
            if result.returncode == 0:
                # Simple count
                lines = result.stdout.split("\n")
                count = len([l for l in lines if "====" in l])
                security_info["installed_certificates"] = f"{count} certificates in Root store"
        except:
            pass

        # Generate security recommendations
        if not self.is_admin:
            security_info["recommendations"].append(
                "Run as Administrator for full security audit"
            )
        if security_info["uefi_secure_boot"] != "Enabled":
            security_info["recommendations"].append(
                "Enable Secure Boot in BIOS/UEFI settings"
            )
        if len(security_info["security_products"]) == 0:
            security_info["recommendations"].append("Install antivirus software")
        if security_info["lsa_protection"] != "Enabled":
            security_info["recommendations"].append(
                "Enable LSA protection (RunAsPPL) for enhanced security"
            )

        self.data["Security"] = security_info
        return security_info

    def analyze_performance(self):
        """Run performance benchmarks (enhanced with multi-threading and disk speed)"""
        EnhancedUI.print_section_header("Performance Benchmarks")

        perf_info = {
            "cpu_benchmark": {},
            "memory_benchmark": {},
            "disk_benchmark": {},
            "gpu_benchmark": {},
            "scores": {},
            "recommendations": [],
        }

        print("  Running CPU benchmark (multi-threaded)...")
        cpu_score = self._benchmark_cpu_advanced()
        perf_info["cpu_benchmark"] = cpu_score

        print("  Running memory benchmark...")
        mem_score = self._benchmark_memory()
        perf_info["memory_benchmark"] = mem_score

        print("  Running disk benchmark (sequential & random)...")
        disk_score = self._benchmark_disk_advanced()
        perf_info["disk_benchmark"] = disk_score

        print("  Calculating GPU score...")
        gpu_score = self._benchmark_gpu()
        perf_info["gpu_benchmark"] = gpu_score

        # Calculate overall scores
        overall = (
            cpu_score.get("score", 0)
            + mem_score.get("score", 0)
            + disk_score.get("score", 0)
            + gpu_score.get("score", 0)
        ) / 4

        perf_info["scores"] = {
            "cpu": cpu_score.get("score", 0),
            "memory": mem_score.get("score", 0),
            "disk": disk_score.get("score", 0),
            "gpu": gpu_score.get("score", 0),
            "overall": overall,
            "rating": self._get_performance_rating(overall),
        }

        # Generate recommendations
        if cpu_score.get("score", 0) < 5:
            perf_info["recommendations"].append(
                "Consider CPU upgrade for better performance"
            )
        if mem_score.get("score", 0) < 5:
            perf_info["recommendations"].append(
                "Consider adding more RAM or faster memory"
            )
        if disk_score.get("score", 0) < 5:
            perf_info["recommendations"].append(
                "Consider upgrading to SSD for faster storage"
            )
        if gpu_score.get("score", 0) < 3:
            perf_info["recommendations"].append(
                "Consider dedicated GPU for graphics-intensive tasks"
            )

        self.data["Performance"] = perf_info
        return perf_info

    def _benchmark_cpu_advanced(self):
        """Multi-threaded CPU benchmark"""
        import concurrent.futures

        def worker(n):
            start = time.perf_counter()
            for i in range(n):
                _ = math.sqrt(i) if i % 2 == 0 else math.pow(i, 0.5)
            return time.perf_counter() - start

        num_threads = os.cpu_count() or 4
        iterations_per_thread = 500000  # Adjust for reasonable time

        start_total = time.perf_counter()
        with concurrent.futures.ThreadPoolExecutor(max_workers=num_threads) as executor:
            futures = [executor.submit(worker, iterations_per_thread) for _ in range(num_threads)]
            results = [f.result() for f in futures]
        total_time = time.perf_counter() - start_total

        avg_time = sum(results) / len(results)
        # Score based on average time
        if avg_time < 0.2:
            score = 10
        elif avg_time < 0.4:
            score = 8
        elif avg_time < 0.6:
            score = 6
        elif avg_time < 0.8:
            score = 4
        elif avg_time < 1.0:
            score = 2
        else:
            score = 1

        return {
            "total_time_seconds": round(total_time, 3),
            "avg_thread_time": round(avg_time, 3),
            "threads": num_threads,
            "score": score,
            "rating": self._get_performance_rating(score),
        }

    def _benchmark_memory(self):
        """Benchmark memory performance"""
        start_time = time.perf_counter()

        # Memory-intensive operations
        data = list(range(1000000))
        doubled = [x * 2 for x in data]
        filtered = [x for x in doubled if x % 3 == 0]

        elapsed = time.perf_counter() - start_time

        # Score based on time
        if elapsed < 0.2:
            score = 10
        elif elapsed < 0.4:
            score = 8
        elif elapsed < 0.6:
            score = 6
        elif elapsed < 0.8:
            score = 4
        elif elapsed < 1.0:
            score = 2
        else:
            score = 1

        return {
            "time_seconds": round(elapsed, 3),
            "score": score,
            "rating": self._get_performance_rating(score),
        }

    def _benchmark_disk_advanced(self):
        """Benchmark disk sequential and random read/write performance"""
        try:
            import tempfile
            import os
            import random

            temp_file = None
            try:
                # Create temporary file
                with tempfile.NamedTemporaryFile(delete=False, mode="wb") as f:
                    temp_file = f.name

                    # Sequential write test (10MB)
                    data = os.urandom(10 * 1024 * 1024)  # 10MB
                    write_start = time.perf_counter()
                    f.write(data)
                    f.flush()
                    os.fsync(f.fileno())
                    write_time = time.perf_counter() - write_start

                    # Sequential read test
                    read_start = time.perf_counter()
                    with open(temp_file, "rb") as rf:
                        rf.read()
                    read_time = time.perf_counter() - read_start

                # Random read/write test (smaller file)
                with tempfile.NamedTemporaryFile(delete=False, mode="wb") as f:
                    temp_file2 = f.name
                    # Write 1000 random 4KB blocks
                    block_size = 4096
                    num_blocks = 1000
                    data_blocks = [os.urandom(block_size) for _ in range(num_blocks)]

                    # Random write
                    random_write_start = time.perf_counter()
                    for _ in range(num_blocks):
                        pos = random.randint(0, num_blocks - 1) * block_size
                        f.seek(pos)
                        f.write(data_blocks[pos // block_size])
                    f.flush()
                    os.fsync(f.fileno())
                    random_write_time = time.perf_counter() - random_write_start

                    # Random read
                    random_read_start = time.perf_counter()
                    with open(temp_file2, "rb") as rf:
                        for _ in range(num_blocks):
                            pos = random.randint(0, num_blocks - 1) * block_size
                            rf.seek(pos)
                            rf.read(block_size)
                    random_read_time = time.perf_counter() - random_read_start

                total_time = write_time + read_time + random_write_time + random_read_time

                # Score based on total time
                if total_time < 0.5:
                    score = 10
                elif total_time < 1.0:
                    score = 8
                elif total_time < 2.0:
                    score = 6
                elif total_time < 3.0:
                    score = 4
                elif total_time < 5.0:
                    score = 2
                else:
                    score = 1

                return {
                    "seq_write_seconds": round(write_time, 3),
                    "seq_read_seconds": round(read_time, 3),
                    "rand_write_seconds": round(random_write_time, 3),
                    "rand_read_seconds": round(random_read_time, 3),
                    "total_time_seconds": round(total_time, 3),
                    "throughput_seq_mbps": round(10 / (write_time + read_time), 2) if (write_time + read_time) > 0 else 0,
                    "score": score,
                    "rating": self._get_performance_rating(score),
                }

            finally:
                # Clean up
                if temp_file and os.path.exists(temp_file):
                    os.unlink(temp_file)
                if 'temp_file2' in locals() and os.path.exists(temp_file2):
                    os.unlink(temp_file2)
        except:
            return {
                "seq_write_seconds": "N/A",
                "seq_read_seconds": "N/A",
                "rand_write_seconds": "N/A",
                "rand_read_seconds": "N/A",
                "total_time_seconds": "N/A",
                "throughput_seq_mbps": "N/A",
                "score": 0,
                "rating": "Unknown",
            }

    def _benchmark_gpu(self):
        """Estimate GPU performance based on available info"""
        gpu_info = self.data.get("Graphics", {})
        gpus = gpu_info.get("gpus", [])

        score = 0

        if gpus:
            for gpu in gpus:
                gpu_type = gpu.get("type", "")
                vram = gpu.get("adapter_ram", "0")

                # Extract VRAM number
                vram_num = 0
                if "GB" in vram:
                    try:
                        vram_num = float(vram.split()[0])
                    except:
                        pass

                # Score based on GPU type and VRAM
                if "Dedicated" in gpu_type:
                    if vram_num >= 8:
                        score += 10
                    elif vram_num >= 4:
                        score += 8
                    elif vram_num >= 2:
                        score += 6
                    elif vram_num >= 1:
                        score += 4
                    else:
                        score += 2
                elif "Integrated" in gpu_type:
                    if vram_num >= 2:
                        score += 3
                    else:
                        score += 1

        # Cap at 10
        score = min(score, 10)

        return {
            "score": score,
            "rating": self._get_performance_rating(score),
            "gpu_count": len(gpus),
        }

    def _get_performance_rating(self, score):
        """Get performance rating based on score"""
        if score >= 9:
            return "Excellent"
        elif score >= 7:
            return "Very Good"
        elif score >= 5:
            return "Good"
        elif score >= 3:
            return "Fair"
        else:
            return "Poor"

    def analyze_software(self):
        """Collect software information"""
        EnhancedUI.print_section_header("Software")

        software_info = {
            "installed_programs": [],
            "windows_updates": [],
            "services": [],
            "processes": [],
            "python_packages": [],
        }

        # Get installed programs (limited without admin)
        if self.wmi and self.is_admin:
            try:
                for product in self.wmi.Win32_Product()[:50]:  # Limit to 50
                    program = {
                        "name": product.Name,
                        "version": product.Version if product.Version else "Unknown",
                        "vendor": product.Vendor if product.Vendor else "Unknown",
                        "install_date": (
                            product.InstallDate if product.InstallDate else "Unknown"
                        ),
                    }
                    software_info["installed_programs"].append(program)
            except:
                software_info["installed_programs"] = ["Requires admin privileges"]

        # Get Python packages
        try:
            result = subprocess.run(
                [sys.executable, "-m", "pip", "list", "--format=json"],
                capture_output=True,
                text=True,
                timeout=10,
            )
            if result.returncode == 0:
                packages = json.loads(result.stdout)
                software_info["python_packages"] = [
                    p["name"] for p in packages[:20]
                ]  # First 20
        except:
            pass

        # Get running processes (limited info without admin)
        if "psutil" in self.deps:
            try:
                processes = []
                for proc in self.deps["psutil"].process_iter(
                    ["pid", "name", "username"]
                )[
                    :20
                ]:  # First 20
                    try:
                        processes.append(
                            {
                                "pid": proc.info["pid"],
                                "name": proc.info["name"],
                                "user": (
                                    proc.info["username"]
                                    if proc.info["username"]
                                    else "Unknown"
                                ),
                            }
                        )
                    except:
                        continue
                software_info["processes"] = processes
            except:
                pass

        self.data["Software"] = software_info
        return software_info

    def analyze_hardware_health(self):
        """Analyze hardware health status"""
        EnhancedUI.print_section_header("Hardware Health")

        health_info = {"components": [], "warnings": [], "recommendations": []}

        # Check CPU temperature
        cpu_temp = self.data.get("Processor", {}).get("temperatures", {})
        if cpu_temp:
            for name, temp in cpu_temp.items():
                current = float(temp.get("current", "0").replace("°C", ""))
                if current > 80:
                    health_info["warnings"].append(f"CPU temperature high: {current}°C")
                elif current > 70:
                    health_info["warnings"].append(
                        f"CPU temperature elevated: {current}°C"
                    )

        # Check memory usage
        memory = self.data.get("Memory", {}).get("virtual_memory", {})
        if memory and "percent" in memory:
            usage = float(memory["percent"].replace("%", ""))
            if usage > 90:
                health_info["warnings"].append(f"Memory usage critical: {usage}%")
            elif usage > 80:
                health_info["warnings"].append(f"Memory usage high: {usage}%")

        # Check disk space
        storage = self.data.get("Storage", {}).get("logical_disks", [])
        for disk in storage:
            if "percent_used" in disk:
                usage = float(disk["percent_used"].replace("%", ""))
                if usage > 95:
                    health_info["warnings"].append(
                        f"Disk {disk.get('device_id', 'Unknown')} almost full: {usage}%"
                    )
                elif usage > 85:
                    health_info["warnings"].append(
                        f"Disk {disk.get('device_id', 'Unknown')} running low: {usage}%"
                    )

        # Check battery health
        power = self.data.get("Power", {}).get("battery", {}).get("wmi", [])
        for battery in power:
            if "health_percent" in battery:
                health = float(battery["health_percent"].replace("%", ""))
                if health < 50:
                    health_info["warnings"].append(f"Battery health poor: {health}%")
                elif health < 70:
                    health_info["warnings"].append(f"Battery health reduced: {health}%")

        # Check SMART status
        storage_smart = self.data.get("Storage", {}).get("smart_data", [])
        for smart in storage_smart:
            if smart.get("data", {}).get("status", "").upper() not in ["OK", "HEALTHY"]:
                health_info["warnings"].append(
                    f"Disk {smart['disk']} SMART status: {smart['data'].get('status', 'Unknown')}"
                )

        # Generate recommendations
        if len(health_info["warnings"]) == 0:
            health_info["recommendations"].append(
                "All hardware components appear healthy"
            )
        else:
            health_info["recommendations"].append(
                "Address the warnings above to maintain system health"
            )

        self.data["Hardware Health"] = health_info
        return health_info

    # New analysis sections

    def analyze_registry(self):
        """Collect registry information"""
        EnhancedUI.print_section_header("Registry")

        reg_info = {
            "installed_software": [],
            "startup_programs": [],
            "environment_variables": {},
            "windows_features": [],
            "device_classes": {},
        }

        try:
            import winreg

            # Installed software (Uninstall keys)
            uninstall_paths = [
                (winreg.HKEY_LOCAL_MACHINE, r"SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall"),
                (winreg.HKEY_LOCAL_MACHINE, r"SOFTWARE\WOW6432Node\Microsoft\Windows\CurrentVersion\Uninstall"),
                (winreg.HKEY_CURRENT_USER, r"SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall"),
            ]

            for hive, path in uninstall_paths:
                try:
                    with winreg.OpenKey(hive, path) as key:
                        i = 0
                        while True:
                            try:
                                subkey_name = winreg.EnumKey(key, i)
                                with winreg.OpenKey(key, subkey_name) as subkey:
                                    try:
                                        name, _ = winreg.QueryValueEx(subkey, "DisplayName")
                                        version, _ = winreg.QueryValueEx(subkey, "DisplayVersion")
                                        publisher, _ = winreg.QueryValueEx(subkey, "Publisher")
                                        install_date, _ = winreg.QueryValueEx(subkey, "InstallDate")
                                        reg_info["installed_software"].append({
                                            "name": name,
                                            "version": version,
                                            "publisher": publisher,
                                            "install_date": install_date,
                                        })
                                    except:
                                        pass
                                i += 1
                            except OSError:
                                break
                except:
                    pass

            # Startup programs
            startup_paths = [
                (winreg.HKEY_LOCAL_MACHINE, r"SOFTWARE\Microsoft\Windows\CurrentVersion\Run"),
                (winreg.HKEY_CURRENT_USER, r"SOFTWARE\Microsoft\Windows\CurrentVersion\Run"),
                (winreg.HKEY_LOCAL_MACHINE, r"SOFTWARE\Microsoft\Windows\CurrentVersion\RunOnce"),
                (winreg.HKEY_CURRENT_USER, r"SOFTWARE\Microsoft\Windows\CurrentVersion\RunOnce"),
            ]

            for hive, path in startup_paths:
                try:
                    with winreg.OpenKey(hive, path) as key:
                        i = 0
                        while True:
                            try:
                                name, value, _ = winreg.EnumValue(key, i)
                                reg_info["startup_programs"].append({
                                    "name": name,
                                    "command": value,
                                    "location": path,
                                })
                                i += 1
                            except OSError:
                                break
                except:
                    pass

            # Environment variables
            env_paths = [
                (winreg.HKEY_LOCAL_MACHINE, r"SYSTEM\CurrentControlSet\Control\Session Manager\Environment"),
                (winreg.HKEY_CURRENT_USER, r"Environment"),
            ]
            for hive, path in env_paths:
                try:
                    with winreg.OpenKey(hive, path) as key:
                        i = 0
                        while True:
                            try:
                                name, value, _ = winreg.EnumValue(key, i)
                                reg_info["environment_variables"][name] = value
                                i += 1
                            except OSError:
                                break
                except:
                    pass

            # Windows features (from registry)
            try:
                key = winreg.OpenKey(
                    winreg.HKEY_LOCAL_MACHINE,
                    r"SOFTWARE\Microsoft\Windows\CurrentVersion\Component Based Servicing\Packages",
                )
                i = 0
                features = set()
                while True:
                    try:
                        subkey_name = winreg.EnumKey(key, i)
                        if "~~" in subkey_name:
                            parts = subkey_name.split("~")
                            if len(parts) > 1:
                                feature = parts[1]
                                features.add(feature)
                        i += 1
                    except OSError:
                        break
                reg_info["windows_features"] = list(features)[:20]  # Limit
            except:
                pass

        except Exception as e:
            self.errors.append(f"Registry error: {str(e)}")

        self.data["Registry"] = reg_info
        return reg_info

    def analyze_modern_features(self):
        """Check modern Windows features: WSL, Hyper-V, Sandbox, Containers"""
        EnhancedUI.print_section_header("Modern Windows Features")

        features = {
            "hyper_v": "Unknown",
            "wsl": "Unknown",
            "windows_sandbox": "Unknown",
            "containers": "Unknown",
            "credential_guard": "Unknown",
            "device_guard": "Unknown",
            "applocker": "Unknown",
        }

        # Hyper-V
        try:
            result = subprocess.run(
                ["powershell", "-Command", "(Get-WindowsOptionalFeature -Online -FeatureName Microsoft-Hyper-V).State"],
                capture_output=True,
                text=True,
                shell=True,
            )
            features["hyper_v"] = "Enabled" if "Enabled" in result.stdout else "Disabled"
        except:
            pass

        # WSL
        try:
            result = subprocess.run(["wsl", "-l", "-v"], capture_output=True, text=True, shell=True)
            if result.returncode == 0:
                features["wsl"] = "Installed"
                # Could parse versions
            else:
                features["wsl"] = "Not installed"
        except:
            features["wsl"] = "Not available"

        # Windows Sandbox
        try:
            result = subprocess.run(
                ["powershell", "-Command", "(Get-WindowsOptionalFeature -Online -FeatureName Containers-DisposableClientVM).State"],
                capture_output=True,
                text=True,
                shell=True,
            )
            features["windows_sandbox"] = "Enabled" if "Enabled" in result.stdout else "Disabled"
        except:
            pass

        # Containers
        try:
            result = subprocess.run(
                ["powershell", "-Command", "(Get-WindowsOptionalFeature -Online -FeatureName Containers).State"],
                capture_output=True,
                text=True,
                shell=True,
            )
            features["containers"] = "Enabled" if "Enabled" in result.stdout else "Disabled"
        except:
            pass

        # Credential Guard / Device Guard (via registry)
        try:
            import winreg
            key = winreg.OpenKey(
                winreg.HKEY_LOCAL_MACHINE,
                r"SYSTEM\CurrentControlSet\Control\DeviceGuard",
            )
            enable, _ = winreg.QueryValueEx(key, "EnableVirtualizationBasedSecurity")
            features["credential_guard"] = "Enabled" if enable == 1 else "Disabled"
        except:
            pass

        # AppLocker
        try:
            result = subprocess.run(
                ["powershell", "-Command", "Get-AppLockerPolicy -Effective | Select-Object -ExpandProperty RuleCollections"],
                capture_output=True,
                text=True,
                shell=True,
            )
            if result.returncode == 0 and result.stdout.strip():
                features["applocker"] = "Configured"
            else:
                features["applocker"] = "Not configured"
        except:
            pass

        self.data["Modern Windows Features"] = features
        return features

    def analyze_windows_updates(self):
        """Get Windows Update history"""
        EnhancedUI.print_section_header("Windows Updates")

        updates = {"last_checked": "Unknown", "installed_updates": []}

        try:
            # Try using PowerShell to get update history
            ps_cmd = """
            Get-WmiObject -Class Win32_QuickFixEngineering | 
            Select-Object HotFixID, Description, InstalledOn | 
            ConvertTo-Json
            """
            result = subprocess.run(
                ["powershell", "-Command", ps_cmd],
                capture_output=True,
                text=True,
                shell=True,
            )
            if result.returncode == 0 and result.stdout.strip():
                data = json.loads(result.stdout)
                if isinstance(data, list):
                    for item in data[:20]:  # Limit to 20
                        updates["installed_updates"].append({
                            "hotfix": item.get("HotFixID"),
                            "description": item.get("Description"),
                            "installed_on": item.get("InstalledOn"),
                        })
                else:
                    updates["installed_updates"] = [data]
        except:
            pass

        # Last checked time from registry
        try:
            import winreg
            key = winreg.OpenKey(
                winreg.HKEY_LOCAL_MACHINE,
                r"SOFTWARE\Microsoft\Windows\CurrentVersion\WindowsUpdate\Auto Update",
            )
            last_checked, _ = winreg.QueryValueEx(key, "LastWaitTimeout")
            if last_checked:
                # Convert from Windows file time
                dt = datetime(1601, 1, 1) + timedelta(seconds=last_checked / 10**7)
                updates["last_checked"] = dt.strftime("%Y-%m-%d %H:%M:%S")
        except:
            pass

        self.data["Windows Updates"] = updates
        return updates

    # ==================== MAIN ANALYSIS METHODS ====================

    def quick_overview(self):
        """Quick overview similar to IObit System Information"""
        print(
            f"\n{EnhancedUI.color_text('Running Quick System Overview...', 'OKBLUE')}"
        )

        overview_data = {}

        # Run essential analyses only
        sections = [
            ("System Overview", self.analyze_system_overview),
            ("Operating System", self.analyze_operating_system),
            ("Processor", self.analyze_processor),
            ("Graphics", self.analyze_graphics),
            ("Memory", self.analyze_memory),
            ("Storage", self.analyze_storage),
            ("Network", self.analyze_network),
        ]

        for i, (name, analyzer) in enumerate(sections):
            EnhancedUI.show_progress(i + 1, len(sections), f"Analyzing {name}")
            try:
                overview_data[name] = analyzer()
            except Exception as e:
                self.errors.append(f"{name}: {str(e)}")
                overview_data[name] = {"error": str(e)}

        return overview_data

    def comprehensive_hardware_analysis(self):
        """Comprehensive hardware analysis"""
        print(
            f"\n{EnhancedUI.color_text('Running Comprehensive Hardware Analysis...', 'OKBLUE')}"
        )

        hardware_data = {}

        sections = [
            ("System Overview", self.analyze_system_overview),
            ("Motherboard", self.analyze_motherboard),
            ("Processor", self.analyze_processor),
            ("Graphics", self.analyze_graphics),
            ("Memory", self.analyze_memory),
            ("Storage", self.analyze_storage),
            ("Audio", self.analyze_audio),
            ("Power", self.analyze_power),
        ]

        for i, (name, analyzer) in enumerate(sections):
            EnhancedUI.show_progress(i + 1, len(sections), f"Analyzing {name}")
            try:
                hardware_data[name] = analyzer()
            except Exception as e:
                self.errors.append(f"{name}: {str(e)}")
                hardware_data[name] = {"error": str(e)}

        return hardware_data

    def full_diagnostics(self):
        """Full system diagnostics with all sections"""
        print(
            f"\n{EnhancedUI.color_text('Running Full System Diagnostics...', 'OKBLUE')}"
        )

        self.scan_start_time = time.time()

        all_data = OrderedDict()

        sections = [
            ("System Overview", self.analyze_system_overview),
            ("Operating System", self.analyze_operating_system),
            ("Motherboard", self.analyze_motherboard),
            ("Processor", self.analyze_processor),
            ("Graphics", self.analyze_graphics),
            ("Memory", self.analyze_memory),
            ("Storage", self.analyze_storage),
            ("Network", self.analyze_network),
            ("Audio", self.analyze_audio),
            ("Power", self.analyze_power),
            ("Security", self.analyze_security),
            ("Performance", self.analyze_performance),
            ("Software", self.analyze_software),
            ("Hardware Health", self.analyze_hardware_health),
            ("Registry", self.analyze_registry),
            ("Modern Windows Features", self.analyze_modern_features),
            ("Windows Updates", self.analyze_windows_updates),
        ]

        for i, (name, analyzer) in enumerate(sections):
            EnhancedUI.show_progress(i + 1, len(sections), f"Analyzing {name}")
            try:
                all_data[name] = analyzer()
            except Exception as e:
                self.errors.append(f"{name}: {str(e)}")
                all_data[name] = {"error": str(e)}

        # Add metadata
        all_data["metadata"] = {
            "scan_type": "full_diagnostics",
            "scan_start": datetime.fromtimestamp(self.scan_start_time).isoformat(),
            "scan_duration_seconds": round(time.time() - self.scan_start_time, 2),
            "tool_version": Config.VERSION,
            "privileges": "Admin" if self.is_admin else "User",
            "errors_count": len(self.errors),
            "warnings_count": len(self.warnings),
        }

        self.data = all_data
        return all_data


# ==================== PROFESSIONAL REPORT GENERATOR ====================
class ProfessionalReportGenerator:
    """Generate professional reports in multiple formats"""

    def __init__(self, analyzer, output_dir="reports"):
        self.analyzer = analyzer
        self.timestamp = datetime.now()
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(exist_ok=True)

        self.filename_base = f"SystemAnalysis_{socket.gethostname()}_{self.timestamp.strftime('%Y%m%d_%H%M%S')}"

    def generate_text_report(self, data):
        """Generate comprehensive text report"""
        filename = self.output_dir / f"{self.filename_base}.txt"

        print(f"\n{EnhancedUI.color_text('Generating text report...', 'OKBLUE')}")

        with open(filename, "w", encoding="utf-8") as f:
            # Header
            f.write("=" * 80 + "\n")
            f.write(" " * 30 + "SYSTEM ANALYSIS REPORT\n")
            f.write("=" * 80 + "\n\n")

            f.write(
                f"Report Generated: {self.timestamp.strftime('%Y-%m-%d %H:%M:%S')}\n"
            )
            f.write(f"System: {socket.gethostname()}\n")
            f.write(f"Tool: Ultimate System Analyzer v{Config.VERSION}\n")
            f.write(
                f"Privileges: {'Administrator' if self.analyzer.is_admin else 'Standard User'}\n"
            )
            f.write("-" * 80 + "\n\n")

            # Executive Summary
            f.write("EXECUTIVE SUMMARY\n")
            f.write("-" * 40 + "\n")
            self._write_executive_summary(f, data)
            f.write("\n")

            # Detailed Sections
            for section_name, section_data in data.items():
                if section_name == "metadata":
                    continue

                f.write("\n" + "=" * 60 + "\n")
                f.write(f"{section_name.upper()}\n")
                f.write("=" * 60 + "\n\n")

                self._write_section_text(f, section_name, section_data)

            # Errors and Warnings
            if self.analyzer.errors or self.analyzer.warnings:
                f.write("\n" + "=" * 60 + "\n")
                f.write("ERRORS & WARNINGS\n")
                f.write("=" * 60 + "\n\n")

                if self.analyzer.errors:
                    f.write("Errors encountered:\n")
                    for error in self.analyzer.errors[:10]:
                        f.write(f"  • {error}\n")
                    if len(self.analyzer.errors) > 10:
                        f.write(f"  • ... and {len(self.analyzer.errors) - 10} more\n")
                    f.write("\n")

                if self.analyzer.warnings:
                    f.write("Warnings:\n")
                    for warning in self.analyzer.warnings:
                        f.write(f"  • {warning}\n")

            # Footer
            f.write("\n" + "=" * 80 + "\n")
            f.write("END OF REPORT\n")
            f.write("=" * 80 + "\n")

            if "metadata" in data:
                meta = data["metadata"]
                f.write(
                    f"\nScan Duration: {meta.get('scan_duration_seconds', 0)} seconds\n"
                )
                f.write(f"Total Components Analyzed: {len(data) - 1}\n")

        print(f"{EnhancedUI.color_text('✓ Text report saved:', 'OKGREEN')} {filename}")
        return str(filename)

    def _write_executive_summary(self, f, data):
        """Write executive summary"""
        # System Overview
        system = data.get("System Overview", {})
        f.write(f"Computer Name: {system.get('computer_name', 'Unknown')}\n")
        f.write(f"Manufacturer: {system.get('manufacturer', 'Unknown')}\n")
        f.write(f"Model: {system.get('model', 'Unknown')}\n")
        f.write(f"Serial: {system.get('serial_number', 'Unknown')}\n\n")

        # Operating System
        os_info = data.get("Operating System", {})
        f.write(
            f"OS: {os_info.get('windows_edition', os_info.get('name', 'Unknown'))}\n"
        )
        f.write(
            f"Version: {os_info.get('display_version', os_info.get('version', 'Unknown'))}\n"
        )
        f.write(f"Build: {os_info.get('build_number', 'Unknown')}\n\n")

        # Processor
        cpu = data.get("Processor", {}).get("basic_info", {})
        f.write(f"CPU: {cpu.get('brand', 'Unknown')}\n")
        f.write(f"Cores/Threads: {cpu.get('cores', 'Unknown')}\n")
        f.write(f"Speed: {cpu.get('hz_actual', 'Unknown')}\n\n")

        # Memory
        memory = data.get("Memory", {}).get("virtual_memory", {})
        f.write(f"Memory: {memory.get('total', 'Unknown')} Total\n")
        f.write(f"Available: {memory.get('available', 'Unknown')}\n")
        f.write(f"Usage: {memory.get('percent', 'Unknown')}\n\n")

        # Storage
        storage = data.get("Storage", {})
        disks = storage.get("physical_disks", [])
        if disks:
            total_size = 0
            for disk in disks:
                size_str = disk.get("size", "0 Bytes")
                try:
                    size_num = float(size_str.split()[0])
                    unit = size_str.split()[1]
                    if unit == "GB":
                        total_size += size_num
                    elif unit == "TB":
                        total_size += size_num * 1024
                except:
                    pass
            f.write(
                f"Storage: {total_size:.1f} GB total across {len(disks)} drive(s)\n\n"
            )

        # Graphics
        graphics = data.get("Graphics", {}).get("gpus", [])
        if graphics:
            gpu = graphics[0]
            f.write(f"Graphics: {gpu.get('name', 'Unknown')}\n")
            f.write(f"VRAM: {gpu.get('adapter_ram', 'Unknown')}\n\n")

        # Performance
        perf = data.get("Performance", {}).get("scores", {})
        if perf:
            f.write(
                f"Performance Score: {perf.get('overall', 0):.1f}/10 ({perf.get('rating', 'Unknown')})\n"
            )

    def _write_section_text(self, f, section_name, section_data):
        """Write section data to text file"""
        if isinstance(section_data, dict):
            if "error" in section_data:
                f.write(f"Error: {section_data['error']}\n\n")
                return

            for key, value in section_data.items():
                if key == "error":
                    continue

                # Handle nested dictionaries
                if isinstance(value, dict):
                    f.write(f"{key.replace('_', ' ').title()}:\n")
                    for subkey, subvalue in value.items():
                        if isinstance(subvalue, (list, dict)):
                            if subvalue:  # Only write if not empty
                                f.write(f"  {subkey.replace('_', ' ').title()}:\n")
                                self._write_nested(f, subvalue, indent=4)
                        else:
                            if subvalue and subvalue != "Unknown":
                                f.write(
                                    f"  {subkey.replace('_', ' ').title()}: {subvalue}\n"
                                )
                    f.write("\n")

                # Handle lists
                elif isinstance(value, list):
                    if value:  # Only write if not empty
                        f.write(f"{key.replace('_', ' ').title()} ({len(value)}):\n")
                        for item in value:
                            if isinstance(item, dict):
                                f.write("\n")
                                for subkey, subvalue in item.items():
                                    if subvalue and subvalue != "Unknown":
                                        f.write(
                                            f"    {subkey.replace('_', ' ').title()}: {subvalue}\n"
                                        )
                            else:
                                f.write(f"  • {item}\n")
                        f.write("\n")

                # Handle simple values
                else:
                    if value and value != "Unknown":
                        f.write(f"{key.replace('_', ' ').title()}: {value}\n")

    def _write_nested(self, f, data, indent=0):
        """Recursively write nested data"""
        indent_str = " " * indent

        if isinstance(data, dict):
            for k, v in data.items():
                if isinstance(v, (dict, list)):
                    f.write(f"{indent_str}{k.replace('_', ' ').title()}:\n")
                    self._write_nested(f, v, indent + 2)
                else:
                    if v and v != "Unknown":
                        f.write(f"{indent_str}{k.replace('_', ' ').title()}: {v}\n")

        elif isinstance(data, list):
            for item in data:
                if isinstance(item, dict):
                    for k, v in item.items():
                        if v and v != "Unknown":
                            f.write(
                                f"{indent_str}• {k.replace('_', ' ').title()}: {v}\n"
                            )
                    f.write("\n")
                else:
                    f.write(f"{indent_str}• {item}\n")

    def generate_json_report(self, data):
        """Generate JSON report"""
        filename = self.output_dir / f"{self.filename_base}.json"

        report_data = {
            "metadata": {
                "generated": self.timestamp.isoformat(),
                "system": socket.gethostname(),
                "tool": f"Ultimate System Analyzer v{Config.VERSION}",
                "privileges": "Admin" if self.analyzer.is_admin else "User",
            },
            "analysis_data": data,
        }

        with open(filename, "w", encoding="utf-8") as f:
            json.dump(report_data, f, indent=2, default=str)

        print(f"{EnhancedUI.color_text('✓ JSON report saved:', 'OKGREEN')} {filename}")
        return str(filename)

    def generate_html_report(self, data):
        """Generate HTML report"""
        filename = self.output_dir / f"{self.filename_base}.html"

        # Create a simple HTML report
        html = f"""<!DOCTYPE html>
<html>
<head>
    <title>System Analysis Report</title>
    <meta charset="utf-8">
    <style>
        body {{ font-family: Arial, sans-serif; margin: 40px; background: #f5f5f5; }}
        .container {{ max-width: 1200px; margin: 0 auto; background: white; padding: 30px; border-radius: 10px; box-shadow: 0 0 20px rgba(0,0,0,0.1); }}
        h1 {{ color: #2c3e50; border-bottom: 3px solid #3498db; padding-bottom: 10px; }}
        h2 {{ color: #34495e; border-left: 5px solid #3498db; padding-left: 15px; margin-top: 30px; }}
        .section {{ margin: 20px 0; padding: 15px; background: #f8f9fa; border-radius: 5px; }}
        .item {{ margin: 8px 0; }}
        .label {{ font-weight: bold; color: #2c3e50; min-width: 200px; display: inline-block; }}
        .value {{ color: #7f8c8d; }}
        .good {{ color: #27ae60; font-weight: bold; }}
        .warning {{ color: #f39c12; font-weight: bold; }}
        .error {{ color: #e74c3c; font-weight: bold; }}
        .summary {{ background: #e8f4fc; padding: 20px; border-radius: 5px; margin: 20px 0; }}
        table {{ width: 100%; border-collapse: collapse; margin: 15px 0; }}
        th {{ background: #3498db; color: white; padding: 10px; text-align: left; }}
        td {{ padding: 10px; border-bottom: 1px solid #ddd; }}
        tr:nth-child(even) {{ background: #f8f9fa; }}
        .footer {{ margin-top: 40px; padding-top: 20px; border-top: 2px solid #ecf0f1; color: #7f8c8d; font-size: 0.9em; text-align: center; }}
    </style>
</head>
<body>
    <div class="container">
        <h1>System Analysis Report</h1>
        
        <div class="summary">
            <div class="item"><span class="label">Generated:</span> <span class="value">{self.timestamp.strftime('%Y-%m-%d %H:%M:%S')}</span></div>
            <div class="item"><span class="label">System:</span> <span class="value">{socket.gethostname()}</span></div>
            <div class="item"><span class="label">Tool:</span> <span class="value">Ultimate System Analyzer v{Config.VERSION}</span></div>
            <div class="item"><span class="label">Privileges:</span> <span class="value">{'Administrator' if self.analyzer.is_admin else 'Standard User'}</span></div>
        </div>
"""

        # Add sections
        for section_name, section_data in data.items():
            if section_name == "metadata":
                continue

            html += f"""
        <h2>{section_name}</h2>
        <div class="section">
"""

            if isinstance(section_data, dict) and "error" in section_data:
                html += f'<div class="error">Error: {section_data["error"]}</div>'
            else:
                html += self._dict_to_html(section_data)

            html += """
        </div>
"""

        # Footer
        html += f"""
        <div class="footer">
            <p>Generated by Ultimate System Analyzer v{Config.VERSION}</p>
            <p>Report ID: {self.filename_base}</p>
        </div>
    </div>
</body>
</html>"""

        with open(filename, "w", encoding="utf-8") as f:
            f.write(html)

        print(f"{EnhancedUI.color_text('✓ HTML report saved:', 'OKGREEN')} {filename}")
        return str(filename)

    def _dict_to_html(self, data, level=0):
        """Convert dictionary to HTML"""
        html = ""

        if isinstance(data, dict):
            for key, value in data.items():
                if key == "error":
                    continue

                if isinstance(value, dict):
                    html += f'<div style="margin-left: {level * 20}px;"><strong>{key.replace("_", " ").title()}:</strong><br>'
                    html += self._dict_to_html(value, level + 1)
                    html += "</div>"
                elif isinstance(value, list):
                    if value:
                        html += f'<div style="margin-left: {level * 20}px;"><strong>{key.replace("_", " ").title()} ({len(value)}):</strong><br>'
                        for item in value:
                            if isinstance(item, dict):
                                html += self._dict_to_html(item, level + 1)
                            else:
                                html += f'<div style="margin-left: {(level + 1) * 20}px;">• {item}</div>'
                        html += "</div>"
                else:
                    if value and value != "Unknown":
                        # Apply styling based on value
                        if isinstance(value, str):
                            if "Excellent" in value or "Good" in value:
                                value_class = "good"
                            elif "Warning" in value or "Fair" in value:
                                value_class = "warning"
                            elif "Error" in value or "Poor" in value:
                                value_class = "error"
                            else:
                                value_class = "value"
                        else:
                            value_class = "value"

                        html += f'<div class="item" style="margin-left: {level * 20}px;"><span class="label">{key.replace("_", " ").title()}:</span> <span class="{value_class}">{value}</span></div>'

        return html

    def generate_pdf_report(self, data):
        """Generate PDF report (if reportlab is available)"""
        try:
            from reportlab.lib.pagesizes import A4
            from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
            from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
            from reportlab.lib import colors
            from reportlab.lib.units import inch

            filename = self.output_dir / f"{self.filename_base}.pdf"
            doc = SimpleDocTemplate(str(filename), pagesize=A4)
            styles = getSampleStyleSheet()
            story = []

            # Title
            title = Paragraph(f"System Analysis Report - {socket.gethostname()}", styles['Title'])
            story.append(title)
            story.append(Spacer(1, 0.2*inch))

            # Metadata
            meta = Paragraph(f"Generated: {self.timestamp.strftime('%Y-%m-%d %H:%M:%S')}<br/>Tool: Ultimate System Analyzer v{Config.VERSION}", styles['Normal'])
            story.append(meta)
            story.append(Spacer(1, 0.2*inch))

            # Executive Summary as table
            system = data.get("System Overview", {})
            os_info = data.get("Operating System", {})
            cpu = data.get("Processor", {}).get("basic_info", {})
            memory = data.get("Memory", {}).get("virtual_memory", {})

            summary_data = [
                ["Computer Name", system.get("computer_name", "Unknown")],
                ["Manufacturer", system.get("manufacturer", "Unknown")],
                ["Model", system.get("model", "Unknown")],
                ["OS", os_info.get("windows_edition", os_info.get("name", "Unknown"))],
                ["CPU", cpu.get("brand", "Unknown")],
                ["Cores", cpu.get("cores", "Unknown")],
                ["Memory", memory.get("total", "Unknown")],
            ]
            summary_table = Table(summary_data, colWidths=[1.5*inch, 4*inch])
            summary_table.setStyle(TableStyle([
                ('BACKGROUND', (0,0), (-1,0), colors.grey),
                ('TEXTCOLOR', (0,0), (-1,0), colors.whitesmoke),
                ('ALIGN', (0,0), (-1,-1), 'LEFT'),
                ('FONTNAME', (0,0), (-1,0), 'Helvetica-Bold'),
                ('FONTSIZE', (0,0), (-1,0), 12),
                ('BOTTOMPADDING', (0,0), (-1,0), 12),
                ('BACKGROUND', (0,1), (-1,-1), colors.beige),
                ('GRID', (0,0), (-1,-1), 1, colors.black)
            ]))
            story.append(summary_table)
            story.append(Spacer(1, 0.2*inch))

            # Add sections (simplified)
            for section_name, section_data in list(data.items())[:10]:  # Limit for PDF
                if section_name == "metadata":
                    continue
                story.append(Paragraph(section_name, styles['Heading2']))
                story.append(Spacer(1, 0.1*inch))
                # Convert dict to string for simplicity
                text = str(section_data)[:500]
                story.append(Paragraph(text, styles['Normal']))
                story.append(Spacer(1, 0.2*inch))

            doc.build(story)
            print(f"{EnhancedUI.color_text('✓ PDF report saved:', 'OKGREEN')} {filename}")
            return str(filename)
        except ImportError:
            print(f"{EnhancedUI.color_text('⚠️ ReportLab not installed, skipping PDF.', 'WARNING')}")
            return None

    def generate_csv_report(self, data):
        """Generate CSV report for selected sections (if pandas available)"""
        try:
            import pandas as pd
            filename = self.output_dir / f"{self.filename_base}.csv"
            # Flatten data for CSV (simplified)
            rows = []
            for section, content in data.items():
                if isinstance(content, dict):
                    for key, value in content.items():
                        rows.append({"Section": section, "Key": key, "Value": str(value)})
                else:
                    rows.append({"Section": section, "Key": "", "Value": str(content)})
            df = pd.DataFrame(rows)
            df.to_csv(filename, index=False)
            print(f"{EnhancedUI.color_text('✓ CSV report saved:', 'OKGREEN')} {filename}")
            return str(filename)
        except ImportError:
            print(f"{EnhancedUI.color_text('⚠️ Pandas not installed, skipping CSV.', 'WARNING')}")
            return None

    def generate_all_reports(self, data):
        """Generate all report formats"""
        reports = {}

        print(
            f"\n{EnhancedUI.color_text('Generating professional reports...', 'HEADER')}"
        )

        reports["text"] = self.generate_text_report(data)
        reports["json"] = self.generate_json_report(data)
        reports["html"] = self.generate_html_report(data)
        pdf = self.generate_pdf_report(data)
        if pdf:
            reports["pdf"] = pdf
        csv = self.generate_csv_report(data)
        if csv:
            reports["csv"] = csv

        # Create README file
        readme_file = self.output_dir / f"{self.filename_base}_README.txt"
        with open(readme_file, "w", encoding="utf-8") as f:
            f.write(
                f"""System Analysis Reports
Generated: {self.timestamp.strftime('%Y-%m-%d %H:%M:%S')}
System: {socket.gethostname()}

Available Reports:
1. {Path(reports['text']).name} - Comprehensive text report
2. {Path(reports['json']).name} - Complete JSON data
3. {Path(reports['html']).name} - HTML report for web viewing
"""
            )
            if "pdf" in reports:
                f.write(f"4. {Path(reports['pdf']).name} - PDF report\n")
            if "csv" in reports:
                f.write(f"5. {Path(reports['csv']).name} - CSV data\n")

            f.write("""
Analysis Includes:
- System Overview and Identification
- Operating System Details
- Processor (CPU) Specifications
- Graphics (GPU) Information
- Memory (RAM) Analysis
- Storage Devices and Partitions (with SMART)
- Network Configuration (Wi-Fi, DNS, ARP)
- Audio Devices
- Motherboard and BIOS
- Power and Battery Status (cycle count, wear)
- Security Audit (UAC, LSA, TPM, Defender)
- Performance Benchmarks (multi-threaded CPU, disk)
- Software Inventory
- Hardware Health Check
- Registry Analysis (installed software, startup)
- Modern Windows Features (WSL, Hyper-V, Sandbox)
- Windows Update History

Tool: Ultimate System Analyzer v{Config.VERSION}
Privileges: {'Administrator' if self.analyzer.is_admin else 'Standard User'}

Note: Run with Administrator privileges for complete system analysis.
"""
            )

        print(
            f"\n{EnhancedUI.color_text('✓ All reports generated successfully!', 'OKGREEN')}"
        )
        print(
            f"{EnhancedUI.color_text('📁 Output directory:', 'BOLD')} {self.output_dir.absolute()}"
        )

        return reports


# ==================== MAIN APPLICATION ====================
class UltimateApplication:
    """Main application controller"""

    def __init__(self):
        self.dependencies = {}
        self.analyzer = None
        self.is_admin = PrivilegeManager.is_admin()
        self.reports = []

    def run(self):
        """Main application loop"""
        try:
            # Initial setup
            EnhancedUI.clear_screen()
            print(EnhancedUI.color_text(Config.get_banner(), "HEADER"))

            # Check Python version
            if not DependencyInstaller.check_python_version():
                input(f"\n{EnhancedUI.color_text('Press ENTER to exit...', 'WARNING')}")
                return

            # Check privileges
            print(
                f"\n{EnhancedUI.color_text('Checking system privileges...', 'OKBLUE')}"
            )
            self.is_admin = PrivilegeManager.check_privilege_requirements()

            # Ask about privilege escalation
            if not self.is_admin:
                if EnhancedUI.ask_yes_no(
                    "\nWould you like to restart as Administrator for full analysis?",
                    default=True,
                ):
                    if PrivilegeManager.request_admin_privileges():
                        return  # Original instance exits

            # Install dependencies
            print(
                f"\n{EnhancedUI.color_text('Checking and installing dependencies...', 'OKBLUE')}"
            )
            self.dependencies, failed = DependencyInstaller.install_all_dependencies(
                ask_for_optional=True, silent=False
            )

            # Check if we have minimal dependencies
            if len(self.dependencies) < 3:  # At least psutil, wmi, cpuinfo
                print(
                    f"\n{EnhancedUI.color_text('❌ Insufficient dependencies installed.', 'FAIL')}"
                )
                print("Please install manually: pip install psutil wmi py-cpuinfo")
                input(f"\n{EnhancedUI.color_text('Press ENTER to exit...', 'WARNING')}")
                return

            # Initialize analyzer
            print(
                f"\n{EnhancedUI.color_text('Initializing system analyzer...', 'OKBLUE')}"
            )
            self.analyzer = ComprehensiveAnalyzer(self.dependencies, self.is_admin)

            # Main menu loop
            while True:
                choice = EnhancedUI.show_menu()

                if choice == 0:
                    print(
                        f"\n{EnhancedUI.color_text('👋 Thank you for using Ultimate System Analyzer!', 'OKGREEN')}"
                    )
                    break

                elif choice == 1:
                    self.run_quick_overview()

                elif choice == 2:
                    self.run_comprehensive_hardware()

                elif choice == 3:
                    self.run_full_diagnostics()

                elif choice == 4:
                    self.run_performance_benchmark()

                elif choice == 5:
                    self.run_security_check()

                elif choice == 6:
                    self.export_reports()

                elif choice == 7:
                    self.run_realtime_monitoring()

                elif choice == 8:
                    self.show_tools_menu()

                if choice != 0:
                    input(
                        f"\n{EnhancedUI.color_text('Press ENTER to continue...', 'OKBLUE')}"
                    )

        except KeyboardInterrupt:
            print(
                f"\n\n{EnhancedUI.color_text('⚠️  Interrupted by user. Exiting...', 'WARNING')}"
            )
        except Exception as e:
            print(f"\n{EnhancedUI.color_text('❌ Unexpected error:', 'FAIL')} {str(e)}")
            print(f"{EnhancedUI.color_text('Traceback:', 'FAIL')}")
            traceback.print_exc()
            input(f"\n{EnhancedUI.color_text('Press ENTER to exit...', 'WARNING')}")

    def run_quick_overview(self):
        """Run quick system overview"""
        print(f"\n{EnhancedUI.color_text('═' * 60, 'OKBLUE')}")
        print(
            f"{EnhancedUI.color_text('  QUICK SYSTEM OVERVIEW (IObit Style)', 'HEADER')}"
        )
        print(f"{EnhancedUI.color_text('═' * 60, 'OKBLUE')}")

        data = self.analyzer.quick_overview()

        # Display quick summary
        print(f"\n{EnhancedUI.color_text('📋 SYSTEM SUMMARY', 'BOLD')}")
        print(f"{EnhancedUI.color_text('─' * 40, 'OKBLUE')}")

        # Display key information
        system = data.get("System Overview", {})
        print(
            f"{EnhancedUI.color_text('Computer:', 'BOLD')} {system.get('computer_name', 'Unknown')}"
        )
        print(
            f"{EnhancedUI.color_text('Manufacturer:', 'BOLD')} {system.get('manufacturer', 'Unknown')}"
        )
        print(
            f"{EnhancedUI.color_text('Model:', 'BOLD')} {system.get('model', 'Unknown')}"
        )
        print(
            f"{EnhancedUI.color_text('Serial:', 'BOLD')} {system.get('serial_number', 'Unknown')}"
        )

        os_info = data.get("Operating System", {})
        print(
            f"\n{EnhancedUI.color_text('OS:', 'BOLD')} {os_info.get('windows_edition', os_info.get('name', 'Unknown'))}"
        )
        print(
            f"{EnhancedUI.color_text('Version:', 'BOLD')} {os_info.get('display_version', os_info.get('version', 'Unknown'))}"
        )

        cpu = data.get("Processor", {}).get("basic_info", {})
        print(
            f"\n{EnhancedUI.color_text('CPU:', 'BOLD')} {cpu.get('brand', 'Unknown')}"
        )
        print(
            f"{EnhancedUI.color_text('Cores:', 'BOLD')} {cpu.get('cores', 'Unknown')}"
        )
        print(
            f"{EnhancedUI.color_text('Speed:', 'BOLD')} {cpu.get('hz_actual', 'Unknown')}"
        )

        memory = data.get("Memory", {}).get("virtual_memory", {})
        print(
            f"\n{EnhancedUI.color_text('Memory:', 'BOLD')} {memory.get('total', 'Unknown')}"
        )
        print(
            f"{EnhancedUI.color_text('Available:', 'BOLD')} {memory.get('available', 'Unknown')}"
        )
        print(
            f"{EnhancedUI.color_text('Usage:', 'BOLD')} {memory.get('percent', 'Unknown')}"
        )

        graphics = data.get("Graphics", {}).get("gpus", [])
        if graphics:
            gpu = graphics[0]
            print(
                f"\n{EnhancedUI.color_text('Graphics:', 'BOLD')} {gpu.get('name', 'Unknown')}"
            )
            print(
                f"{EnhancedUI.color_text('VRAM:', 'BOLD')} {gpu.get('adapter_ram', 'Unknown')}"
            )

        storage = data.get("Storage", {})
        disks = storage.get("physical_disks", [])
        if disks:
            print(
                f"\n{EnhancedUI.color_text('Storage:', 'BOLD')} {len(disks)} drive(s)"
            )
            for disk in disks[:2]:  # Show first 2 drives
                print(
                    f"  {disk.get('model', 'Unknown')} - {disk.get('size', 'Unknown')}"
                )

        # Ask about saving report
        if EnhancedUI.ask_yes_no("\nSave detailed report?", default=True):
            generator = ProfessionalReportGenerator(self.analyzer)
            generator.generate_text_report(data)

    def run_comprehensive_hardware(self):
        """Run comprehensive hardware analysis"""
        print(f"\n{EnhancedUI.color_text('═' * 60, 'OKBLUE')}")
        print(f"{EnhancedUI.color_text('  COMPREHENSIVE HARDWARE ANALYSIS', 'HEADER')}")
        print(f"{EnhancedUI.color_text('═' * 60, 'OKBLUE')}")

        if not EnhancedUI.ask_yes_no(
            "This analysis may take 1-2 minutes. Continue?", default=True
        ):
            return

        data = self.analyzer.comprehensive_hardware_analysis()

        # Display summary
        print(f"\n{EnhancedUI.color_text('✅ Hardware Analysis Complete!', 'OKGREEN')}")

        # Generate reports
        if EnhancedUI.ask_yes_no("\nGenerate professional reports?", default=True):
            generator = ProfessionalReportGenerator(self.analyzer)
            reports = generator.generate_all_reports(data)

            # Show summary
            print(f"\n{EnhancedUI.color_text('📊 HARDWARE SUMMARY:', 'BOLD')}")

            cpu = data.get("Processor", {}).get("basic_info", {})
            print(
                f"  CPU: {cpu.get('brand', 'Unknown')} ({cpu.get('cores', 'Unknown')} cores)"
            )

            memory = data.get("Memory", {}).get("virtual_memory", {})
            print(f"  RAM: {memory.get('total', 'Unknown')}")

            graphics = data.get("Graphics", {}).get("gpus", [])
            if graphics:
                print(f"  GPU: {graphics[0].get('name', 'Unknown')}")

            storage = data.get("Storage", {}).get("physical_disks", [])
            if storage:
                total_gb = 0
                for disk in storage:
                    size_str = disk.get("size", "0 GB")
                    try:
                        total_gb += float(size_str.split()[0])
                    except:
                        pass
                print(f"  Storage: {total_gb:.1f} GB total")

            motherboard = data.get("Motherboard", {}).get("baseboard", {})
            print(
                f"  Motherboard: {motherboard.get('manufacturer', 'Unknown')} {motherboard.get('product', 'Unknown')}"
            )

    def run_full_diagnostics(self):
        """Run full system diagnostics"""
        print(f"\n{EnhancedUI.color_text('═' * 60, 'OKBLUE')}")
        print(f"{EnhancedUI.color_text('  FULL SYSTEM DIAGNOSTICS', 'HEADER')}")
        print(f"{EnhancedUI.color_text('═' * 60, 'OKBLUE')}")

        print(
            f"\n{EnhancedUI.color_text('⚠️  This will perform a complete system analysis.', 'WARNING')}"
        )
        print(
            f"{EnhancedUI.color_text('   It may take 3-5 minutes and will analyze all components.', 'WARNING')}"
        )

        if not EnhancedUI.ask_yes_no("\nContinue with full diagnostics?", default=True):
            return

        print(
            f"\n{EnhancedUI.color_text('Starting full system diagnostics...', 'OKBLUE')}"
        )

        data = self.analyzer.full_diagnostics()

        # Generate reports
        print(f"\n{EnhancedUI.color_text('✅ Diagnostics Complete!', 'OKGREEN')}")

        if EnhancedUI.ask_yes_no("\nGenerate comprehensive reports?", default=True):
            generator = ProfessionalReportGenerator(self.analyzer)
            reports = generator.generate_all_reports(data)

            # Show quick stats
            if "metadata" in data:
                meta = data["metadata"]
                print(f"\n{EnhancedUI.color_text('📈 DIAGNOSTICS SUMMARY:', 'BOLD')}")
                print(f"  Duration: {meta.get('scan_duration_seconds', 0)} seconds")
                print(f"  Sections: {len(data) - 1}")
                print(f"  Errors: {meta.get('errors_count', 0)}")

            # Show performance score
            perf = data.get("Performance", {}).get("scores", {})
            if perf:
                rating = perf.get("rating", "")
                color = (
                    "OKGREEN"
                    if rating in ["Excellent", "Very Good", "Good"]
                    else "WARNING" if rating == "Fair" else "FAIL"
                )
                print(
                    f"  Performance: {EnhancedUI.color_text(f'{perf.get("overall", 0):.1f}/10 ({rating})', color)}"
                )

    def run_performance_benchmark(self):
        """Run performance benchmark only"""
        print(f"\n{EnhancedUI.color_text('═' * 60, 'OKBLUE')}")
        print(f"{EnhancedUI.color_text('  PERFORMANCE BENCHMARK', 'HEADER')}")
        print(f"{EnhancedUI.color_text('═' * 60, 'OKBLUE')}")

        data = self.analyzer.analyze_performance()

        # Display results
        print(f"\n{EnhancedUI.color_text('📊 BENCHMARK RESULTS:', 'BOLD')}")
        print(f"{EnhancedUI.color_text('─' * 40, 'OKBLUE')}")

        scores = data.get("scores", {})

        # CPU Score
        cpu_score = scores.get("cpu", 0)
        cpu_color = (
            "OKGREEN" if cpu_score >= 7 else "WARNING" if cpu_score >= 5 else "FAIL"
        )
        print(
            f"  CPU Performance: {EnhancedUI.color_text(f'{cpu_score}/10', cpu_color)}"
        )

        # Memory Score
        mem_score = scores.get("memory", 0)
        mem_color = (
            "OKGREEN" if mem_score >= 7 else "WARNING" if mem_score >= 5 else "FAIL"
        )
        print(
            f"  Memory Performance: {EnhancedUI.color_text(f'{mem_score}/10', mem_color)}"
        )

        # Disk Score
        disk_score = scores.get("disk", 0)
        disk_color = (
            "OKGREEN" if disk_score >= 7 else "WARNING" if disk_score >= 5 else "FAIL"
        )
        print(
            f"  Disk Performance: {EnhancedUI.color_text(f'{disk_score}/10', disk_color)}"
        )

        # GPU Score
        gpu_score = scores.get("gpu", 0)
        gpu_color = (
            "OKGREEN" if gpu_score >= 7 else "WARNING" if gpu_score >= 5 else "FAIL"
        )
        print(
            f"  Graphics Performance: {EnhancedUI.color_text(f'{gpu_score}/10', gpu_color)}"
        )

        # Overall Score
        overall = scores.get("overall", 0)
        rating = scores.get("rating", "Unknown")
        overall_color = (
            "OKGREEN" if overall >= 7 else "WARNING" if overall >= 5 else "FAIL"
        )

        print(
            f"\n  {EnhancedUI.color_text('Overall Performance:', 'BOLD')} {EnhancedUI.color_text(f'{overall:.1f}/10 ({rating})', overall_color)}"
        )

        # Recommendations
        recommendations = data.get("recommendations", [])
        if recommendations:
            print(f"\n{EnhancedUI.color_text('💡 RECOMMENDATIONS:', 'BOLD')}")
            for rec in recommendations:
                print(f"  • {rec}")

        # Save results
        if EnhancedUI.ask_yes_no("\nSave benchmark results?", default=False):
            generator = ProfessionalReportGenerator(self.analyzer)
            filename = (
                generator.output_dir
                / f"benchmark_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
            )

            with open(filename, "w", encoding="utf-8") as f:
                f.write(f"Performance Benchmark Results\n")
                f.write(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
                f.write(f"System: {socket.gethostname()}\n")
                f.write("-" * 40 + "\n\n")

                f.write(f"CPU Score: {cpu_score}/10\n")
                f.write(f"Memory Score: {mem_score}/10\n")
                f.write(f"Disk Score: {disk_score}/10\n")
                f.write(f"Graphics Score: {gpu_score}/10\n")
                f.write(f"\nOverall: {overall:.1f}/10 ({rating})\n")

                if recommendations:
                    f.write("\nRecommendations:\n")
                    for rec in recommendations:
                        f.write(f"• {rec}\n")

            print(
                f"{EnhancedUI.color_text('✓ Benchmark saved:', 'OKGREEN')} {filename}"
            )

    def run_security_check(self):
        """Run security check"""
        print(f"\n{EnhancedUI.color_text('═' * 60, 'OKBLUE')}")
        print(f"{EnhancedUI.color_text('  SECURITY & HEALTH CHECK', 'HEADER')}")
        print(f"{EnhancedUI.color_text('═' * 60, 'OKBLUE')}")

        # Run security analysis
        security_data = self.analyzer.analyze_security()
        health_data = self.analyzer.analyze_hardware_health()

        # Display security status
        print(f"\n{EnhancedUI.color_text('🔒 SECURITY STATUS:', 'BOLD')}")
        print(f"{EnhancedUI.color_text('─' * 40, 'OKBLUE')}")

        print(
            f"  Running as Admin: {EnhancedUI.color_text('Yes' if self.is_admin else 'No', 'OKGREEN' if self.is_admin else 'WARNING')}"
        )
        print(f"  UEFI Secure Boot: {security_data.get('uefi_secure_boot', 'Unknown')}")
        print(
            f"  Windows Defender: {'Installed' if security_data.get('windows_defender', {}).get('installed') == 'Yes' else 'Not detected'}"
        )
        print(
            f"  Antivirus Software: {len(security_data.get('security_products', []))} detected"
        )

        # Display hardware health
        print(f"\n{EnhancedUI.color_text('🩺 HARDWARE HEALTH:', 'BOLD')}")
        print(f"{EnhancedUI.color_text('─' * 40, 'OKBLUE')}")

        warnings = health_data.get("warnings", [])
        if warnings:
            print(f"{EnhancedUI.color_text('⚠️  Warnings Found:', 'WARNING')}")
            for warning in warnings[:5]:  # Show first 5 warnings
                print(f"  • {warning}")
            if len(warnings) > 5:
                print(f"  • ... and {len(warnings) - 5} more")
        else:
            print(f"{EnhancedUI.color_text('✅ All systems normal', 'OKGREEN')}")

        # Recommendations
        recommendations = security_data.get("recommendations", []) + health_data.get(
            "recommendations", []
        )
        if recommendations:
            print(f"\n{EnhancedUI.color_text('💡 RECOMMENDATIONS:', 'BOLD')}")
            for rec in recommendations:
                print(f"  • {rec}")

        # Save report
        if EnhancedUI.ask_yes_no("\nSave security report?", default=False):
            generator = ProfessionalReportGenerator(self.analyzer)

            # Combine data
            combined_data = {"Security": security_data, "Hardware Health": health_data}

            filename = (
                generator.output_dir
                / f"security_check_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
            )

            with open(filename, "w", encoding="utf-8") as f:
                f.write(f"Security & Health Check Report\n")
                f.write(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
                f.write(f"System: {socket.gethostname()}\n")
                f.write(
                    f"Privileges: {'Administrator' if self.is_admin else 'Standard User'}\n"
                )
                f.write("-" * 50 + "\n\n")

                f.write("SECURITY STATUS\n")
                f.write("-" * 30 + "\n")
                f.write(f"Running as Admin: {'Yes' if self.is_admin else 'No'}\n")
                f.write(
                    f"UEFI Secure Boot: {security_data.get('uefi_secure_boot', 'Unknown')}\n"
                )
                f.write(
                    f"Windows Defender: {'Installed' if security_data.get('windows_defender', {}).get('installed') == 'Yes' else 'Not detected'}\n"
                )
                f.write(
                    f"Antivirus Software: {len(security_data.get('security_products', []))} detected\n\n"
                )

                f.write("HARDWARE HEALTH\n")
                f.write("-" * 30 + "\n")
                if warnings:
                    f.write("Warnings:\n")
                    for warning in warnings:
                        f.write(f"• {warning}\n")
                else:
                    f.write("All systems normal\n\n")

                if recommendations:
                    f.write("\nRECOMMENDATIONS:\n")
                    for rec in recommendations:
                        f.write(f"• {rec}\n")

            print(
                f"{EnhancedUI.color_text('✓ Security report saved:', 'OKGREEN')} {filename}"
            )

    def export_reports(self):
        """Export reports menu"""
        print(f"\n{EnhancedUI.color_text('═' * 60, 'OKBLUE')}")
        print(f"{EnhancedUI.color_text('  EXPORT PROFESSIONAL REPORTS', 'HEADER')}")
        print(f"{EnhancedUI.color_text('═' * 60, 'OKBLUE')}")

        if not hasattr(self.analyzer, "data") or not self.analyzer.data:
            print(
                f"\n{EnhancedUI.color_text('⚠️  No data to export. Run a scan first.', 'WARNING')}"
            )
            return

        print(f"\n{EnhancedUI.color_text('Available export formats:', 'BOLD')}")
        print("  1. 📄 Text Report (.txt)")
        print("  2. 📊 JSON Data (.json)")
        print("  3. 🌐 HTML Report (.html)")
        print("  4. 📦 All Formats (including PDF/CSV if available)")
        print("  0. ↩️  Back")

        choice = input(
            f"\n{EnhancedUI.color_text('Select format', 'BOLD')} [0-4]: "
        ).strip()

        if choice == "0":
            return
        elif choice in ["1", "2", "3", "4"]:
            generator = ProfessionalReportGenerator(self.analyzer)

            if choice == "1":
                generator.generate_text_report(self.analyzer.data)
            elif choice == "2":
                generator.generate_json_report(self.analyzer.data)
            elif choice == "3":
                generator.generate_html_report(self.analyzer.data)
            elif choice == "4":
                generator.generate_all_reports(self.analyzer.data)
        else:
            print(f"{EnhancedUI.color_text('Invalid choice.', 'FAIL')}")

    def run_realtime_monitoring(self):
        """Experimental real-time monitoring with network I/O"""
        print(f"\n{EnhancedUI.color_text('═' * 60, 'OKBLUE')}")
        print(
            f"{EnhancedUI.color_text('  REAL-TIME MONITORING (Experimental)', 'HEADER')}"
        )
        print(f"{EnhancedUI.color_text('═' * 60, 'OKBLUE')}")

        print(
            f"\n{EnhancedUI.color_text('⚠️  This feature is experimental and may not work on all systems.', 'WARNING')}"
        )

        if not EnhancedUI.ask_yes_no("\nStart real-time monitoring?", default=False):
            return

        try:
            if "psutil" not in self.deps:
                print(
                    f"{EnhancedUI.color_text('❌ Psutil required for monitoring.', 'FAIL')}"
                )
                return

            print(
                f"\n{EnhancedUI.color_text('📊 Real-time monitoring started. Press Ctrl+C to stop.', 'OKGREEN')}"
            )
            print(
                f"{EnhancedUI.color_text('   Monitoring CPU, Memory, Disk, and Network usage...', 'OKBLUE')}"
            )
            print(f"\n{EnhancedUI.color_text('─' * 60, 'OKBLUE')}")

            import time
            import signal

            stop_monitoring = False

            def signal_handler(sig, frame):
                nonlocal stop_monitoring
                stop_monitoring = True

            signal.signal(signal.SIGINT, signal_handler)

            # Previous network counters for delta
            last_net = self.deps["psutil"].net_io_counters()
            last_time = time.time()

            try:
                while not stop_monitoring:
                    # Clear previous output
                    sys.stdout.write("\033[2J\033[H")

                    # Get current metrics
                    cpu_percent = self.deps["psutil"].cpu_percent(interval=0.5, percpu=True)
                    memory = self.deps["psutil"].virtual_memory()
                    disk = self.deps["psutil"].disk_usage("/")
                    net = self.deps["psutil"].net_io_counters()
                    now = time.time()
                    delta_time = now - last_time

                    # Calculate network speeds
                    bytes_sent_per_sec = (net.bytes_sent - last_net.bytes_sent) / delta_time
                    bytes_recv_per_sec = (net.bytes_recv - last_net.bytes_recv) / delta_time

                    # Update last
                    last_net = net
                    last_time = now

                    # Display metrics
                    print(
                        f"\n{EnhancedUI.color_text('REAL-TIME SYSTEM MONITOR', 'HEADER')}"
                    )
                    print(f"{EnhancedUI.color_text('─' * 40, 'OKBLUE')}")

                    # CPU per core
                    for i, percent in enumerate(cpu_percent):
                        bar = self._create_progress_bar(percent, 20)
                        print(
                            f"{EnhancedUI.color_text(f'CPU Core {i}:', 'BOLD')} {percent:5.1f}% {bar}"
                        )

                    # Memory
                    mem_percent = memory.percent
                    mem_bar = self._create_progress_bar(mem_percent, 40)
                    print(
                        f"\n{EnhancedUI.color_text('Memory:', 'BOLD')} {mem_percent:5.1f}% {mem_bar}"
                    )
                    print(
                        f"      Used: {self.analyzer.format_size(memory.used)} / {self.analyzer.format_size(memory.total)}"
                    )

                    # Disk
                    disk_percent = disk.percent
                    disk_bar = self._create_progress_bar(disk_percent, 40)
                    print(
                        f"\n{EnhancedUI.color_text('Disk (C:):', 'BOLD')} {disk_percent:5.1f}% {disk_bar}"
                    )
                    print(
                        f"      Used: {self.analyzer.format_size(disk.used)} / {self.analyzer.format_size(disk.total)}"
                    )

                    # Network
                    print(
                        f"\n{EnhancedUI.color_text('Network:', 'BOLD')}"
                    )
                    print(
                        f"      ↓ Download: {self.analyzer.format_size(bytes_recv_per_sec)}/s"
                    )
                    print(
                        f"      ↑ Upload:   {self.analyzer.format_size(bytes_sent_per_sec)}/s"
                    )
                    print(
                        f"      Total Sent: {self.analyzer.format_size(net.bytes_sent)}"
                    )
                    print(
                        f"      Total Recv: {self.analyzer.format_size(net.bytes_recv)}"
                    )

                    print(
                        f"\n{EnhancedUI.color_text('Press Ctrl+C to stop monitoring', 'WARNING')}"
                    )
                    time.sleep(2)

            except KeyboardInterrupt:
                pass

            print(f"\n{EnhancedUI.color_text('✅ Monitoring stopped.', 'OKGREEN')}")

        except Exception as e:
            print(f"{EnhancedUI.color_text(f'❌ Monitoring error: {str(e)}', 'FAIL')}")

    def _create_progress_bar(self, percent, length=40):
        """Create a progress bar for monitoring"""
        filled = int(length * percent / 100)
        bar = "█" * filled + "░" * (length - filled)

        if percent >= 90:
            color = "FAIL"
        elif percent >= 70:
            color = "WARNING"
        else:
            color = "OKGREEN"

        return EnhancedUI.color_text(bar, color)

    def show_tools_menu(self):
        """Show tools and utilities menu"""
        print(f"\n{EnhancedUI.color_text('═' * 60, 'OKBLUE')}")
        print(f"{EnhancedUI.color_text('  TOOLS & UTILITIES', 'HEADER')}")
        print(f"{EnhancedUI.color_text('═' * 60, 'OKBLUE')}")

        print(f"\n{EnhancedUI.color_text('Available tools:', 'BOLD')}")
        print("  1. 🔄 Reinstall Dependencies")
        print("  2. 📦 Check Package Updates")
        print("  3. 🧹 Clean Temporary Files")
        print("  4. 🔍 System Information (Command Line)")
        print("  5. 🖥️  Open System Configuration")
        print("  6. 📂 Registry Explorer (Basic)")
        print("  0. ↩️  Back")

        choice = input(
            f"\n{EnhancedUI.color_text('Select tool', 'BOLD')} [0-6]: "
        ).strip()

        if choice == "0":
            return
        elif choice == "1":
            self.reinstall_dependencies()
        elif choice == "2":
            self.check_updates()
        elif choice == "3":
            self.clean_temp_files()
        elif choice == "4":
            self.show_system_info_cli()
        elif choice == "5":
            self.open_system_config()
        elif choice == "6":
            self.registry_explorer()
        else:
            print(f"{EnhancedUI.color_text('Invalid choice.', 'FAIL')}")

    def reinstall_dependencies(self):
        """Reinstall dependencies"""
        print(f"\n{EnhancedUI.color_text('Reinstalling dependencies...', 'OKBLUE')}")
        self.dependencies, failed = DependencyInstaller.install_all_dependencies(
            ask_for_optional=False, silent=False
        )

        if failed:
            print(
                f"{EnhancedUI.color_text('❌ Some dependencies failed to install.', 'FAIL')}"
            )
        else:
            print(
                f"{EnhancedUI.color_text('✅ Dependencies reinstalled successfully.', 'OKGREEN')}"
            )

            # Reinitialize analyzer
            self.analyzer = ComprehensiveAnalyzer(self.dependencies, self.is_admin)

    def check_updates(self):
        """Check for package updates"""
        print(f"\n{EnhancedUI.color_text('Checking for updates...', 'OKBLUE')}")

        try:
            result = subprocess.run(
                [sys.executable, "-m", "pip", "list", "--outdated", "--format=json"],
                capture_output=True,
                text=True,
                timeout=30,
            )

            if result.returncode == 0:
                packages = json.loads(result.stdout)
                if packages:
                    print(
                        f"\n{EnhancedUI.color_text('📦 Packages with updates available:', 'BOLD')}"
                    )
                    for pkg in packages[:10]:  # Show first 10
                        print(
                            f"  • {pkg['name']}: {pkg['version']} → {pkg['latest_version']}"
                        )

                    if len(packages) > 10:
                        print(f"  • ... and {len(packages) - 10} more")

                    if EnhancedUI.ask_yes_no("\nUpdate all packages?", default=False):
                        subprocess.run(
                            [
                                sys.executable,
                                "-m",
                                "pip",
                                "install",
                                "--upgrade",
                                "pip",
                            ],
                            capture_output=True,
                        )
                        for pkg in packages:
                            print(f"  Updating {pkg['name']}...")
                            subprocess.run(
                                [
                                    sys.executable,
                                    "-m",
                                    "pip",
                                    "install",
                                    "--upgrade",
                                    pkg["name"],
                                ],
                                capture_output=True,
                            )
                        print(
                            f"{EnhancedUI.color_text('✅ Packages updated.', 'OKGREEN')}"
                        )
                else:
                    print(
                        f"{EnhancedUI.color_text('✅ All packages are up to date.', 'OKGREEN')}"
                    )
            else:
                print(f"{EnhancedUI.color_text('❌ Failed to check updates.', 'FAIL')}")
        except:
            print(f"{EnhancedUI.color_text('❌ Failed to check updates.', 'FAIL')}")

    def clean_temp_files(self):
        """Clean temporary files"""
        print(f"\n{EnhancedUI.color_text('Cleaning temporary files...', 'OKBLUE')}")

        temp_dirs = [
            os.environ.get("TEMP", ""),
            os.environ.get("TMP", ""),
            os.path.expanduser("~\\AppData\\Local\\Temp"),
            r"C:\Windows\Temp",
        ]

        total_freed = 0
        files_removed = 0

        for temp_dir in temp_dirs:
            if os.path.exists(temp_dir):
                try:
                    for root, dirs, files in os.walk(temp_dir):
                        for file in files:
                            try:
                                file_path = os.path.join(root, file)
                                # Only delete files older than 1 day
                                if os.path.getmtime(file_path) < time.time() - 86400:
                                    size = os.path.getsize(file_path)
                                    os.remove(file_path)
                                    total_freed += size
                                    files_removed += 1
                            except:
                                continue
                except:
                    continue

        if files_removed > 0:
            print(
                f"{EnhancedUI.color_text(f'✅ Removed {files_removed} files, freed {self.analyzer.format_size(total_freed)}', 'OKGREEN')}"
            )
        else:
            print(
                f"{EnhancedUI.color_text('✅ No temporary files to clean.', 'OKGREEN')}"
            )

    def show_system_info_cli(self):
        """Show system information via command line"""
        print(
            f"\n{EnhancedUI.color_text('System Information (Command Line):', 'HEADER')}"
        )
        print(f"{EnhancedUI.color_text('─' * 40, 'OKBLUE')}")

        commands = [
            ("System Info", "systeminfo"),
            ("Disk Info", "wmic logicaldisk get size,freespace,caption"),
            ("Network Info", "ipconfig /all"),
            ("Process List", "tasklist"),
            ("Service List", "sc query"),
        ]

        for name, cmd in commands:
            if EnhancedUI.ask_yes_no(f"\nRun '{name}' command?", default=False):
                print(f"\n{EnhancedUI.color_text(f'{name}:', 'BOLD')}")
                try:
                    result = subprocess.run(
                        cmd, shell=True, capture_output=True, text=True, timeout=10
                    )
                    print(result.stdout[:500])  # Limit output
                except:
                    print(
                        f"{EnhancedUI.color_text('❌ Command failed or timed out.', 'FAIL')}"
                    )

    def open_system_config(self):
        """Open system configuration tools"""
        print(f"\n{EnhancedUI.color_text('System Configuration Tools:', 'HEADER')}")

        tools = [
            ("System Properties", "sysdm.cpl"),
            ("Device Manager", "devmgmt.msc"),
            ("Disk Management", "diskmgmt.msc"),
            ("Event Viewer", "eventvwr.msc"),
            ("Services", "services.msc"),
            ("Task Manager", "taskmgr"),
            ("Control Panel", "control"),
            ("Windows Features", "optionalfeatures"),
        ]

        print(f"{EnhancedUI.color_text('─' * 40, 'OKBLUE')}")
        for i, (name, command) in enumerate(tools, 1):
            print(f"  {i}. {name}")
        print(f"  0. ↩️  Back")

        choice = input(
            f"\n{EnhancedUI.color_text('Select tool to open', 'BOLD')} [0-{len(tools)}]: "
        ).strip()

        try:
            choice_num = int(choice)
            if choice_num == 0:
                return
            elif 1 <= choice_num <= len(tools):
                name, command = tools[choice_num - 1]
                print(f"\n{EnhancedUI.color_text(f'Opening {name}...', 'OKBLUE')}")
                os.system(f"start {command}")
            else:
                print(f"{EnhancedUI.color_text('Invalid choice.', 'FAIL')}")
        except:
            print(f"{EnhancedUI.color_text('Invalid choice.', 'FAIL')}")

    def registry_explorer(self):
        """Basic registry explorer"""
        print(f"\n{EnhancedUI.color_text('Registry Explorer (Basic)', 'HEADER')}")
        print(f"{EnhancedUI.color_text('─' * 40, 'OKBLUE')}")
        print("This tool lists common registry keys.")
        print("1. List installed software")
        print("2. List startup programs")
        print("3. List environment variables")
        print("4. Back")
        sub_choice = input(f"\n{EnhancedUI.color_text('Select', 'BOLD')}: ").strip()
        if sub_choice == "1":
            if not self.analyzer:
                print("Analyzer not initialized.")
                return
            reg_data = self.analyzer.analyze_registry()
            print(f"\n{EnhancedUI.color_text('Installed Software (first 20):', 'BOLD')}")
            for prog in reg_data.get("installed_software", [])[:20]:
                print(f"  • {prog.get('name')} {prog.get('version')} ({prog.get('publisher')})")
        elif sub_choice == "2":
            if not self.analyzer:
                print("Analyzer not initialized.")
                return
            reg_data = self.analyzer.analyze_registry()
            print(f"\n{EnhancedUI.color_text('Startup Programs:', 'BOLD')}")
            for prog in reg_data.get("startup_programs", []):
                print(f"  • {prog.get('name')} -> {prog.get('command')}")
        elif sub_choice == "3":
            if not self.analyzer:
                print("Analyzer not initialized.")
                return
            reg_data = self.analyzer.analyze_registry()
            print(f"\n{EnhancedUI.color_text('Environment Variables:', 'BOLD')}")
            for key, val in reg_data.get("environment_variables", {}).items():
                print(f"  • {key} = {val}")
        else:
            return


# ==================== ENTRY POINT ====================
if __name__ == "__main__":
    try:
        app = UltimateApplication()
        app.run()
    except KeyboardInterrupt:
        print(
            f"\n\n{EnhancedUI.color_text('⚠️  Interrupted by user. Exiting...', 'WARNING')}"
        )
    except Exception as e:
        print(f"\n{EnhancedUI.color_text('❌ Fatal error:', 'FAIL')} {str(e)}")
        traceback.print_exc()
        input(f"\n{EnhancedUI.color_text('Press ENTER to exit...', 'WARNING')}")