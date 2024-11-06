# Mengimport modul socket untuk membuat sebuah koneksi jaringan antar server dan client
from socket import *

# Mendeklarasi Server IP dan Server_Port
server_ip = '0.0.0.0'  # IP Local Host
server_port = 8080  # Port proxy

# Set up dan start proxy server socket
tcpSerSock = socket(AF_INET, SOCK_STREAM)  # membuat Socket tcpSerSock dengan protokol IPv4 (AF_INET) dan TCP (SOCK_STREAM)
tcpSerSock.bind((server_ip, server_port))  # Menghubungkan ip socket ke server_ip dan server_port
tcpSerSock.listen(5)  # menerima antrean dengan maksimal 5 antrean
print(f'Proxy server is ready to serve at {server_ip} on port {server_port}')  # Menampilkan apabila Proxy tersedia

while True:  # Memulai Loop tanpa stop untuk menerima koneksi dari klien
    tcpCliSock, addr = tcpSerSock.accept()  # Ketika Client terhubung, maka mengembalikkan tcpCliSock dan addr
    print('Connection from:', addr)  # Menampilkan client yang terhubung

    try:
        # Menerima permintaan HTTP dari Klien (Maksimal 1024 Byte) dan convert ke String
        request_data = tcpCliSock.recv(1024).decode()

        # Memastikan data yang diterima tidak kosong (Memastikan ada pengguna)
        if not request_data:
            print("No data received from client.")
            tcpCliSock.close() # Akan di close dan dimulai ulang sampai ketemu data dari pengguna
            continue  # Lanjutkan ke iterasi berikutnya (kembali ke awal loop)

        # Memastikan data yang diterima memiliki format yang valid
        request_parts = request_data.split() # split digunakan untuk memisahkan berdasarkan spasi
        if len(request_parts) < 2: # cek kalau path dari split kurang dari dua
            print("Invalid HTTP request format.") # kalau kurang print ini
            tcpCliSock.close() # menutup koneksi klient
            continue  # Lanjutkan ke iterasi berikutnya (kembali ke awal loop)

        # Mengambil filename dari permintaan (cache)
        filename = request_parts[1].partition("/")[2]

        # Jika tidak ada filename setelah '/', atur ke 'index.html'
        if not filename:
            filename = "index.html"  # Ganti dengan halaman default (misalnya index.html)

        # Cek kalau udah ada Cache
        try:
            # Mengecek cache apakah sudah ada file secara read-binary
            with open(filename, "rb") as f:
                tcpCliSock.sendall(b"HTTP/1.0 200 OK\r\nContent-Type:text/html\r\n\r\n")
                # Jika ditemukan, mengirim file header kalau filenya ada dan konten nya berupa text/html
                tcpCliSock.sendfile(f)
                # Setelah konten ada, akan dikirim ke client
            print('Cache loaded')
            # Menampilkan pesan apabila cache atau file telah ditemukan

        # Cek kalau belum ada cache
        except IOError:
            # Apabila tidak ada file pada cache, akan terus meneruskan permintaan ke server asal
            hostn = filename.replace("www.", "", 1)
            # Menghilangkan www dari file agar dapat terhubung ke server yang benar
            with socket(AF_INET, SOCK_STREAM) as c:
                # Membuat socket baru bernama c
                c.connect((hostn, 80))
                c.sendall(f"GET /{filename} HTTP/1.0\r\nHost: {hostn}\r\n\r\n".encode())
                # Mengirimkan permintaan HTTP ke server asal untuk meminta file
                
                # Setelah dikirim, maka cache file akan diterima data dari server asal dalam potongan 4096 byte.
                response_data = b"".join(iter(lambda: c.recv(4096), b""))
                # Membuka file write binary yang memungkinkan menyimpan data biner seperti HTML, Gambar atau lainnya.
                with open(filename, "wb") as tmpFile:
                    # Menulis semua data yang telah diterima oleh response_data
                    tmpFile.write(response_data)
                
                # Mengirimkan Data yang sama ke Klien
                tcpCliSock.sendall(response_data)
                # Print apabila data berhasil didapatkan dari server dan disimpan pada cache
                print("Data Downloaded and saved as cache.")

    # Pesan keluar apabila ada kesalahan
    except Exception as e:
        print("Error:", e)
        tcpCliSock.sendall(b"HTTP/1.0 404 Not Found\r\n\r\nFile not found")

    # Menutup koneksi klien
    finally:
        tcpCliSock.close()

# Menutup koneksi klien saat while Loop berhenti
tcpSerSock.close()