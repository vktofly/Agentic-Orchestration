import time
import sys
from pathlib import Path
from dotenv import load_dotenv
import dspy

# Add project root to Python path so we can import src modules
sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from src.cli.dspy_queue import get_next_job, complete_job
from src.vector_store.qdrant_store import QdrantDSPyRM
from src.dspy_modules.qa_system import compile_rag_module
from src.dspy_modules.model_factory import get_model

def worker():
    print("==================================================")
    print(" Background DSPy Queue Worker")
    print("==================================================")
    
    env_path = Path(__file__).resolve().parents[2] / ".env.local"
    load_dotenv(dotenv_path=env_path)
    
    print("[*] Worker started. Polling for jobs...")
    
    while True:
        job = get_next_job()
        if not job:
            time.sleep(5)
            continue
            
        print(f"\n[*] Picked up job {job['id']} for provider: {job['provider']}")
        try:
            model = get_model(job['provider'])
            rm = QdrantDSPyRM()
            dspy.settings.configure(lm=model, rm=rm)
            
            print(f"[*] Starting DSPy compilation for job {job['id']}...")
            compiled_rag = compile_rag_module(auto_compile=True)
            
            if compiled_rag:
                print(f"[+] Job {job['id']} finished successfully.")
                complete_job(job['id'], 'completed')
            else:
                print(f"[!] Job {job['id']} failed during compilation.")
                complete_job(job['id'], 'failed')
        except Exception as e:
            print(f"[!] Job {job['id']} crashed: {e}")
            complete_job(job['id'], 'crashed')

if __name__ == "__main__":
    worker()
