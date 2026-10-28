# Injection Challenge Lab

Lab CTF kategori Web Exploitation (Command Injection & SSTI).

---

## 🚀 Cara Menjalankan Lab

Tersedia beberapa cara untuk menjalankan lab ini. Sangat disarankan menggunakan **Docker** atau **Docker Compose** agar lingkungan terisolasi dengan aman.

### Opsi 1: Menggunakan Docker Compose (Paling Mudah)
1. Jalankan container:
   ```bash
   docker compose up -d --build
   ```
2. Akses aplikasi melalui browser:
   ```
   http://localhost:5001
   ```
   *(Ganti `localhost` dengan IP VPS/server jika dihosting secara remote)*
3. Untuk menghentikan container:
   ```bash
   docker compose down
   ```

---

### Opsi 2: Menggunakan Docker CLI Biasa
1. Build image Docker:
   ```bash
   docker build -t injection-challenge .
   ```
2. Jalankan container:
   ```bash
   docker run -d --name injection_challenge -p 5001:5001 injection-challenge
   ```
3. Untuk menghentikan & menghapus container:
   ```bash
   docker stop injection_challenge && docker rm injection_challenge
   ```

---

### Opsi 3: Menjalankan Langsung dengan Python (Lokal / Tanpa Docker)
> **Catatan:** Jalankan di environment terisolasi karena lab ini rentan terhadap Command Execution.

1. Install dependensi:
   ```bash
   pip install flask
   ```
   *(Pastikan tool `ping` terinstall di OS)*
2. Taruh `flag.txt` di root `/flag.txt` (atau sesuaikan dengan kebutuhan):
   ```bash
   sudo cp flag.txt /flag.txt
   ```
3. Jalankan server:
   ```bash
   python3 app.py
   ```

---

## 🚩 Konfigurasi Flag
Isi file `flag.txt` sebelum mem-build image Docker jika ingin mengganti flag:
```
NCS{1nj3K_1nj3K_4j4}
```
Jika sudah terlanjur berjalan di Docker, flag dapat diubah via:
```bash
docker exec -it injection_challenge sh -c "echo 'FLAG_BARU_DISINI' > /flag.txt"
```

