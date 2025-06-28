const https = require('https');
const http = require('http');
const fs = require('fs');
const path = require('path');
const { execSync } = require('child_process');

const PORT = 8443;
const HTTP_PORT = 8000;

// Function to create self-signed certificate
function createCertificate() {
    if (!fs.existsSync('cert.pem') || !fs.existsSync('key.pem')) {
        console.log('🔐 Kreiranje SSL sertifikata...');
        try {
            // Create certificate using openssl
            const cmd = `openssl req -x509 -newkey rsa:2048 -keyout key.pem -out cert.pem -days 365 -nodes -subj "/C=RS/ST=Serbia/L=Belgrade/O=EngleskiApp/CN=localhost"`;
            execSync(cmd, { stdio: 'pipe' });
            console.log('✅ SSL sertifikati uspešno kreirani');
            return true;
        } catch (error) {
            console.log('❌ OpenSSL nije dostupan. Pokretanje HTTP servera...');
            return false;
        }
    }
    return true;
}

// Function to get MIME type
function getMimeType(filePath) {
    const ext = path.extname(filePath).toLowerCase();
    const mimeTypes = {
        '.html': 'text/html',
        '.js': 'application/javascript',
        '.css': 'text/css',
        '.json': 'application/json',
        '.png': 'image/png',
        '.jpg': 'image/jpeg',
        '.jpeg': 'image/jpeg',
        '.gif': 'image/gif',
        '.svg': 'image/svg+xml',
        '.ico': 'image/x-icon'
    };
    return mimeTypes[ext] || 'application/octet-stream';
}

// Function to serve files
function serveFile(req, res) {
    let filePath = '.' + req.url;
    
    // Default to index.html
    if (filePath === './') {
        filePath = './index.html';
    }
    
    // Remove query parameters
    filePath = filePath.split('?')[0];
    
    fs.readFile(filePath, (err, data) => {
        if (err) {
            res.writeHead(404, { 'Content-Type': 'text/html' });
            res.end('<h1>404 - File Not Found</h1>');
            return;
        }
        
        const mimeType = getMimeType(filePath);
        res.writeHead(200, { 
            'Content-Type': mimeType,
            'Access-Control-Allow-Origin': '*',
            'Access-Control-Allow-Methods': 'GET, POST, OPTIONS',
            'Access-Control-Allow-Headers': 'Content-Type'
        });
        res.end(data);
    });
}

// Create server
if (createCertificate()) {
    // HTTPS Server
    const options = {
        key: fs.readFileSync('key.pem'),
        cert: fs.readFileSync('cert.pem')
    };
    
    const server = https.createServer(options, (req, res) => {
        serveFile(req, res);
    });
    
    server.listen(PORT, '0.0.0.0', () => {
        console.log(`🚀 HTTPS Server pokrenut na https://0.0.0.0:${PORT}`);
        console.log(`📱 Lokalna mreža: https://192.168.31.214:${PORT}`);
        console.log(`💻 Lokalno: https://localhost:${PORT}`);
        console.log('⚠️  Browser će upozoriti o self-signed sertifikatu');
        console.log('   Kliknite "Advanced" -> "Proceed to localhost (unsafe)"');
        console.log('🛑 Za zaustavljanje pritisnite Ctrl+C');
    });
} else {
    // HTTP Server (fallback)
    const server = http.createServer((req, res) => {
        serveFile(req, res);
    });
    
    server.listen(HTTP_PORT, '0.0.0.0', () => {
        console.log(`🚀 HTTP Server pokrenut na http://0.0.0.0:${HTTP_PORT}`);
        console.log(`📱 Lokalna mreža: http://192.168.31.214:${HTTP_PORT}`);
        console.log(`💻 Lokalno: http://localhost:${HTTP_PORT}`);
        console.log('🛑 Za zaustavljanje pritisnite Ctrl+C');
    });
} 