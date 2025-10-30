import os
import math
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
from pandas import read_csv, DataFrame, Series
from numpy import ndarray
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import r2_score, mean_squared_error
from sklearn.model_selection import train_test_split
from joblib import dump, load


def build_model(
    x_train: DataFrame | Series, y_train: DataFrame | Series | ndarray
) -> None:
    model = RandomForestRegressor(
        n_estimators=150, max_depth=4, random_state=67, min_samples_split=24
    )
    model.fit(x_train, y_train)
    # export model
    base_dir = os.path.dirname(__file__)
    figures_dir = os.path.join(base_dir, "figures")
    os.makedirs(figures_dir, exist_ok=True)

    dump(model, os.path.join(base_dir, "bike_ride_price.model.pkl"))

    # Evaluación sobre los datos provistos (rápido sanity check)
    try:
        y_pred = model.predict(x_train)
        r2 = r2_score(y_train, y_pred)
        rmse = math.sqrt(mean_squared_error(y_train, y_pred))
        metrics_df = pd.DataFrame({"Métrica": ["R2", "RMSE"], "Valor": [r2, rmse]})
        metrics_df.to_csv(os.path.join(figures_dir, "model_metrics.csv"), index=False)

        # Gráficos básicos
        plt.figure(figsize=(8,6))
        plt.scatter(y_train, y_pred, alpha=0.6)
        plt.xlabel("Valores reales")
        plt.ylabel("Predicciones")
        plt.title("Predicción vs Real - Bike price")
        plt.savefig(os.path.join(figures_dir, "pred_vs_real.png"), bbox_inches="tight")
        plt.close()

        # Si las columnas son numéricas, mostrar matriz de correlación
        try:
            df = pd.concat([x_train.reset_index(drop=True), pd.Series(y_train).reset_index(drop=True)], axis=1)
            corr = df.corr()
            plt.figure(figsize=(8,6))
            sns.heatmap(corr, cmap="coolwarm", center=0)
            plt.title("Matriz de correlación - Bike price")
            plt.savefig(os.path.join(figures_dir, "correlation_matrix.png"), bbox_inches="tight")
            plt.close()
        except Exception:
            pass
    except Exception:
        # no bloquear el entrenamiento si la exportación falla
        pass

def split_data() -> None:
    data = read_csv("./train.csv")

    train_data, test_data = train_test_split(
            data, test_size=.3, random_state=67
            )
    train_data.to_csv("train_data.csv")
    test_data.to_csv("test_data.csv")

def test_model() -> None:
    base_dir = os.path.dirname(__file__)
    model_path = os.path.join(base_dir, "bike_ride_price.model.pkl")
    model: RandomForestRegressor = load(model_path)
    test = read_csv(os.path.join(base_dir, "test_data.csv"))
    test = test.dropna()
    # x_test = test[["driver-tip", "mta-tax", "distance", "toll-amount", "rate-code"]]
    x_test = test[["distance", "rate-code"]]
    y_true = test["total-amount"]
    y_pred = model.predict(x_test)
    print("R² =", r2_score(y_true, y_pred))
    from sklearn.metrics import mean_squared_error
    rmse = math.sqrt(mean_squared_error(y_true, y_pred))
    print("RMSE =", rmse)

    # export figures for test evaluation
    figures_dir = os.path.join(base_dir, "figures")
    os.makedirs(figures_dir, exist_ok=True)
    try:
        import pandas as _pd
        metrics_df = _pd.DataFrame({"Métrica": ["R2", "RMSE"], "Valor": [r2_score(y_true, y_pred), rmse]})
        metrics_df.to_csv(os.path.join(figures_dir, "model_metrics_test.csv"), index=False)

        plt.figure(figsize=(8,6))
        plt.scatter(y_true, y_pred, alpha=0.6)
        plt.xlabel("Valores reales")
        plt.ylabel("Predicciones")
        plt.title("Predicción vs Real - Bike price (test)")
        plt.savefig(os.path.join(figures_dir, "pred_vs_real_test.png"), bbox_inches="tight")
        plt.close()
    except Exception:
        pass

# NOTE: this model is questionable at best, but it'll do, the other models are
# literal crap
# R² = 0.7938826430474483                                                                                                                                                                       
# RMSE = 6.862557308745646
# driver-tip, mta-tax, distance, toll-amount, rate-code
if __name__ == "__main__":
    test_model()
    # split_data()
    exit(0)
    data = read_csv("./train_data.csv", parse_dates=False)
    data = data.dropna()
    # x_train = data[["driver-tip", "mta-tax", "distance", "toll-amount", "rate-code"]]
    x_train = data[["distance", "rate-code"]]
    y_train = data["total-amount"]
    build_model(x_train, y_train)
