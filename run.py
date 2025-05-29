import sys
import os
import subprocess

def run_streamlit():
    subprocess.Popen(["streamlit", "run", "src/streamlit_ui.py", "--server.port", "8501","--server.runOnSave","true"])

def run_pytests():
    return subprocess.Popen(["ptw", "--clear"])

def run_fastapi():
    os.environ["PYTHONPATH"] = "./src"
    return subprocess.Popen(["uvicorn", "api.api:app", "--reload", "--reload-dir", "src", "--port", "8512"])

def run_all():
    procs = [run_pytests(), run_fastapi()]

    try:
        for proc in procs:
            proc.wait()
    except KeyboardInterrupt:
        print("\nStopping processes...")
        for proc in procs:
            proc.terminate()
        for proc in procs:
            try:
                proc.wait(timeout=5)
            except subprocess.TimeoutExpired:
                proc.kill()
    finally:
        input("Press Enter to exit...")


def main():
    if len(sys.argv) < 2:
        print("Usage: python run.py [streamlit|test|fastapi|all]")
        sys.exit(1)

    cmd = sys.argv[1]

    if cmd == "ui":
        run_streamlit()
    elif cmd == "test":
        run_pytests().wait()
    elif cmd == "api":
        run_fastapi().wait()
    elif cmd == "all":
        run_all()
    else:
        print(f"Unknown command: {cmd}")
        sys.exit(1)


if __name__ == "__main__":
    main()
