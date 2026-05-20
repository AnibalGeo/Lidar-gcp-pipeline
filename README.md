# LiDAR-GCP Pipeline

**Multitemporal LiDAR change detection on Google Cloud Platform**
Cloud-native pipeline for processing aerial LiDAR point clouds, classifying ground returns, and computing volumetric change between epochs — applicable to mining, forestry, and infrastructure monitoring.

[![Status](https://img.shields.io/badge/status-active%20development-yellow)]()
[![GCP](https://img.shields.io/badge/cloud-GCP-4285F4)]()
[![PDAL](https://img.shields.io/badge/PDAL-2.10-orange)]()
[![Terraform](https://img.shields.io/badge/IaC-Terraform-7B42BC)]()

---

## Overview

This pipeline ingests raw LiDAR point clouds (LAS/LAZ), applies a reproducible classification workflow (statistical noise removal → SMRF ground filtering → IDW interpolation), and produces Digital Terrain Models (DTMs) ready for volumetric difference analysis (`Z_new - Z_old`).

The architecture is **event-driven and serverless**: a file lands in Cloud Storage → Pub/Sub triggers a Cloud Run service → Cloud Batch executes the containerized PDAL pipeline → results are stored in GCS and indexed in BigQuery GIS.

**Status:** active development — pre-production.

---

## Why this matters

Manual LiDAR processing of multi-epoch datasets in desktop tools takes hours per file and doesn't scale. This pipeline demonstrates a path from a working local Docker workflow to a cloud-native architecture capable of processing hundreds of files in parallel — relevant for:

- **Mining**: extraction/stockpile volume monitoring
- **Forestry**: biomass change, harvest tracking
- **Utilities**: vegetation encroachment on transmission corridors
- **Disaster response**: post-event erosion and slope movement

---

## Architecture

```
   ┌──────────────┐      ┌─────────────┐      ┌──────────────────┐
   │  LAZ upload  │─────▶│  Cloud      │─────▶│  Cloud Run       │
   │  (raw/)      │      │  Storage    │      │  (trigger)       │
   └──────────────┘      └─────────────┘      └────────┬─────────┘
                                                       │
                                                       ▼
                         ┌───────────────────────────────────────┐
                         │  Cloud Batch                          │
                         │  ┌─────────────────────────────────┐  │
                         │  │  lidar-worker:v1 (Docker)       │  │
                         │  │  PDAL 2.10 + GDAL + Python      │  │
                         │  │                                 │  │
                         │  │  SOR → SMRF → IDW → DTM         │  │
                         │  └─────────────────────────────────┘  │
                         └────────────────┬──────────────────────┘
                                          │
                              ┌───────────┴───────────┐
                              ▼                       ▼
                      ┌──────────────┐       ┌────────────────┐
                      │ Cloud        │       │ BigQuery GIS   │
                      │ Storage      │       │ (metadata,     │
                      │ (DTM, DoD)   │       │  volumes)      │
                      └──────────────┘       └────────────────┘
```

Detailed architecture: [`docs/architecture/SDD-001_Event_Driven_LiDAR.md`](docs/architecture/SDD-001_Event_Driven_LiDAR.md)

---

## Tech stack

| Layer | Technology |
|---|---|
| Point cloud processing | PDAL 2.10, GDAL, laspy |
| Containerization | Docker, Google Artifact Registry |
| Compute | Cloud Run, Cloud Batch |
| Storage | Cloud Storage, BigQuery GIS |
| Orchestration | Pub/Sub, Eventarc |
| IaC | Terraform |
| Language | Python 3.11 |
| CRS | EPSG:25830 (ETRS89 / UTM zone 30N) |

---

## Repository structure

```
.
├── src/                              # Python workers and entry points
│   ├── lidar_worker.py
│   └── process_lidar_docker.py
├── pipelines/                        # PDAL pipeline definitions (JSON)
│   ├── cleaning_ground.json
│   └── generate_dtm.json
├── docs/
│   ├── architecture/
│   │   └── SDD-001_Event_Driven_LiDAR.md
│   ├── review_policies.md
│   └── roadmap.md
├── archive/                          # Legacy scripts (reference only)
├── Dockerfile                        # lidar-worker container definition
├── docker-compose.yml                # Local development setup
├── main.tf                           # Terraform infrastructure
├── comandos_gcloud_storage.md        # gcloud storage CLI reference
├── PROGRESS.md                       # Current state and next steps
├── GEMINI.md                         # Project standards
└── roadmap.md                        # Development roadmap
```

**Note on data:** Raw and processed LiDAR files (`.laz`, `.tif`) are excluded from this repository (see `.gitignore`). The pipeline expects data mounted from `C:\data` (local) or `gs://lidar-pnoa-portfolio/` (cloud).

---

## Quick start (local)

### Prerequisites
- Docker Desktop (Linux containers)
- Google Cloud SDK authenticated
- LAZ/LAS files in a local directory

### Run the pipeline

```powershell
docker run --rm `
  -v "C:/Users/amata/Desktop/Google:/codigo" `
  -v "C:/data:/datos" `
  europe-west1-docker.pkg.dev/geomatica-portfolio/lidar-tool-repo/lidar-worker:v1 `
  pdal pipeline /codigo/pipelines/generate_dtm.json `
  --readers.las.filename=/datos/input_raw_old.laz `
  --writers.gdal.filename=/datos/old_dtm.tif
```

---

## Dataset

Validation uses publicly available LiDAR data from **PNOA (Plan Nacional de Ortofotografía Aérea, Spain)** — a mountainous region (~1200–2400 m altitude, ~13 km² coverage, ~5 pts/m² density). The processing methodology is fully applicable to confidential mining or forestry datasets; only the data source changes.

---

## Roadmap

This project is part of a structured 28-week development plan toward **Google Cloud certifications and Senior Cloud Geomatics role** (target: December 2026).

| Phase | Timeline | Milestone |
|---|---|---|
| A — GCP Fundamentals | Weeks 1-6 | Associate Cloud Engineer certification |
| B — Data Engineering | Weeks 7-13 | Professional Data Engineer certification |
| C — Machine Learning | Weeks 14-22 | Professional ML Engineer certification |
| D — Application | Weeks 23-28 | Portfolio finalization, job applications |

Full roadmap: [`roadmap.md`](roadmap.md) · Current status: [`PROGRESS.md`](PROGRESS.md)

---

## Contact

**Aníbal Matamala M.** — Senior Geomatics Engineer (LiDAR / Photogrammetry / Cloud)

- LinkedIn: [linkedin.com/in/amatamalamunoz](https://www.linkedin.com/in/amatamalamunoz)
- Email: anibal.geomatico@gmail.com
- GitHub: [@AnibalGeo](https://github.com/AnibalGeo)

---

<details>
<summary><strong>🇪🇸 Versión en español</strong></summary>

## Resumen

Pipeline cloud-native para procesamiento de nubes de puntos LiDAR aéreas, clasificación de retornos de suelo y cálculo de cambios volumétricos entre épocas. Aplicable a minería, forestal y monitoreo de infraestructura.

La arquitectura es **event-driven y serverless**: un archivo llega a Cloud Storage → Pub/Sub dispara un servicio Cloud Run → Cloud Batch ejecuta el pipeline PDAL containerizado → los resultados se almacenan en GCS e indexan en BigQuery GIS.

**Estado:** desarrollo activo — pre-producción.

## ¿Por qué importa?

El procesamiento manual de datasets LiDAR multitemporales en herramientas de escritorio toma horas por archivo y no escala. Este pipeline demuestra el camino desde un workflow local Docker funcional hacia una arquitectura cloud-native capaz de procesar cientos de archivos en paralelo — relevante para:

- **Minería**: monitoreo de volúmenes de extracción y acopio
- **Forestal**: cambios de biomasa, seguimiento de cosecha
- **Utilities**: invasión vegetal en corredores eléctricos
- **Respuesta a catástrofes**: erosión post-evento y movimiento de taludes

## Stack técnico

| Capa | Tecnología |
|---|---|
| Procesamiento de nubes | PDAL 2.10, GDAL, laspy |
| Containerización | Docker, Google Artifact Registry |
| Cómputo | Cloud Run, Cloud Batch |
| Almacenamiento | Cloud Storage, BigQuery GIS |
| Orquestación | Pub/Sub, Eventarc |
| IaC | Terraform |
| Lenguaje | Python 3.11 |
| CRS | EPSG:25830 (ETRS89 / UTM zona 30N) |

## Dataset

La validación utiliza datos LiDAR públicos del **PNOA (Plan Nacional de Ortofotografía Aérea, España)** — una región montañosa (~1200–2400 m altitud, ~13 km² de cobertura, ~5 pts/m² de densidad). La metodología es aplicable a datasets confidenciales de minería o forestal; solo cambia la fuente de los datos.

## Contacto

**Aníbal Matamala M.** — Ingeniero Geomático Senior (LiDAR / Fotogrametría / Cloud)

- LinkedIn: [linkedin.com/in/amatamalamunoz](https://www.linkedin.com/in/amatamalamunoz)
- Email: anibal.geomatico@gmail.com

</details>

---

*Last updated: May 2026*
