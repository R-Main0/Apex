import subprocess

XBOX_WAKE_SCRIPT = r"C:\Users\cathy\Apex\src\3.10_python_files\xbox_wake.py"

def power_on():
    try:
        subprocess.Popen(
            ["py", "-3.10", XBOX_WAKE_SCRIPT]
        )
        print("Wake command dispatched")
    except Exception as e:
        print(f"Error dispatching wake command: {e}")