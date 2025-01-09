import os
from django.shortcuts import  render
from .models import Car
from django.http import JsonResponse
from cars.scraper import get_car_data
import pandas as pd
import joblib
from django.core.management import call_command
from cars.management.commands.collect_data import fetch_data_and_save


#Toplanan veriyi excelden siteye gönderir
def collected_data(request):
    # Excel dosyasını oku
    user_profile = os.getenv("USERPROFILE")  # Windows kullanıcı profilini al
    file_path = os.path.join(user_profile, "Desktop", "DjangoProjem", "projefinal", "car_project", "Arac_Verileri_Yeni.xlsx")
    df = pd.read_excel(file_path)

    # Veriyi template'e gönder
    data = df.to_dict(orient='records')  # Veriyi dict formatında gönderiyoruz
    return render(request, 'cars/collected_data.html', {'data': data})

# Veri çekme fonksiyonu
# Varsayılan veri çekme limiti 5 olarak ayarlandı, buradan değiştirebilirsiniz.
FETCH_LIMIT = 5
def start_data_collection(request):
    if request.method == 'GET':
        try:
            # Veri çekme işlemi
            car_data = fetch_data_and_save(limit=FETCH_LIMIT)

            if not car_data:
                return JsonResponse({'status': 'error', 'message': 'Hiç veri çekilemedi.'}, status=500)

            # Veriyi Excel'e kaydetme
            df = pd.DataFrame(car_data)
            user_profile = os.getenv("USERPROFILE")  # Windows kullanıcı profilini al
            excel_file = os.path.join(user_profile, "Desktop", "DjangoProjem", "projefinal", "car_project", "Arac_Verileri_Yeni.xlsx")
            df.to_excel(excel_file, index=False)

            # Mesaj döndürme
            return JsonResponse({
                'status': 'success',
                'message': f'{len(car_data)} araç başarıyla çekildi ve kaydedildi.',
            })
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': f'Hata: {str(e)}'}, status=500)
    return JsonResponse({'status': 'error', 'message': 'Sadece GET istekleri destekleniyor.'}, status=405)


#Tahminleme modeli
def predict_price(request):
    prediction = None
    if request.method == 'POST':
        # Kullanıcıdan alınan veriler
        marka = request.POST.get('marka')
        model = request.POST.get('model')
        yil = request.POST.get('yil')
        renk = request.POST.get('renk')
        km = request.POST.get('km')
        yakit = request.POST.get('yakit')
        vites = request.POST.get('vites')

        # Modeli, scaler'ı ve diğer dosyaları yükle
        user_profile = os.getenv("USERPROFILE")  # Windows kullanıcı profilini al
        model_path = os.path.join(user_profile, "Desktop", "DjangoProjem", "projefinal", "car_project", "lasso_price_model.pkl")
        scaler_path = os.path.join(user_profile, "Desktop", "DjangoProjem", "projefinal", "car_project", "scaler.pkl")
        columns_path = os.path.join(user_profile, "Desktop", "DjangoProjem", "projefinal", "car_project", "model_columns.pkl")
        

        model = joblib.load(model_path)
        scaler = joblib.load(scaler_path)
        model_columns = joblib.load(columns_path)

        # Kullanıcıdan alınan veriyi DataFrame'e dönüştür
        input_data = pd.DataFrame({
            'Marka': [marka],
            'Model': [model],
            'Yıl': [int(yil)],
            'Renk': [renk],
            'KM': [int(km)],
            'Yakıt Türü': [yakit],
            'Vites Türü': [vites],
            'Şehir': [''] * 1,
            'Kaza Raporu': [''] * 1,
            'Araç Durumu': [''] * 1,
            'Takas Durumu': [''] * 1,
            'Çekiş': [''] * 1,
            'Motor Hacmi': [0] * 1,
            'Motor Gücü': [0] * 1,
            'Kasa Tipi': [''] * 1,
            'Kimden': [''] * 1
        })

        # Kategorik verileri sayısallaştırma
        input_data = pd.get_dummies(input_data)

        # Modelde bulunan kolonları sıfır ile doldur
        input_data = input_data.reindex(columns=model_columns, fill_value=0)

        # Veriyi standartlaştırma
        input_data_scaled = scaler.transform(input_data)

        # Tahmin yap
        prediction = model.predict(input_data_scaled)[0]

    return render(request, 'cars/predict.html', {'prediction': prediction})

#Marka seçildikten sonra modelleri getir.
def get_models(request):
    marka = request.GET.get('marka')
    if marka:
        models = Car.objects.filter(marka=marka).values_list('model', flat=True).distinct()
        return JsonResponse({'models': list(models)})
    return JsonResponse({'models': []})

#Trend.analysis.html isteği getirir
def trend_analysis(request):
    return render(request, '/trend_analysis.html')

#Scraping.html
def scraping(request):
    car_data = get_car_data()  # Verileri scraping fonksiyonundan alıyoruz
    return render(request, 'cars/scraping.html', {'cars': car_data})  # Verileri şablona gönderiyoruz

#Anasayfada verileri getir
def home(request):
    marka = request.GET.get('marka')
    model = request.GET.get('model')
    renk = request.GET.get('renk')
    yil = request.GET.get('yil', '')
    km_min = request.GET.get('km_min', '')
    km_max = request.GET.get('km_max', '')
    fiyat_min = request.GET.get('fiyat_min', '')
    fiyat_max = request.GET.get('fiyat_max', '')
    kaza_raporu = request.GET.get('kaza_raporu', '')
    yakit_turu = request.GET.get('yakit_turu', '')
    vites_turu = request.GET.get('vites_turu', '')
    arac_durumu = request.GET.get('arac_durumu', '')
    takas_durumu = request.GET.get('takas_durumu', '')
    cekis = request.GET.get('cekis', '')
    motor_gucu = request.GET.get('motor_gucu', '')
    motor_hacmi = request.GET.get('motor_hacmi', '')
    cars = Car.objects.all()
    
    if marka:
        cars = cars.filter(marka=marka)
    if renk:
        cars = cars.filter(renk=renk)
    if model:
        cars = cars.filter(model=model)
    if yil:
        if yil == '2000once':
            cars = cars.filter(yil__lt=2000)
        elif yil == '2000_2005arasi':
            cars = cars.filter(yil_gte=2000, yil_lte=2005)
        elif yil == '2005_2010arasi':
            cars = cars.filter(yil_gte=2005, yil_lte=2010)
        elif yil == '2010_2020arasi':
            cars = cars.filter(yil_gte=2010, yil_lte=2020)
        elif yil == '2020sonra':
            cars = cars.filter(yil__gt=2020)
    if km_min or km_max:
        if km_min:
            cars = cars.filter(km__gte=int(km_min))
        if km_max:
            cars = cars.filter(km__lte=int(km_max))

    if fiyat_min or fiyat_max:
        if fiyat_min:
            cars = cars.filter(fiyat__gte=int(fiyat_min))
        if fiyat_max:
            cars = cars.filter(fiyat__lte=int(fiyat_max))
    if kaza_raporu:
        cars = cars.filter(kaza_raporu=kaza_raporu)
    if yakit_turu:
        cars = cars.filter(yakit_turu=yakit_turu)
    if vites_turu:
        cars = cars.filter(vites_turu=vites_turu)
    if arac_durumu:
        cars = cars.filter(arac_durumu=arac_durumu)
    if takas_durumu:
        cars = cars.filter(takas_durumu=takas_durumu)
    if cekis:
        cars = cars.filter(cekis=cekis)

    # Motor gücü aralığını temizleyip filtrelemek
    if motor_gucu:
        try:
            motor_gucu = float(motor_gucu)  # motor gücünü sayıya dönüştürme
            cars = cars.filter(motor_gucu__gte=motor_gucu)
        except ValueError:
            pass  # Hatalı değer girildiyse filtreyi uygulama

    if motor_hacmi:
        try:
            motor_hacmi = float(motor_hacmi)  # motor hacmini sayıya dönüştürme
            cars = cars.filter(motor_hacmi__gte=motor_hacmi)
        except ValueError:
            pass  # Hatalı değer girildiyse filtreyi uygulama

    return render(request, 'cars/home.html', {'cars': cars})

def collected_data(request):
    # Excel dosyasını oku
    user_profile = os.getenv("USERPROFILE")  # Windows kullanıcı profilini al
    file_path = os.path.join(user_profile, "Desktop", "DjangoProjem", "projefinal", "car_project", "Arac_Verileri_Yeni.xlsx")
    df = pd.read_excel(file_path)

    # Veriyi template'e gönder
    data = df.to_dict(orient='records')  # Veriyi dict formatında gönderiyoruz
    return render(request, 'cars/home.html', {'data': data})

def collected_data(request):
    # Excel dosyasını oku
    user_profile = os.getenv("USERPROFILE")  # Windows kullanıcı profilini al
    file_path = os.path.join(user_profile, "Desktop", "DjangoProjem", "projefinal", "car_project", "Arac_Verileri_Yeni.xlsx")
    df = pd.read_excel(file_path)

    # Filtreleme için GET parametrelerini al
    marka = request.GET.get('marka')
    renk = request.GET.get('renk')
    model = request.GET.get('model')
    yil = request.GET.get('yil')
    km_min = request.GET.get('km_min')
    km_max = request.GET.get('km_max')
    fiyat_min = request.GET.get('fiyat_min')
    fiyat_max = request.GET.get('fiyat_max')
    kaza_raporu = request.GET.get('kaza_raporu')
    yakit_turu = request.GET.get('yakit_turu')
    vites_turu = request.GET.get('vites_turu')
    arac_durumu = request.GET.get('arac_durumu')
    takas_durumu = request.GET.get('takas_durumu')
    cekis = request.GET.get('cekis')
    motor_gucu = request.GET.get('motor_gucu')
    motor_hacmi = request.GET.get('motor_hacmi')

    # Filtreleme işlemleri
    if marka:
        df = df[df['marka'].str.contains(marka, case=False, na=False)]
    if renk:
        df = df[df['renk'].str.contains(renk, case=False, na=False)]
    if model:
        df = df[df['model'].str.contains(model, case=False, na=False)]
    if yil:
        if yil == '2000once':
            df = df[df['yil'] < 2000]
        elif yil == '2000_2005arasi':
            df = df[(df['yil'] >= 2000) & (df['yil'] <= 2005)]
        elif yil == '2005_2010arasi':
            df = df[(df['yil'] >= 2005) & (df['yil'] <= 2010)]
        elif yil == '2010_2020arasi':
            df = df[(df['yil'] >= 2010) & (df['yil'] <= 2020)]
        elif yil == '2020sonra':
            df = df[df['yil'] > 2020]
    if km_min or km_max:
        if km_min:
            df = df[df['km'] >= int(km_min)]
        if km_max:
            df = df[df['km'] <= int(km_max)]
    if fiyat_min or fiyat_max:
        if fiyat_min:
            df = df[df['fiyat'] >= float(fiyat_min)]
        if fiyat_max:
            df = df[df['fiyat'] <= float(fiyat_max)]
    if kaza_raporu:
        df = df[df['kaza_raporu'].str.contains(kaza_raporu, case=False, na=False)]
    if yakit_turu:
        df = df[df['yakit_turu'].str.contains(yakit_turu, case=False, na=False)]
    if vites_turu:
        df = df[df['vites_turu'].str.contains(vites_turu, case=False, na=False)]
    if arac_durumu:
        df = df[df['arac_durumu'].str.contains(arac_durumu, case=False, na=False)]
    if takas_durumu:
        df = df[df['takas_durumu'].str.contains(takas_durumu, case=False, na=False)]
    if cekis:
        df = df[df['cekis'].str.contains(cekis, case=False, na=False)]
    
    # Motor gücü aralığını temizleyip filtrelemek
    if motor_gucu:
        try:
            motor_gucu = float(motor_gucu)  # motor gücünü sayıya dönüştürme
            df = df[df['motor_gucu'] >= motor_gucu]
        except ValueError:
            pass  # Hatalı değer girildiyse filtreyi uygulama

    if motor_hacmi:
        try:
            motor_hacmi = float(motor_hacmi)  # motor hacmini sayıya dönüştürme
            df = df[df['motor_hacmi'] >= motor_hacmi]
        except ValueError:
            pass  # Hatalı değer girildiyse filtreyi uygulama

    # Filtrelenmiş veriyi dict formatında gönder
    data = df.to_dict(orient='records')

    return render(request, 'cars/collected_data.html', {'data': data})

#Trend analizi sayfasında trendleri tablolaştır
def trend_analysis(request):

    # Excel dosyasını okuyun
    user_profile = os.getenv("USERPROFILE")  # Windows kullanıcı profilini al
    file_path = os.path.join(user_profile, "Desktop", "DjangoProjem", "projefinal", "car_project", "Araba_Verileri_Duzenli_pivot.xlsx")
    sheet_name = "Sayfa1"
    df = pd.read_excel(file_path, sheet_name=sheet_name)

    # İstatistik Analizleri
    stats = {
    "highest_prices": df.nlargest(5, "Fiyat")[["Marka", "Model", "Fiyat"]].to_dict(orient="records"),
    "top_cities": df["Şehir"].value_counts().head(5).to_dict(),
    "popular_colors": df["Renk"].value_counts().head(5).to_dict(),
    "popular_brands": df["Marka"].value_counts().head(5).to_dict(),
    "oldest_cars": df.nsmallest(5, "Yıl")[["Marka", "Model", "Yıl"]].to_dict(orient="records"),
    "newest_cars": df.nlargest(5, "Yıl")[["Marka", "Model", "Yıl"]].to_dict(orient="records"),
    "highest_km": df.nlargest(5, "KM")[["Marka", "Model", "KM"]].to_dict(orient="records"),
    "lowest_km": df.nsmallest(5, "KM")[["Marka", "Model", "KM"]].to_dict(orient="records"),
    "avg_prices_by_city": df.groupby("Şehir")["Fiyat"].mean().nlargest(5).to_dict(),
    "popular_fuel_types": df["Yakıt Türü"].value_counts().head(5).to_dict(),
    "popular_transmissions": df["Vites Türü"].value_counts().head(5).to_dict(),
    "top_conditions": df["Araç Durumu"].value_counts().head(5).to_dict(),
    "popular_body_types": df["Kasa Tipi"].value_counts().head(5).to_dict(),
    }


    return render(request, "cars/trend_analysis.html",stats)