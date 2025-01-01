import os, sys

from Phishing_classifier_2.components import data_ingestion
from Phishing_classifier_2.components import data_transformation
from Phishing_classifier_2.components import model_trainer
from src.Phishing_classifier_2.components.data_ingestion import DataIngestion
from src.Phishing_classifier_2.components.data_transformation import DataTransformation
from src.Phishing_classifier_2.components.model_trainer import ModelTrainer
from src.Phishing_classifier_2.exception import CustomException


class TrainingPipeline:

    def start_data_ingestion(self):
        try:
            data_ingestion = DataIngestion()
            feature_store_file_path = data_ingestion.initiate_data_ingestion()
            return feature_store_file_path
        except Exception as e:
            raise CustomException(e,sys)
        
    def start_data_transformation(self, feature_store_file_path):
        try:
            data_transformation = DataTransformation(feature_store_file_path=feature_store_file_path)
            train_arr, test_arr, preprocessor_path = data_transformation.initiate_data_transformation()
            return train_arr, test_arr, preprocessor_path
        
        except Exception as e:
            raise CustomException(e, sys)
    def start_model_training(self, train_arr, test_arr):
        try:
            model_trainer = ModelTrainer()
            model_score = model_trainer.initiate_model_trainer(
                train_arr, test_arr
            )

            return model_score
        except Exception as e:
            raise CustomException(e, sys)
        
    def run_pipeline(self):
        try:
            feature_store_file_path = self.start_data_ingestion()
            train_arr, test_arr, preprocessor_path = self.start_data_transformation()
            r2_score = self.start_model_training(train_arr, test_arr)

            print("Training completed. Trained model score: ", r2_score)

        except Exception as e:
            raise CustomException(e, sys)