import os
import textwrap
from matplotlib.backends.backend_pdf import PdfPages
import matplotlib.pyplot as plt
import pandas as pd
# Config
ROOT = os.path.dirname(os.path.dirname(__file__))  # repo root
REPORT_PATH = os.path.join(ROOT, "reports")
os.makedirs(REPORT_PATH, exist_ok=True)
OUT_PDF = os.path.join(REPORT_PATH, "models_report.pdf")

folders = {
    "Bike Price": os.path.join(ROOT, "models", "bike_price", "figures"),
    "Car Price": os.path.join(ROOT, "models", "car_price", "figures"),
    "Cirrhosis": os.path.join(ROOT, "models", "cirrhosis", "figures"),
    "Hepatitis": os.path.join(ROOT, "models", "hepatitis", "figures"),
    "Stroke": os.path.join(ROOT, "models", "stroke", "figures"),
}

metrics_files = {
    "Bike Price": os.path.join(folders["Bike Price"], "model_metrics_test.csv"),
    "Car Price": os.path.join(folders["Car Price"], "model_metrics_test.csv"),
    "Cirrhosis": os.path.join(folders["Cirrhosis"], "classification_report_test.csv"),
    "Hepatitis": os.path.join(folders["Hepatitis"], "classification_report_test.csv"),
    "Stroke": os.path.join(folders["Stroke"], "classification_report_test.csv"),
}

code_files = {
    "Bike Price": os.path.join(ROOT, "models", "bike_price", "build_model.py"),
    "Car Price": os.path.join(ROOT, "models", "car_price", "build_model.py"),
    "Cirrhosis": os.path.join(ROOT, "models", "cirrhosis", "build_model.py"),
    "Hepatitis": os.path.join(ROOT, "models", "hepatitis", "build_model.py"),
    "Stroke": os.path.join(ROOT, "models", "stroke", "build_model.py"),
}

descriptions = {
    "Bike Price": "Predicción del precio total de un viaje en bicicleta (regresión). Variables: distancia, rate-code y otras características del viaje.",
    "Car Price": "Predicción del precio de venta de un automóvil (regresión). Variables: características codificadas del vehículo (Car_Name_Code, Year, Present_Price, etc.).",
    "Cirrhosis": "Clasificación del estado del paciente con cirrosis (multiclase). Variables clínicas y codificaciones (Drug, Sex, Ascites, etc.).",
    "Hepatitis": "Clasificación de la categoría de Hepatitis C (multiclase) según parámetros bioquímicos y demográficos.",
    "Stroke": "Predicción del riesgo de stroke (clasificación binaria) según edad, hipertensión, nivel de glucosa, BMI y otros." ,
}

dataset_links = {
    "Bike Price": "",
    "Car Price": "",
    "Cirrhosis": "",
    "Hepatitis": "",
    "Stroke": "",
}


def add_title_page(pdf, model_name, description):
    plt.figure(figsize=(11, 8.5))
    plt.axis('off')
    plt.text(0.5, 0.7, f"Modelo: {model_name}", fontsize=22, ha='center')
    plt.text(0.5, 0.5, description, fontsize=12, ha='center', wrap=True)
    pdf.savefig()
    plt.close()


def add_metrics_table(pdf, metrics_path, model_name):
    if not os.path.exists(metrics_path):
        return
    try:
        metrics = pd.read_csv(metrics_path)
    except Exception:
        return
    fig, ax = plt.subplots(figsize=(11, 4))
    ax.axis('off')
    table_data = metrics.values.tolist()
    col_labels = metrics.columns.tolist()
    table = ax.table(cellText=table_data, colLabels=col_labels, loc='center', cellLoc='center')
    table.auto_set_font_size(False)
    table.set_fontsize(10)
    table.scale(1, 1.4)
    plt.title(f"Métricas del modelo {model_name}", fontsize=14)
    pdf.savefig()
    plt.close()


def add_image_pages(pdf, figures_folder, model_name):
    if not os.path.isdir(figures_folder):
        return
    for file in sorted(os.listdir(figures_folder)):
        if file.lower().endswith('.png'):
            img_path = os.path.join(figures_folder, file)
            try:
                img = plt.imread(img_path)
                fig, ax = plt.subplots(figsize=(11, 8.5))
                ax.imshow(img)
                ax.axis('off')
                plt.title(f"{model_name} - {file}", fontsize=14)
                pdf.savefig()
                plt.close()
            except Exception:
                continue


# Build PDF following requested format
with PdfPages(OUT_PDF) as pdf:
    # No cover page per request — start directly with models
    for model_name in ["Bike Price", "Car Price", "Cirrhosis", "Hepatitis", "Stroke"]:
        add_title_page(pdf, model_name, descriptions.get(model_name, ""))
        # show metrics as table
        metrics_path = metrics_files.get(model_name)
        add_metrics_table(pdf, metrics_path, model_name)
        # show images
        figures_folder = folders.get(model_name)
        add_image_pages(pdf, figures_folder, model_name)

    # Code section at the end
    lines_per_page = 50
    for model_name, code_file in code_files.items():
        if os.path.exists(code_file):
            with open(code_file, 'r', encoding='utf-8') as f:
                code_lines = f.readlines()
            for i in range(0, len(code_lines), lines_per_page):
                block = "".join(code_lines[i:i+lines_per_page])
                plt.figure(figsize=(11, 8.5))
                plt.axis('off')
                plt.text(0.01, 0.99, block, fontsize=8, va='top', family='monospace')
                plt.title(f"Código Python - {model_name} (líneas {i+1}-{min(i+lines_per_page,len(code_lines))})", fontsize=12)
                pdf.savefig()
                plt.close()

print(f"PDF generado en: {OUT_PDF}")
