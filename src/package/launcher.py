import subprocess
import sys
from pathlib import Path

def main():
    project_root = Path(__file__).parent
    main_file = project_root / "main.py"

    subprocess.run(
        [sys.executable, "-m", "streamlit", "run", str(main_file)],
        check=True,
    )

if __name__ == "__main__":
    main()