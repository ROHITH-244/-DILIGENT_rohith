import subprocess
import sys
import os
import threading
import time

def run_backend():
    """Run the FastAPI backend server."""
    try:
        # Change to backend directory
        os.chdir("backend")
        # Run the FastAPI server
        subprocess.run([sys.executable, "-m", "uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000", "--reload"])
    except KeyboardInterrupt:
        print("Backend server stopped.")

def run_frontend():
    """Run the Streamlit frontend."""
    try:
        # Change to ui directory
        os.chdir("../ui")
        # Run the Streamlit app
        subprocess.run([sys.executable, "-m", "streamlit", "run", "chat_ui.py", "--server.port", "8501"])
    except KeyboardInterrupt:
        print("Frontend server stopped.")

def main():
    print("Starting Jarvis AI Assistant...")
    print("Setting up backend server on http://localhost:8000")
    print("Setting up frontend on http://localhost:8501")
    print("\nPress Ctrl+C to stop both servers.\n")
    
    # Start backend in a separate thread
    backend_thread = threading.Thread(target=run_backend)
    backend_thread.daemon = True
    backend_thread.start()
    
    # Wait a moment for backend to start
    time.sleep(2)
    
    # Start frontend (in main thread)
    run_frontend()

if __name__ == "__main__":
    main()