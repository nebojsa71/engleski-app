#!/usr/bin/env python3
import http.server
import socketserver
import ssl
import os
import subprocess
import sys

# Server configuration
PORT = 8443
DIRECTORY = "."
CERT = 'cert.pem'
KEY = 'key.pem'

def generate_certificates():
    """Generate SSL certificates if they don't exist"""
    if not (os.path.exists(CERT) and os.path.exists(KEY)):
        print('❗ Nema sertifikata! Pokreni sledeću komandu u terminalu:')
        print('openssl req -x509 -newkey rsa:2048 -keyout key.pem -out cert.pem -days 365 -nodes -subj "/C=RS/ST=Serbia/L=Belgrade/O=EngleskiApp/CN=localhost"')
        exit(1)

def create_simple_certificates():
    """Create simple self-signed certificates using Python"""
    from cryptography import x509
    from cryptography.x509.oid import NameOID
    from cryptography.hazmat.primitives import hashes, serialization
    from cryptography.hazmat.primitives.asymmetric import rsa
    from datetime import datetime, timedelta
    
    # Generate private key
    private_key = rsa.generate_private_key(
        public_exponent=65537,
        key_size=2048,
    )
    
    # Create certificate
    subject = issuer = x509.Name([
        x509.NameAttribute(NameOID.COUNTRY_NAME, "RS"),
        x509.NameAttribute(NameOID.STATE_OR_PROVINCE_NAME, "Serbia"),
        x509.NameAttribute(NameOID.LOCALITY_NAME, "Belgrade"),
        x509.NameAttribute(NameOID.ORGANIZATION_NAME, "EngleskiApp"),
        x509.NameAttribute(NameOID.COMMON_NAME, "localhost"),
    ])
    
    cert = x509.CertificateBuilder().subject_name(
        subject
    ).issuer_name(
        issuer
    ).public_key(
        private_key.public_key()
    ).serial_number(
        x509.random_serial_number()
    ).not_valid_before(
        datetime.utcnow()
    ).not_valid_after(
        datetime.utcnow() + timedelta(days=365)
    ).add_extension(
        x509.SubjectAlternativeName([
            x509.DNSName("localhost"),
            x509.IPAddress("127.0.0.1"),
        ]),
        critical=False,
    ).sign(private_key, hashes.SHA256())
    
    # Write certificates to files
    with open(CERT, "wb") as f:
        f.write(cert.public_bytes(serialization.Encoding.PEM))
    
    with open(KEY, "wb") as f:
        f.write(private_key.private_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PrivateFormat.PKCS8,
            encryption_algorithm=serialization.NoEncryption()
        ))
    
    print("✅ SSL sertifikati kreirani pomoću Python-a")

class MyHTTPRequestHandler(http.server.SimpleHTTPRequestHandler):
    def end_headers(self):
        # Add CORS headers for better compatibility
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        super().end_headers()

    def do_OPTIONS(self):
        self.send_response(200)
        self.end_headers()

if __name__ == "__main__":
    # Change to the directory containing the files
    os.chdir(DIRECTORY)
    
    # Generate certificates if needed
    generate_certificates()
    
    # Create HTTP server
    httpd = socketserver.TCPServer(('0.0.0.0', PORT), MyHTTPRequestHandler)
    
    # Wrap with SSL
    httpd.socket = ssl.wrap_socket(httpd.socket, keyfile=KEY, certfile=CERT, server_side=True)
    
    print(f"🚀 HTTPS Server pokrenut na https://0.0.0.0:{PORT}")
    print(f"📱 Lokalna mreža: https://192.168.31.214:{PORT}")
    print(f"💻 Lokalno: https://localhost:{PORT}")
    print("⚠️  Browser će upozoriti o self-signed sertifikatu - kliknite 'Advanced' -> 'Proceed'")
    print("🛑 Za zaustavljanje pritisnite Ctrl+C")
    
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\n🛑 Server zaustavljen")
        httpd.shutdown() 