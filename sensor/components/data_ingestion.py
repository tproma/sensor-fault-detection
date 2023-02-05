from sensor.exception import SensorException
from sensor.logger import logging
from sensor.entity.config_entity import DataIngestionConfig
from sensor.entity.artifact_entity import DataIngestionArtifact
from sensor.data_accsess.sensor_data import SensorData
from pandas import DataFrame
import os, sys


class DataIngestion:

    def __init__(self, data_ingestion_config: DataIngestionConfig):
        try:
            self.data_ingestion_config = data_ingestion_config
        except Exception as e:
            raise SensorException(e,sys)
    
    def export_data_into_feature_store(self) -> DataFrame:
        """
        Export Mongo db collection record as data frame into feature
        """
        try:
            logging.info("exporting data from mongodb to feature store")
            sensor_data = SensorData()
            dataframe = sensor_data.export_collection_as_dataframe(collection_name=self.data_ingestion_config.collection_name)
            feature_store_file_path= self.data_ingestion_config.feature_store_file_path

            #creating folder
            dir_path = os.path.dirname(feature_store_file_path)
            os.mkdir(dir_path, exist_ok = True)

            dataframe.to_csv(feature_store_file_path, index = False, header=True)
            return dataframe



        except Exception as e:
            raise SensorException(e,sys)

    def split_data_as_train_test(self, dataframe: DataFrame) -> None:
        """
        Feature store dataset will be split into train and test file
        """
        
        pass


    def initiate_data_ingestion(self) -> DataIngestionArtifact:
        try:
            pass
        except Exception as e:
            raise SensorException(e,sys)
