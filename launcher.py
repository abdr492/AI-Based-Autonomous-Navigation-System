import subprocess
import time
import threading

def run_simulation():
    """Continuously run the virtual simulation, restarting if it exits"""
    while True:
        try:
            print("[LAUNCHER] Starting virtual simulation...", flush=True)
            process = subprocess.Popen(
                ["python", "virtual_simulation.py"],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True
            )
            process.wait()
            print("[LAUNCHER] Simulation exited, restarting in 2 seconds...", flush=True)
            time.sleep(2)
        except Exception as e:
            print(f"[LAUNCHER] Error: {e}", flush=True)
            time.sleep(2)

if __name__ == "__main__":
    print("[LAUNCHER] Starting Multi-Agent Navigation System", flush=True)
    print("[LAUNCHER] Flask Dashboard: http://127.0.0.1:5000/", flush=True)
    print("[LAUNCHER] Virtual Simulation: Starting...", flush=True)
    
    # Start simulation in a background thread
    sim_thread = threading.Thread(target=run_simulation, daemon=True)
    sim_thread.start()
    
    # Keep the launcher running
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\n[LAUNCHER] Shutting down...", flush=True)
