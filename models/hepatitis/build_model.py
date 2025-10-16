from pandas import read_csv, DataFrame, Series
from numpy import ndarray
from joblib import dump, load
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import r2_score, root_mean_squared_error, confusion_matrix
from warnings import filterwarnings


def build_model(
    x_train: DataFrame | Series, y_train: DataFrame | Series | ndarray
) -> None:
    model = RandomForestClassifier(n_estimators=100, max_depth=4)
    model.fit(x_train, y_train)
    dump(model, "hepatitis.model.pkl")


def split_data() -> None:
    data = read_csv("./HepatitisCdata.csv")
    data["Category"] = data["Category"].astype("category")
    data["Sex"] = data["Sex"].astype("category")

    data["Category_Code"] = data["Category"].cat.codes
    data["Sex_Code"] = data["Sex"].cat.codes

    DataFrame(
        {"Category": data["Category"], "Category_Code": data["Category_Code"]}
    ).to_csv("category_and_category_codes.csv")
    DataFrame({"Sex": data["Sex"], "Sex_Code": data["Sex_Code"]}).to_csv(
        "sex_and_sex_codes.csv"
    )

    train_data: DataFrame
    test_data: DataFrame
    train_data, test_data = train_test_split(
        data, test_size=0.3, random_state=67
    )  # type:ignore
    train_data.to_csv("train_data.csv")
    test_data.to_csv("test_data.csv")


def test_model() -> None:
    model: RandomForestClassifier = load("./hepatitis.model.pkl")
    test = read_csv("./test_data.csv")
    x_test = test[
        [
            "Age",
            "Sex_Code",
            "ALB",
            "ALP",
            "ALT",
            "AST",
            "BIL",
            "CHE",
            "CHOL",
            "CREA",
            "GGT",
            "PROT",
        ]
    ]
    y_true = test["Category_Code"]
    y_pred = model.predict(x_test)

    print("R² =", r2_score(y_true, y_pred))
    print("RMSE =", root_mean_squared_error(y_true, y_pred))


# NOTE: got these values, this also seems like a very solid model
# R² = 0.7130585217443179                                                                                                                                                                       
# RMSE = 0.5301708036860207

if __name__ == "__main__":
    filterwarnings("ignore")
    test_model()
    exit(0)
    train_data = read_csv("./train_data.csv")
    x_train = train_data[["Age", "Sex_Code", "ALB", "ALP", "ALT", "AST", "BIL", "CHE", "CHOL", "CREA", "GGT", "PROT"]]
    y_train = train_data["Category_Code"]
    build_model(x_train, y_train)
