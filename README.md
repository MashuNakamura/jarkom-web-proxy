# jarkom-web-proxy

## For Middle Test Jaringan Komputer

## Nama File : federico
## Path folder : /home/federico/proxy_server/proxy.py

## Cara Bekerja : 

### Pertama Buka terminal untuk menjalankan server dengan "python proxy.py" dan pastikan server udah "Proxy server is ready to serve at 0.0.0.0 on port 8080"

### Kedua akses pada web localhost:8080

### Ketiga Periksa pada terminal apakah cache melakukan Download / Load. Jika Load akan memunculkan "index.html served." yang menunjukkan bahwa file cache telah tersedia pada Client. Jikalau belum ada file cache, maka akan otomatis Download dan memunculkan "Icon Downloaded and Cached" yang menunjukkan akan ada proses Write pada Client.

### Note : Apabila menjalankan di Raspberry, ganti localhost menjadi IP dari Raspberry tersebut.
### Contoh 192.168.5.83:8080 (Jangan melupakan port 8080)

### Maka Web Proxy sudah berjalan dengan Mengirim sebuah Cache ke Client dari Server.

### Apabila ingin mengganti IP dapat mengganti bagian

```py
server_ip = '0.0.0.0'  # IP Local Host
server_port = 8080  # Port proxy
```

## Dokumentasi Demo Code

### Import Library penting untuk membangun sebuah Koneksi Socket
```py
from socket import *
import os
import urllib.parse
```

### Untuk Deklarasi

```py
server_ip = '0.0.0.0'  # IP Local Host
server_port = 8080  # Port Proxy
favicon_url = "png.pngtree.com"  # Domain untuk mengambil Icon
favicon_path = "/png-vector/20201223/ourmid/pngtree-outdoor-camping-camping-icon-logo-vector-png-image_2589489.jpg" # Path Icon
```

### Download Icon

```py
def download_favicon():
    filename = "favicon.jpg"  # Ganti nama sesuai dengan format Icon/Gambar yang diambil
```

### Membuat Koneksi Socket TCP untuk menghubungkan ke favicon_url yang di deklarasi diawal dengan port 80

```py
with socket(AF_INET, SOCK_STREAM) as c:
    c.connect((favicon_url, 80)) # Membuka Koneksi Server
```

### Kirim sebuah Request Download Icon dan menerima data dalam blok 4096 byte hingga semua data diterima (saat recv() mengembalikan nilai kosong).

```py
# Mengirim permintaan untuk mengunduh favicon
c.sendall(f"GET {favicon_path} HTTP/1.0\r\nHost: {favicon_url}\r\n\r\n".encode())
# Membaca respons data dan menyimpannya
response_data = b"".join(iter(lambda: c.recv(4096), b""))
```

### Menyimpan data ke favicon.jpg (Write)

```py
with open(filename, "wb") as tmpFile:
    tmpFile.write(response_data)
```

### Detail

```py
print("Icon Downloaded and Cached.") # Print saat berhasil Di Download
except Exception as e:
    print("Error downloading favicon:", e) # Print saat Gagal saat Download
```

### Memastikan bahwa Icon telah Di Download

```py
if not os.path.exists("favicon.jpg"):
    download_favicon() # Kalau tidak ada, akan menjalankan fungsi Download Icon
```

### Membuat HTML untuk menampilkan Icon + data HTML sebagai contoh Cache

```py
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
```

### Setup untuk memulai Proxy Server

```py
# Set up dan start proxy server socket
tcpSerSock = socket(AF_INET, SOCK_STREAM) # Membuat TCP baru
tcpSerSock.bind((server_ip, server_port)) # Menghubungkan Socket ke IP dan Port yang telah ditentukan
tcpSerSock.listen(5) # Menerima koneksi hingga 5
print(f'Proxy server is ready to serve at {server_ip} on port {server_port}') # Print apabila Server sudah Ready
```

### Loop sampai mendapatkan koneksi dari Client

```py
while True:
    tcpCliSock, addr = tcpSerSock.accept() # Menerima koneksi baru dari Client dan disimpan pada tcpCliSock
    print('Connection from:', addr) # Cetak alamat IP Client yang terkoneksi
```

### Menerima Request dari Client dan convert ke String

```py
request_data = tcpCliSock.recv(1024).decode()
```

### Kalau IP tidak Valid atau IP kosong, maka ulang ke awal loop

```py
if not request_data:
    print("No data received from client.")
    tcpCliSock.close()
    continue
```

### Memastikan data yang diterima itu Valid

```py
request_parts = request_data.split()
if len(request_parts) < 2: # Cek apakah request nya ini berupa GET /index.html HTTP/1.1 -> dihitung 3
    print("Invalid HTTP request format.") # Kalau Part dari Request kurang dari 2, maka print
    tcpCliSock.close() # Lalu Close
    continue # Kembali Loop
```

### Mengekstrak URL dan Path

```py
# Mengambil URL dari permintaan klien
url = request_parts[1] # Ekstrak Url Request
parsed_url = urllib.parse.urlparse(url) # Memecah Url menjadi bagian Terstruktur
host = parsed_url.netloc  # Mendapatkan host dari URL
path = parsed_url.path or '/'  # Mendapatkan path atau default ke /
```

### Cek apakah Client mengakses Proxy

```py
 if path == "/":
    path = "/index.html"  # Kalau mendapatkan path default / maka arahkan ke index.html
```

### Cek apakah cache udah ada pada Client atau belum

```py
if path == "/index.html" and os.path.exists("index.html"): # Cek path yang direquest oleh Client
    with open("index.html", "rb") as f: # Membuka file pada index.html secara read biner (agar tidak ada perubahan format)
        tcpCliSock.sendall(b"HTTP/1.0 200 OK\r\nContent-Type:text/html\r\n\r\n") # Header HTTP bahwa OK
        tcpCliSock.sendfile(f) # Kirim File yang berisi index.html dari cache ke Client
        print("index.html served.") # Print kalau berhasil
```

### Berlaku seperti sebelumnya, namun ini untuk Icon

```py
elif path == "/favicon.jpg" and os.path.exists("favicon.jpg"):
    with open("favicon.jpg", "rb") as f:
    tcpCliSock.sendall(b"HTTP/1.0 200 OK\r\nContent-Type:image/jpeg\r\n\r\n")
    tcpCliSock.sendfile(f)
    print("favicon.jpg served from cache.")
```

### Jika tidak ada cache, maka akan membuat suatu Request

```py
else:
    # Jika tidak ada di cache, teruskan permintaan ke server asal
    with socket(AF_INET, SOCK_STREAM) as origin_sock:
        origin_sock.connect((host, 80))  # Menghubungkan ke port 80 server asal
        origin_sock.sendall(f"GET {path} HTTP/1.0\r\nHost: {host}\r\n\r\n".encode()) # Mengirim Request berupa GET ke path
                
        # Menerima respons dari server asal dan mengirimkannya kembali ke klien
        while True: # Loop hingga True
            response_data = origin_sock.recv(4096) # Menerima data dari server dengan ukuran 4MB
            if not response_data: # Kalau tidak mendapatkan respon akan di break (loop berhenti)
                break
            tcpCliSock.sendall(response_data) # Mengirim data yang diterima server ke client yang melakukan Request
```

### Print apabila Error Program 404 Not Found

```py
except Exception as e:
    print("Error:", e)
    tcpCliSock.sendall(b"HTTP/1.0 404 Not Found\r\n\r\nFile not found")
```

### Menutup setiap melakukan Request

```py
finally:
    tcpCliSock.close()
```

### Menutup Koneksi saat loop berhenti

```py
tcpSerSock.close()
```

# Universitas Katolik Darma Cendika IF 2023