from cryptography import x509
from cryptography.x509.oid import NameOID
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives import serialization, hashes

def generate_node_cert(common_name, ca_key, ca_cert):
    # 1. Generate private key
    key = rsa.generate_private_key(public_exponent=65537, key_size=2048)

    # 2. Build CSR
    csr = x509.CertificateSigningRequestBuilder().subject_name(x509.Name([
        x509.NameAttribute(NameOID.COMMON_NAME, common_name),
    ])).sign(key, hashes.SHA256())

    # 3. Sign certificate with CA
    cert = (
        x509.CertificateBuilder()
        .subject_name(csr.subject)
        .issuer_name(ca_cert.subject)
        .public_key(csr.public_key())
        .serial_number(x509.random_serial_number())
        .not_valid_before(...)
        .not_valid_after(...)
        .sign(ca_key, hashes.SHA256())
    )

    return key, cert
