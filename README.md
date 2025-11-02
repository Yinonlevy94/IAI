# IAI Home Task

This project delivers a full CI/CD pipeline for deploying cloud-native microservices into a secure, private Kubernetes cluster on AWS. I've put an emphasis on security, separation of concerns, and robustness over more flashy or feature-rich apps.

---

## High-Level Architecture

<p align="center">
  <img src="./Arch.png" width="900" />
</p>

- React frontend + Flask backend
- Kubernetes cluster 
- Public ALB → Nginx Ingress → Services → Pods
- GitHub Actions for CI and a self-hosted runner for CD
- Container images pushed to ECR according to requirements
- Images are signed using cosign

## Components

### **Frontend**
- React SPA served via Nginx 
- Public access via ALB → Nginx Ingress → Pod
- Communicates with the backend cluster-internally

### **Backend**
- Flask API + Gunicorn
- Exposed via ClusterIP service

### **Kubernetes**
- Self-managed kubeadm cluster 
- CNI: Cilium, no eBPF mode 
- Ingress: Nginx   
- Namespace separation for each component

### **AWS**
- VPC with public & private subnets
- Spanning across 2 AZs for ALB usage 
- NAT instance for private egress
- ALB for HTTPS entry
- ECR for container images
- TLS termination occurs at the internet-facing ALB

---

## CI/CD Flow

<p align="center">
  <img src="./CICD.png" width="900" />
</p>


2. **CI (GitHub-hosted runners):**
   - Run tests 
   - Linting 
   - Build & tag Docker images
   - Trivy security scan
   - Generate SBOM 
   - Push images to ECR
   - Sign images with Sigstore (cosign)
3. **CD (self-hosted runner in VPC):**
   - Uses injected kubeconfig for context
   - Refresh ECR registry secret
   - Confirm image digest
   - Apply Kubernetes manifests
   - Verify rollout success

---

## Security Highlights

- No private keys stored or managed anywhere — Cosign uses keyless signing
- Roles and policies follow the least privileged concept
- Fresh ECR credentials generated every deploy (tokens expire after 12h)
- Vulnerability + secret scanning before images reach production
- SBOM provides full dependency visibility

---

## The App

The app is accessible at: https://iai.yinonlevy.online
