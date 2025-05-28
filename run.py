import os
import subprocess

def run_streamlit():
    os.environ["PYTHONPATH"] = "./src"
    subprocess.run(["streamlit", "run", "src/APIExplorerUI.py", "--server.port", "8501", "--server.runOnSave", "true"], check=True)

def run_pytests():
    subprocess.run(["ptw", "--clear"])

def run_fastapi():
    os.environ["PYTHONPATH"] = "./src"
    try:
        subprocess.run(["uvicorn", "api.api:app", "--reload", "--reload-dir", "src", "--port", "8512"], check=True)
    except KeyboardInterrupt:
        print("\nStopped.")
    finally:
        input("Press Enter to continue...")


if __name__ == "__main__":
    run_streamlit()
    # run_pytests()
    # run_fastapi()
