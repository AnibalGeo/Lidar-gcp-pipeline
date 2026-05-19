import subprocess
import json
import os
import argparse
from pathlib import Path
import logging

# Configuración de Logging para un entorno Senior
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# En el contenedor, el path es /project
# Localmente, el script usará la ruta relativa
BASE_DIR = Path("/project") if Path("/project").exists() else Path(".")
PIPELINE_DIR = BASE_DIR / "pipelines"
EPSG_DEFAULT = "EPSG:25830"

def run_pdal(pipeline_template, input_file, output_file, custom_params=None):
    """Ejecuta un pipeline de PDAL inyectando parámetros dinámicamente."""
    if not pipeline_template.exists():
        logger.error(f"No se encuentra el pipeline: {pipeline_template}")
        return False

    try:
        with open(pipeline_template, 'r') as f:
            pipeline = json.load(f)
        
        # Inyectamos rutas (asumiendo Reader en [0] y Writer en [-1])
        pipeline[0]['filename'] = str(input_file)
        pipeline[-1]['filename'] = str(output_file)
        
        # Aplicamos parámetros extra si existen (ej: EPSG)
        if custom_params:
            for key, value in custom_params.items():
                # Buscamos el componente del pipeline que necesita el parámetro
                for stage in pipeline:
                    if key in stage:
                        stage[key] = value

        temp_json = PIPELINE_DIR / f"temp_{input_file.stem}.json"
        with open(temp_json, 'w') as f:
            json.dump(pipeline, f)
        
        logger.info(f"⚙️ Ejecutando PDAL para: {input_file.name}")
        cmd = ["pdal", "pipeline", str(temp_json)]
        
        result = subprocess.run(cmd, capture_output=True, text=True)
        
        if temp_json.exists():
            os.remove(temp_json)

        if result.returncode == 0:
            logger.info(f"✅ Éxito: {output_file.name}")
            return True
        else:
            logger.error(f"❌ Fallo en PDAL para {input_file.name}")
            logger.error(result.stderr)
            return False
    except Exception as e:
        logger.exception(f"Error inesperado procesando {input_file.name}: {e}")
        return False

def fix_crs_only(input_file, output_file, epsg):
    """Corrige el CRS si no es necesario correr un pipeline complejo."""
    logger.info(f"⚙️ Corrigiendo CRS ({epsg}) para: {input_file.name}")
    cmd = [
        "pdal", "translate", str(input_file), str(output_file),
        f"--writers.las.a_srs={epsg}"
    ]
    result = subprocess.run(cmd, capture_output=True, text=True)
    return result.returncode == 0

def process_sector(sector_path, output_base, epsg):
    """Orquesta el procesamiento de un sector completo."""
    sector_path = Path(sector_path)
    output_base = Path(output_base) / sector_path.name
    
    if not sector_path.exists():
        logger.error(f"La ruta del sector no existe: {sector_path}")
        return

    output_base.mkdir(parents=True, exist_ok=True)
    
    laz_files = [f for f in sector_path.glob("*.laz")]
    logger.info(f"🚀 Procesando Sector: {sector_path.name} ({len(laz_files)} archivos)")

    for f in laz_files:
        # 1. Definir rutas de salida
        # Paso intermedio: CRS corregido (si es necesario)
        temp_crs = output_base / f"{f.stem}_crs.laz"
        # Paso final: Clasificado y DTM
        final_laz = output_base / f"{f.stem}_classified.laz"
        final_dtm = output_base / f"{f.stem}_dtm.tif"

        # 2. Paso 1: Fix CRS
        if not fix_crs_only(f, temp_crs, epsg):
            continue

        # 3. Paso 2: Clasificación (Cleaning Ground)
        pipeline_clean = PIPELINE_DIR / "cleaning_ground.json"
        if run_pdal(pipeline_clean, temp_crs, final_laz):
            # 4. Paso 3: Generación de DTM
            pipeline_dtm = PIPELINE_DIR / "generate_dtm.json"
            run_pdal(pipeline_dtm, final_laz, final_dtm)
            
            # Limpieza de archivos temporales para ahorrar espacio
            if temp_crs.exists():
                os.remove(temp_crs)
        else:
            logger.error(f"Se detuvo el pipeline para {f.name} por error en clasificación.")

def main():
    parser = argparse.ArgumentParser(description="Lidar Worker: Procesamiento atómico por sector.")
    parser.add_argument("--input", "-i", required=True, help="Carpeta del sector (ej: Sectores/20260513_Sector001)")
    parser.add_argument("--output", "-o", default="processed", help="Carpeta base para resultados")
    parser.add_argument("--epsg", default=EPSG_DEFAULT, help="Sistema de coordenadas objetivo")
    
    args = parser.parse_args()
    process_sector(args.input, args.output, args.epsg)

if __name__ == "__main__":
    main()
