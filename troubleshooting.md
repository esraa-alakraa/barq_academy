# Troubleshooting journal

Keep chronological entries. Copy this block for each meaningful investigation.

## Entry / 2026-09-25 / 02:24
- Symptom:`app-01` and `app-02` containers reported `(unhealthy)` status.
- Hypothesis:Healthcheck URL in `docker-compose.yml` does not match Flask routes in `app/server.py`.
- Command or test:`docker inspect app-01` and inspected `app/server.py`.
- Actual output:Server exposes `/health`, but compose file was requesting `/healthz` (404 Not Found).
- Failed attempt and what changed your thinking:.
- Root cause:Mismatched healthcheck endpoint (`/healthz` instead of `/health`) and `app-02` had `INSTANCE_ID: "app-01"`.
- Fix:Corrected endpoint path to `/health` and updated `app-02` `INSTANCE_ID` to `"app-02"` in `docker-compose.yml`.
- Retest evidence:`docker compose ps` showed `app-01` and `app-02` in `Up (healthy)` state.
- Related commit:`fix(docker): correct healthcheck endpoint to /health and fix app-02 instance ID`
- Remaining uncertainty:.
## Entry / 2026-09-25 / 04:30
- Symptom: Nginx container mapped host port to `81/tcp` instead of `80/tcp` (`127.0.0.1:8080->81/tcp`).
- Hypothesis: Mismatched target port in `docker-compose.yml` for Nginx service.
- Command or test: `docker compose ps -a`
- Actual output: `nginx` container exposed `127.0.0.1:8080->81/tcp`.
- Failed attempt and what changed your thinking: .
- Root cause: Incorrect target port binding in `docker-compose.yml` (`8080:81` instead of `8080:80`).
- Fix: Changed Nginx port mapping to `127.0.0.1:${PUBLIC_PORT:-8080}:80` in `docker-compose.yml`.
- Retest evidence: `docker compose ps` confirmed port mapping updated to `127.0.0.1:8080->80/tcp`.
- Related commit: `fix(nginx): update container target port from 81 to 80 in docker-compose`
- Remaining uncertainty: .
## Entry / 2026-09-25 / 04:45
- Symptom: Requests to `http://localhost:8080` still failed with `502 Bad Gateway`.
- Hypothesis: Flask app is bound to loopback `127.0.0.1` inside container, rejecting proxy connections from Nginx network interface.
- Command or test: Checked `APP_HOST` in `docker-compose.yml` and tested container logs.
- Actual output: Nginx failed to connect to `app-01:8080` (connection refused).
- Failed attempt and what changed your thinking: .
- Root cause: `APP_HOST` was configured as `127.0.0.1` instead of `0.0.0.0`, restricting incoming traffic to internal container loopback only.
- Fix: Updated `APP_HOST` to `0.0.0.0` in `docker-compose.yml`.
- Retest evidence: `curl -i http://localhost:8080` returned `HTTP/1.1 200 OK`.
- Related commit: `fix(docker): change APP_HOST binding from 127.0.0.1 to 0.0.0.0`
- Remaining uncertainty: .
## Entry / 2026-09-25 / 05:10
- Symptom: Nginx service was connected to both `frontend` and `backend` networks, violating strict network isolation policies.
- Hypothesis: Nginx does not require direct access to database services (`postgres` and `redis`) on the internal `backend` network.
- Command or test: Inspected `networks` configuration for `nginx` service in `docker-compose.yml`.
- Actual output: `nginx` had `networks: [frontend, backend]`.
- Failed attempt and what changed your thinking: .
- Root cause: Over-privileged network configuration exposing backend database segment to the reverse proxy container.
- Fix: Updated `nginx` service configuration in `docker-compose.yml` to restrict network participation strictly to `networks: [frontend]`.
- Retest evidence: Ran `docker inspect nginx` and verified it is attached solely to the `frontend` bridge network, while application endpoints remained fully operational.
- Related commit: `fix(security): restrict nginx network access solely to frontend network`
- Remaining uncertainty: .
Do not fabricate a failed attempt just to fill the template. Record actual attempts.
