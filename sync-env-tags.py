#!/usr/bin/env python3
import re

container_name = None

with open("docker-compose.yml", "r") as f:
    lines = f.readlines()

with open(".env", "r") as f:
    env_content = f.read()

for line in lines:
    cn_match = re.match(r"^\s*container_name:\s*(.+)", line)
    if cn_match:
        container_name = cn_match.group(1).strip()
        continue

    img_match = re.match(r"^\s*image:\s*[^:]+:([^@]+@sha256:[a-f0-9]+)", line)
    if img_match and container_name:
        value = img_match.group(1)
        env_var = f"{container_name.upper()}_TAG"
        replacement = f"{env_var}={value}"

        if re.search(rf"^{env_var}=", env_content, re.MULTILINE):
            env_content = re.sub(rf"^{env_var}=.*", replacement, env_content, flags=re.MULTILINE)
        else:
            env_content += f"\n{replacement}"

        container_name = None

with open(".env", "w") as f:
    f.write(env_content)
