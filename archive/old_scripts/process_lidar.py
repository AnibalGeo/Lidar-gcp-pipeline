import subprocess
import json
import os
import argparse
from pathlib import Path

# Rutas base y configuración
BASE_DIR = Path(r"C:\Users\amata\Desktop\Google")
PIPELINE_CLEAN = BASE_DIR / "pipelines" / "cleaning_ground.json"
PIPELINE_DTM = BASE_DIR / "pipelines" / "generate_dtm.json"
CONDA_ENV = "geomatica-gcp"

def run_pdal(pipeline_template, input_file, output_file):
    if not pipeline_template.exists():
        print(f"❌ Error: No se encuentra el pipeline {pipeline_template}")
        return False

    with open(pipeline_template, 'r') as f:
        pipeline = json.load(f)
    
    # Inyectamos las rutas reales
    pipeline[0]['filename'] = str(input_file)
    pipeline[-1]['filename'] = str(output_file)
    
    temp_json = BASE_DIR / "pipelines" / f"temp_{input_file.stem}.json"
    with open(temp_json, 'w') as f:
        json.dump(pipeline, f)
    
    print(f"⚙️  Procesando: {input_file.name}")
    cmd = ["conda", "run", "-n", CONDA_ENV, "pdal", "pipeline", str(temp_json)]
    
    result = subprocess.run(cmd, capture_output=True, text=True)
    
    if temp_json.exists():
        os.remove(temp_json)

    if result.returncode == 0:
        print(f"   ✅ OK: {output_file.name}")
        return True
    else:
        print(f"   ❌ ERROR en {input_file.name}")
        print(result.stderr)
        return False

def main():
    parser = argparse.ArgumentParser(description="Pipeline flexible de procesamiento LiDAR para Portfolio GCP")
    parser.add_argument("--input", "-i", required=True, help="Ruta de la carpeta con archivos LAZ/LAS brutos")
    parser.add_argument("--output", "-o", required=True, help="Ruta de la carpeta para los resultados")
    
    args = parser.parse_args()
    
    input_path = Path(args.input)
    output_path = Path(args.output)
    
    if not input_path.exists():
        print(f"❌ La ruta de entrada no existe: {input_path}")
        return

    if not output_path.exists():
        print(f"📁 Creando carpeta de salida: {output_path}")
        output_path.mkdir(parents=True)

    # Buscar archivos .laz y .las (insensible a mayúsculas)
    laz_files = [f for f in input_path.rglob("*") if f.suffix.lower() in [".laz", ".las"]]
    
    print(f"🚀 Iniciando procesamiento de {len(laz_files)} archivos...\n")

    for f in laz_files:
        # Definir nombres de salida manteniendo la estructura de subcarpetas si se desea
        # Por ahora lo pondremos plano en el output
        classified_laz = output_path / f.name.replace(f.suffix, "_classified.laz")
        dtm_tif = output_path / f.name.replace(f.suffix, "_dtm.tif")

        # Paso 1: Limpieza y Clasificación
        success = False
        if not classified_laz.exists():
            success = run_pdal(PIPELINE_CLEAN, f, classified_laz)
        else:
            print(f"⏭️  Ya existe clasificado: {classified_laz.name}")
            success = True

        # Paso 2: Generación de DTM
        if success and classified_laz.exists() and not dtm_tif.exists():
            run_pdal(PIPELINE_DTM, classified_laz, dtm_tif)
        elif dtm_tif.exists():
            print(f"   ⏭️  Ya existe DTM: {dtm_tif.name}")

    print("\n🏁 Proceso finalizado.")

if __name__ == "__main__":
    main()
