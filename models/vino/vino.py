# Importar librerías
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
import joblib
import os

base_dir = os.path.dirname(__file__)
data_path = os.path.join(base_dir, "data", "vino.csv")
figures_dir = os.path.join(base_dir, "figures")
os.makedirs(figures_dir, exist_ok=True)

# Cargar datos
df = pd.read_csv(data_path)

plt.figure(figsize=(8,6))
sns.heatmap(df.select_dtypes(include=np.number).corr(), annot=False, cmap="coolwarm")
plt.title("Correlación entre variables numéricas")
plt.savefig(os.path.join(figures_dir, "correlation_matrix.png"), bbox_inches="tight")
plt.close()

plt.figure(figsize=(6,4))
sns.histplot(df["quality"], bins=10, kde=True)
plt.title("Distribución de la calidad del vino")
plt.savefig(os.path.join(figures_dir, "quality_distribution.png"), bbox_inches="tight")
plt.close()

# Preparación de datos
X = df.drop("quality", axis=1)
X = pd.get_dummies(X, drop_first=True)
y = df["quality"]

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Entrenamiento del modelo
model = RandomForestRegressor(n_estimators=200, random_state=42)
model.fit(X_train, y_train)

# Evaluación del modelo
y_pred = model.predict(X_test)
mae = mean_absolute_error(y_test, y_pred)
mse = mean_squared_error(y_test, y_pred)
r2 = r2_score(y_test, y_pred)
results = pd.DataFrame({"Métrica":["MAE","MSE","R²"],"Valor":[mae,mse,r2]})
results.to_csv(os.path.join(figures_dir, "model_metrics.csv"), index=False)
print("Resultados del modelo:")
print(results)

plt.figure(figsize=(6,6))
plt.scatter(y_test, y_pred, alpha=0.7)
plt.xlabel("Valores Reales")
plt.ylabel("Predicciones")
plt.title("Predicción de calidad del vino")
plt.savefig(os.path.join(figures_dir, "pred_vs_real.png"), bbox_inches="tight")
plt.close()

plt.figure(figsize=(8,5))
importances = pd.Series(model.feature_importances_, index=X.columns).sort_values(ascending=False)
sns.barplot(x=importances.values, y=importances.index)
plt.title("Importancia de las Variables")
plt.savefig(os.path.join(figures_dir, "feature_importance.png"), bbox_inches="tight")
plt.close()

# Guardar modelo entrenado
joblib.dump(model, os.path.join(base_dir, "vino_quality_model.pkl"))
