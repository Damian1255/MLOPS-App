import numpy as np
import pandas as pd

class Preprocessors:
    def __init__(self):
        pass

    def extract_brand(self, entry):
        parts = entry.capitalize().split()
        if len(parts) >= 2 and parts[0] == 'Land' and parts[1] == 'rover':
            return 'Land Rover'
        else:
            return parts[0]    

    def preprocess_car_data(self, data):
        luxury_brands = [
        'audi', 'bmw', 'mercedes-benz', 
        'porsche', 'jaguar', 'land rover',
        'volvo', 'bentley', 'lamborghini'
        ]
        
        data['Mileage'] = data['Mileage'].str.extract('(\d+\.?\d*)')[0].astype(float)
        data['Engine'] = data['Engine'].str.extract('(\d+)')[0].astype(float)
        data['Power'] = data['Power'].str.extract('(\d+\.?\d*)')[0].astype(float)
        data["Brand"] = data["Brand_Model"].apply(self.extract_brand)
        data['Luxury_Flag'] = data['Brand'].str.lower().isin(luxury_brands).astype(int)

        # convert year to numeric
        data["Year"] = data["Year"].astype(int)
        data["Kilometers_Driven"] = data["Kilometers_Driven"].astype(int)
        data["Seats"] = data["Seats"].astype(float)
        data["Mileage"] = data["Mileage"].astype(float)
        data["Engine"] = data["Engine"].astype(float)
        data["Power"] = data["Power"].astype(float)
        data["Luxury_Flag"] = data["Luxury_Flag"].astype(int)
        
        return data
    
    def preprocess_house_data(self, data):
        data['Log_Price'] = 0
        data['Date'] = pd.to_datetime(data['Date'], format='%d/%m/%Y')
        data['Rooms'] = data['Rooms'].astype(int)
        data['Distance'] = data['Distance'].astype(float)
        data['Bathroom'] = data['Bathroom'].astype(int)
        data['Car'] = data['Car'].astype(int)
        data['Landsize'] = data['Landsize'].astype(float)
        data['BuildingArea'] = data['BuildingArea'].astype(float)
        data['YearBuilt'] = data['YearBuilt'].astype(int)
        data['Postcode'] = data['Postcode'].astype(int)
        data['Propertycount'] = data['Propertycount'].astype(int)
        data['Bedroom2'] = data['Bedroom2'].astype(int)
        data['Longtitude'] = data['Longtitude'].astype(float)
        data['Lattitude'] = data['Lattitude'].astype(float)
        

        return data