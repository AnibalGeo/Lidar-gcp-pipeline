@echo off
conda activate geomatica-gcp

for /D %%s in ("C:\Users\amata\Desktop\Google\Sectores\sector_*") do (
    for %%f in ("%%s\*.laz") do (
        echo Procesando: %%f
        pdal translate "%%f" "%%~dpfs%%~nf_epsg25830.laz" --writers.las.a_srs="EPSG:25830"
    )
)
echo.
echo Todos los archivos procesados
pause