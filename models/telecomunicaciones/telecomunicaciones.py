import os
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix
import joblib

base_dir = os.path.dirname(__file__)
data_path = os.path.join(base_dir, "data", "telecomunicaciones.csv")
figures_dir = os.path.join(base_dir, "figures")
os.makedirs(figures_dir, exist_ok=True)

# Cargar datos
df = pd.read_csv(data_path)

# Preprocesamiento
df = df.drop("customerID", axis=1)
df["TotalCharges"] = pd.to_numeric(df["TotalCharges"], errors='coerce')
df = df.dropna()

categorical_cols = df.select_dtypes(include="object").columns
le = LabelEncoder()
for col in categorical_cols:
    df[col] = le.fit_transform(df[col])

X = df.drop("Churn", axis=1)
y = df["Churn"]

# División de datos
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)

# Entrenamiento del modelo
model = RandomForestClassifier(n_estimators=200, random_state=42)
model.fit(X_train, y_train)

# Evaluación del modelo
y_pred = model.predict(X_test)

acc = accuracy_score(y_test, y_pred)
report = classification_report(y_test, y_pred, output_dict=True)
report_df = pd.DataFrame(report).transpose()
report_df.to_csv(os.path.join(figures_dir, "classification_report.csv"))

print("Accuracy del modelo:", acc)
print("\nReporte de clasificación:")
print(report_df)

plt.figure(figsize=(6,5))
sns.heatmap(confusion_matrix(y_test, y_pred), annot=True, fmt="d", cmap="Blues")
plt.title("Matriz de Confusión")
plt.xlabel("Predicción")
plt.ylabel("Valor real")
plt.savefig(os.path.join(figures_dir, "confusion_matrix.png"), bbox_inches="tight")
plt.close()

plt.figure(figsize=(8,5))
importances = pd.Series(model.feature_importances_, index=X.columns).sort_values(ascending=False)
sns.barplot(x=importances.values, y=importances.index)
plt.title("Importancia de las variables")
plt.savefig(os.path.join(figures_dir, "feature_importance.png"), bbox_inches="tight")
plt.close()

# Guardar modelo entrenado
joblib.dump(model, os.path.join(base_dir, "telecomunicaciones_model.pkl"))
