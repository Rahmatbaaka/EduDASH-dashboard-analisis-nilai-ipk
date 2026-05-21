from abc import ABC, abstractmethod
import pandas as pd
import joblib
import os

class BasePredictionModel(ABC):
    @abstractmethod
    def load_model(self):
        pass

    @abstractmethod
    def predict(self, input_data: dict):
        pass

    @abstractmethod
    def load_dataset(self, dataset_path: str = None):
        pass

class AcademicPerformanceModel(BasePredictionModel):
    def __init__(self, model_name, model_path=None, dataset_path=None):
        self.__model_name = model_name 
        self.__is_loaded = False
        self.__model_instance = None
        self.__dataset_path = dataset_path
        self.__dataset = None
        self.__model_path = model_path

    def _get_model_status(self):
        return f"Model {self.__model_name} Loaded: {self.__is_loaded}"

    def load_model(self):
        if self.__is_loaded:
            return self._get_model_status()

        if self.__model_path and os.path.exists(self.__model_path):
            try:
                self.__model_instance = joblib.load(self.__model_path)
                self.__is_loaded = True
                print(f"=== SUCCESS: Model {self.__model_name} loaded from {self.__model_path} ===")
            except Exception as e:
                print(f"=== ERROR: Failed to load model from {self.__model_path}: {e} ===")
                self.__model_instance = None
        else:
            print(f"=== ERROR: Model file NOT FOUND at {self.__model_path} ===")
        return self._get_model_status()

    def load_dataset(self, dataset_path: str = None):
        if self.__dataset is not None:
            return self.__dataset

        path = dataset_path or self.__dataset_path
        if path and os.path.exists(path):
            try:
                self.__dataset = pd.read_csv(path)
                print(f"=== Dataset loaded successfully from {path} ===")
                return self.__dataset
            except Exception as e:
                print(f"Error loading dataset from {path}: {e}")
                self.__dataset = None
        else:
            print(f"Dataset path not provided or file not found: {path}")
            self.__dataset = None
        return self.__dataset

    def get_avg_ipk(self):
        if self.__dataset is not None:
            return round(self.__dataset['ipk'].mean(), 2)
        return 0.0

    def predict(self, input_data: dict):
        if not self.__is_loaded:
            self.load_model()
        
        try:
            laptop_input = input_data.get('memiliki_laptop')
            laptop_val = 1 if laptop_input in ['yes', '1', 1, True] else 0

            feature_dict = {
                'rata2_tidur_hari': [float(input_data.get('rata2_tidur_hari', 0) or 0)],
                'rata2_belajar_hari': [float(input_data.get('rata2_belajar_hari', 0) or 0)],
                'rata2_buka_sosmed_hari': [float(input_data.get('rata2_buka_sosmed_hari', 0) or 0)],
                'jumlah_kopi_hari': [float(input_data.get('jumlah_kopi_hari', 0) or 0)],
                'rata2_olahraga_hari': [float(input_data.get('rata2_olahraga_hari', 0) or 0)],
                'memiliki_laptop': [laptop_val],
                'rata2_bermain_game_hari': [float(input_data.get('rata2_bermain_game_hari', 0) or 0)]
            }
            
            input_df = pd.DataFrame(feature_dict)
            
            if self.__model_instance and hasattr(self.__model_instance, 'predict'):
                prediction = self.__model_instance.predict(input_df)
                return round(float(prediction[0]), 2)
        except Exception as e:
            print(f"Prediction error: {e}")
            
        return None