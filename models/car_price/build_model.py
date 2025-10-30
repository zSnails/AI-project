import os
import math
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
from pandas import read_csv, DataFrame, Series
from numpy import ndarray
from joblib import dump, load
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import r2_score, mean_squared_error
from warnings import filterwarnings


def build_model(
    x_train: DataFrame | Series, y_train: DataFrame | Series | ndarray
) -> None:
    model = RandomForestRegressor(n_estimators=100, max_depth=4)
    model.fit(x_train, y_train)
    base_dir = os.path.dirname(__file__)
    figures_dir = os.path.join(base_dir, "figures")
    os.makedirs(figures_dir, exist_ok=True)

    dump(model, os.path.join(base_dir, "car_price.model.pkl"))

    # Evaluación rápida sobre los datos proporcionados
    try:
        y_pred = model.predict(x_train)
        r2 = r2_score(y_train, y_pred)
        rmse = math.sqrt(mean_squared_error(y_train, y_pred))
        metrics_df = pd.DataFrame({"Métrica": ["R2", "RMSE"], "Valor": [r2, rmse]})
        metrics_df.to_csv(os.path.join(figures_dir, "model_metrics.csv"), index=False)

        plt.figure(figsize=(6,6))
        plt.scatter(y_train, y_pred, alpha=0.6)
        plt.xlabel("Valores reales")
        plt.ylabel("Predicciones")
        plt.title("Predicción vs Real - Car price")
        plt.savefig(os.path.join(figures_dir, "pred_vs_real.png"), bbox_inches="tight")
        plt.close()

        # Importance (si aplica)
        try:
            importances = pd.Series(model.feature_importances_, index=x_train.columns).sort_values(ascending=False)
            plt.figure(figsize=(8,5))
            sns.barplot(x=importances.values, y=importances.index)
            plt.title("Importancia de las variables - Car price")
            plt.savefig(os.path.join(figures_dir, "feature_importance.png"), bbox_inches="tight")
            plt.close()
        except Exception:
            pass
    except Exception:
        pass


def split_data() -> None:
    data = read_csv("./car_data.csv")
    data["Car_Name"] = data["Car_Name"].astype("category")
    data["Fuel_Type"] = data["Fuel_Type"].astype("category")
    data["Seller_Type"] = data["Seller_Type"].astype("category")
    data["Transmission"] = data["Transmission"].astype("category")

    data["Car_Name_Code"] = data["Car_Name"].cat.codes
    data["Fuel_Type_Code"] = data["Fuel_Type"].cat.codes
    data["Seller_Type_Code"] = data["Seller_Type"].cat.codes
    data["Transmission_Code"] = data["Transmission"].cat.codes

    # DataFrame({ "Car_Name": data["Car_Name"], "Car_Name_Code": data["Car_Name_Code"]}).to_csv("car_name_and_codes.csv")
    # DataFrame({ "Fuel_Type": data["Fuel_Type"], "Fuel_Type_Code": data["Fuel_Type_Code"]}).to_csv("fuel_type_and_codes.csv")
    # DataFrame({ "Seller_Type": data["Seller_Type"], "Seller_Type_Code": data["Seller_Type_Code"]}).to_csv("seller_type_and_codes.csv")
    # DataFrame({ "Transmission": data["Transmission"], "Transmission_Code": data["Transmission_Code"]}).to_csv("transmission_and_codes.csv")
    # exit(0)
    train_data: DataFrame
    test_data: DataFrame
    train_data, test_data = train_test_split(
        data, test_size=0.3, random_state=67
    )  # type:ignore
    train_data.to_csv("train_data.csv")
    test_data.to_csv("test_data.csv")


def test_model() -> None:
    base_dir = os.path.dirname(__file__)
    model_path = os.path.join(base_dir, "car_price.model.pkl")
    model: RandomForestRegressor = load(model_path)
    test = read_csv(os.path.join(base_dir, "test_data.csv"))
    x_test = test[
        [
            "Car_Name_Code",
            "Year",
            "Present_Price",
            "Kms_Driven",
            "Fuel_Type_Code",
            "Seller_Type_Code",
            "Transmission_Code",
            "Owner",
        ]
    ]
    y_true = test["Selling_Price"]
    y_pred = model.predict(x_test)

    x_test["predicted"] = y_pred
    x_test["real_value"] = test["Selling_Price"]
    x_test["difference"] = x_test["predicted"] - test["Selling_Price"]
    print(y_true)
    print("R² =", r2_score(y_true, y_pred))
    rmse = math.sqrt(mean_squared_error(y_true, y_pred))
    print("RMSE =", rmse)

    # export figures for test evaluation
    figures_dir = os.path.join(base_dir, "figures")
    os.makedirs(figures_dir, exist_ok=True)
    try:
        metrics_df = pd.DataFrame({"Métrica": ["R2", "RMSE"], "Valor": [r2_score(y_true, y_pred), rmse]})
        metrics_df.to_csv(os.path.join(figures_dir, "model_metrics_test.csv"), index=False)

        plt.figure(figsize=(6,6))
        plt.scatter(y_true, y_pred, alpha=0.6)
        plt.xlabel("Valores reales")
        plt.ylabel("Predicciones")
        plt.title("Predicción vs Real - Car price (test)")
        plt.savefig(os.path.join(figures_dir, "pred_vs_real_test.png"), bbox_inches="tight")
        plt.close()
    except Exception:
        pass


# NOTE: got these results (based off of the R² metric this looks like a nice model)
# R² = 0.968924492355013
# RMSE = 0.7458721572349319

if __name__ == "__main__":
    filterwarnings("ignore")
    test_model()
    exit(0)
    train_data = read_csv("./train_data.csv")
    x_train = train_data[
        [
            "Car_Name_Code",
            "Year",
            "Present_Price",
            "Kms_Driven",
            "Fuel_Type_Code",
            "Seller_Type_Code",
            "Transmission_Code",
            "Owner",
        ]
    ]
    y_train = train_data["Selling_Price"]
    build_model(x_train, y_train)
