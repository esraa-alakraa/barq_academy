#!/usr/bin/env python3
"""Candidate deliverable: implement environment validation; PASS/FAIL checks."""

import sys
import urllib.request

BASE_URL = "http://localhost:8080"
endpoints = ["/", "/health", "/ready", "/instance", "/counter"]

def main():
    print("=== Starting Environment Validation ===")
    success = True

    for path in endpoints:
        url = BASE_URL + path
        try:
            with urllib.request.urlopen(url, timeout=3) as res:
                if res.status == 200:
                    print(f"[PASS] {path} returned 200 OK")
                else:
                    print(f"[FAIL] {path} returned status {res.status}")
                    success = False
        except Exception as e:
            print(f"[FAIL] {path} error: {e}")
            success = False

    if success:
        print("\n=== SUCCESS: All checks passed! ===")
        sys.exit(0)
    else:
        print("\n=== FAILURE: Some checks failed. ===")
        sys.exit(1)

if __name__ == "__main__":
    main()
