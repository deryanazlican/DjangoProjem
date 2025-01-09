import json
from .models import Car
import pandas as pd

def load_data_to_db(json_file="car_data.json"):
    with open(json_file, "r", encoding="utf-8") as f:
        data_list = json.load(f)
        for data in data_list:
            Car.objects.create(**data)

def export_to_excel():
    cars = Car.objects.all().values()
    df = pd.DataFrame(cars)
    df.to_excel('cars.xlsx', index=False)
    