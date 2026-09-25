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

Do not fabricate a failed attempt just to fill the template. Record actual attempts.
