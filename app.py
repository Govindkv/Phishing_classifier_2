from flask import Flask, render_template, jsonify, request, send_file
from src.Phishing_classifier_2.exception import CustomException
from src.Phishing_classifier_2.logger import logging as lg
import os, sys
from src.Phishing_classifier_2.pipeline import train_pipeline, prediction_pipeline
from src.Phishing_classifier_2.pipeline.train_pipeline import TrainingPipeline
from src.Phishing_classifier_2.pipeline.prediction_pipeline import PredictionPipeline


app =  Flask(__name__)

@app.route("/")
def home():
    return "Welcome to the Phishing Website Detection Application."

@app.route("/train")
def train_route():
    train_pipeline = TrainingPipeline()
    train_pipeline.run_pipeline()

    return "Training is complete."

@app.route("/predict", methods=["POST", "GET"])
def upload():
    try:
        if request.method == "POST":
            prediction_pipeline = PredictionPipeline(request)

            prediction_file_detail = prediction_pipeline.run_pipeline()

            lg.info("Prediction is complete. Dowloading prediction file.")

            return send_file(prediction_file_detail.prediction_file_path,
                             download_name=prediction_file_detail.prediction_file_name,
                             as_attachment=True)
        else:
            return render_template("Upload_file.html")
    
    except Exception as e:
        raise CustomException(e, sys)

if __name__=="__main__":
    app.run(host="0.0.0.0", port = 5000, debug=True)