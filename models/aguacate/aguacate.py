# Importar librerías
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
import joblib
import os

base_dir = os.path.dirname(__file__)
data_path = os.path.join(base_dir, "data", "aguacate.csv")
figures_dir = os.path.join(base_dir, "figures")
os.makedirs(figures_dir, exist_ok=True)

# Cargar datos
data = pd.read_csv(data_path)

# Visualización inicial
plt.figure(figsize=(8,5))
sns.histplot(data["AveragePrice"], bins=30, kde=True, color='green')
plt.title("Distribución del Precio Promedio del Aguacate")
plt.savefig(os.path.join(figures_dir, "averageprice_distribution.png"), bbox_inches="tight")
plt.close()

plt.figure(figsize=(8,5))
sns.boxplot(x="year", y="AveragePrice", data=data)
plt.title("Precio promedio por año")
plt.savefig(os.path.join(figures_dir, "price_by_year.png"), bbox_inches="tight")
plt.close()

plt.figure(figsize=(10,5))
sns.boxplot(x="type", y="AveragePrice", data=data)
plt.title("Precio promedio por tipo de aguacate")
plt.savefig(os.path.join(figures_dir, "price_by_type.png"), bbox_inches="tight")
plt.close()

# Preparación de datos
data = data.drop(columns=["id", "Date"])

label_encoders = {}
for col in ["type", "region"]:
    le = LabelEncoder()
    data[col] = le.fit_transform(data[col])
    label_encoders[col] = le

X = data.drop(columns=["AveragePrice"])
y = data["AveragePrice"]

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Modelo de IA
model = RandomForestRegressor(n_estimators=200, random_state=42)
model.fit(X_train, y_train)

# Evaluación
y_pred = model.predict(X_test)
mae = mean_absolute_error(y_test, y_pred)
rmse = np.sqrt(mean_squared_error(y_test, y_pred))
r2 = r2_score(y_test, y_pred)

results = pd.DataFrame({"Métrica": ["MAE", "RMSE", "R²"], "Valor": [mae, rmse, r2]})
results.to_csv(os.path.join(figures_dir, "model_metrics.csv"), index=False)
print("Evaluación del modelo:")
print(results)

# Visualización de resultados
plt.figure(figsize=(8,6))
sns.scatterplot(x=y_test, y=y_pred)
plt.xlabel("Valores reales")
plt.ylabel("Predicciones")
plt.title("Predicción vs Realidad - Precio de Aguacate")
plt.savefig(os.path.join(figures_dir, "pred_vs_real.png"), bbox_inches="tight")
plt.close()

# Importancia de variables
importances = pd.Series(model.feature_importances_, index=X.columns).sort_values(ascending=False)
plt.figure(figsize=(8,5))
sns.barplot(x=importances.values, y=importances.index)
plt.title("Importancia de las variables en el modelo")
plt.savefig(os.path.join(figures_dir, "feature_importance.png"), bbox_inches="tight")
plt.close()

# Exportar modelo
joblib.dump(model, os.path.join(base_dir, "modelo_precio_aguacate.pkl"))
print("\nModelo exportado exitosamente a 'modelo_precio_aguacate.pkl'")
