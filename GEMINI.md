# Project Instructions: LiDAR & GCP Portfolio (Refactored)

## Context
Senior-level pipeline development for LiDAR processing integrated with Google Cloud Platform.
**Current Stage:** Phase A - GCP Advanced Fundamentals (Weeks 1-3).
**Goal:** Fast-Track ACE Certification, Terraform Foundations & Automated Batch Architecture.

## Standards
- **Cloud Native Architecture:** Prioritize event-driven microservices. Abandon manual local flows.
- **Infrastructure as Code (IaC):** Every bucket, service account, and permission must be provisioned via Terraform (.tf).
- **Automated Processing:** Use Google Cloud Batch connected to Artifact Registry for scalable processing of .laz datasets.
- **Data Integrity:** Strict CRS validation (EPSG:25830) implemented within containerized environments.

## Architecture Guidelines (Senior Level)
- **ADR Required:** Every architectural change must document its justification in `/docs/adr/`.
- **Review Policy:** Automate implementations using CLI/Scripts, verify permissions using the principle of least privilege (IAM).
