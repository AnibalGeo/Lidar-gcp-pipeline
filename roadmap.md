# Strategic Roadmap — Senior GCP & LiDAR Architecture

**Professional:** Aníbal Matamala Muñoz
**Focus:** Cloud Engineering, Geomatics Automation, GCP Scalability.

---

## 1. Tactical Objective
Accelerate ACE Certification to **Week 3** to maximize depth in Infrastructure (IaC) and Data Engineering. Transform the current local Docker setup into a production-grade **Google Cloud Batch** pipeline by Week 2.

## 2. Infrastructure Metrics
| ID | Milestone | Status |
|----|-----------|--------|
| M1 | Terraform state managed in GCS | Pending |
| M2 | Automated CI/CD to Artifact Registry | In Progress |
| M3 | Cloud Batch Job executing PDAL pipeline | Pending |
| M4 | ACE Certification (June 2026) | Target: Week 3 |

---

## 3. Accelerated Roadmap (Phase A & B)

### FASE A — Accelerated ACE & Cloud-Native Pivot (Weeks 1-3)

#### Week 1: Cloud Foundation & Storage (Current)
- [x] GCS Bucket Architecture (`gs://lidar-pnoa-portfolio/`)
- [x] Initial IAM & Service Account setup.
- [ ] **GCP Skills:** Mastery of `gcloud storage` and basic IAM (Roles vs Scopes).
- [ ] **Engineering Task:** Draft **SDD-001** (Event-Driven LiDAR Ingestion).
- [ ] **Infra:** Move Terraform state to a GCS backend.

#### Week 2: Shift-Left (IaC & Batch Compute)
- [ ] **Terraform (Tier 1):** Provision Artifact Registry, Cloud Batch, and Service Accounts.
- [ ] **GCP Skills:** IAM Deep-dive (Custom Roles, Workload Identity) and VPC Networking (Subnets, Firewall, NAT).
- [ ] **Automation:** Script to build/tag/push Docker image to Artifact Registry.
- [ ] **Deployment:** First Cloud Batch Job deployment using `gcloud batch jobs submit`.

#### Week 3: ACE Certification & Network Hardening
- [ ] **Networking:** Implement VPC Service Controls or private access for GCS.
- [ ] **GCP Skills:** Monitoring, Logging, and Deployment Manager/Terraform comparisons.
- [ ] **Hito:** **ACE Certification Obtained** ✓ (Early June 2026).

---

### FASE B — Data Engineering & Scalability (Weeks 4-9)

#### Week 4: BigQuery GIS & Ingest Automation
- [ ] Initialize BigQuery datasets via Terraform.
- [ ] Pipeline: GCS Trigger (Pub/Sub) -> Cloud Run (Trigger) -> Cloud Batch (Processing).
- [ ] Start PDE Learning Path (Cloud Skills Boost).

#### Week 5-6: Advanced Scaling & Optimization
- [ ] Scale to 100+ parallel Batch tasks.
- [ ] Cost optimization (Spot Instances for Batch).
- [ ] Integration with Vertex AI (preliminary feature extraction).

#### Week 7-9: Advanced PDE & Optimization
- [ ] Full CI/CD with GitHub Actions or Cloud Build.
- [ ] **Hito:** **PDE Certification Obtained** ✓ (August 2026).

---

## 4. Engineering Records (ADRs & SDDs)
*Location: `/docs/`*
- **ADR-001:** Use **Google Cloud Batch** over Cloud Run for heavy LiDAR processing (VPC/Spot optimization).
- **ADR-002:** Terraform as the sole source of truth for GCP resources.
- **SDD-001:** Event-Driven Architecture for Automated LiDAR Ingestion.

---

## 5. System Architecture (Event-Driven)
- **Ingress:** GCS (Raw) -> Pub/Sub Notification.
- **Trigger:** Cloud Run (minimal container) to parse metadata and trigger Batch.
- **Processing:** Google Cloud Batch (PDAL Container).
- **Storage:** GCS (Processed) + BigQuery GIS (Metadata).
- **Security:** Service Account with granular IAM (PoLP).
