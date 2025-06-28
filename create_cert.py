#!/usr/bin/env python3
"""
Script za kreiranje SSL sertifikata bez OpenSSL-a
"""
import os
import ssl
import tempfile
import subprocess
import ipaddress
import socket
import sys

def get_local_ip():
    """Get local IP address"""
    try:
        # Connect to a remote address to determine local IP
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        local_ip = s.getsockname()[0]
        s.close()
        return local_ip
    except:
        return "127.0.0.1"

def create_certificates():
    """Create SSL certificates for local development"""
    print("🔐 Kreiranje SSL sertifikata...")
    
    # Get local IP
    local_ip = get_local_ip()
    print(f"📡 Lokalna IP adresa: {local_ip}")
    
    # Check if OpenSSL is available
    try:
        subprocess.run(['openssl', 'version'], capture_output=True, check=True)
        print("📝 Koristim OpenSSL...")
        
        # Create certificate with local IP
        cmd = [
            'openssl', 'req', '-x509', '-newkey', 'rsa:2048',
            '-keyout', 'key.pem', '-out', 'cert.pem',
            '-days', '365', '-nodes',
            '-subj', f'/C=RS/ST=Serbia/L=Belgrade/O=EngleskiApp/CN=localhost',
            '-addext', f'subjectAltName=DNS:localhost,DNS:127.0.0.1,IP:{local_ip}'
        ]
        
        subprocess.run(cmd, check=True)
        print("✅ SSL sertifikati kreirani pomoću OpenSSL")
        
    except (subprocess.CalledProcessError, FileNotFoundError):
        print("📝 OpenSSL nije dostupan. Kreiranje sertifikata pomoću Python-a...")
        create_simple_certificates(local_ip)

def create_simple_certificates(local_ip):
    """Create simple self-signed certificates using Python"""
    try:
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
                x509.IPAddress(ipaddress.IPv4Address("127.0.0.1")),
                x509.IPAddress(ipaddress.IPv4Address(local_ip)),
            ]),
            critical=False,
        ).sign(private_key, hashes.SHA256())
        
        # Write certificates to files
        with open('cert.pem', "wb") as f:
            f.write(cert.public_bytes(serialization.Encoding.PEM))
        
        with open('key.pem', "wb") as f:
            f.write(private_key.private_bytes(
                encoding=serialization.Encoding.PEM,
                format=serialization.PrivateFormat.PKCS8,
                encryption_algorithm=serialization.NoEncryption()
            ))
        
        print("✅ SSL sertifikati kreirani pomoću Python-a")
        
    except ImportError:
        print("❌ Greška: Potrebna je 'cryptography' biblioteka")
        print("Instaliraj sa: pip install cryptography")
        sys.exit(1)

if __name__ == "__main__":
    create_certificates()
    
    print("\n🎉 Sertifikati su kreirani!")
    print("📁 cert.pem - javni sertifikat")
    print("📁 key.pem - privatni ključ")
    print("\n🚀 Sada možeš pokrenuti HTTPS server sa:")
    print("   python https_server.py")
    print("\n🌐 Pristup:")
    print(f"   Lokalno: https://localhost:8443")
    print(f"   Mreža: https://{get_local_ip()}:8443")
    print("\n⚠️  Napomena: Browser će i dalje upozoriti na self-signed sertifikat")
    print("   Za PWA instalaciju, koristi localhost ili dodaj sertifikat u browser") 