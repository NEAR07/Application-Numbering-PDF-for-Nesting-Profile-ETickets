# Deskripsi Program
Program ini adalah aplikasi desktop yang ditulis dalam Python menggunakan PyQt5 untuk antarmuka pengguna dan PyPDF2 serta ReportLab untuk manipulasi PDF. Aplikasi ini dirancang untuk menambahkan nomor blok dan nomor lembar ke dalam file PDF yang berisi etiket profil nesting. Pengguna dapat mengunggah file PDF, memilih ukuran kertas, dan memasukkan nomor blok serta nomor lembar untuk setiap halaman. Setelah semua data dimasukkan, aplikasi akan memproses PDF dan menyimpan hasilnya sebagai file PDF baru dengan informasi yang ditambahkan. Program ini sangat berguna bagi para insinyur dan perancang yang bekerja dengan dokumen teknis dan memerlukan cara yang efisien untuk menambahkan informasi ke dalam PDF.

# Tutorial Cara Menjalankan Program dan Deploy
### Persyaratan
Sebelum menjalankan program, pastikan telah menginstal Python dan pustaka yang diperlukan.

### Instalasi Pustaka yang Diperlukan
- Buka terminal atau command prompt.
- Jalankan perintah berikut untuk menginstal pustaka yang diperlukan:
```console
pip install PyPDF2 reportlab PyQt5 fitz
```

### Menyimpan Kode Program
- Salin kode program di atas.
- Buka editor teks (seperti Notepad, VSCode, atau PyCharm) dan tempelkan kode tersebut.
- Simpan file dengan nama pdf_numbering_app.py.

### Menjalankan Program
- Buka terminal atau command prompt.
- Arahkan ke direktori tempat menyimpan file pdf_numbering_app.py menggunakan perintah cd. Contoh:
```console
cd path\to\your\directory
```
- Jalankan program dengan perintah:
```console
python pdf_numbering_app.py
```

### Menggunakan Aplikasi
- Setelah program dijalankan, jendela aplikasi akan muncul.
- Klik tombol "Upload PDF" untuk memilih file PDF yang ingin di tambahkan nomor blok dan nomor lembar.
- Pilih ukuran kertas dari dropdown.
- Masukkan nomor blok dan nomor lembar untuk setiap halaman yang ditampilkan.
- Gunakan tombol "Next Page" dan "Previous Page" untuk navigasi antar halaman.
- Setelah semua data dimasukkan, klik tombol "Finish" untuk memproses PDF dan menyimpan hasilnya.
- Pilih lokasi dan nama file untuk menyimpan file PDF yang dihasilkan.
- Setelah proses selesai, aplikasi akan menampilkan pesan konfirmasi dengan lokasi file yang telah disimpan.

### Men-deploy Aplikasi
Jika ingin mendistribusikan aplikasi ini kepada pengguna lain, Dapat menggunakan alat seperti PyInstaller untuk mengonversi skrip Python menjadi file executable (.exe).

- Instal PyInstaller:
```console
pip install pyinstaller
```
- Jalankan perintah berikut untuk membuat executable:
```console
python -m PyInstaller --onefile --windowed --add-data "C:\\Windows\\Fonts\\verdana.ttf;." NumberingPDF_Eticket_NestProf.py
```
Setelah proses selesai, Maka akan menemukan file executable di dalam folder dist.
