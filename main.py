from kubernetes import client, config
from datetime import datetime, timedelta

config.load_kube_config()

v1 = client.CoreV1Api

while True:
    print("Getting Pods")
    ret = v1.list_pod_for_all_namespaces(watch=False)
    for i in ret.items:
        if i.start_time > (datetime.now() - timedelta(seconds=60)):
            print(f"Deleting Pod {i.metadata.name}")
            v1.delete_namespaced_pod(name=i.metadata.name, namespace=i.metadata.namespace)
