import os
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor

# Veriyi yükle
user_profile = os.getenv("USERPROFILE")  # Windows kullanıcı profilini al
file_path = os.path.join(user_profile, "Desktop", "DjangoProjem", "projefinal", "car_project", "Araba_Verileri_Duzenli_pivot.xlsx")
data = pd.read_excel(file_path)  # Excel dosyasının adını değiştir
features = data[['Marka', 'Renk', 'KM']]
target = data['Fiyat']

# Kategorik verileri dönüştür
features = pd.get_dummies(features)

# Veriyi böl
X_train, X_test, y_train, y_test = train_test_split(features, target, test_size=0.2, random_state=42)

# Modeli eğit
model = RandomForestRegressor()
model.fit(X_train, y_train)

# Modeli kaydet
import joblib
joblib.dump(model, 'price_model.pkl')