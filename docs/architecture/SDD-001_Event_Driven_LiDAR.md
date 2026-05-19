# SDD-001: Event-Driven LiDAR Ingestion & Processing

## 1. Problem Statement
Manual uploading and local processing of LiDAR data is non-scalable and error-prone. We need an automated, cloud-native system that reacts to new data and scales horizontally.

## 2. Proposed Architecture
A decoupled event-driven system leveraging Google Cloud native services.

### 2.1 Workflow
1. **Ingest:** User/Sensor uploads `.laz` file to `gs://lidar-pnoa-portfolio/raw/`.
2. **Notify:** GCS Pub/Sub Notification triggers a message to a topic.
3. **Trigger:** A Cloud Run service (Ingestion-Trigger) receives the message.
4. **Validation:** Ingestion-Trigger checks CRS (EPSG:25830) and metadata.
5. **Orchestrate:** Ingestion-Trigger submits a **Google Cloud Batch Job**.
6. **Process:** Cloud Batch spins up a PDAL container, processes the data, and writes to `gs://lidar-pnoa-portfolio/processed/`.
7. **Complete:** Batch job updates metadata in BigQuery GIS.

## 3. Component Details
- **Pub/Sub Topic:** `lidar-ingestion-events`
- **Cloud Run Service:** `lidar-trigger-service`
- **Compute:** `google-cloud-batch` (Using Spot Instances).
- **Container Registry:** Artifact Registry (`lidar-repo`).

## 4. Security (IAM)
- `sa-lidar-trigger`: Permisos de `pubsub.subscriber` y `batch.jobs.create`.
- `sa-lidar-worker`: Permisos de `storage.objectAdmin` y `bigquery.dataEditor`.

## 5. Scalability & Cost
- **Concurrency:** Batch allows thousands of parallel tasks.
- **Cost:** Spot Instances reduce compute cost by up to 90%.
- **Storage:** GCS Lifecycle policies move raw data to Nearline after 30 days.

## 6. Implementation Plan (Week 2-3)
- [ ] Phase 1: Terraform provisioning of Pub/Sub and Artifact Registry.
- [ ] Phase 2: Ingestion-Trigger service (Python/Flask) deployment.
- [ ] Phase 3: Cloud Batch Job template definition.
