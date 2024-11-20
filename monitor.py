import psutil
import time
import sys
import os
from threading import Thread, Event

def monitor_process_with_children(pid):
    """
    Monitors a process and its child processes by PID.
    Tracks CPU and memory usage, as well as maximum usage.
    Allows resetting the maximum counters by pressing 'R'.
    """
    try:
        # Get the main process by PID
        main_process = psutil.Process(pid)
        print(f"Monitoring main process with PID: {pid}")
        print(f"Command executed: {' '.join(main_process.cmdline())}\n")

        # Variables for tracking maximum usage
        max_cpu = 0
        max_ram = 0

        # Event to reset the maximum counters
        reset_event = Event()

        # Function to listen for the 'R' key to reset maximum usage
        def listen_for_reset():
            while True:
                key = input().strip().lower()
                if key == 'r':
                    reset_event.set()

        # Start a thread to listen for the reset key
        Thread(target=listen_for_reset, daemon=True).start()

        # Monitor the main process and its children
        while True:
            try:
                # Reset the maximum counters if the reset event is triggered
                if reset_event.is_set():
                    max_cpu = 0
                    max_ram = 0
                    reset_event.clear()
                    print("\n[INFO] Maximum counters have been reset.\n")

                # Monitor the main process
                main_cpu = main_process.cpu_percent(interval=0.1)
                main_ram = main_process.memory_info().rss / (1024 * 1024)  # Convert bytes to MB

                # Monitor child processes
                child_processes = main_process.children(recursive=True)
                total_child_cpu = 0
                total_child_ram = 0

                for child in child_processes:
                    try:
                        child_cpu = child.cpu_percent(interval=0.1)
                        child_ram = child.memory_info().rss / (1024 * 1024)
                        total_child_cpu += child_cpu
                        total_child_ram += child_ram
                    except psutil.NoSuchProcess:
                        continue

                # Calculate total usage
                total_cpu = main_cpu + total_child_cpu
                total_ram = main_ram + total_child_ram

                # Update maximum usage
                max_cpu = max(max_cpu, total_cpu)
                max_ram = max(max_ram, total_ram)

                # Clear the console and display updated stats
                os.system('clear' if os.name == 'posix' else 'cls')
                print(f"Monitoring main process with PID: {pid}")
                print(f"Command executed: {' '.join(main_process.cmdline())}\n")
                print(f"Total CPU: {total_cpu:.2f}% (Max: {max_cpu:.2f}%)")
                print(f"Total RAM: {total_ram:.2f} MB (Max: {max_ram:.2f} MB)")
                print("\nPress 'R' to reset the maximum counters.")
            except psutil.NoSuchProcess:
                print(f"\nThe main process with PID {pid} has terminated.")
                break
            time.sleep(0.1)
    except psutil.NoSuchProcess:
        print(f"No process found with PID {pid}.")
    except Exception as e:
        print(f"Error monitoring the process: {e}")

if __name__ == "__main__":
    # Check if the PID is provided as an argument
    if len(sys.argv) != 2:
        print(f"Usage: python {sys.argv[0]} <PID>")
        sys.exit(1)

    try:
        # Convert the PID argument to an integer and start monitoring
        pid = int(sys.argv[1])
        monitor_process_with_children(pid)
    except ValueError:
        print("The PID must be an integer.")
