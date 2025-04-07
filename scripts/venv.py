import os
import sys
import subprocess

VENV_DIR = "venv"

PYTHON = sys.executable

def create_venv():
    """Creates a virtual environment."""
    if not os.path.exists(VENV_DIR):
        print("📦 Creating virtual environment...")
        subprocess.run([PYTHON, "-m", "venv", VENV_DIR], check=True)
        print("✅ Virtual environment created successfully!")
    else:
        print("⚡ Virtual environment already exists.")

def install_requirements():
    """Installs dependencies if requirements.txt exists."""
    if os.path.exists("requirements.txt"):
        print("📜 Installing dependencies from requirements.txt...")
        pip_executable = os.path.join(VENV_DIR, "Scripts" if os.name == "nt" else "bin", "pip")
        subprocess.run([pip_executable, "install", "-r", "requirements.txt"], check=True)
        print("✅ Dependencies installed successfully!")
    else:
        print("⚠️ No requirements.txt found, skipping dependency installation.")

def print_activation_instructions():
    """Prints the activation instructions for different OS."""
    activate_script = os.path.join(VENV_DIR, "Scripts" if os.name == "nt" else "bin", "activate")

    print("\n🚀 To activate the virtual environment, run:")
    if os.name == "nt":  # Windows
        print(f"   .\\{VENV_DIR}\\Scripts\\activate")
    else:  # macOS/Linux
        print(f"   source {VENV_DIR}/bin/activate")

if __name__ == "__main__":
    create_venv()
    install_requirements()
    print_activation_instructions()
