#!/usr/bin/env python3
"""
MDEC Virtual NOC - Deployment Verifier
"Trust, but Verify"
"""
import requests
import socket
import sys
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

def create_session():
    session = requests.Session()
    retries = Retry(total=3, backoff_factor=0.5, status_forcelist=[500, 502, 503, 504])
    session.mount('http://', HTTPAdapter(max_retries=retries))
    return session

def check_local_service(port=3000, name="MDEC-Consortium"):
    print(f"[*] NOC CHECK: Verifying {name} on Port {port}...")
    url = f"http://localhost:{port}/"
    
    try:
        # Check 1: Socket Binding
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            if s.connect_ex(('localhost', port)) != 0:
                print(f"[-] CRITICAL: Port {port} is CLOSED.")
                return False
        
        # Check 2: HTTP Status
        session = create_session()
        response = session.get(url, timeout=2)
        
        if response.status_code == 200:
            print(f"[+] SUCCESS: {name} is responding (200 OK).")
            print(f"    Title: {response.text.split('<title>')[1].split('</title>')[0] if '<title>' in response.text else 'No Title'}")
            return True
        elif response.status_code == 403:
            print(f"[-] PERMISSION DENIED (403): Service is blocking access (Check traversal rules).")
            return False
        else:
            print(f"[-] WARNING: Service returned status {response.status_code}.")
            return False

    except Exception as e:
        print(f"[-] ERROR: Connectivity check failed: {e}")
        return False

def main():
    print("=== VIRTUAL NOC ENGINEER REPORT ===")
    print("target: local_deployment_zone")
    print("-----------------------------------")
    
    mdec_status = check_local_service(3000, "MDEC Documentation Portal")
    
    if mdec_status:
        print("\n[+] VALIDATION COMPLETE: Deployment is Stable.")
        sys.exit(0)
    else:
        print("\n[-] VALIDATION FAILED: Deployment requires attention.")
        sys.exit(1)

if __name__ == "__main__":
    main()
