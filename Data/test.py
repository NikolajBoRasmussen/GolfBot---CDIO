from IPython import display
display.clear_output()
import subprocess
subprocess.run(["yolo", "mode=checks"], check=True)