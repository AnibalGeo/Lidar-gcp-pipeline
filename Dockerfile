# Imagen base con PDAL preinstalado
FROM pdal/pdal:latest

# Instalación de Python y herramientas básicas
RUN apt-get update && apt-get install -y \
    python3 \
    python3-pip \
    curl \
    gnupg \
    && rm -rf /var/lib/apt/lists/*

# Instalación de Google Cloud SDK (para interactuar con GCS desde el contenedor)
RUN echo "deb [signed-by=/usr/share/keyrings/cloud.google.gpg] http://packages.cloud.google.com/apt cloud-sdk main" | \
    tee -a /etc/apt/sources.list.d/google-cloud-sdk.list && \
    curl https://packages.cloud.google.com/apt/doc/apt-key.gpg | \
    apt-key --keyring /usr/share/keyrings/cloud.google.gpg  add - && \
    apt-get update -y && apt-get install google-cloud-cli -y

# Instalación de librerías Python necesarias para geomática
RUN pip3 install --no-cache-dir \
    laspy[lazrs,helio] \
    numpy \
    pandas \
    geopandas \
    rasterio

# Directorio de trabajo
WORKDIR /project

# Comando por defecto: verificar versiones
CMD ["sh", "-c", "pdal --version && python3 --version && gcloud --version"]
