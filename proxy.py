from socket import *
import os
import urllib.parse

# Deklarasi Server IP dan Server Port
server_ip = '0.0.0.0'  # IP Local Host
server_port = 8080  # Port proxy
favicon_url = "png.pngtree.com"  # Domain untuk favicon
favicon_path = "/png-vector/20201223/ourmid/pngtree-outdoor-camping-camping-icon-logo-vector-png-image_2589489.jpg"

# Fungsi untuk mengunduh favicon dari server asal
def download_favicon():
    filename = "favicon.jpg"  # Ganti ekstensi sesuai dengan format gambar
    try:
        with socket(AF_INET, SOCK_STREAM) as c:
            c.connect((favicon_url, 80))
            # Mengirim permintaan untuk mengunduh favicon
            c.sendall(f"GET {favicon_path} HTTP/1.0\r\nHost: {favicon_url}\r\n\r\n".encode())
            # Membaca respons data dan menyimpannya
            response_data = b"".join(iter(lambda: c.recv(4096), b""))
            with open(filename, "wb") as tmpFile:
                tmpFile.write(response_data)
            print("Favicon downloaded and cached.")
    except Exception as e:
        print("Error downloading favicon:", e)

# Unduh favicon.jpg saat server proxy dijalankan jika belum ada
if not os.path.exists("favicon.jpg"):
    download_favicon()

# Membuat file index.html yang berisi gambar favicon.jpg
with open("index.html", "w") as f:
    f.write("""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Web Proxy</title>
</head>
<body>
    <h1>Hello World!</h1>
    <img src="https://png.pngtree.com/png-vector/20201223/ourmid/pngtree-outdoor-camping-camping-icon-logo-vector-png-image_2589489.jpg" alt="Favicon">
</body>
</html>""")

# Set up dan start proxy server socket
tcpSerSock = socket(AF_INET, SOCK_STREAM)
tcpSerSock.bind((server_ip, server_port))
tcpSerSock.listen(5)
print(f'Proxy server is ready to serve at {server_ip} on port {server_port}')

# Memulai Loop tanpa henti untuk menerima koneksi dari klien
while True:
    tcpCliSock, addr = tcpSerSock.accept()
    print('Connection from:', addr)
    
    try:
        # Menerima permintaan HTTP dari klien (maks 1024 Byte) dan mengubahnya menjadi string
        request_data = tcpCliSock.recv(1024).decode()

        # Memastikan data yang diterima tidak kosong
        if not request_data:
            print("No data received from client.")
            tcpCliSock.close()
            continue

        # Memastikan data yang diterima memiliki format yang valid
        request_parts = request_data.split()
        if len(request_parts) < 2:
            print("Invalid HTTP request format.")
            tcpCliSock.close()
            continue

        # Mengambil URL dari permintaan klien
        url = request_parts[1]
        parsed_url = urllib.parse.urlparse(url)
        host = parsed_url.netloc  # Mendapatkan host dari URL
        path = parsed_url.path or '/'  # Mendapatkan path atau default ke /

        # Cek apakah klien mengakses root (localhost:8080)
        if path == "/":
            path = "/index.html"  # Arahkan ke index.html

        # Cek apakah file adalah index.html atau favicon.jpg dan sudah ada di cache
        if path == "/index.html" and os.path.exists("index.html"):
            with open("index.html", "rb") as f:
                tcpCliSock.sendall(b"HTTP/1.0 200 OK\r\nContent-Type:text/html\r\n\r\n")
                tcpCliSock.sendfile(f)
            print("index.html served.")

        elif path == "/favicon.jpg" and os.path.exists("favicon.jpg"):
            with open("favicon.jpg", "rb") as f:
                tcpCliSock.sendall(b"HTTP/1.0 200 OK\r\nContent-Type:image/jpeg\r\n\r\n")
                tcpCliSock.sendfile(f)
            print("favicon.jpg served from cache.")

        else:
            # Jika tidak ada di cache, teruskan permintaan ke server asal
            with socket(AF_INET, SOCK_STREAM) as origin_sock:
                origin_sock.connect((host, 80))  # Menghubungkan ke port 80 server asal
                origin_sock.sendall(f"GET {path} HTTP/1.0\r\nHost: {host}\r\n\r\n".encode())
                
                # Menerima respons dari server asal dan mengirimkannya kembali ke klien
                while True:
                    response_data = origin_sock.recv(4096)
                    if not response_data:
                        break
                    tcpCliSock.sendall(response_data)

    except Exception as e:
        print("Error:", e)
        tcpCliSock.sendall(b"HTTP/1.0 404 Not Found\r\n\r\nFile not found")
    
    finally:
        tcpCliSock.close()

# Menutup koneksi server saat loop berhenti
tcpSerSock.close()