import os
import sys
from pathlib import Path
import argparse
from dotenv import load_dotenv

# Add project root to Python path so we can import src modules
sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from src.cli.dspy_queue import add_job

def main():
    print("==================================================")
    print(" Submit DSPy Compilation Job")
    print("==================================================")
    
    # Load environment variables for defaults
    env_path = Path(__file__).resolve().parents[2] / ".env.local"
    load_dotenv(dotenv_path=env_path)
    
    parser = argparse.ArgumentParser(description="Queue a DSPy compilation.")
    parser.add_argument("--provider", type=str, default=os.getenv("DEFAULT_PROVIDER", "gemini"), help="LLM Provider")
    args = parser.parse_args()
    
    job_id = add_job(args.provider)
    print(f"[+] Added compilation job #{job_id} for provider '{args.provider}'.")
    print("    Ensure the queue worker is running: uv run python src/cli/queue_worker.py")

if __name__ == "__main__":
    main()
