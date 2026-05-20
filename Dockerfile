# Imagen base PDAL — pineada al SHA del 18 May 2026
# PDAL no publica tags por versión; usamos SHA específico para reproducibilidad
# Para actualizar: revisar https://hub.docker.com/r/pdal/pdal/tags
FROM pdal/pdal:sha-72443981-amd64

LABEL maintainer="anibal.geomatico@gmail.com"
LABEL description="LiDAR processing worker — PDAL + Python for GCP"

WORKDIR /app

# La imagen base usa conda; python3-pip del sistema NO comparte
# packages con el python que usa PDAL.
# NOTA: el RUN apt-get anterior ya no es estrictamente necesario
# (la imagen base ya tiene python3-pip dentro de conda), pero
# lo mantenemos por si algún paquete del sistema lo requiriera.
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
        python3-pip \
        python3-dev && \
    rm -rf /var/lib/apt/lists/*

# Instalamos paquetes Python en el environment 'pdal' del conda interno.
# Esto garantiza que laspy/numpy/gcs estén accesibles desde scripts
# que se ejecuten con el python de PDAL.
RUN /opt/conda/envs/pdal/bin/pip install --no-cache-dir \
    laspy[lazrs] \
    numpy \
    google-cloud-storage

ENTRYPOINT ["pdal"]