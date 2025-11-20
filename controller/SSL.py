import ssl
import socket
import yaml


with open("config.yaml") as f:
    config = yaml.safe_load(f)

ssl_conf = config["ssl"]
net_conf = config["network"]

context = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)
context.load_cert_chain(certfile=ssl_conf["cert"], keyfile=ssl_conf["key"])
context.load_verify_locations(cafile=ssl_conf["ca_cert"])
context.verify_mode = ssl.CERT_REQUIRED

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.bind((net_conf["host"], net_conf["port"]))
sock.listen(5)

secure_sock = context.wrap_socket(sock, server_side=True)