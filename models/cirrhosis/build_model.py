from warnings import filterwarnings
from pandas import DataFrame, Series, read_csv
from numpy import ndarray
from sklearn.metrics import r2_score, root_mean_squared_error
from joblib import dump, load
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier


def build_model(
    x_train: DataFrame | Series, y_train: DataFrame | Series | ndarray
) -> None:
    model = DecisionTreeClassifier(
            max_depth=15, random_state=67, min_samples_split=24
    )
    model.fit(x_train, y_train)
    dump(model, "cirrhosis.model.pkl")


def split_data() -> None:
    data = read_csv("./cirrhosis.csv")
    data["Status"] = data["Status"].astype("category")
    data["Drug"] = data["Drug"].astype("category")
    data["Sex"] = data["Sex"].astype("category")
    data["Ascites"] = data["Ascites"].astype("category")
    data["Hepatomegaly"] = data["Hepatomegaly"].astype("category")
    data["Spiders"] = data["Spiders"].astype("category")
    data["Edema"] = data["Edema"].astype("category")

    data["Status_Code"] = data["Status"].cat.codes
    data["Drug_Code"] = data["Drug"].cat.codes
    data["Sex_Code"] = data["Sex"].cat.codes
    data["Ascites_Code"] = data["Ascites"].cat.codes
    data["Hepatomegaly_Code"] = data["Hepatomegaly"].cat.codes
    data["Spiders_Code"] = data["Spiders"].cat.codes
    data["Edema_Code"] = data["Edema"].cat.codes

    train_data, test_data = train_test_split(
        data, test_size=0.3, random_state=67
    )
    train_data.to_csv("train_data.csv")
    test_data.to_csv("test_data.csv")


def test_model() -> None:
    model: DecisionTreeClassifier = load("./cirrhosis.model.pkl")
    test = read_csv("./test_data.csv")
    x_test = test[
        [
            "N_Days",
            "Drug_Code",
            "Age",
            "Sex_Code",
            "Ascites_Code",
            "Hepatomegaly_Code",
            "Spiders_Code",
            "Edema_Code",
            "Bilirubin",
            "Cholesterol",
            "Albumin",
            "Copper",
            "Alk_Phos",
            "SGOT",
            "Tryglicerides",
            "Platelets",
            "Prothrombin",
            "Stage",
        ]
    ]
    y_true = test["Status_Code"]
    y_pred = model.predict(x_test)

    print("R² =", r2_score(y_true, y_pred))
    print("RMSE =", root_mean_squared_error(y_true, y_pred))
    ...


if __name__ == "__main__":
    filterwarnings("ignore")
    test_model()
    exit(0)
    # split_data()
    # exit(0)
    train_data = read_csv("./train_data.csv")
    train_data.dropna()
    x_train = train_data[
        [
            "N_Days",
            "Drug_Code",
            "Age",
            "Sex_Code",
            "Ascites_Code",
            "Hepatomegaly_Code",
            "Spiders_Code",
            "Edema_Code",
            "Bilirubin",
            "Cholesterol",
            "Albumin",
            "Copper",
            "Alk_Phos",
            "SGOT",
            "Tryglicerides",
            "Platelets",
            "Prothrombin",
            "Stage",
        ]
    ]
    y_train = train_data["Status_Code"]
    build_model(x_train, y_train)
