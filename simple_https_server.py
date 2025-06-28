#!/usr/bin/env python3
import http.server
import socketserver
import ssl
import os
import subprocess

# Server configuration
PORT = 8443
DIRECTORY = "."

def create_simple_cert():
    """Create a simple self-signed certificate using openssl"""
    if not (os.path.exists('cert.pem') and os.path.exists('key.pem')):
        print("🔐 Kreiranje SSL sertifikata...")
        try:
            # Create certificate using openssl
            cmd = [
                'openssl', 'req', '-x509', '-newkey', 'rsa:2048',
                '-keyout', 'key.pem', '-out', 'cert.pem',
                '-days', '365', '-nodes',
                '-subj', '/C=RS/ST=Serbia/L=Belgrade/O=EngleskiApp/CN=localhost'
            ]
            result = subprocess.run(cmd, capture_output=True, text=True)
            if result.returncode == 0:
                print("✅ SSL sertifikati uspešno kreirani")
            else:
                print(f"❌ Greška pri kreiranju sertifikata: {result.stderr}")
                return False
        except FileNotFoundError:
            print("❌ OpenSSL nije instaliran. Instalirajte OpenSSL ili koristite HTTP server.")
            return False
    return True

class MyHTTPRequestHandler(http.server.SimpleHTTPRequestHandler):
    def end_headers(self):
        # Add CORS headers
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
    
    # Create certificates
    if not create_simple_cert():
        print("🔄 Pokretanje HTTP servera umesto HTTPS...")
        # Fallback to HTTP server
        httpd = socketserver.TCPServer(("0.0.0.0", 8000), MyHTTPRequestHandler)
        print(f"🚀 HTTP Server pokrenut na http://0.0.0.0:8000")
        print(f"📱 Lokalna mreža: http://192.168.31.214:8000")
        print(f"💻 Lokalno: http://localhost:8000")
    else:
        # Create HTTPS server
        httpd = socketserver.TCPServer(("0.0.0.0", PORT), MyHTTPRequestHandler)
        
        # Wrap with SSL
        context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
        context.load_cert_chain('cert.pem', 'key.pem')
        httpd.socket = context.wrap_socket(httpd.socket, server_side=True)
        
        print(f"🚀 HTTPS Server pokrenut na https://0.0.0.0:{PORT}")
        print(f"📱 Lokalna mreža: https://192.168.31.214:{PORT}")
        print(f"💻 Lokalno: https://localhost:{PORT}")
        print("⚠️  Browser će upozoriti o self-signed sertifikatu")
        print("   Kliknite 'Advanced' -> 'Proceed to localhost (unsafe)'")
    
    print("🛑 Za zaustavljanje pritisnite Ctrl+C")
    
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\n🛑 Server zaustavljen")
        httpd.shutdown() 