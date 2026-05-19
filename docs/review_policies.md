# Agent Review & Approval Policies

## 1. Goal
Ensure all infrastructure and critical automation code meets Senior Engineering standards and is validated by the Technical Approver (User) before deployment.

## 2. Workflow
1. **Generation:** The Agent generates the proposed code (Terraform, Dockerfiles, Scripts).
2. **Review:** The Agent presents the code with a technical rationale.
3. **Validation:** 
   - For Terraform: The User runs `terraform plan` or the Agent simulates it.
   - For Scripts: The User reviews logic and security (PoLP).
4. **Approval:** The User provides explicit approval (e.g., "Approved", "Proceed").
5. **Execution:** Only after approval, the Agent proceeds with deployment or further automation.

## 3. Technology Stack (Mandatory)
- **IaC:** Terraform >= 1.5.0
- **Cloud:** Google Cloud Platform (GCP)
- **Compute:** Cloud Batch, Cloud Run
- **Data:** Cloud Storage, BigQuery GIS

## 4. Security Standards
- No hardcoded secrets. Use Secret Manager if needed.
- All Service Accounts must follow Principle of Least Privilege.
- VPC Service Controls for sensitive data paths.
