# Technical Decisions

Record at least 5 decisions. Include assumptions and limits.

## Decision 1: Base Image Selection
- Choice: Using official lightweight Python (`python:3.10-slim`) and Nginx (`nginx:alpine`) base images.
- Why: Minimizes security attack surface, reduces final container image size, and ensures stability with standard packages.
- Alternative: Using full-fat Debian/Ubuntu base images or custom corporate base images.
- Trade-off: Smaller images lack some pre-installed diagnostic tools (like `curl` or `vim`), requiring manual installation during builds if debugging inside containers is needed.
- Evidence / commit: `docker-compose.yml`, `Dockerfile`
- Production improvement: Integrate automated vulnerability scanning (e.g., Trivy) in the CI pipeline to continuously track base image CVEs.

---

## Decision 2: Multi-Instance Deployment & Health Checks
- Choice: Deploying dual application instances (`app-01`, `app-02`) behind Nginx with strict HTTP health checks (`/ready` endpoint).
- Why: Ensures high availability, load distribution, and allows Nginx to automatically drop unhealthy nodes from traffic rotation.
- Alternative: Running a single monolithic container instance.
- Trade-off: Slightly higher memory consumption and stateless app design requirements versus robust fault tolerance.
- Evidence / commit: `docker-compose.yml`, `nginx/nginx.conf`
- Production improvement: Implement dynamic service discovery (e.g., Consul or Kubernetes ingress controllers) for automated scaling under heavy traffic loads.

---

## Decision 3: Network Isolation (Frontend & Backend Segregation)
- Choice: Separating containers into two distinct Docker bridge networks (`frontend` and `backend`).
- Why: Enhances security by ensuring databases (`PostgreSQL`, `Redis`) are isolated from direct public/frontend exposure, allowing only backend-connected apps to access them.
- Alternative: Placing all services on a single flat default bridge network.
- Trade-off: Requires explicit network configuration and multi-network container attachments (`app-01`, `app-02`), increasing configuration complexity.
- Evidence / commit: `docker-compose.yml`
- Production improvement: Enforce strict firewall rules (iptables/NetworkPolicies) and mTLS encryption for inter-service communication in production clusters.

---

## Decision 4: Storage & Volume Persistence
- Choice: Using named Docker volumes (`postgres_data`, `redis_data`) coupled with a graceful shutdown strategy (avoiding `--volumes` on down commands).
- Why: Guarantees that transactional data and cache states survive container restarts and deployments without accidental data loss.
- Alternative: Relying on ephemeral container storage or host bind-mounts.
- Trade-off: Persistent volumes require manual cleanup commands (`docker volume prune` or `down -v`) when doing a complete factory reset.
- Evidence / commit: `docker-compose.yml`, `backup.sh`, `restore.sh`
- Production improvement: Implement automated cloud-native snapshot backups stored in secure off-site object storage (e.g., AWS S3 with lifecycle rules).

---

## Decision 5: Timeouts, Retries & Restart Policies
- Choice: Configuring exponential backoff retry mechanisms in the application layer combined with container `restart: unless-stopped` policies.
- Why: Prevents cascading service failures during temporary network blips or startup dependency delays (e.g., waiting for PostgreSQL to become healthy).
- Alternative: Infinite immediate restarts or failing instantly on first timeout.
- Trade-off: Adds slight latency to initial startup sequences while waiting for dependencies to report healthy status.
- Evidence / commit: `docker-compose.yml`, `validate.py`, `failure_test.py`
- Production improvement: Integrate centralized distributed tracing and observability tools (like Prometheus and Grafana) to monitor timeout thresholds and error spikes in real time.
