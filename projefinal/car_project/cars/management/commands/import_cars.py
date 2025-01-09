import os
import pandas as pd
from django.core.management.base import BaseCommand
from cars.models import Car

#Araba verileri excelden çekilir
class Command(BaseCommand):
    help = 'Import car data from Excel'

    def handle(self, *args, **kwargs):
        user_profile = os.getenv("USERPROFILE")  # Windows kullanıcı profilini al
        file_path = os.path.join(user_profile, "Desktop", "DjangoProjem", "projefinal", "car_project", "Araba_Verileri_Duzenli.xlsx")
        df = pd.read_excel(file_path)
        for _, row in df.iterrows():
            Car.objects.create(
                marka=row['Marka'],
                model=row['Model'],
                yil=row['Yıl'],
                km=row['KM'],
                fiyat=row['Fiyat (TL)'],
                sehir=row['Şehir'],
                kaza_raporu=row['Kaza Raporu'],
                renk=row['Renk'],
                yakit_turu=row['Yakıt Türü'],
                vites_turu=row['Vites Türü'],
                arac_durumu=row['Araç Durumu'],
                takas_durumu=row['Takas Durumu'],
                cekis=row['Çekiş'],
                motor_hacmi=row['Motor Hacmi'],
                motor_gucu=row['Motor Gücü'],
                kasa_tipi=row['Kasa Tipi'],
                kimden=row['Kimden']
            )
                