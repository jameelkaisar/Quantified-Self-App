import subprocess
import os

if not os.path.exists("Quantified-Self-App"):
    subprocess.call(["chmod", "+x", "init.sh"])
    subprocess.call(["./init.sh"])

subprocess.call(["chmod", "+x", "run.sh"])
subprocess.call(["./run.sh"])
