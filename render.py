import os
import subprocess
import sys

import yaml

if len(sys.argv) != 2 or sys.argv[1] not in ("dev", "prod"):
    print("Usage: python render.py <dev|prod>")
    sys.exit(1)

env_name = sys.argv[1]

with open("k8s/config.yaml") as f:
    config = yaml.safe_load(f)

env = config["environments"][env_name]

subprocess.run(["kubectl", "config", "use-context", env["cluster"]], check=True)
print(f"Switched kubectl context to '{env['cluster']}'")

with open("k8s/app-deployment.yaml") as f:
    template = f.read()

rendered = (
    template
    .replace("{{ENVIRONMENT}}", env_name)
    .replace("++REPLICAS++", str(env["replicas"]))
    .replace("++CPU_REQUEST++", env["cpu_request"])
    .replace("++MEMORY_REQUEST++", env["memory_request"])
)

os.makedirs("k8s/rendered", exist_ok=True)
output_path = "k8s/rendered/app-deployment.yaml"
with open(output_path, "w") as f:
    f.write(rendered)

print(f"Rendered {output_path} for environment '{env_name}'")
print(f"Now run: kubectl apply -f {output_path}")
