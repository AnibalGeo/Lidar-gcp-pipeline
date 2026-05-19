from pathlib import Path
import subprocess
import sys

SECTORES_DIR = Path(r"C:\Users\amata\Desktop\Google\Sectores")
EPSG = "EPSG:25830"

def fix_crs(input_path: Path) -> None:
    # Skip si ya tiene epsg25830 en el nombre
    if "epsg25830" in input_path.name:
        print(f"⏭️  Skip (ya procesado): {input_path.name}")
        return

    output_path = input_path.with_stem(f"{input_path.stem}_epsg25830")

    # Skip si el output ya existe
    if output_path.exists():
        print(f"⏭️  Skip (ya existe): {output_path.name}")
        return

    print(f"⚙️  Procesando: {input_path.name}")
    result = subprocess.run(
        ["pdal", "translate", str(input_path), str(output_path),
         f"--writers.las.a_srs={EPSG}"],
        capture_output=True, text=True
    )

    if result.returncode == 0:
        print(f"✅ OK: {output_path.name}")
    else:
        print(f"❌ ERROR: {input_path.name}")
        print(result.stderr)

def main():
    laz_files = [
        f for f in SECTORES_DIR.rglob("*.laz")
        if "epsg25830" not in f.name  # excluye ya procesados
    ]

    print(f"📦 Archivos encontrados: {len(laz_files)}")
    for f in laz_files:
        print(f"   {f.relative_to(SECTORES_DIR)}")

    print("\n¿Procesar todos? (s/n): ", end="")
    if input().strip().lower() != "s":
        print("Cancelado.")
        sys.exit(0)

    for f in laz_files:
        fix_crs(f)

    print("\n🏁 Proceso completado")

if __name__ == "__main__":
    main()