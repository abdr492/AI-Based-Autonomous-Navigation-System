import sys
import traceback

try:
    print("Starting virtual simulation debug...", flush=True)
    import virtual_simulation
    print("Module imported successfully", flush=True)
    virtual_simulation.main()
    print("Main function completed", flush=True)
except Exception as e:
    print(f"Error occurred: {e}", flush=True)
    traceback.print_exc()
    sys.exit(1)
