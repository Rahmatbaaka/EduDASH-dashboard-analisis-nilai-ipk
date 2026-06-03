from django.db import models
from django.utils import timezone

class Mahasiswa(models.Model):
    umur = models.IntegerField()
    gender = models.CharField(max_length=20)
    rata2_tidur_hari = models.FloatField()
    rata2_belajar_hari = models.FloatField()
    rata2_bermain_game_hari = models.FloatField()
    rata2_buka_sosmed_hari = models.FloatField()
    jumlah_kopi_hari = models.IntegerField()
    jumlah_matcha_hari = models.IntegerField()
    jumlah_ukm = models.IntegerField()
    jarak_kampus_km = models.FloatField()
    asal_sekolah = models.CharField(max_length=20)
    rata2_olahraga_hari = models.FloatField()
    memiliki_laptop = models.IntegerField()
    bekerja = models.IntegerField()
    ipk = models.FloatField()
    ipk_group = models.CharField(max_length=30)

    class Meta:
        verbose_name_plural = "Data Mahasiswa"

    def __str__(self):
        return f"Mhs {self.id} - IPK: {self.ipk}"

class PredictionLog(models.Model): 
    tidur = models.FloatField()
    belajar = models.FloatField()
    bermain = models.FloatField()
    sosmed = models.FloatField()
    kopi = models.FloatField()
    olahraga = models.FloatField()
    laptop = models.IntegerField()
    hasil_ipk = models.FloatField()
    waktu_prediksi = models.DateTimeField(auto_now_add=True)

    hasil_ipk = models.FloatField()
    waktu_prediksi = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"Prediksi {self.hasil_ipk:.2f} - {self.waktu_prediksi.strftime('%d/%m/%Y %H:%M')}"