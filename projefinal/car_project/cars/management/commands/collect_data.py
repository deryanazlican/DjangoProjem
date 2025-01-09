import os
import time
import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd
from cars.models import Car


def clean_km_value(km):
    """KM değerini temizler ve sayısal formata dönüştürür."""
    return int(km.replace('.', '').replace(' km', ''))

def clean_price_value(price):
    """Fiyat değerini temizler ve sayısal formata dönüştürür."""
    return float(price.replace(' TL', '').replace('.', '').replace(',', '.'))

def save_to_excel(data):
    """Çekilen verileri Excel dosyasına kaydeder."""
    if not data:
        print("Kaydedilecek veri bulunamadı.")
        return
    
    df = pd.DataFrame(data)
    user_profile = os.getenv("USERPROFILE")  # Windows kullanıcı profilini al
    excel_file = os.path.join(user_profile, "Desktop", "DjangoProjem", "projefinal", "car_project", "Arac_Verileri_Yeni.xlsx")
    df.to_excel(excel_file, index=False)
    print("Veriler Excel dosyasına kaydedildi.")

#Limit default olarak 5'e ayarlandı buradan değiştirebilirsiniz.(1)
def fetch_data_and_save(limit=5):
    """Arabam.com'dan veri çeker, veritabanına ve Excel dosyasına kaydeder."""
    options = uc.ChromeOptions()
    options.add_argument("--start-maximized")
    driver = uc.Chrome(options=options)
    
    data = []  # Excel'e kaydedilecek veri listesi
    
    try:
        url = "https://www.arabam.com/ikinci-el/otomobil"
        driver.get(url)

        # Çerezleri kabul et
        try:
            cookie_accept_button = WebDriverWait(driver, 5).until(
                EC.element_to_be_clickable((By.XPATH, '//button[contains(text(), "Kabul Et")]'))
            )
            cookie_accept_button.click()
        except Exception:
            print("Çerez kabul butonu bulunamadı.")

        index = 0
        page_number = 1
        count = 0  # Çekilen araç sayısını takip etmek için

        while count < limit:
            car_links = WebDriverWait(driver, 15).until(
                EC.presence_of_all_elements_located((By.XPATH, '//tbody/tr/td[3]/a'))
            )
            if index >= len(car_links):
                page_number += 1
                next_page_url = f"https://www.arabam.com/ikinci-el/otomobil?page={page_number}"
                driver.get(next_page_url)
                index = 0
                time.sleep(2)
                continue

            car_links[index].click()
            time.sleep(2)

            try:
                # Verileri çek
                brand = WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located((By.XPATH, '/html[1]/body[1]/div[2]/div[2]/div[3]/div[1]/div[1]/div[1]/div[2]/div[2]/div[2]/div[3]/div[2]'))
                ).text

                model = WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located((By.XPATH, '/html[1]/body[1]/div[2]/div[2]/div[3]/div[1]/div[1]/div[1]/div[2]/div[2]/div[2]/div[5]/div[2]'))
                ).text

                year = WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located((By.XPATH, '/html[1]/body[1]/div[2]/div[2]/div[3]/div[1]/div[1]/div[1]/div[2]/div[2]/div[2]/div[6]/div[2]'))
                ).text

                mileage = WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located((By.XPATH, '/html[1]/body[1]/div[2]/div[2]/div[3]/div[1]/div[1]/div[1]/div[2]/div[2]/div[2]/div[7]/div[2]'))
                ).text

                price = WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located((By.XPATH, '/html[1]/body[1]/div[2]/div[2]/div[3]/div[1]/div[1]/div[1]/div[2]/div[2]/div[1]/div[1]/div[2]/div[1]'))
                ).text

                city = WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located((By.XPATH, '/html[1]/body[1]/div[2]/div[2]/div[3]/div[1]/div[1]/div[1]/div[1]/div[1]/div[1]/span[1]/span[1]'))
                ).text

                crash_report = WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located((By.XPATH, '/html[1]/body[1]/div[2]/div[2]/div[3]/div[1]/div[1]/div[1]/div[2]/div[2]/div[2]/div[18]/div[2]'))
                ).text

                color = WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located((By.XPATH, '/html[1]/body[1]/div[2]/div[2]/div[3]/div[1]/div[1]/div[1]/div[2]/div[2]/div[2]/div[11]/div[2]'))
                ).text

                fuel_type = WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located((By.XPATH, '/html[1]/body[1]/div[2]/div[2]/div[3]/div[1]/div[1]/div[1]/div[2]/div[2]/div[2]/div[9]/div[2]'))
                ).text

                gear_type = WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located((By.XPATH, '/html/body/div[2]/div[2]/div[3]/div/div[1]/div[1]/div[2]/div[2]/div[2]/div[8]/div[2]'))
                ).text

                vehicle_condition = WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located((By.XPATH, '/html/body/div[2]/div[2]/div[3]/div/div[1]/div[1]/div[2]/div[2]/div[2]/div[15]/div[2]'))
                ).text

                trade_status = WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located((By.XPATH, '/html/body/div[2]/div[2]/div[3]/div/div[1]/div[1]/div[2]/div[2]/div[2]/div[19]/div[2]'))
                ).text

                drive_type = WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located((By.XPATH, '/html/body/div[2]/div[2]/div[3]/div/div[1]/div[1]/div[2]/div[2]/div[2]/div[14]/div[2]'))
                ).text

                engine_size = WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located((By.XPATH, '/html[1]/body[1]/div[2]/div[2]/div[3]/div[1]/div[1]/div[1]/div[2]/div[2]/div[2]/div[12]/div[2]'))
                ).text

                engine_power = WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located((By.XPATH, '/html/body/div[2]/div[2]/div[3]/div/div[1]/div[1]/div[2]/div[2]/div[2]/div[13]/div[2]'))
                ).text

                # Veriyi listeye ekle
                data.append({
                    'marka': brand,
                    'model': model,
                    'yil': year,
                    'km': clean_km_value(mileage),
                    'fiyat': clean_price_value(price),
                    'sehir': city,
                    'kaza_raporu': crash_report,
                    'renk': color,
                    'yakit_turu': fuel_type,
                    'vites_turu': gear_type,
                    'arac_durumu': vehicle_condition,
                    'takas_durumu': trade_status,
                    'cekis': drive_type,
                    'motor_hacmi': engine_size,
                    'motor_gucu': engine_power,
                })

                # Veritabanına kaydet
                car = Car(
                    marka=brand,
                    model=model,
                    yil=year,
                    km=clean_km_value(mileage),
                    fiyat=clean_price_value(price),
                    sehir=city,
                    kaza_raporu=crash_report,
                    renk=color,
                    yakit_turu=fuel_type,
                    vites_turu=gear_type,
                    arac_durumu=vehicle_condition,
                    takas_durumu=trade_status,
                    cekis=drive_type,
                    motor_hacmi=engine_size,
                    motor_gucu=engine_power,
                )
                car.save()
                count += 1  # Çekilen araç sayısını artır

            except Exception as e:
                print(f"Bilgi alınamadı: {e}")

            driver.back()
            time.sleep(2)
            index += 1
        
    finally:
        driver.quit()

    # Verileri Excel dosyasına kaydet
        save_to_excel(data)
        return data