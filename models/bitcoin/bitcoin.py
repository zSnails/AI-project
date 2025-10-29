# Importar librerías
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix
import os
import joblib

base_dir = os.path.dirname(__file__)
data_path = os.path.join(base_dir, "data", "bitcoin.csv")
figures_dir = os.path.join(base_dir, "figures")
os.makedirs(figures_dir, exist_ok=True)

# Cargar datos
data = pd.read_csv(data_path)

# Limpiar columnas numéricas con comas y símbolos
for col in ["Volume", "Market Cap"]:
    data[col] = data[col].astype(str).replace({",": ""}, regex=True)
    data[col] = data[col].replace(r"[^0-9\.\-]", "", regex=True)
    data[col] = pd.to_numeric(data[col], errors='coerce')

# Convertir fecha y ordenar
data["Date"] = pd.to_datetime(data["Date"])
data = data.sort_values("Date")

# Crear features
data["Return"] = data["Close"].pct_change()
data["MA3"] = data["Close"].rolling(3).mean()
data["MA7"] = data["Close"].rolling(7).mean()
data["Volatility"] = data["Close"].rolling(7).std()
data["Next_Close"] = data["Close"].shift(-1)
data["Direction"] = (data["Next_Close"] > data["Close"]).astype(int)
data = data.dropna()

# Variables predictoras y etiqueta
X = data[["Open", "High", "Low", "Close", "Volume", "Market Cap", "Return", "MA3", "MA7", "Volatility"]]
y = data["Direction"]

# División de datos
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=777, shuffle=True)

# Entrenamiento del modelo
model = RandomForestClassifier(n_estimators=200, random_state=777)
model.fit(X_train, y_train)

# Evaluación
y_pred = model.predict(X_test)
acc = accuracy_score(y_test, y_pred)
report_dict = classification_report(y_test, y_pred, output_dict=True)
report_df = pd.DataFrame(report_dict).transpose()
report_df.to_csv(os.path.join(figures_dir, "classification_report.csv"))

print(f"Accuracy del modelo: {acc:.4f}")
print("\nReporte de clasificación:")
print(report_df)

# Visualizaciones
plt.figure(figsize=(10,5))
sns.lineplot(x="Date", y="Close", data=data)
plt.title("Evolución del precio de cierre de Bitcoin")
plt.savefig(os.path.join(figures_dir, "1_evolucion_precio.png"), bbox_inches="tight")
plt.close()

plt.figure(figsize=(6,4))
sns.heatmap(confusion_matrix(y_test, y_pred), annot=True, fmt="d", cmap="Greens")
plt.title("Matriz de confusión")
plt.xlabel("Predicción")
plt.ylabel("Valor real")
plt.savefig(os.path.join(figures_dir, "2_matriz_confusion.png"), bbox_inches="tight")
plt.close()

importances = pd.Series(model.feature_importances_, index=X.columns).sort_values(ascending=False)
plt.figure(figsize=(8,5))
sns.barplot(x=importances.values, y=importances.index, color='orange')
plt.title("Importancia de las variables")
plt.savefig(os.path.join(figures_dir, "3_importancia_variables.png"), bbox_inches="tight")
plt.close()

# Guardar modelo entrenado
joblib.dump(model, os.path.join(base_dir, "modelo_direccion_bitcoin.pkl"))
print("\nModelo exportado a 'modelo_direccion_bitcoin.pkl' y figuras guardadas en /figures")
