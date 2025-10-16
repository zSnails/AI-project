from flask import Flask, jsonify, request
from joblib import load
from numpy import array
from sklearn.ensemble import RandomForestClassifier, RandomForestRegressor
from sklearn.tree import DecisionTreeClassifier


app = Flask(__name__)


bike_toll_model: RandomForestRegressor = load(
    "./models/bike_price/bike_ride_price.model.pkl"
)


@app.route("/api/models/bike-toll", methods=["GET"])
def bike_toll():
    distance = request.args.get("distance")
    rate_code = request.args.get("rate-code")
    return jsonify(
        {
            "prediction": float(bike_toll_model.predict(
                array([distance, rate_code]).reshape(1, -1)
            )[0])
        }
    )


car_price_model: RandomForestRegressor = load(
    "./models/car_price/car_price.model.pkl"
)


@app.route("/api/models/car-price", methods=["GET"])
def car_price():
    car_name_code = request.args.get("car-name-code")
    year = request.args.get("year")
    present_price = request.args.get("present-price")
    kms_driven = request.args.get("kms-driven")
    fuel_type_code = request.args.get("fuel-type-code")
    seller_type_code = request.args.get("seller-type-code")
    transmission_code = request.args.get("transmission-code")
    owner = request.args.get("owner")
    return jsonify(
        {
            "prediction": float(car_price_model.predict(
                array([
                    car_name_code,
                    year,
                    present_price,
                    kms_driven,
                    fuel_type_code,
                    seller_type_code,
                    transmission_code,
                    owner,
                ]).reshape(1, -1)
            )[0])
        }
    )


cirrhosis_model: DecisionTreeClassifier = load(
    "./models/cirrhosis/cirrhosis.model.pkl"
)

cirrhosis_status_codes = ["C", "CL", "D"]


@app.route("/api/models/cirrhosis", methods=["GET"])
def cirrhosis():
    n_days = request.args.get("n-days")
    drug_code = request.args.get("drug-code")
    age = request.args.get("age")
    sex_code = request.args.get("sex-code")
    ascites_code = request.args.get("ascites-code")
    hepatomegaly_code = request.args.get("hepatomegaly-code")
    spiders_code = request.args.get("spiders-code")
    edema_code = request.args.get("edema-code")
    bilirubin = request.args.get("bilirubin")
    cholesterol = request.args.get("cholesterol")
    albumin = request.args.get("albumin")
    copper = request.args.get("copper")
    alk_phos = request.args.get("alk_phos")
    sgot = request.args.get("sgot")
    tryglicerides = request.args.get("tryglicerides")
    platelets = request.args.get("platelets")
    prothrombin = request.args.get("prothrombin")
    stage = request.args.get("stage")

    return jsonify(
        {
            "prediction": cirrhosis_status_codes[
                int(
                    cirrhosis_model.predict(
                        array(
                            [
                                n_days,
                                drug_code,
                                age,
                                sex_code,
                                ascites_code,
                                hepatomegaly_code,
                                spiders_code,
                                edema_code,
                                bilirubin,
                                cholesterol,
                                albumin,
                                copper,
                                alk_phos,
                                sgot,
                                tryglicerides,
                                platelets,
                                prothrombin,
                                stage,
                            ]
                        ).reshape(1, -1)
                    )[0]
                )
            ]
        }
    )


hepatitis_model: RandomForestRegressor = load(
    "./models/hepatitis/hepatitis.model.pkl"
)

hepatitis_codes = [
    "Blood Donor",
    "Suspect Blood Donor",
    "Hepatitis",
    "Fibrosis",
    "Cirrhosis",
]


@app.route("/api/models/hepatitis", methods=["GET"])
def hepatitis_prediction():
    age = request.args.get("age")
    sex_code = request.args.get("sex-code")
    alb = request.args.get("alb")
    alp = request.args.get("alp")
    alt = request.args.get("alt")
    ast = request.args.get("ast")
    bil = request.args.get("bil")
    che = request.args.get("che")
    chol = request.args.get("chol")
    crea = request.args.get("crea")
    ggt = request.args.get("ggt")
    prot = request.args.get("prot")
    data = array(
        [
            age,
            sex_code,
            alb,
            alp,
            alt,
            ast,
            bil,
            che,
            chol,
            crea,
            ggt,
            prot,
        ]
    ).reshape(1, -1)
    category = int(hepatitis_model.predict(data)[0])
    return jsonify({"prediction": hepatitis_codes[category]})


stroke_model: RandomForestClassifier = load("./models/stroke/stroke.model.pkl")


# stroke
@app.route("/api/models/stroke", methods=["GET"])
def stroke_prediction():
    age = request.args.get("age")
    hypertension = request.args.get("hypertension")
    heart_disease = request.args.get("heart-disease")
    avg_glocose_level = request.args.get("avg-glocose-level")
    ever_married_code = request.args.get("ever-married-code")
    bmi = request.args.get("bmi")
    data = array(
        [
            age,
            hypertension,
            heart_disease,
            avg_glocose_level,
            ever_married_code,
            bmi,
        ]
    )

    return jsonify(
        {"prediction": int(stroke_model.predict(data.reshape(1, -1))[0]) == 1}
    )


if __name__ == "__main__":
    app.run("0.0.0.0", 8080, debug=True)
