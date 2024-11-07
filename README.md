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

# Universitas Katolik Darma Cendika IF 2023