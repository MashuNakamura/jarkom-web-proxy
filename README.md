# jarkom-web-proxy

## For Middle Test Jaringan Komputer

## Nama File : federico
## Path folder : /home/federico/proxy_server/proxy.py

### Note : Dokumentasi sudah lengkap dibagian comment code proxy.py

## Cara Bekerja : 

### Pertama Buka terminal untuk menjalankan server dengan "python proxy.py" dan pastikan server udah "Proxy server is ready to serve at 0.0.0.0 on port 8080"

### Kedua akses pada web localhost:8080

### Ketiga Periksa pada terminal apakah cache sudah berhasil, jika iya maka akan print "Cache loaded and sent to client."

### Note : Apabila menjalankan di Raspberry, ganti localhost menjadi IP dari Raspberry tersebut.
### Contoh 192.168.5.83:8080 (Jangan melupakan port 8080)

### Maka Web Proxy sudah berjalan dengan Mengirim sebuah Cache ke Client dari Server.

### Apabila ingin mengganti IP dapat mengganti bagian


# Universitas Katolik Darma Cendika IF 2023

```py
server_ip = '0.0.0.0'  # IP Local Host
server_port = 8080  # Port proxy
```