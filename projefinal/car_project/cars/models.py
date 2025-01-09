from django.db import models

#Araba modelleri tanımlandı
class Car(models.Model):
    marka = models.CharField(max_length=50)
    model = models.CharField(max_length=50)
    yil = models.IntegerField()
    km = models.IntegerField()
    fiyat = models.DecimalField(max_digits=10, decimal_places=2)
    sehir = models.CharField(max_length=50)
    kaza_raporu = models.CharField(max_length=50)
    renk = models.CharField(max_length=20)
    yakit_turu = models.CharField(max_length=20)
    vites_turu = models.CharField(max_length=20)
    arac_durumu = models.CharField(max_length=20)
    takas_durumu = models.CharField(max_length=20)
    cekis = models.CharField(max_length=20)
    motor_hacmi = models.CharField(max_length=20)
    motor_gucu = models.CharField(max_length=20)
    kasa_tipi = models.CharField(max_length=20)
    kimden = models.CharField(max_length=50)

    def __str__(self):
        return f"{self.marka} {self.model} "
