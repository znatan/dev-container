from kubernetes import client, config
import sys
from datetime import datetime
import time

def main():
    try:
        # Load in-cluster config when running inside pod
        config.load_incluster_config()
    except config.ConfigException:
        # Fall back to kubeconfig for local development
        config.load_kube_config()

    # Create API client
    v1 = client.CoreV1Api()

    while True:  # Continuous monitoring
        try:
            timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            sys.stdout.write(f"\n[{timestamp}] Starting Pod Status Report\n")
            sys.stdout.write("=====================================\n")
            sys.stdout.flush()

            pods = v1.list_pod_for_all_namespaces()
            
            for pod in pods.items:
                sys.stdout.write(f"\nNamespace: {pod.metadata.namespace}\n")
                sys.stdout.write(f"Pod Name: {pod.metadata.name}\n")
                sys.stdout.write(f"Status: {pod.status.phase}\n")
                sys.stdout.write(f"Node: {pod.spec.node_name}\n")
                sys.stdout.write(f"IP: {pod.status.pod_ip}\n")
                sys.stdout.write("-------------------------------------\n")
                sys.stdout.flush()

        except Exception as e:
            sys.stdout.write(f"\nError: {str(e)}\n")
            sys.stdout.flush()
            
        time.sleep(10)  # Update every 10 seconds

if __name__ == "__main__":
    main()