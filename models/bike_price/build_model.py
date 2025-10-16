from matplotlib.pyplot import show
from pandas import read_csv, DataFrame, Series
from numpy import ndarray
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import r2_score, root_mean_squared_error
from sklearn.model_selection import train_test_split
from seaborn import heatmap
from joblib import dump, load


def build_model(
    x_train: DataFrame | Series, y_train: DataFrame | Series | ndarray
) -> None:
    model = RandomForestRegressor(
        n_estimators=150, max_depth=4, random_state=67, min_samples_split=24
    )
    model.fit(x_train, y_train)
    dump(model, "bike_ride_price.model.pkl")

def split_data() -> None:
    data = read_csv("./train.csv")

    train_data, test_data = train_test_split(
            data, test_size=.3, random_state=67
            )
    train_data.to_csv("train_data.csv")
    test_data.to_csv("test_data.csv")

def test_model() -> None:
    model: RandomForestRegressor = load("./bike_ride_price.model.pkl")
    test = read_csv("./test_data.csv")
    test = test.dropna()
    x_test = test[["driver-tip", "mta-tax", "distance", "toll-amount", "rate-code"]]
    y_true = test["total-amount"]
    y_pred = model.predict(x_test)

    print("R² =", r2_score(y_true, y_pred))
    print("RMSE =", root_mean_squared_error(y_true, y_pred))

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
    x_train = data[["driver-tip", "mta-tax", "distance", "toll-amount", "rate-code"]]
    y_train = data["total-amount"]
    build_model(x_train, y_train)
