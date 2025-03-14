import os
import json
import hydra
import numpy as np
import pandas as pd
import src.preprocess as preprocess
import src.functions as functions
import pycaret.regression as pr
from hydra import initialize, compose
from omegaconf import DictConfig
import pycaret.classification as pc
from flask import Flask, request, render_template, jsonify


app = Flask(__name__, template_folder="templates", static_folder="static")
pp = preprocess.Preprocessors()
fn = functions.Functions()

global variables 
with initialize(version_base=None, config_path="config"):
    cfg = compose(config_name="config")
    variables = cfg

car_prices_model = pr.load_model(variables.model.car_prices.path)
car_prices_data = pd.read_excel(variables.data.car_prices.processed.path)
house_prices_model = pc.load_model(variables.model.house_prices.path)
house_prices_data = pd.read_csv(variables.data.house_prices.raw.path)
wheat_prices_data = pd.read_csv(variables.data.wheat_prices.raw.path)
wheat_prices_model = pc.load_model(variables.model.wheat_prices.path)


@app.route("/")
def home():
    return render_template("home.html")


@app.route("/predict/car-price", methods=["GET", "POST"])
def car_prices_page(): 
    if request.method == "POST":
        convert_to_object = ["Seats", "Year"]
        convert_to_int = ["Mileage", "Engine", "Power"]

        attributes = fn.get_column_attributes(car_prices_data, convert_to_object, convert_to_int)
        return jsonify({"attributes": attributes})
    else:
        return render_template("carprices.html")


@app.route("/predict/house-price", methods=["GET", "POST"])
def house_prices_page(): 
    if request.method == "POST":
        convert_to_object = []
        convert_to_int = []

        attributes = fn.get_column_attributes(house_prices_data, convert_to_object, convert_to_int)
        return jsonify({"attributes": attributes})
    else:
        return render_template("houseprices.html")
    

@app.route("/api/predict/car-price", methods=["POST"])
def predict_car_prices():
    # convert request data to dataframe
    data = request.json
    data_df = pd.DataFrame(data, index=[0])
    data_df = pp.preprocess_car_data(data_df)

    # predict
    prediction = pr.predict_model(car_prices_model, data=data_df)
    prediction = prediction["prediction_label"].values[0]

    # return prediction
    return jsonify({"prediction": prediction})


@app.route("/api/predict/house-price", methods=["POST"])
def predict_house_prices():
    # convert request data to dataframe
    data = request.json
    data_df = pd.DataFrame(data, index=[0])
    data_df = pp.preprocess_house_data(data_df)
    # predict
    prediction = pr.predict_model(house_prices_model, data=data_df)
    prediction = prediction["prediction_label"].values[0]

    # return prediction
    return jsonify({"prediction": prediction})


@app.route("/predict/wheat-type", methods=["GET", "POST"])
def wheat_prices_page(): 
    if request.method == "POST":
        convert_to_object = []
        convert_to_int = ["Area", "Groove",
                          "Length", "Perimeter", "Width"]

        attributes = fn.get_column_attributes(wheat_prices_data, convert_to_object, convert_to_int)
        return jsonify({"attributes": attributes})
    else:
        return render_template("wheatprices.html")


@app.route("/api/predict/wheat-type", methods=["POST"])
def predict_wheat_prices():
    # convert request data to dataframe
    data = request.json
    data_df = pd.DataFrame(data, index=[0])
    data_df = pp.preprocess_wheat_data(data_df)
    # predict
    prediction = pr.predict_model(wheat_prices_model, data=data_df)
    prediction = prediction["prediction_label"].values[0]
    # return prediction
    return jsonify({"prediction": str(prediction)})


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))
    app.run(debug=True, host="0.0.0.0", port=port)
