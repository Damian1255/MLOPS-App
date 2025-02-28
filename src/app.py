import os
import json
import hydra
import numpy as np
import pandas as pd
import src.preprocess as preprocess
import src.functions as functions
import pycaret.regression as pr
from omegaconf import DictConfig
import pycaret.classification as pc
from flask import Flask, request, render_template, jsonify


app = Flask(__name__, template_folder="../templates", static_folder="../static")
pp = preprocess.Preprocessors()
fn = functions.Functions()

@hydra.main(config_path="../config", config_name="config.yaml")
def load_models(cfg: DictConfig):
    global variables 
    variables = cfg

    return variables

load_models()

car_prices_model = pr.load_model(variables.model.car_prices.path)
car_prices_data = pd.read_excel(variables.data.car_prices.processed.path)
car_prices_colums = variables.columns.car_prices


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


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))
    app.run(debug=True, port=port)
