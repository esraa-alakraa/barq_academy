<img src="assets/barq-logo.svg" alt="BARQ Systems" width="180">

# BARQ Academy DevOps Assessment - Solution

This repository contains the complete implementation and documentation for the BARQ Academy DevOps Assessment, delivered by **Esraa Alakraa**. 

## Project Overview
This project involves troubleshooting, securing, containerizing, and orchestrating a multi-service web application stack (Flask API, PostgreSQL, Redis, and Nginx) using Docker Compose, alongside implementing an automated CI/CD pipeline and backup/recovery strategies.

---

## Prerequisites
- Linux or WSL2
- Git
- Docker & Docker Compose (with Linux containers support)
- Python 3.10+ (for running local unit tests)

---

## Getting Started & Setup

1. **Clone the Repository:**
   ```bash
   git clone [https://github.com/esraa-alakraa/barq_academy.git](https://github.com/esraa-alakraa/barq_academy.git)
   cd barq_academy

## Configure Environment Variables:
Copy the example environment file and customize it if needed:
cp .env.example .env

## Build and Run Instructions
Build and start the application stack using Docker Compose:

docker compose -p barq-assessment up --build -d

## Verify container status:

docker compose -p barq-assessment ps -a

## Check container logs

docker compose -p barq-assessment logs --no-color

## Testing & Validation
Run Application Unit Tests (App-only):

python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
python -m unittest discover -s tests -v

## Run Environmental Validation Script:

python3 validate.py

## Run Failure/Resilience Tests:

python3 failure_test.py

## Backup and Restore Operations
Create a Database Backup:
./backup.sh
Restore Database from Backup:
./restore.sh

## Stop and Cleanup Safely
To stop the application stack without wiping persistent database volumes:

docker compose -p barq-assessment down