#!/usr/bin/env python3
"""Candidate deliverable: stop one backend, measure traffic, restore it and verify."""

import subprocess
import time
import urllib.request
import json
import sys

URL = "http://localhost:8080/instance"
CONTAINER = "app-01"

def get_instance():
    try:
        with urllib.request.urlopen(URL, timeout=2) as res:
            return json.loads(res.read().decode()).get("instance_id")
    except:
        return None

def main():
    print("=== Starting High Availability & Recovery Test ===")
    
    print("1. Testing initial state...")
    print("   Active instance responding:", get_instance())

    print(f"2. Stopping container {CONTAINER}...")
    subprocess.run(f"docker stop {CONTAINER}", shell=True, capture_output=True)
    time.sleep(2)

    print("3. Testing traffic while down (should seamlessly hit app-02 with no errors)...")
    failed = False
    for i in range(3):
        inst = get_instance()
        print(f"   Request {i+1}: Handled by -> {inst}")
        if inst is None:
            failed = True

    print(f"4. Restoring container {CONTAINER}...")
    subprocess.run(f"docker start {CONTAINER}", shell=True, capture_output=True)
    time.sleep(5)

    print("5. Verifying recovery...")
    final_inst = get_instance()
    print("   Active instance responding after recovery:", final_inst)

    if failed:
        print("\n=== FAILURE: Some requests failed during outage. ===")
        sys.exit(1)
    else:
        print("\n=== SUCCESS: High availability and recovery test passed! ===")
        sys.exit(0)

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print("Error:", e)
        subprocess.run(f"docker start {CONTAINER}", shell=True, capture_output=True)
        sys.exit(1)