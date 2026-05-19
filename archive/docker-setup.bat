@echo off
echo 🛠️  Construyendo imagen de Docker...
docker-compose build

echo 🚀 Verificando herramientas en el contenedor...
docker-compose run --rm lidar-tool

echo.
echo ✅ Entorno Docker listo. 
echo Puedes correr comandos usando: docker-compose run --rm lidar-tool [comando]
echo Ejemplo: docker-compose run --rm lidar-tool pdal info Sectores/sector_1/archivo.laz
