# Mengimport modul socket untuk membuat koneksi jaringan antar server dan client
from socket import *
import os

# Deklarasi Server IP dan Server Port
server_ip = '0.0.0.0'  # IP Local Host
server_port = 8080  # Port proxy
favicon_url = "example.com"  # Ganti dengan domain yang memiliki favicon.ico yang ingin diunduh

# Fungsi untuk mengunduh favicon dari server asal
def download_favicon(hostn):
    filename = "favicon.ico"
    try:
        with socket(AF_INET, SOCK_STREAM) as c:
            c.connect((hostn, 80))
            # Mengirim permintaan untuk mengunduh favicon.ico
            c.sendall(b"GET /favicon.ico HTTP/1.0\r\nHost: %b\r\n\r\n" % hostn.encode())
            # Membaca respons data dan menyimpannya
            response_data = b"".join(iter(lambda: c.recv(4096), b""))
            with open(filename, "wb") as tmpFile:
                tmpFile.write(response_data)
            print("Favicon.ico downloaded and cached.")
    except Exception as e:
        print("Error downloading favicon:", e)

# Unduh favicon.ico saat server proxy dijalankan jika belum ada
if not os.path.exists("favicon.ico"):
    download_favicon(favicon_url)

# Membuat file index.html yang berisi gambar favicon.ico
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
    <img src="https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcS9X34V_1sfElRuZpF--9DuST9YGHVVWb6fqw&s" alt="Example">
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

        # Mengambil nama file dari permintaan klien
        filename = request_parts[1].partition("/")[2] or "index.html"

        # Cek apakah file adalah index.html atau favicon.ico dan sudah ada di cache
        if filename == "index.html" and os.path.exists("index.html"):
            with open("index.html", "rb") as f:
                tcpCliSock.sendall(b"HTTP/1.0 200 OK\r\nContent-Type:text/html\r\n\r\n")
                tcpCliSock.sendfile(f)
            print("index.html served.")

        elif filename == "favicon.ico" and os.path.exists("favicon.ico"):
            with open("favicon.ico", "rb") as f:
                tcpCliSock.sendall(b"HTTP/1.0 200 OK\r\nContent-Type:image/x-icon\r\n\r\n")
                tcpCliSock.sendfile(f)
            print("favicon.ico served from cache.")

    # Pesan keluar jika ada kesalahan
    except Exception as e:
        print("Error:", e)
        tcpCliSock.sendall(b"HTTP/1.0 404 Not Found\r\n\r\nFile not found")
    
    # Menutup koneksi klien
    finally:
        tcpCliSock.close()

# Menutup koneksi server saat loop berhenti
tcpSerSock.close()