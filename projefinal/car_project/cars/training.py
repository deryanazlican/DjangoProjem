import os
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import Lasso
from sklearn.preprocessing import StandardScaler
import joblib

# Veriyi yükle
user_profile = os.getenv("USERPROFILE")  # Windows kullanıcı profilini al
excel_path = os.path.join(user_profile, "Desktop", "DjangoProjem", "projefinal", "car_project", "Araba_Verileri_Duzenli.xlsx")
data = pd.read_excel(excel_path)

# Özellikler ve hedef
features = data[['Marka', 'Model', 'Yıl', 'KM', 'Şehir', 'Kaza Raporu', 'Renk', 'Yakıt Türü', 
                 'Vites Türü', 'Araç Durumu', 'Takas Durumu', 'Çekiş', 'Motor Hacmi', 'Motor Gücü', 
                 'Kasa Tipi', 'Kimden']]  # Tüm gerekli özellikler
target = data['Fiyat']  # Hedef değişken: Fiyat

# Kategorik verileri sayısal verilere dönüştür
features = pd.get_dummies(features)  # Kategorik verileri sayısallaştır

# Veriyi standartlaştırma
scaler = StandardScaler()
X_scaled = scaler.fit_transform(features)

# Eğitim ve test setlerine ayırma (80% eğitim, 20% test)
X_train, X_test, y_train, y_test = train_test_split(X_scaled, target, test_size=0.2, random_state=42)

# Lasso Regression modelini oluştur ve eğit
model = Lasso(alpha=0.1)  # alpha parametresi düzenleme gücünü belirler
model.fit(X_train, y_train)

# Modelin doğruluğunu kontrol et
accuracy = model.score(X_test, y_test)
print(f"Lasso Regression Modelinin doğruluğu: {accuracy * 100:.2f}%")

# Modeli kaydet (gelecekte tahmin için kullanmak üzere)
joblib.dump(model, 'lasso_price_model.pkl')

# Scaler'ı kaydet
joblib.dump(scaler, 'scaler.pkl')

# Kullanılan kolonları kaydet
joblib.dump(features.columns, 'model_columns.pkl')