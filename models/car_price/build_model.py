from pandas import read_csv, DataFrame, Series
from numpy import ndarray
from joblib import dump, load
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import r2_score, root_mean_squared_error, confusion_matrix
from warnings import filterwarnings


def build_model(
    x_train: DataFrame | Series, y_train: DataFrame | Series | ndarray
) -> None:
    model = RandomForestRegressor(n_estimators=100, max_depth=4)
    model.fit(x_train, y_train)
    dump(model, "car_price.model.pkl")


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
    model: RandomForestRegressor = load("./car_price.model.pkl")
    test = read_csv("./test_data.csv")
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
    print("RMSE =", root_mean_squared_error(y_true, y_pred))


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
