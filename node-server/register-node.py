import requests
import os
import stat

API_URL = "https://192.168.189.8/register"
TOKEN = "ABCD1234"

CERT_BASE = "./certs"
CA_DIR = os.path.join(CERT_BASE, "ca")
NODE_DIR = os.path.join(CERT_BASE, "node")


def ensure_dirs():
    os.makedirs(CA_DIR, exist_ok=True)
    os.makedirs(NODE_DIR, exist_ok=True)


def write_secure_file(path, data):
    """Write a file with chmod 600 permissions."""
    with open(path, "w") as f:
        f.write(data)
    os.chmod(path, stat.S_IRUSR | stat.S_IWUSR)


def register_node():
    ensure_dirs()

    payload = {
        "token": TOKEN,
        "hostname": os.uname().nodename,
        "platform": os.uname().sysname,
        "architecture": os.uname().machine,
    }

    try:
        response = requests.post(API_URL, json=payload, timeout=10)
        response.raise_for_status()
        data = response.json()
    except Exception as e:
        print("[!] Failed to contact controller:", e)
        return False

    required = {"node_crt", "node_key", "ca_crt"}
    if not required.issubset(data):
        print("[!] Controller response missing fields")
        return False

    # Save the files to the new structure
    write_secure_file(os.path.join(NODE_DIR, "node.crt"), data["node_crt"])
    write_secure_file(os.path.join(NODE_DIR, "node.key"), data["node_key"])
    write_secure_file(os.path.join(CA_DIR, "ca.crt"), data["ca_crt"])

    print("[✓] Registration successful")
    print("[✓] Certificates saved in certs/ca and certs/node")
    return True


if __name__ == "__main__":
    register_node()
