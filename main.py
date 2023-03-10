from sensor.configuration.mongo_db_connection import MongoDBClient
from sensor.exception import SensorException
import os,sys
from sensor.logger import logging
from sensor.pipeline.training_pipeline import TrainPipeline
#from sensor.entity.config_entity import TrainingPipelineConfig, DataIngestionConfig


from fastapi import FastAPI
from sensor.constant.application import APP_HOST, APP_PORT
from starlette.responses import RedirectResponse
from uvicorn import run as app_run
from fastapi.responses import Response
from fastapi.middleware.cors import CORSMiddleware

from sensor.utils.main_utils import read_yaml_file, load_object
from sensor.constant.training_pipeline import SAVED_MODEL_DIR
from sensor.ml.model.estimator import ModelResolver, TargetValueMapping


#MongoDB code


app = FastAPI()

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)



@app.get("/", tags=["authentication"])
async def index():
   return RedirectResponse(url = "/docs")


@app.get("/train")
async def train_route():
   try:
      train_pipeline = TrainPipeline()
      if train_pipeline.is_pipeline_running:
         return Response("Training pipeline is aalready running.")
      train_pipeline.run_pipeline()
      return Response("Training successful !")
   except Exception as e:
      raise Response(f"Error occured! {e}")

@app.get("/predict")
async def predict_route():
   try:
      ###
      ###
      df = None
      
      
      model_resolver = ModelResolver(model_dir = SAVED_MODEL_DIR)
      if not model_resolver.is_model_exists():
         return Response("Model is not available.")

      best_model_path = model_resolver.get_best_model_path()
      model= load_object(file_path=best_model_path)
      y_pred = model.predict(df)
      df['predicted-column'] = y_pred
      df['predicted_column'].replace(TargetValueMapping().reverse_mapping(), inplace = True)
      
      ###

   except Exception as e:
      raise Response(f"Error occured! {e}")



def main():
   try:
      train_pipeline = TrainPipeline()
      train_pipeline.run_pipeline()
   except Exception as e:
      print(e)
      logging.exception(e)
   


if __name__=="__main__":
   app_run(app , host=APP_HOST, port = APP_PORT)



"""
    training_pipeline_config = TrainingPipelineConfig()
    data_ingestion_config = DataIngestionConfig(training_pipeline_config=training_pipeline_config )
    print(data_ingestion_config.__dict__)
"""

   # mongodb_client = MongoDBClient()
   # print("collection name:", mongodb_client.database.list_collection_names())
    