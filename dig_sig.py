from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import ec
from cryptography.hazmat.primitives import serialization
'''
private_key = ec.generate_private_key(ec.SECP256R1())
public_key = private_key.public_key()

with open("private_key.pem", "wb") as f:
    f.write(private_key.private_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PrivateFormat.PKCS8,
        encryption_algorithm=serialization.NoEncryption()
    ))
with open("public_key.pem", "wb") as f:
    f.write(public_key.public_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PublicFormat.SubjectPublicKeyInfo
    ))
'''
'''
with open("private_key.pem", "rb") as f:
    pem_data = f.read()
private_key = serialization.load_pem_private_key(pem_data, password=None)

file_path="./test/sudoku_solver.py"

with open(file_path, "rb") as f:
    message = f.read()

signature = private_key.sign(
    message,
    ec.ECDSA(hashes.SHA256())
)

with open("signature.sig", "wb") as f:
    f.write(signature)


'''
file_path="./test/sudoku_solver.py"
with open(file_path, "rb") as f:
    message = f.read()

with open("public_key.pem", "rb") as f:
    pem_data = f.read()
public_key = serialization.load_pem_public_key(pem_data)

with open("signature.sig", "rb") as f:
    signature = f.read()

try:
    public_key.verify(
        signature,
        message,
        ec.ECDSA(hashes.SHA256())
    )
    print("Signature is valid.")
except:
    print("Signature is invalid.")
