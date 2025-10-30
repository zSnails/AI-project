import os
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
from joblib import load, dump
from pandas import DataFrame, Series, read_csv
from numpy.random import rand
from numpy import ndarray
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report, confusion_matrix, accuracy_score
from sklearn.tree import DecisionTreeClassifier


def build_model(
    x_train: DataFrame | Series, y_train: DataFrame | Series | ndarray
) -> None:
    model = RandomForestClassifier(n_estimators=200, max_depth=4)
    model.fit(x_train, y_train)
    base_dir = os.path.dirname(__file__)
    figures_dir = os.path.join(base_dir, "figures")
    os.makedirs(figures_dir, exist_ok=True)

    dump(model, os.path.join(base_dir, "stroke.model.pkl"))

    # Exportar métricas y figuras (sanity check)
    try:
        y_pred = model.predict(x_train)
        report = classification_report(y_train, y_pred, output_dict=True)
        report_df = pd.DataFrame(report).transpose()
        report_df.to_csv(os.path.join(figures_dir, "classification_report.csv"))

        cm = confusion_matrix(y_train, y_pred)
        plt.figure(figsize=(6,5))
        sns.heatmap(cm, annot=True, fmt="d", cmap="Greens")
        plt.title("Matriz de confusión - Stroke")
        plt.xlabel("Predicción")
        plt.ylabel("Valor real")
        plt.savefig(os.path.join(figures_dir, "confusion_matrix.png"), bbox_inches="tight")
        plt.close()
    except Exception:
        pass


def split_data() -> None:
    data = read_csv("./healthcare-dataset-stroke-data.csv")

    data["gender"] = data["gender"].astype("category")
    data["ever_married"] = data["ever_married"].astype("category")
    data["work_type"] = data["work_type"].astype("category")
    data["residence_type"] = data["residence_type"].astype("category")
    data["smoking_status"] = data["smoking_status"].astype("category")

    data["gender_code"] = data["gender"].cat.codes
    data["ever_married_code"] = data["ever_married"].cat.codes
    data["work_type_code"] = data["work_type"].cat.codes
    data["smoking_status_code"] = data["smoking_status"].cat.codes

    # DataFrame({ "Car_Name": data["Car_Name"], "Car_Name_Code": data["Car_Name_Code"]}).to_csv("car_name_and_codes.csv")
    # DataFrame({ "Fuel_Type": data["Fuel_Type"], "Fuel_Type_Code": data["Fuel_Type_Code"]}).to_csv("fuel_type_and_codes.csv")
    # DataFrame({ "Seller_Type": data["Seller_Type"], "Seller_Type_Code": data["Seller_Type_Code"]}).to_csv("seller_type_and_codes.csv")
    # DataFrame({ "Transmission": data["Transmission"], "Transmission_Code": data["Transmission_Code"]}).to_csv("transmission_and_codes.csv")
    # exit(0)
    train_data: DataFrame
    test_data: DataFrame
    train_data, test_data = train_test_split(
        data, test_size=0.2, random_state=67
    )  # type:ignore
    train_data.to_csv("train_data.csv")
    test_data.to_csv("test_data.csv")


def test_model() -> None:
    base_dir = os.path.dirname(__file__)
    model: RandomForestClassifier = load(os.path.join(base_dir, "stroke.model.pkl"))
    test = read_csv(os.path.join(base_dir, "test_data.csv"))
    y_true = test["stroke"]
    x_test = test[
        [
            "age",
            "hypertension",
            "heart_disease",
            "avg_glucose_level",
            "ever_married_code",
            "bmi",
        ]
    ]
    y_pred = model.predict(x_test)
    print("Accuracy =", accuracy_score(y_true, y_pred))
    from sklearn.metrics import classification_report
    print("Reporte de clasificación:\n", classification_report(y_true, y_pred))

    # export figures for test evaluation
    figures_dir = os.path.join(base_dir, "figures")
    os.makedirs(figures_dir, exist_ok=True)
    try:
        report = classification_report(y_true, y_pred, output_dict=True)
        report_df = pd.DataFrame(report).transpose()
        report_df.to_csv(os.path.join(figures_dir, "classification_report_test.csv"))

        cm = confusion_matrix(y_true, y_pred)
        plt.figure(figsize=(6,5))
        sns.heatmap(cm, annot=True, fmt="d", cmap="Greens")
        plt.title("Matriz de confusión - Stroke (test)")
        plt.xlabel("Predicción")
        plt.ylabel("Valor real")
        plt.savefig(os.path.join(figures_dir, "confusion_matrix_test.png"), bbox_inches="tight")
        plt.close()
    except Exception:
        pass


if __name__ == "__main__":
    test_model()
    # split_data()
    exit(0)
    train_data = read_csv("./train_data.csv")
    y_train = train_data["stroke"]
    x_train = train_data[
        [
            "age",
            "hypertension",
            "heart_disease",
            "avg_glucose_level",
            "ever_married_code",
            "bmi",
        ]
    ]
    build_model(x_train, y_train)
