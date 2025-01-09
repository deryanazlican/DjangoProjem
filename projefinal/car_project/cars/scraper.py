import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

#Araba verileri çekilir
def get_car_data():
    # Tarayıcı başlatma
    options = uc.ChromeOptions()
    options.add_argument("--start-maximized")
    driver = uc.Chrome(options=options)

    car_data = []

    try:
        # Arabam.com adresine git
        url = "https://www.arabam.com/ikinci-el/otomobil"
        driver.get(url)

        # Çerezleri kabul et
        try:
            cookie_accept_button = WebDriverWait(driver, 5).until(
                EC.element_to_be_clickable((By.XPATH, '//button[contains(text(), "Kabul Et")]'))
            )
            cookie_accept_button.click()
            print("Çerezler kabul edildi.")
        except Exception:
            print("Çerez kabul butonu bulunamadı veya hata oluştu.")

        # Linkleri takip etmek için index kullan
        index = 0
        page_number = 1  # Başlangıç sayfa numarası

        while True:
            try:
                # Sayfadaki tüm araç linklerini yeniden bul
                car_links = WebDriverWait(driver, 15).until(
                    EC.presence_of_all_elements_located((By.XPATH, '//tbody/tr/td[3]/a'))
                )

                if index >= len(car_links):
                    # Sonraki sayfaya geçmek için URL değiştir
                    page_number += 1
                    next_page_url = f"https://www.arabam.com/ikinci-el/otomobil?page={page_number}"
                    driver.get(next_page_url)
                    print(f"{page_number}. sayfaya geçiliyor...")
                    index = 0  # Yeni sayfada sıfırdan başla
                    time.sleep(2)
                    continue

                # Linke tıkla
                car_links[index].click()
                time.sleep(2)  # Bekleme süresi

                # Verileri çek
                try:
                    # Marka bilgisi
                    brand = WebDriverWait(driver, 10).until(
                        EC.presence_of_element_located((By.XPATH, '/html[1]/body[1]/div[2]/div[2]/div[3]/div[1]/div[1]/div[1]/div[2]/div[2]/div[2]/div[3]/div[2]'))
                    ).text

                    # Model bilgisi
                    model = WebDriverWait(driver, 10).until(
                        EC.presence_of_element_located((By.XPATH, '/html[1]/body[1]/div[2]/div[2]/div[3]/div[1]/div[1]/div[1]/div[2]/div[2]/div[2]/div[5]/div[2]'))
                    ).text

                    # Yıl bilgisi
                    year = WebDriverWait(driver, 10).until(
                        EC.presence_of_element_located((By.XPATH, '/html[1]/body[1]/div[2]/div[2]/div[3]/div[1]/div[1]/div[1]/div[2]/div[2]/div[2]/div[6]/div[2]'))
                    ).text

                    # Mileage bilgisi
                    mileage = WebDriverWait(driver, 10).until(
                        EC.presence_of_element_located((By.XPATH, '/html[1]/body[1]/div[2]/div[2]/div[3]/div[1]/div[1]/div[1]/div[2]/div[2]/div[2]/div[7]/div[2]'))
                    ).text

                    # Fiyat bilgisi
                    price = WebDriverWait(driver, 10).until(
                        EC.presence_of_element_located((By.XPATH, '/html[1]/body[1]/div[2]/div[2]/div[3]/div[1]/div[1]/div[1]/div[2]/div[2]/div[1]/div[1]/div[2]/div[1]'))
                    ).text

                    # Şehir bilgisi
                    city = WebDriverWait(driver, 10).until(
                        EC.presence_of_element_located((By.XPATH, '/html[1]/body[1]/div[2]/div[2]/div[3]/div[1]/div[1]/div[1]/div[1]/div[1]/div[1]/span[1]/span[1]'))
                    ).text

                    # Kaza raporu bilgisi
                    crash_report = WebDriverWait(driver, 10).until(
                        EC.presence_of_element_located((By.XPATH, '/html[1]/body[1]/div[2]/div[2]/div[3]/div[1]/div[1]/div[1]/div[2]/div[2]/div[2]/div[18]/div[2]'))
                    ).text

                    # Renk bilgisi
                    color = WebDriverWait(driver, 10).until(
                        EC.presence_of_element_located((By.XPATH, '/html[1]/body[1]/div[2]/div[2]/div[3]/div[1]/div[1]/div[1]/div[2]/div[2]/div[2]/div[11]/div[2]'))
                    ).text

                    # Yakıt Türü
                    fuel_type = WebDriverWait(driver, 10).until(
                        EC.presence_of_element_located((By.XPATH, '/html[1]/body[1]/div[2]/div[2]/div[3]/div[1]/div[1]/div[1]/div[2]/div[2]/div[2]/div[9]/div[2]'))
                    ).text

                    # Vites Türü
                    gear_type = WebDriverWait(driver, 10).until(
                        EC.presence_of_element_located((By.XPATH, '/html/body/div[2]/div[2]/div[3]/div/div[1]/div[1]/div[2]/div[2]/div[2]/div[8]/div[2]'))
                    ).text

                    # Araç Durumu
                    vehicle_condition = WebDriverWait(driver, 10).until(
                        EC.presence_of_element_located((By.XPATH, '/html/body/div[2]/div[2]/div[3]/div/div[1]/div[1]/div[2]/div[2]/div[2]/div[15]/div[2]'))
                    ).text

                    # Takas Durumu
                    trade_status = WebDriverWait(driver, 10).until(
                        EC.presence_of_element_located((By.XPATH, '/html/body/div[2]/div[2]/div[3]/div/div[1]/div[1]/div[2]/div[2]/div[2]/div[19]/div[2]'))
                    ).text

                    # Çekiş
                    drive_type = WebDriverWait(driver, 10).until(
                        EC.presence_of_element_located((By.XPATH, '/html/body/div[2]/div[2]/div[3]/div/div[1]/div[1]/div[2]/div[2]/div[2]/div[14]/div[2]'))
                    ).text

                    # Motor Hacmi
                    engine_size = WebDriverWait(driver, 10).until(
                        EC.presence_of_element_located((By.XPATH, '/html[1]/body[1]/div[2]/div[2]/div[3]/div[1]/div[1]/div[1]/div[2]/div[2]/div[2]/div[12]/div[2]'))
                    ).text

                    # Motor Gücü
                    engine_power = WebDriverWait(driver, 10).until(
                        EC.presence_of_element_located((By.XPATH, '/html/body/div[2]/div[2]/div[3]/div/div[1]/div[1]/div[2]/div[2]/div[2]/div[13]/div[2]'))
                    ).text

                    # Çıktıyı yazdır
                    print("------")
                    print(f"Marka: {brand}")
                    print(f"Model: {model}")
                    print(f"Yıl: {year}")
                    print(f"KM: {mileage}")
                    print(f"Fiyat: {price}")
                    print(f"Şehir: {city}")
                    print(f"Kaza Raporu: {crash_report}")
                    print(f"Renk: {color}")
                    print(f"Yakıt Türü: {fuel_type}")
                    print(f"Vites Türü: {gear_type}")
                    print(f"Araç Durumu: {vehicle_condition}")
                    print(f"Takas Durumu: {trade_status}")
                    print(f"Çekiş: {drive_type}")
                    print(f"Motor Hacmi: {engine_size}")
                    print(f"Motor Gücü: {engine_power}")

                except Exception as e:
                    print(f"Bilgi alınamadı: {e}")

                # Geri dön ve index artır
                driver.back()
                time.sleep(2)  # Bekleme süresi
                index += 1

            except Exception as e:
                print(f"Genel hata oluştu: {e}")
                break

    finally:
        # Tarayıcıyı kapat
        driver.quit()

    return car_data
