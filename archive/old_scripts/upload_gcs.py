from pathlib import Path
import subprocess
import shutil

SECTORES = Path(r"C:\Users\amata\Desktop\Google\Sectores")
BUCKET = "gs://lidar-pnoa-portfolio/raw/epoch_1/"

# Encuentra gsutil automáticamente
gsutil = shutil.which("gsutil") or r"C:\Users\amata\AppData\Local\Google\Cloud SDK\google-cloud-sdk\bin\gsutil.cmd"

files = [str(f) for f in SECTORES.rglob("*epsg25830*.laz")]
print(f"Subiendo {len(files)} archivos:")
for f in files:
    print(f"  {f}")

subprocess.run([gsutil, "-m", "cp"] + files + [BUCKET])