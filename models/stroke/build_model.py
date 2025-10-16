from joblib import load, dump
from pandas import DataFrame, Series, read_csv
from numpy.random import rand
from numpy import ndarray, dot, log, e
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import r2_score, root_mean_squared_error
from sklearn.tree import DecisionTreeClassifier


def build_model(
    x_train: DataFrame | Series, y_train: DataFrame | Series | ndarray
) -> None:
    model = RandomForestClassifier(n_estimators=200, max_depth=4)
    model.fit(x_train, y_train)
    dump(model, "stroke.model.pkl")


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
    model: RandomForestClassifier = load("./stroke.model.pkl")
    test = read_csv("./test_data.csv")
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
    print("R² =", r2_score(y_true, y_pred))
    print("RMSE =", root_mean_squared_error(y_true, y_pred))


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
