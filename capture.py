import subprocess
from gridfs import GridFS
try:
    res = subprocess.check_output(["./camera.sh"], universal_newlines=True)
    print(res)
except Exception as e:
    print(e)