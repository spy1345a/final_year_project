import subprocess
import sys
import os
import time

def get_venv_python():
    if sys.platform == "win32":
        venv_python = os.path.join(".venv", "Scripts", "python.exe")
    else:
        venv_python = os.path.join(".venv", "bin", "python")
    return venv_python

def start_api():
    print("[API] Starting FastAPI server...")
    api_process = subprocess.Popen(
        [get_venv_python(), "-m", "uvicorn", "api.main:app", "--host", "0.0.0.0", "--port", "8000"],
        cwd=os.path.dirname(os.path.abspath(__file__))
    )
    return api_process

def start_web():
    print("[WEB] Starting Flask web application...")
    web_process = subprocess.Popen(
        [get_venv_python(), "web_application/flask_app.py"],
        cwd=os.path.dirname(os.path.abspath(__file__))
    )
    return web_process

def main():
    print("=" * 50)
    print("  Starting Expense Tracker Application")
    print("=" * 50)
    print()
    
    api_process = start_api()
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
