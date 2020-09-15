import os
import time
import logging

from kubernetes import client, config
from datetime import datetime, timedelta
from kubernetes.client.rest import ApiException

config.load_incluster_config()
logging.basicConfig(level=logging.INFO)
v1 = client.CoreV1Api()
pod_age = os.environ.get("POD_AGE", "5")
deployment_name = os.environ.get("DEPLOYMENT_NAME", "kube-prometheas")
while True:
    logging.debug("Getting Pods")
    ret = v1.list_pod_for_all_namespaces(watch=False)
    for i in ret.items:
        logging.debug(f"pod_name: {i.metadata.name}")
        logging.debug(f"startsWith {deployment_name}: {i.metadata.name.startswith(deployment_name)}")
        if not i.metadata.name.startswith(deployment_name):
            logging.debug(f"timestamp delta: { (datetime.now() - timedelta(seconds=int(pod_age))).timestamp() - i.metadata.creation_timestamp.timestamp()}")
            if datetime.utcnow().timestamp() - i.metadata.creation_timestamp.timestamp() > float(pod_age):
                logging.info(f"Deleting Pod {i.metadata.name}")
                try:
                    v1.delete_namespaced_pod(i.metadata.name, i.metadata.namespace)
                except ApiException:
                    logging.error(f"Pod not found: {i.metadata.name} :: {i.metadata.namespace}")
    time.sleep(2)
