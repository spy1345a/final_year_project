import subprocess
import sys
import os
import shutil

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
VENV_DIR = os.path.join(SCRIPT_DIR, ".venv")
REQUIREMENTS_FILE = os.path.join(SCRIPT_DIR, "requirements.txt")
ENV_FILE = os.path.join(SCRIPT_DIR, ".env")
ENV_EXAMPLE_FILE = os.path.join(SCRIPT_DIR, ".env.example")

def get_system_python():
    if sys.platform == "win32":
        return "python"
    return "python3"

def get_venv_python():
    if sys.platform == "win32":
        return os.path.join(VENV_DIR, "Scripts", "python.exe")
    return os.path.join(VENV_DIR, "bin", "python")

def get_venv_pip():
    if sys.platform == "win32":
        return os.path.join(VENV_DIR, "Scripts", "pip.exe")
    return os.path.join(VENV_DIR, "bin", "pip")

def check_venv():
    return os.path.exists(get_venv_python())

def is_running_in_venv():
    return sys.prefix != sys.base_prefix

def create_venv():
    print("[SETUP] Creating virtual environment...")
    python = get_system_python()
    subprocess.run([python, "-m", "venv", VENV_DIR], check=True)
    print("[SETUP] Virtual environment created")

def install_dependencies():
    print("[SETUP] Installing dependencies...")
    subprocess.run([get_venv_python(), "-m", "pip", "install", "--upgrade", "pip"], check=False)
    subprocess.run([get_venv_python(), "-m", "pip", "install", "-r", REQUIREMENTS_FILE], check=True)
    print("[SETUP] Dependencies installed")

def setup_env():
    if not os.path.exists(ENV_FILE):
        if os.path.exists(ENV_EXAMPLE_FILE):
            print("[SETUP] Creating .env from .env.example...")
            shutil.copy(ENV_EXAMPLE_FILE, ENV_FILE)
            print("[SETUP] .env file created")
        else:
            print("[SETUP] WARNING: No .env or .env.example found!")
    else:
        print("[SETUP] .env file already exists")

def run_in_venv():
    if is_running_in_venv():
        return
    
    venv_python = get_venv_python()
    if not check_venv():
        create_venv()
        install_dependencies()
    
    print("[INFO] Re-running script in virtual environment...")
    os.execv(venv_python, [venv_python] + sys.argv)

def setup():
    run_in_venv()
    setup_env()
    print("[SETUP] Using virtual environment:", VENV_DIR)
    print()

def start_api():
    print("[API] Starting FastAPI server...")
    api_process = subprocess.Popen(
        [get_venv_python(), "-m", "uvicorn", "api.main:app", "--host", "0.0.0.0", "--port", "8000"],
        cwd=SCRIPT_DIR
    )
    return api_process

def start_web():
    print("[WEB] Starting Flask web application...")
    web_process = subprocess.Popen(
        [get_venv_python(), "web_application/flask_app.py"],
        cwd=SCRIPT_DIR
    )
    return web_process

def main():
    print("=" * 50)
    print("  Expense Tracker Application")
    print("=" * 50)
    print()
    
    setup()
    
    print("=" * 50)
    print("  Starting Services...")
    print("=" * 50)
    print()
    
    api_process = start_api()
    import time
    time.sleep(2)
    web_process = start_web()
    
    print()
    print("=" * 50)
    print("  Application Started Successfully!")
    print("  API:     http://localhost:8000")
    print("  Web:     http://localhost:5000")
    print("  Swagger: http://localhost:8000/docs")
    print("=" * 50)
    print()
    print("Press Ctrl+C to stop all services")
    print()
    
    try:
        api_process.wait()
        web_process.wait()
    except KeyboardInterrupt:
        print("\n[STOPPING] Shutting down services...")
        api_process.terminate()
        web_process.terminate()
        api_process.wait()
        web_process.wait()
        print("[STOPPED] All services stopped")

if __name__ == "__main__":
    main()
