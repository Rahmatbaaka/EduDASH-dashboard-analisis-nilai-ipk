from abc import ABC, abstractmethod
import pandas as pd
import joblib
import os
from django.http import HttpResponse

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
        """OOP Abstraksi: Mengambil data dari SQL melalui Django ORM alih-alih CSV"""
        from .models import Mahasiswa
        queryset = Mahasiswa.objects.all().values()
        if queryset.exists():
            self.__dataset = pd.DataFrame(list(queryset))
            print("=== SUCCESS: Dataset loaded from SQL Database via ORM ===")
        else:
            print("=== WARNING: SQL Database is empty! Harap jalankan migrasi data CSV. ===")
            self.__dataset = pd.DataFrame()
        return self.__dataset

    def get_avg_ipk(self):
        if self.__dataset is not None:
            return round(self.__dataset['ipk'].mean(), 2)
        return 0.0

    def predict(self, input_data: dict):
        if not self.__is_loaded:
            self.load_model()
        
        try:
            l_in = input_data.get('memiliki_laptop')
            laptop_val = 1 if str(l_in) in ['1', '1.0', 'yes', 'True'] or l_in in [1, 1.0, True] else 0

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
    
class BaseExporter(ABC):
    """Abstract Class sebagai cetak biru untuk semua jenis exporter"""
    @abstractmethod
    def export_data(self, data):
        pass

class CSVHistoryExporter(BaseExporter):
    """Polimorfisme: Mengunduh data ke dalam format CSV"""
    def export_data(self, queryset):
        df = pd.DataFrame(list(queryset.values(
            'tidur', 'belajar', 'bermain', 'sosmed', 'kopi', 'olahraga', 'laptop', 'hasil_ipk', 'waktu_prediksi'
        )))
        
        if not df.empty and 'waktu_prediksi' in df.columns:
            df['waktu_prediksi'] = pd.to_datetime(df['waktu_prediksi']).dt.strftime('%Y-%m-%d %H:%M')

        return self.export_dataframe(df, "riwayat_prediksi.csv")

    def export_dataframe(self, df, filename):
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = f'attachment; filename="{filename}"'
        df.to_csv(path_or_buf=response, index=False)
        return response


class ExcelHistoryExporter(BaseExporter):
    """Polimorfisme: Mengunduh data ke dalam format Excel"""
    def export_data(self, queryset):
        df = pd.DataFrame(list(queryset.values(
            'tidur', 'belajar', 'bermain', 'sosmed', 'kopi', 'olahraga', 'laptop', 'hasil_ipk', 'waktu_prediksi'
        )))
        
        if not df.empty and 'waktu_prediksi' in df.columns:
            df['waktu_prediksi'] = pd.to_datetime(df['waktu_prediksi']).dt.tz_localize(None)
        
        return self.export_dataframe(df, "riwayat_prediksi.xlsx")

    def export_dataframe(self, df, filename):
        response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
        response['Content-Disposition'] = f'attachment; filename="{filename}"'
        
        with pd.ExcelWriter(response, engine='openpyxl') as writer:
            df.to_excel(writer, index=False, sheet_name='Dataset')
            
        return response