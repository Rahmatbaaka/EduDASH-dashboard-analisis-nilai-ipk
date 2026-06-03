window.showMenu = function(menuId) {
    console.log("--- Menjalankan showMenu untuk:", menuId, "---");
    const sections = document.querySelectorAll('.content-section');
    
    sections.forEach(section => section.classList.remove('active-section'));
    
    const activeSection = document.getElementById(menuId);
    if (activeSection) {
        activeSection.classList.add('active-section');
        console.log(`Berhasil menampilkan section: ${menuId}`);
        window.scrollTo({ top: 0, behavior: 'smooth' });
    } else {
        console.error(`ERROR: Elemen dengan ID "${menuId}" tidak ditemukan di halaman.`);
    }

    const sidebarLinks = document.querySelectorAll('.sidebar-link');
    sidebarLinks.forEach(link => link.classList.remove('active-menu'));
    
    const activeLink = document.getElementById(`btn-${menuId}`);
    if (activeLink) activeLink.classList.add('active-menu');

    const sidebar = document.getElementById('sidebar');
    const menuButton = document.getElementById('menuButton');
    const overlay = document.getElementById('overlay');
    const mainContent = document.querySelector('.main-content');
    
    if (sidebar && sidebar.classList.contains('active')) {
        sidebar.classList.remove('active');
        if (overlay) overlay.classList.remove('active');
        if (mainContent) mainContent.classList.remove('shifted');
        if (menuButton) menuButton.classList.remove('move');
    }
};

document.addEventListener('DOMContentLoaded', function() {
    const menuButton = document.getElementById('menuButton');
    const sidebar = document.getElementById('sidebar');
    const overlay = document.getElementById('overlay');
    const mainContent = document.querySelector('.main-content');

    if (menuButton && sidebar && overlay) {
        menuButton.addEventListener('click', () => {
            sidebar.classList.toggle('active');
            overlay.classList.toggle('active');
            mainContent.classList.toggle('shifted');
            menuButton.classList.toggle('move');
        });

        overlay.addEventListener('click', () => {
            sidebar.classList.remove('active');
            overlay.classList.remove('active');
            mainContent.classList.remove('shifted');
            menuButton.classList.remove('move');
        });
    }

    const data = window.dashboardData;
    if (!data) {
        console.error("Data dashboardData tidak ditemukan di window. Periksa template HTML.");
        return;
    }

    if (data.activeMenu) {
        setTimeout(() => window.showMenu(data.activeMenu), 200);
    }

    const setCardContent = (id, title, narasi, desc, actions) => {
        const titleEl = document.getElementById(`title-chart-${id}`);
        const narasiEl = document.getElementById(`narasi-chart-${id}`);
        const descEl = document.getElementById(`desc-chart-${id}`);
        const actionEl = document.getElementById(`action-chart-${id}`);
        
        if (titleEl) titleEl.innerText = title;
        if (narasiEl) narasiEl.innerText = narasi;
        if (descEl) descEl.innerHTML = desc;
        if (actionEl) actionEl.innerHTML = actions.map(a => `<li>${a}</li>`).join('');
    };

    Chart.defaults.color = '#B0C4DE';
    Chart.defaults.borderColor = 'rgba(255, 255, 255, 0.05)';

    const ctx1 = document.getElementById('canvas-chart-1');
    if (ctx1 && data.chart1) {
        new Chart(ctx1, {
            type: 'bubble',
            data: { datasets: [{ label: 'Mahasiswa', data: data.chart1, backgroundColor: data.chart1.map(d => d.color) }] },
            options: {
                scales: {
                    x: { title: { display: true, text: 'Jam Belajar' } },
                    y: { title: { display: true, text: 'Jam Tidur' } }
                },
                plugins: { tooltip: { callbacks: { label: (c) => `IPK: ${c.raw.ipk} | Kopi: ${(c.raw.r-4)/4} Gelas` } } }
            }
        });
        setCardContent(1, "The Hustle vs Health Balance", "Mitos Begadang Demi Nilai",
            "Data menunjukkan konsumsi kopi tinggi (bubble besar) tidak selalu linear dengan IPK jika tidur < 5 jam.",
            ["Batasi kopi maks 2 gelas", "Prioritaskan tidur 6-7 jam"]);
    }

    const ctx2 = document.getElementById('canvas-chart-2');
    if (ctx2 && data.chart2) {
        new Chart(ctx2, {
            type: 'scatter',
            data: { datasets: [{ label: 'Aktivitas Digital', data: data.chart2, backgroundColor: data.chart2.map(d => d.color) }] },
            options: {
                scales: { 
                    x: { title: { display: true, text: 'Jam Game' } },
                    y: { title: { display: true, text: 'Jam Sosmed' } }
                }
            }
        });
        setCardContent(2, "The Digital Distraction Grid", "Memetakan Garis Batas", 
            "Terjadi penurunan warna (IPK) saat kombinasi game dan sosmed melebihi ambang batas 5 jam per hari.",
            ["Gunakan filter fokus saat jam produktif", "Audit waktu layar mingguan"]);
    }

    const ctx3 = document.getElementById('canvas-chart-3');
    if (ctx3 && data.chart3) {
        new Chart(ctx3, {
            type: 'radar',
            data: {
                labels: ['Belajar', 'Tidur', 'Olahraga', 'Akses Laptop'],
                datasets: [
                    { 
                        label: 'Sangat Baik', 
                        data: data.chart3.high, 
                        borderColor: '#10B981',
                        backgroundColor: 'rgba(16,185,129,0.1)',
                        pointBackgroundColor: '#10B981',
                        borderWidth: 2
                    },
                    { 
                        label: 'Rendah', 
                        data: data.chart3.low, 
                        borderColor: '#fbbf24', 
                        backgroundColor: 'rgba(251,191,36,0.1)',
                        pointBackgroundColor: '#fbbf24',
                        borderWidth: 2
                    }
                ]
            },
            options: {
                scales: {
                    r: {
                        angleLines: { color: 'rgba(255,255,255,0.1)' },
                        grid: { color: 'rgba(255,255,255,0.1)' },
                        pointLabels: { color: 'rgba(255,255,255,0.7)', font: { size: 12 } },
                        ticks: { display: false }
                    }
                }
            }
        });
        setCardContent(3, "The Support System Gap", "Di Balik Angka IPK", 
            "Ketimpangan fasilitas (laptop) dan kebiasaan olahraga menjadi pembeda utama antara profil IPK tinggi vs rendah.",
            ["Program pinjaman perangkat", "Akses fasilitas olahraga gratis"]);
    }

    const ctx4 = document.getElementById('canvas-chart-4');
        if (ctx4 && data.chart4) {
            new Chart(ctx4, {
                type: 'bar',
                data: data.chart4,
                options: { 
                    scales: { 
                        x: { title: { display: true, text: 'Kategori Mahasiswa' } }, 
                        y: { title: { display: true, text: 'Rata-rata IPK' }, min: 0, max: 4 } 
                    } 
                }
            });
            setCardContent(4, "The Digital & Economic Equity Gap", "Analisis Dampak Fasilitas & Status Kerja", 
                "Mahasiswa yang memiliki laptop dan tidak harus membagi waktu dengan bekerja secara umum mencatatkan rata-rata pencapaian IPK yang lebih stabil.",
                ["Sediakan program bantuan peminjaman perangkat kampus", "Berikan fleksibilitas atau penyesuaian jadwal kuliah bagi mahasiswa bekerja"]);
        }

    const ctx5 = document.getElementById('canvas-chart-5');
        if (ctx5 && data.chart5) {
            new Chart(ctx5, {
                type: 'bubble',
                data: { datasets: [{ label: 'Sebaran Mahasiswa', data: data.chart5, backgroundColor: '#ef4444' }] },
                options: { scales: { x: { title: { display: true, text: 'Jam Belajar / Hari' } }, y: { title: { display: true, text: 'Capaian IPK' }, min: 0, max: 4 } } }
            });
            setCardContent(5, "Learning Efficiency Analysis", "Hubungan Durasi Belajar Terhadap IPK", 
                "Grafik memperlihatkan peningkatan jam belajar harian berkorelasi positif dengan pergeseran nilai IPK ke arah yang lebih tinggi.",
                ["Adakan workshop metode belajar efektif (Smart Study)", "Dorong pembentukan kelompok belajar (Study Group) di kelas"]);
        }

    const ctx6 = document.getElementById('canvas-chart-6');
        if (ctx6 && data.chart6) {
            new Chart(ctx6, {
                type: 'scatter',
                data: {
                    datasets: [{
                        label: 'Pola Tidur',
                        data: data.chart6,
                        pointRadius: 6,
                        backgroundColor: data.chart6.map(d => d.color || 'rgba(16, 185, 129, 0.6)')
                    }]
                },
                options: { scales: { x: { title: { display: true, text: 'Jam Tidur / Hari' } }, y: { title: { display: true, text: 'IPK' }, min: 0, max: 4 } } }
            });
            setCardContent(6, "The Sleep & Academic Tipping Point", "Batas Toleransi Istirahat", 
                "Data menunjukkan penurunan performa akademik yang cukup drastis pada mahasiswa yang memiliki pola tidur kronis di bawah 5 jam per hari.",
                ["Kampanyekan pentingnya manajemen waktu istirahat (Digital Wellbeing)", "Sediakan layanan konseling bagi mahasiswa yang mengalami gangguan tidur/stres"]);
        }

    const ctx7 = document.getElementById('canvas-chart-7');
        if (ctx7 && data.chart7 && data.chart7.labels) {
            new Chart(ctx7, {
                type: 'bar',
                data: {
                    labels: data.chart7.labels,
                    datasets: [{ label: 'Rata-rata IPK', data: data.chart7.values, backgroundColor: ['#059669', '#10b981', '#34d399', '#6ee7b7'] }]
                },
                options: { scales: { y: { min: 0, max: 4, title: { display: true, text: 'Rata-rata IPK' } }, x: { title: { display: true, text: 'Asal Sekolah' } } } }
            });
            setCardContent(7, "Institutional Background Performance", "Analisis Distribusi IPK Berdasarkan Asal Sekolah", 
                "Rata-rata pencapaian nilai IPK dipetakan berdasarkan latar belakang institusi sekolah asal (SMA, SMK, MA) untuk melihat adaptasi akademik awal.",
                ["Lakukan program matrikulasi atau pembekalan dasar bagi mahasiswa baru", "Berikan pendampingan akademik (mentoring) yang merata tanpa memandang latar belakang sekolah"]);
        }
    });
