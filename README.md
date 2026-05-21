# EduDASH: Dashboard Analisis & Prediksi Nilai IPK 🎓📊

EduDASH adalah platform dashboard berbasis web menggunakan **Django Framework** yang dirancang untuk menganalisis pengaruh kebiasaan sehari-hari mahasiswa terhadap nilai Indeks Prestasi Kumulatif (IPK). Proyek ini mengintegrasikan pemrosesan data statistik dengan model Machine Learning untuk memberikan prediksi IPK secara interaktif.

Proyek ini dikembangkan menggunakan repositori resmi:  
🔗 [https://github.com/Rahmatbaaka/EduDASH-dashboard-analisis-nilai-ipk](https://github.com/Rahmatbaaka/EduDASH-dashboard-analisis-nilai-ipk)

---

## 🛠️ Tech Stack & Teknologi

Proyek ini dibangun menggunakan kombinasi teknologi berikut:

* **Backend Framework:** ![Django](https://img.shields.io/badge/django-%23092E20.svg?style=flat&logo=django&logoColor=white) (Python-based Web Framework)
* **Data Wrangling & Processing:** ![Pandas](https://img.shields.io/badge/pandas-%23150458.svg?style=flat&logo=pandas&logoColor=white) ![NumPy](https://img.shields.io/badge/numpy-%23013243.svg?style=flat&logo=numpy&logoColor=white)
* **Machine Learning Deployment:** ![Scikit-Learn](https://img.shields.io/badge/scikit--learn-%23F7931E.svg?style=flat&logo=scikit-learn&logoColor=white) (via `joblib`)
* **Frontend UI & Visualisasi:** ![HTML5](https://img.shields.io/badge/html5-%23E34F26.svg?style=flat&logo=html5&logoColor=white) ![CSS3](https://img.shields.io/badge/css3-%231572B6.svg?style=flat&logo=css3&logoColor=white) ![JavaScript](https://img.shields.io/badge/javascript-%23F7DF1E.svg?style=flat&logo=javascript&logoColor=%23323330)

---

## 👥 Anggota Kelompok
Berikut adalah anggota tim yang berkontribusi dalam pengembangan EduDASH:
* **[Rahmat Hidayat]** - [25051204070] ([@RahmatbaakaGithub](https://github.com/Rahmatbaaka))
* **[Dhany Erlangga]** - [25051204192] ([@DhanyErlangga192](https://github.com/DhanyErlangga192))
* **[Moaadh Ghamdan]** - [25051204253] ([@25051204253-MOAADH](https://github.com/25051204253-MOAADH))
* **[Nama Anggota 4]** - [NIM] ([@usernameGithub](https://github.com/username))

---

## ✨ Fitur Utama
Aplikasi EduDASH menyediakan 3 menu utama untuk memfasilitasi analisis data akademis mahasiswa:

### 1. Menu Insight
Menyajikan visualisasi insight data yang memberikan gambaran terhadap user tentang pola dan tren yang terjadi terhadap nilai IPK, serta hubungan antara fitur aktivitas dengan label. Menu ini didukung oleh 7 grafik interaktif:
* **Hustle Chart (Bubble Chart):** Analisis korelasi waktu belajar (X), waktu tidur (Y), dan konsumsi kopi (R) terhadap tingkat IPK.
* **Distraction Chart (Scatter Chart):** Analisis korelasi durasi bermain game (X) dan membuka sosial media (Y) terhadap IPK.
* **Support Gap Analysis:** Perbandingan rata-rata waktu belajar, tidur, dan olahraga antara mahasiswa ber-IPK tinggi (>3.5) dan rendah (≤3.0).
* **Equity Chart:** Analisis kesenjangan rata-rata IPK berdasarkan kepemilikan laptop dan status bekerja mahasiswa.
* **Anomaly Chart:** Plotting khusus untuk mendeteksi anomali hubungan antara jam belajar harian dengan capaian IPK.
* **Tipping Point Chart:** Visualisasi untuk melihat titik jenuh korelasi antara durasi jam tidur terhadap tingkat IPK mahasiswa.
* **Institutional Chart:** Grafik perbandingan rata-rata IPK berdasarkan latar belakang asal sekolah mahasiswa.

### 2. Menu Prediksi
Menggunakan model Machine Learning (ML) sederhana dengan tingkat akurasi yang optimal (memanfaatkan file `model.joblib`). Melalui fitur interaktif berbasis form POST ini, pengguna dapat menginputkan data aktivitas harian mereka untuk mendapatkan estimasi atau prediksi nilai IPK secara instan.

### 3. Menu Artikel
Menyediakan artikel atau referensi penunjang yang memuat bukti keterkaitan secara ilmiah antara variabel aktivitas harian (seperti jam tidur, belajar, olahraga) dengan nilai IPK atau performa kognitif mahasiswa.

---

## 🛠️ Cara Menjalankan Proyek

### Prasyarat (Prerequisites)
Pastikan perangkat Anda telah terinstal:
* Python 3.8 atau versi di atasnya
* PIP (Python Package Installer)

### Langkah Instalasi

1. **Clone Repositori**
```bash
git clone https://github.com/Rahmatbaaka/EduDASH-dashboard-analisis-nilai-ipk.git
cd EduDASH-dashboard-analisis-nilai-ipk

```
2. **Buat dan Aktifkan Virtual Environment**
* **Windows:**
```bash
python -m venv venv
venv\Scripts\activate

```
* **macOS/Linux:**
```bash
python3 -m venv venv
source venv/bin/activate

```
3. **Instal Dependency**
Pastikan library utama seperti `django`, `pandas`, dan `joblib` terinstal melalui perintah:
```bash
pip install -r requirements.txt

```

4. **Struktur Data Keamanan Aplikasi**
Pastikan file dataset dan model buatan kelompok Anda diletakkan pada direktori berikut:
* Dataset: `dashboard/data/dataset_ipk.csv`
* ML Model: `dashboard/models/model.joblib`


5. **Jalankan Server Django**
```bash
python manage.py runserver

```


6. Buka browser dan akses dashboard melalui URL: `http://127.0.0.1:8000/`

---

## 🧩 Penjelasan Implementasi OOP (Object-Oriented Programming)

Proyek EduDASH menerapkan pilar-pilar utama Pemrograman Berorientasi Objek secara eksplisit menggunakan bahasa Python pada sisi backend (arsitektur layanan data dan visualisasi):

### 1. Abstraction (Abstraksi)

Abstraksi digunakan untuk menyembunyikan detail cetak biru model prediksi dan pembuatan fungsi-fungsi dasar wajib melalui kelas abstrak (*Abstract Base Class*).

* **Implementasi:** Di dalam file `services.py`, kami membuat kelas abstrak `BasePredictionModel` menggunakan modul `abc` dengan *decorator* `@abstractmethod` untuk fungsi `load_model()`, `predict()`, dan `load_dataset()`. Hal ini memastikan kelas turunan mengimplementasikan fungsi tersebut dengan benar tanpa mengekspos struktur kasarnya.

### 2. Inheritance (Pewarisan)

Pewarisan diimplementasikan untuk menurunkan properti dan kontrak *method* dari kelas induk abstrak ke kelas operasional yang lebih spesifik.

* **Implementasi:** Kelas `AcademicPerformanceModel` mewarisi kelas `BasePredictionModel` (`class AcademicPerformanceModel(BasePredictionModel):`). Dengan mewarisi kelas tersebut, seluruh fungsi dasar prediksi dapat dikustomisasi khusus untuk menangani data performa akademik mahasiswa.

### 3. Encapsulation (Pengkapsulan)

Pengkapsulan digunakan untuk melindungi variabel atau status internal objek agar tidak dapat dimodifikasi secara sembarangan dari luar kelas.

* **Implementasi:** Di dalam kelas `AcademicPerformanceModel`, kami menggunakan properti *private* dengan tanda *double underscore* (seperti `self.__model_name`, `self.__model_instance`, `self.__dataset`, dll.). Atribut-atribut ini hanya bisa diakses dan diubah secara internal melalui *method* bawaan kelas seperti `.load_model()` dan `.load_dataset()`.

### 4. Single Responsibility Principle / Polymorphism dalam Pemrosesan Data

Kami memisahkan logika pemrosesan data visual dari Django View menggunakan kelas khusus untuk menjaga kerapian kode (*clean code*).

* **Implementasi:** Kami membuat kelas `DashboardDataProcessor` di file `views.py`. Kelas ini bertugas khusus mengkapsulasi data frame (`pandas.DataFrame`) dan menyediakan berbagai *method* pemrosesan data grafik, seperti `process_chart1_hustle()` hingga `process_chart7_institutional()`, serta pembagian warna otomatis lewat helper OOP `get_color_mapping()`. Fungsi `dashboard_view` di Django cukup memanggil instansiasi dari kelas ini.
