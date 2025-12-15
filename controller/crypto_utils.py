from cryptography import x509
from cryptography.x509.oid import NameOID
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import rsa
import datetime


def generate_cert_and_key(common_name: str):
    # 1. Generate private key
    key = rsa.generate_private_key(
        public_exponent=65537,
        key_size=2048
    )

    # 2. Load CA key and cert
    with open("./certs/ca/ca.key", "rb") as f:
        ca_key = serialization.load_pem_private_key(f.read(), password=None)

    with open("./certs/ca/ca.crt", "rb") as f:
        ca_cert = x509.load_pem_x509_certificate(f.read())

    # 3. Build certificate request
    subject = x509.Name([
        x509.NameAttribute(NameOID.COMMON_NAME, common_name),
    ])

    cert = (
        x509.CertificateBuilder()
        .subject_name(subject)
        .issuer_name(ca_cert.subject)
        .public_key(key.public_key())
        .serial_number(x509.random_serial_number())
        .not_valid_before(datetime.datetime.utcnow())
        .not_valid_after(
            datetime.datetime.utcnow() + datetime.timedelta(days=365)
        )
        .sign(private_key=ca_key, algorithm=hashes.SHA256())
    )

    # 4. Serialize to PEM
    pem_cert = cert.public_bytes(serialization.Encoding.PEM).decode()
    pem_key = key.private_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PrivateFormat.TraditionalOpenSSL,
        encryption_algorithm=serialization.NoEncryption(),
    ).decode()

    print(pem_cert, pem_key)

    return pem_cert, pem_key
