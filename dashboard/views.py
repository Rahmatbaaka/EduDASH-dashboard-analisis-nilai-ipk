import json
import os
import pandas as pd
from django.shortcuts import render, HttpResponse, redirect
from django.conf import settings
from .services import AcademicPerformanceModel
from .models import PredictionLog, Mahasiswa
from .services import CSVHistoryExporter, ExcelHistoryExporter

MODEL_PATH = os.path.join(settings.BASE_DIR, 'dashboard', 'models', 'model.joblib')
DATASET_PATH = os.path.join(settings.BASE_DIR, 'dashboard', 'data', 'dataset_ipk.csv')

model_service = AcademicPerformanceModel(
    model_name="Student Performance Model",
    model_path=MODEL_PATH,
    dataset_path=DATASET_PATH
)

class DashboardDataProcessor:
    def __init__(self, dataframe):
        self.df = dataframe.copy().fillna(0)

    def get_color_mapping(self, ipk_val):
        try:
            ipk_val = float(ipk_val)
        except:
            ipk_val = 0.0
            
        if ipk_val > 3.5: return "#10B981"
        if ipk_val > 3.0: return "#008080"
        if ipk_val > 2.5: return "#556B2F"
        return '#333333'

    def process_chart1_hustle(self):
        return [
            {
                'x': float(row.get('rata2_belajar_hari', 0)),
                'y': float(row.get('rata2_tidur_hari', 0)),
                'r': float(row.get('jumlah_kopi_hari', 0) * 4 + 4),
                'ipk': float(row.get('ipk', 0)),
                'color': self.get_color_mapping(row.get('ipk', 0))
            }
            for _, row in self.df.iterrows()
        ]

    def process_chart2_distraction(self):
        return [
            {
                'x': float(row.get('rata2_bermain_game_hari', 0)),
                'y': float(row.get('rata2_buka_sosmed_hari', 0)),
                'color': self.get_color_mapping(row.get('ipk', 0))
            }
            for _, row in self.df.iterrows()
        ]

    def process_chart3_support_gap(self):
        cols = ['rata2_belajar_hari', 'rata2_tidur_hari', 'rata2_olahraga_hari', 'memiliki_laptop']
        high_df = self.df[self.df['ipk'] > 3.5][cols]
        low_df = self.df[self.df['ipk'] <= 3.0][cols]
        
        high = high_df.mean().fillna(0).tolist() if not high_df.empty else [0, 0, 0, 0]
        low = low_df.mean().fillna(0).tolist() if not low_df.empty else [0, 0, 0, 0]
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
                'x': float(row.get('rata2_belajar_hari', 0)),
                'y': float(row.get('ipk', 0)),
                'r': 6,
                'color': self.get_color_mapping(row.get('ipk', 0))
            }
            for _, row in self.df.iterrows()
        ]

    def process_chart6_tipping_point(self):
        return [
            {
                'x': float(row.get('rata2_tidur_hari', 0)),
                'y': float(row.get('ipk', 0)),
                'prob_low_ipk': 0.8 if float(row.get('ipk', 0)) < 3.0 else 0.2, 
                'color': self.get_color_mapping(row.get('ipk', 0))
            }
            for _, row in self.df.iterrows()
        ]

    def process_chart7_institutional(self):
        school_gap = self.df.groupby('asal_sekolah')['ipk'].mean().fillna(0).to_dict()
        return {
            'labels': list(school_gap.keys()),
            'values': [float(v) for v in school_gap.values()]
        }

def _get_filtered_dataset(request):
    f_gender = request.GET.get('f_gender', 'all')
    f_sekolah = request.GET.get('f_sekolah', 'all')
    f_laptop = request.GET.get('f_laptop', 'all')
    f_bekerja = request.GET.get('f_bekerja', 'all')

    query = Mahasiswa.objects.all()

    gender_map = {'Laki-laki': 'male', 'Perempuan': 'female'}
    target_gender = gender_map.get(f_gender, f_gender)

    if f_gender != 'all':
        query = query.filter(gender=target_gender)
    if f_sekolah != 'all':
        query = query.filter(asal_sekolah=f_sekolah)
    if f_laptop != 'all':
        query = query.filter(memiliki_laptop=int(f_laptop))
    if f_bekerja != 'all':
        query = query.filter(bekerja=int(f_bekerja))

    df_filtered = pd.DataFrame(list(query.values()))
    return df_filtered if not df_filtered.empty else pd.DataFrame(columns=['ipk', 'gender', 'asal_sekolah'])

def dashboard_view(request):
    df_filtered = _get_filtered_dataset(request)

    if df_filtered is None or (df_filtered.empty and 'ipk' not in df_filtered.columns):
        return render(request, 'dashboard.html', {'error': 'Data tidak ditemukan'})

    kpi_total = len(df_filtered)
    
    kpi_avg_ipk = df_filtered['ipk'].mean() if kpi_total > 0 and 'ipk' in df_filtered.columns else 0.0
    if pd.isna(kpi_avg_ipk): kpi_avg_ipk = 0.0
    
    kpi_pct_high = (len(df_filtered[df_filtered['ipk'] > 3.5]) / kpi_total * 100) if kpi_total > 0 and 'ipk' in df_filtered.columns else 0.0
    if pd.isna(kpi_pct_high): kpi_pct_high = 0.0

    processor = DashboardDataProcessor(df_filtered)
    
    chart1_data = processor.process_chart1_hustle()
    chart2_data = processor.process_chart2_distraction()
    chart3_data = processor.process_chart3_support_gap()
    chart4_data = processor.process_chart4_equity()
    chart5_data = processor.process_chart5_anomaly()
    chart6_data = processor.process_chart6_tipping_point()
    chart7_data = processor.process_chart7_institutional()

    prediction_result = ""
    active_menu = 'visualisasi'
    
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
            
            raw_prediction = model_service.predict(input_data)
            
            prediction_result = min(4.00, max(0.00, float(raw_prediction)))
            
            PredictionLog.objects.create(
                tidur=input_data['rata2_tidur_hari'],
                belajar=input_data['rata2_belajar_hari'],
                bermain=input_data['rata2_bermain_game_hari'],
                sosmed=input_data['rata2_buka_sosmed_hari'],
                kopi=input_data['jumlah_kopi_hari'],
                olahraga=input_data['rata2_olahraga_hari'],
                laptop=int(input_data['memiliki_laptop']),
                hasil_ipk=prediction_result
            )
            
        except Exception as e:
            print(f"Error during prediction: {e}")

    riwayat_prediksi = PredictionLog.objects.all().order_by('-waktu_prediksi')

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
        'riwayat_prediksi': riwayat_prediksi,
        'kpi_total': kpi_total,
        'kpi_avg_ipk': kpi_avg_ipk,
        'kpi_pct_high': kpi_pct_high,
    }

    return render(request, 'dashboard.html', context)

def export_history(request, format_type):
    """View polimorfis mengekspor data riwayat dari SQLite"""
    queryset = PredictionLog.objects.all()
    
    if format_type == 'excel':
        exporter = ExcelHistoryExporter()
    else:
        exporter = CSVHistoryExporter()
        
    return exporter.export_data(queryset)

def export_dataset(request, format_type):
    """View untuk mengekspor raw dataset berdasarkan filter aktif"""
    df_filtered = _get_filtered_dataset(request)
    
    if df_filtered is None:
        return HttpResponse("Data tidak ditemukan", status=404)
        
    if format_type == 'excel':
        exporter = ExcelHistoryExporter()
        return exporter.export_dataframe(df_filtered, "dataset_mahasiswa_filtered.xlsx")
    else:
        exporter = CSVHistoryExporter()
        return exporter.export_dataframe(df_filtered, "dataset_mahasiswa_filtered.csv")

def migrate_csv_to_sql(request):
    """Helper View untuk memigrasikan data dari CSV ke SQL Database via Django ORM"""
    
    try:
        df = pd.read_csv(DATASET_PATH)
        df.columns = df.columns.str.strip()
        
        Mahasiswa.objects.all().delete()
        
        mahasiswa_objs = [
            Mahasiswa(**{col: row[col] for col in df.columns})
            for _, row in df.iterrows()
        ]
        Mahasiswa.objects.bulk_create(mahasiswa_objs)
        
        return HttpResponse(f"✨ SUCCESS: {len(mahasiswa_objs)} baris data berhasil dipindahkan ke SQL!")
    except Exception as e:
        return HttpResponse(f"❌ ERROR Migrasi: {e}", status=500)