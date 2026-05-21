window.showMenu = function(menuId) {
    const sections = document.querySelectorAll('.content-section');
    sections.forEach(section => section.classList.remove('active-section'));
    
    const activeSection = document.getElementById(menuId);
    if (activeSection) activeSection.classList.add('active-section');

    const sidebarLinks = document.querySelectorAll('.sidebar-link');
    sidebarLinks.forEach(link => link.classList.remove('active-menu'));
    
    const activeLink = document.getElementById(`btn-${menuId}`);
    if (activeLink) activeLink.classList.add('active-menu');

    const sidebar = document.getElementById('sidebar');
    const menuButton = document.getElementById('menuButton');
    const overlay = document.getElementById('overlay');
    const mainContent = document.querySelector('.main-content');
    
    if (window.innerWidth <= 768 && sidebar && sidebar.classList.contains('active')) {
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
    if (!data) return;

    if (data.activeMenu) {
        window.showMenu(data.activeMenu);
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

    Chart.defaults.color = 'rgba(255, 255, 255, 0.8)'; // Mengubah teks chart menjadi putih transparan agar bersih di card gelap
    Chart.defaults.borderColor = 'rgba(255,255,255,0.1)';

    new Chart(document.getElementById('canvas-chart-1'), {
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

    const ctx2 = document.getElementById('canvas-chart-2');
    if (ctx2) new Chart(ctx2, {
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

    const ctx3 = document.getElementById('canvas-chart-3');
    if (ctx3) new Chart(ctx3, {
        type: 'radar',
        data: { // Menggunakan warna yang lebih konsisten dengan tema
            labels: ['Belajar', 'Tidur', 'Olahraga', 'Akses Laptop'],
            datasets: [
                { 
                    label: 'Sangat Baik', 
                    data: data.chart3.high, 
                    borderColor: '#10b981', // Hijau emerald
                    backgroundColor: 'rgba(16,185,129,0.2)', // Hijau emerald transparan
                    pointBackgroundColor: '#10b981', // Titik hijau
                    borderWidth: 2
                },
                { 
                    label: 'Rendah', 
                    data: data.chart3.low, 
                    borderColor: '#ef4444', // Merah
                    backgroundColor: 'rgba(239,68,68,0.2)', // Merah transparan
                    pointBackgroundColor: '#ef4444', // Titik merah
                    borderWidth: 2
                }
            ]
        },
        options: { // Menyesuaikan skala radar untuk tampilan yang lebih bersih
            scales: {
                r: {
                    angleLines: { color: 'rgba(255,255,255,0.1)' },
                    grid: { color: 'rgba(255,255,255,0.1)' },
                    pointLabels: { color: 'rgba(255,255,255,0.7)', font: { size: 12 } },
                    ticks: { display: false } // Sembunyikan label nilai pada sumbu radar
                }
            }
        }
    });
    setCardContent(3, "The Support System Gap", "Di Balik Angka IPK", 
        "Ketimpangan fasilitas (laptop) dan kebiasaan olahraga menjadi pembeda utama antara profil IPK tinggi vs rendah.",
        ["Program pinjaman perangkat", "Akses fasilitas olahraga gratis"]);

    const ctx4 = document.getElementById('canvas-chart-4');
    if (ctx4) new Chart(ctx4, {
        type: 'bar',
        data: data.chart4,
        options: { scales: { x: { stacked: true }, y: { stacked: true } } }
    });
    setCardContent(4, "The Lifestyle Distribution", "Pergeseran Kurva Fokus", 
        "Distribusi jam tidur menunjukkan kelompok 'Sangat Baik' memiliki pola tidur yang jauh lebih konsisten.",
        ["Workshop manajemen waktu", "Penyuluhan kesehatan mental"]);

    const ctx5 = document.getElementById('canvas-chart-5');
    if (ctx5) new Chart(ctx5, {
        type: 'bubble',
        data: { datasets: [{ label: 'Kelompok Anomali', data: data.chart5, backgroundColor: '#ef4444' }] },
        options: { scales: { x: { title: { display: true, text: 'Jam Belajar' } }, y: { title: { display: true, text: 'IPK' } } } }
    });
    setCardContent(5, "Deeper Dive: Hustle vs Health", "Analisis Kegagalan Kafein", 
        "Fokus pada mahasiswa yang mencoba kompensasi kurang tidur dengan kopi namun jam belajar tetap tidak efektif.",
        ["Evaluasi metode belajar", "Intervensi pola tidur"]);

    const ctx6 = document.getElementById('canvas-chart-6');
    if (ctx6) new Chart(ctx6, {
        type: 'scatter',
        data: {
            datasets: [{
                label: 'Titik Kritis',
                data: data.chart6,
                pointRadius: 15,
                backgroundColor: data.chart6.map(d => `rgba(239, 68, 68, ${d.prob_low_ipk})`)
            }]
        }
    });
    setCardContent(6, "The Digital Tipping Point", "Batas Toleransi Digital", 
        "Probabilitas IPK rendah meningkat 3x lipat setelah melewati ambang batas game > 3.5 jam.",
        ["Edukasi Digital Wellbeing", "Penjadwalan hiburan terstruktur"]);

    const ctx7 = document.getElementById('canvas-chart-7');
    if (ctx7) new Chart(ctx7, {
        type: 'bar',
        data: {
            labels: data.chart7.labels,
            datasets: [{ label: 'Rata-rata IPK', data: data.chart7.values, backgroundColor: ['#3b82f6', '#60a5fa', '#f59e0b', '#fbbf24'] }]
        },
        options: { scales: { y: { min: 2.5, max: 4.0 } } }
    });
    setCardContent(7, "Institutional Support Gap Analysis", "Rekomendasi Program Bantuan", 
        "Selisih IPK antara pemilik laptop dan non-pemilik mencapai 0.13 poin, menunjukkan urgensi bantuan fasilitas. Demikian pula, mahasiswa yang bekerja cenderung memiliki IPK lebih rendah.",
        ["Program subsidi laptop", "Beasiswa khusus mahasiswa bekerja", "Fleksibilitas jadwal kuliah untuk mahasiswa bekerja"]);
});
