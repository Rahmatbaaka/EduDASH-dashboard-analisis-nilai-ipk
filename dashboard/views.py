import json
import os
import pandas as pd
from django.shortcuts import render
from django.conf import settings
from .services import AcademicPerformanceModel

# =====================================================================
# INITIALIZATION: LOAD MODEL & DATASET GLOBAL (BAWAAN ANDA)
# =====================================================================
MODEL_PATH = os.path.join(settings.BASE_DIR, 'dashboard', 'models', 'model.joblib')
DATASET_PATH = os.path.join(settings.BASE_DIR, 'dashboard', 'data', 'dataset_ipk.csv')

model_service = AcademicPerformanceModel(
    model_name="Student Performance Model",
    model_path=MODEL_PATH,
    dataset_path=DATASET_PATH
)

df_global = model_service.load_dataset() 


# =====================================================================
# IMPLEMENTASI OOP: CLASS UNTUK PEMROSESAN DATA GRAFIK
# =====================================================================
class DashboardDataProcessor:
    def __init__(self, dataframe):
        self.df = dataframe.copy()

    def get_color_mapping(self, ipk_val):
        """Helper OOP untuk menentukan warna berdasarkan standar IPK"""
        if ipk_val > 3.5: return "#0E1B7189" 
        if ipk_val > 3.0: return "#0da13eaf" 
        if ipk_val > 2.0: return "#a92f2fce" 
        return '#ef4444' 

    def process_chart1_hustle(self):
        """Format Bubble Chart: x=Belajar, y=Tidur, r=Kopi"""
        return [
            {
                'x': float(row['rata2_belajar_hari']),
                'y': float(row['rata2_tidur_hari']),
                'r': float(row['jumlah_kopi_hari'] * 4 + 4),
                'ipk': float(row['ipk']),
                'color': self.get_color_mapping(row['ipk'])
            }
            for _, row in self.df.iterrows()
        ]

    def process_chart2_distraction(self):
        """Format Scatter Chart: x=Game, y=Sosmed"""
        return [
            {
                'x': float(row['rata2_bermain_game_hari']),
                'y': float(row['rata2_buka_sosmed_hari']),
                'color': self.get_color_mapping(row['ipk'])
            }
            for _, row in self.df.iterrows()
        ]

    def process_chart3_support_gap(self):
        high = self.df[self.df['ipk'] > 3.5][['rata2_belajar_hari', 'rata2_tidur_hari', 'rata2_olahraga_hari']].mean().tolist()
        low = self.df[self.df['ipk'] <= 3.0][['rata2_belajar_hari', 'rata2_tidur_hari', 'rata2_olahraga_hari']].mean().tolist()
        return {'high': high, 'low': low}

    def process_chart4_equity(self):
        laptop_gap = self.df.groupby('memiliki_laptop')['ipk'].mean().to_dict()
        work_gap = self.df.groupby('bekerja')['ipk'].mean().to_dict()
        return {
            'labels': ['Punya Laptop', 'Tanpa Laptop', 'Tidak Bekerja', 'Bekerja'],
            'datasets': [{
                'label': 'Rata-rata IPK',
                'data': [laptop_gap.get(1, 0), laptop_gap.get(0, 0), work_gap.get(0, 0), work_gap.get(1, 0)],
                'backgroundColor': ['#3b82f6', '#60a5fa', '#f59e0b', '#fbbf24']
            }]
        }

    def process_chart5_anomaly(self):
        return [
            {
                'x': float(row['rata2_belajar_hari']),
                'y': float(row['ipk']),
                'color': self.get_color_mapping(row['ipk'])
            }
            for _, row in self.df.iterrows()
        ]

    def process_chart6_tipping_point(self):
        """Memproses Chart 6: Korelasi Jam Tidur terhadap IPK"""
        return [
            {
                'x': float(row['rata2_tidur_hari']),
                'y': float(row['ipk']),
                'color': self.get_color_mapping(row['ipk'])
            }
            for _, row in self.df.iterrows()
        ]

    def process_chart7_institutional(self):
        """Memproses Chart 7: Rata-rata IPK berdasarkan Asal Sekolah"""
        school_gap = self.df.groupby('asal_sekolah')['ipk'].mean().to_dict()
        return {
            'labels': list(school_gap.keys()),
            'values': [float(v) for v in school_gap.values()]
        }


# =====================================================================
# DJANGO VIEW FUNCTION
# =====================================================================
def dashboard_view(request):
    if df_global is None:
        return render(request, 'dashboard.html', {'error': 'Data tidak ditemukan'})

    processor = DashboardDataProcessor(df_global)
    
    chart1_data = processor.process_chart1_hustle()
    chart2_data = processor.process_chart2_distraction()
    chart3_data = processor.process_chart3_support_gap()
    chart4_data = processor.process_chart4_equity()
    chart5_data = processor.process_chart5_anomaly()
    chart6_data = processor.process_chart6_tipping_point()
    chart7_data = processor.process_chart7_institutional()

    prediction_result = ""
    active_menu = 'artikel'
    
    if request.method == 'POST':
        active_menu = 'prediksi'
        
        def safe_float(val, default=0.0):
            try:
                if val is None or str(val).strip() == '':
                    return default
                return float(val)
            except (ValueError, TypeError):
                return default

        try:
            input_data = {
                'rata2_tidur_hari': safe_float(request.POST.get('tidur'), default=6.0),
                'rata2_belajar_hari': safe_float(request.POST.get('belajar'), default=4.0),
                'rata2_bermain_game_hari': safe_float(request.POST.get('bermain'), default=2.0),
                'rata2_buka_sosmed_hari': safe_float(request.POST.get('sosmed'), default=2.0),
                'jumlah_kopi_hari': safe_float(request.POST.get('kopi'), default=0.0),
                'rata2_olahraga_hari': safe_float(request.POST.get('olahraga'), default=1.0),
                'memiliki_laptop': safe_float(request.POST.get('laptop'), default=1.0),
            }
            
            prediction_result = model_service.predict(input_data)
            
        except Exception as e:
            print(f"Error during prediction: {e}")

    context = {
        'chart1_json': json.dumps(chart1_data), 
        'chart2_json': json.dumps(chart2_data), 
        'chart3_json': json.dumps(chart3_data), 
        'chart4_json': json.dumps(chart4_data), 
        'chart5_json': json.dumps(chart5_data), 
        'chart6_json': json.dumps(chart6_data), 
        'chart7_json': json.dumps(chart7_data), 
        'prediction': prediction_result,
        'active_menu': active_menu,
    }

    return render(request, 'dashboard.html', context)