from flask import Flask, jsonify, request, send_from_directory
from flask_cors import CORS
from os.path import join
from typing import List
from face import DetectionResult, generate_labelled_image
from joblib import load
from uuid import uuid4
from numpy import array
from sklearn.ensemble import RandomForestClassifier, RandomForestRegressor
from sklearn.tree import DecisionTreeClassifier
import pandas as pd
import hashlib
from flask import abort
import tempfile
import os

from azure.core.credentials import AzureKeyCredential
from azure.ai.vision.face import FaceClient
from azure.ai.vision.face.models import (
    FaceAttributeTypeDetection01,
    FaceAttributeTypeDetection03,
    FaceDetectionModel,
    FaceRecognitionModel,
)
from dotenv import load_dotenv
from os import environ

load_dotenv()


ENDPOINT = environ["AZURE_FACE_ENDPOINT"]
API_KEY = environ["AZURE_API_KEY"]

id = environ["PERSON_GROUP_ID"]
PERSON_GROUP_ID = id if id != "" else str(uuid4())


face_client = FaceClient(endpoint=ENDPOINT, credential=AzureKeyCredential(API_KEY))

app = Flask(__name__, static_folder="./static")
CORS(app)

app.config["UPLOAD_FOLDER"] = "./uploads/"
app.config["RESULTS_FOLDER"] = "./detection_results/"
app.config["AUDIO_FOLDER"] = "./audio_uploads/"

# Crear carpeta para audios si no existe
os.makedirs(app.config["AUDIO_FOLDER"], exist_ok=True)

# Carga perezosa de Whisper
_whisper_model = None
def get_whisper_model():
    global _whisper_model
    if _whisper_model is None:
        print("Cargando modelo Whisper (lazy)...")
        import whisper 
        _whisper_model = whisper.load_model("base")
        print("Modelo Whisper cargado.")
    return _whisper_model


def _parse_num(val: str | None, name: str, cast=float):
    if val is None:
        abort(400, description=f"missing parameter: {name}")
    try:
        return cast(val)
    except Exception:
        abort(400, description=f"invalid value for {name}: {val}")


def _stable_code(s: str | None, mod: int = 1000) -> int:
    if s is None:
        return 0
    if isinstance(s, (int, float)):
        return int(s)
    h = hashlib.md5(s.encode("utf-8")).hexdigest()[:8]
    return int(h, 16) % mod


def _map_aguacate_type(v: str | None) -> int:
    if v is None:
        return 0
    if str(v).isdigit():
        return int(v)
    m = {"conventional": 0, "organic": 1}
    return m.get(str(v).lower(), _stable_code(str(v), 200))


def _map_region(v: str | None) -> int:
    # Regions are many; try numeric, a small common map, else stable hash
    if v is None:
        return 0
    if str(v).isdigit():
        return int(v)
    common = {"albany": 0, "totalus": 1}
    return common.get(str(v).lower(), _stable_code(str(v), 500))


def _map_bool_yes_no(v: str | None) -> int:
    if v is None:
        return 0
    s = str(v).strip().lower()
    if s in ("yes", "y", "true", "1"):
        return 1
    if s in ("no", "n", "false", "0"):
        return 0
    # keep numeric-like
    if s.isdigit():
        return int(s)
    return 0


def _map_gender(v: str | None) -> int:
    if v is None:
        return 0
    s = str(v).strip().lower()
    if s in ("female", "f"):
        return 0
    if s in ("male", "m"):
        return 1
    if s.isdigit():
        return int(s)
    return 0


def _map_contract(v: str | None) -> int:
    if v is None:
        return 0
    s = str(v).strip().lower()
    if s == "month-to-month":
        return 0
    if s == "one year" or s == "one-year" or s == "one_year":
        return 1
    if s == "two year" or s == "two-year" or s == "two_year":
        return 2
    if s.isdigit():
        return int(s)
    return _stable_code(s, 10)


def _map_internet_service(v: str | None) -> int:
    if v is None:
        return 2
    s = str(v).strip().lower()
    if s == "dsl":
        return 0
    if s == "fiber optic" or s == "fiber":
        return 1
    if s in ("no", "none"):
        return 2
    if s.isdigit():
        return int(s)
    return _stable_code(s, 5)


def _map_payment_method(v: str | None) -> int:
    if v is None:
        return 0
    s = str(v).strip().lower()
    m = {
        "electronic check": 0,
        "mailed check": 1,
        "bank transfer (automatic)": 2,
        "credit card (automatic)": 3,
    }
    if s in m:
        return m[s]
    if s.isdigit():
        return int(s)
    return _stable_code(s, 10)


bike_toll_model: RandomForestRegressor = load("./models/bike_price/bike_ride_price.model.pkl")


@app.route("/", methods=["GET"])
def serve_vue_frontend():
    if app.static_folder:
        return send_from_directory(app.static_folder, "index.html")
    return jsonify({"code": 500, "message": "Internal Server Error"}), 500


@app.route("/api/models/bike-toll", methods=["GET"])
def bike_toll():
    distance = request.args.get("distance")
    rate_code = request.args.get("rate-code")
    return jsonify(
        {
            "prediction": float(
                bike_toll_model.predict(array([distance, rate_code]).reshape(1, -1))[0]
            )
        }
    )


car_price_model: RandomForestRegressor = load("./models/car_price/car_price.model.pkl")


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
            "prediction": float(
                car_price_model.predict(
                    array(
                        [
                            car_name_code,
                            year,
                            present_price,
                            kms_driven,
                            fuel_type_code,
                            seller_type_code,
                            transmission_code,
                            owner,
                        ]
                    ).reshape(1, -1)
                )[0]
            )
        }
    )


cirrhosis_model: DecisionTreeClassifier = load("./models/cirrhosis/cirrhosis.model.pkl")

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


hepatitis_model: RandomForestRegressor = load("./models/hepatitis/hepatitis.model.pkl")

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

    return jsonify({"prediction": int(stroke_model.predict(data.reshape(1, -1))[0]) == 1})


# --- Model endpoints added: aguacate, bitcoin, grasa, telecomunicaciones, vino
# These endpoints follow the project's existing style: accept features via query
# params and return a JSON with the model prediction.


# Aguacate: features order (as trained):
# Total Volume, 4046, 4225, 4770, Total Bags, Small Bags, Large Bags, XLarge Bags, type (encoded), year, region (encoded)
aguacate_model = load("./models/aguacate/modelo_precio_aguacate.pkl")


@app.route("/api/models/aguacate", methods=["GET"])
def aguacate_price():
    total_volume = _parse_num(request.args.get("total-volume"), "total-volume")
    c4046 = _parse_num(request.args.get("4046"), "4046")
    c4225 = _parse_num(request.args.get("4225"), "4225")
    c4770 = _parse_num(request.args.get("4770"), "4770")
    total_bags = _parse_num(request.args.get("total-bags"), "total-bags")
    small_bags = _parse_num(request.args.get("small-bags"), "small-bags")
    large_bags = _parse_num(request.args.get("large-bags"), "large-bags")
    xlarge_bags = _parse_num(request.args.get("xlarge-bags"), "xlarge-bags")
    # accept either type-code (numeric) or type (string)
    type_code = _map_aguacate_type(request.args.get("type-code") or request.args.get("type"))
    year = _parse_num(request.args.get("year"), "year", int)
    region_code = _map_region(request.args.get("region-code") or request.args.get("region"))

    features = [
        total_volume,
        c4046,
        c4225,
        c4770,
        total_bags,
        small_bags,
        large_bags,
        xlarge_bags,
        type_code,
        year,
        region_code,
    ]

    return jsonify({"prediction": float(aguacate_model.predict(array(features).reshape(1, -1))[0])})


# Bitcoin: features used in training:
# Open, High, Low, Close, Volume, Market Cap, Return, MA3, MA7, Volatility
bitcoin_model = load("./models/bitcoin/modelo_direccion_bitcoin.pkl")


@app.route("/api/models/bitcoin", methods=["GET"])
def bitcoin_direction():
    open_p = _parse_num(request.args.get("open"), "open")
    high = _parse_num(request.args.get("high"), "high")
    low = _parse_num(request.args.get("low"), "low")
    close = _parse_num(request.args.get("close"), "close")
    volume = _parse_num(request.args.get("volume"), "volume")
    market_cap = _parse_num(request.args.get("market-cap"), "market-cap")
    ret = _parse_num(request.args.get("return"), "return")
    ma3 = _parse_num(request.args.get("ma3"), "ma3")
    ma7 = _parse_num(request.args.get("ma7"), "ma7")
    volatility = _parse_num(request.args.get("volatility"), "volatility")

    features = [open_p, high, low, close, volume, market_cap, ret, ma3, ma7, volatility]
    return jsonify({"prediction": int(bitcoin_model.predict(array(features).reshape(1, -1))[0])})


# Grasa corporal: features (after preprocessing) roughly:
# Age, Weight, Height, Neck, Chest, Abdomen, Hip, Thigh, Knee, Ankle, Biceps, Forearm, Wrist
grasa_model = load("./models/grasa/bodyfat_model.pkl")


@app.route("/api/models/grasa", methods=["GET"])
def grasa_prediction():
    age = _parse_num(request.args.get("age"), "age", int)
    weight = _parse_num(request.args.get("weight"), "weight")
    height = _parse_num(request.args.get("height"), "height")
    neck = _parse_num(request.args.get("neck"), "neck")
    chest = _parse_num(request.args.get("chest"), "chest")
    abdomen = _parse_num(request.args.get("abdomen"), "abdomen")
    hip = _parse_num(request.args.get("hip"), "hip")
    thigh = _parse_num(request.args.get("thigh"), "thigh")
    knee = _parse_num(request.args.get("knee"), "knee")
    ankle = _parse_num(request.args.get("ankle"), "ankle")
    biceps = _parse_num(request.args.get("biceps"), "biceps")
    forearm = _parse_num(request.args.get("forearm"), "forearm")
    wrist = _parse_num(request.args.get("wrist"), "wrist")

    features = [
        age,
        weight,
        height,
        neck,
        chest,
        abdomen,
        hip,
        thigh,
        knee,
        ankle,
        biceps,
        forearm,
        wrist,
    ]

    return jsonify({"prediction": float(grasa_model.predict(array(features).reshape(1, -1))[0])})


# Telecomunicaciones: features (after preprocessing) roughly:
# gender, SeniorCitizen, Partner, Dependents, tenure, PhoneService, MultipleLines,
# InternetService, OnlineSecurity, OnlineBackup, DeviceProtection, TechSupport,
# StreamingTV, StreamingMovies, Contract, PaperlessBilling, PaymentMethod,
# MonthlyCharges, TotalCharges
telecom_model = load("./models/telecomunicaciones/telecomunicaciones_model.pkl")


@app.route("/api/models/telecomunicaciones", methods=["GET"])
def telecom_prediction():
    gender = _map_gender(request.args.get("gender"))
    senior = _parse_num(request.args.get("senior-citizen"), "senior-citizen", int)
    partner = _map_bool_yes_no(request.args.get("partner"))
    dependents = _map_bool_yes_no(request.args.get("dependents"))
    tenure = _parse_num(request.args.get("tenure"), "tenure", int)
    phone_service = _map_bool_yes_no(request.args.get("phone-service"))
    multiple_lines = _map_bool_yes_no(request.args.get("multiple-lines"))
    internet_service = _map_internet_service(request.args.get("internet-service"))
    online_security = _map_bool_yes_no(request.args.get("online-security"))
    online_backup = _map_bool_yes_no(request.args.get("online-backup"))
    device_protection = _map_bool_yes_no(request.args.get("device-protection"))
    tech_support = _map_bool_yes_no(request.args.get("tech-support"))
    streaming_tv = _map_bool_yes_no(request.args.get("streaming-tv"))
    streaming_movies = _map_bool_yes_no(request.args.get("streaming-movies"))
    contract = _map_contract(request.args.get("contract"))
    paperless = _map_bool_yes_no(request.args.get("paperless-billing"))
    payment_method = _map_payment_method(request.args.get("payment-method"))
    monthly_charges = _parse_num(request.args.get("monthly-charges"), "monthly-charges")
    total_charges = _parse_num(request.args.get("total-charges"), "total-charges")

    data = array([
        [
            gender,
            senior,
            partner,
            dependents,
            tenure,
            phone_service,
            multiple_lines,
            internet_service,
            online_security,
            online_backup,
            device_protection,
            tech_support,
            streaming_tv,
            streaming_movies,
            contract,
            paperless,
            payment_method,
            monthly_charges,
            total_charges,
        ]
    ])

    return jsonify({"prediction": int(telecom_model.predict(data)[0]) == 1})


# Vino: features (original CSV order) with `type` mapped to dummy (white -> 1, else 0)
vino_model = load("./models/vino/vino_quality_model.pkl")


@app.route("/api/models/vino", methods=["GET"])
def vino_prediction():
    type_raw = request.args.get("type")
    type_code = 1 if (type_raw is not None and type_raw.lower() == "white") else 0
    fixed_acidity = _parse_num(request.args.get("fixed-acidity"), "fixed-acidity")
    volatile_acidity = _parse_num(request.args.get("volatile-acidity"), "volatile-acidity")
    citric_acid = _parse_num(request.args.get("citric-acid"), "citric-acid")
    residual_sugar = _parse_num(request.args.get("residual-sugar"), "residual-sugar")
    chlorides = _parse_num(request.args.get("chlorides"), "chlorides")
    free_sulfur = _parse_num(request.args.get("free-sulfur-dioxide"), "free-sulfur-dioxide")
    total_sulfur = _parse_num(request.args.get("total-sulfur-dioxide"), "total-sulfur-dioxide")
    density = _parse_num(request.args.get("density"), "density")
    ph = _parse_num(request.args.get("pH") or request.args.get("ph"), "pH")
    sulphates = _parse_num(request.args.get("sulphates"), "sulphates")
    alcohol = _parse_num(request.args.get("alcohol"), "alcohol")

    # We attempt to match the training order by placing the type dummy first
    features = [
        type_code,
        fixed_acidity,
        volatile_acidity,
        citric_acid,
        residual_sugar,
        chlorides,
        free_sulfur,
        total_sulfur,
        density,
        ph,
        sulphates,
        alcohol,
    ]

    return jsonify({"prediction": float(vino_model.predict(array(features).reshape(1, -1))[0])})


@app.route("/api/market/bitcoin/latest", methods=["GET"])
def bitcoin_market_latest():
    """Return latest computed features for bitcoin from the CSV used in training.

    This mirrors the feature engineering used at training time so the frontend
    can request the latest market snapshot to feed the model when the user
    asks by voice (e.g., "¿Bitcoin va a subir mañana?").
    """
    csv_path = "./models/bitcoin/data/bitcoin.csv"
    try:
        df = pd.read_csv(csv_path)
    except Exception as e:
        return jsonify({"error": f"failed to read bitcoin data: {e}"}), 500

    # Clean numeric fields similar to training script
    for col in ["Volume", "Market Cap"]:
        if col in df.columns:
            df[col] = df[col].astype(str).replace({",": ""}, regex=True)
            df[col] = df[col].replace(r"[^0-9\.\-]", "", regex=True)
            df[col] = pd.to_numeric(df[col], errors="coerce")

    # parse date and sort
    if "Date" in df.columns:
        df["Date"] = pd.to_datetime(df["Date"], errors="coerce")
        df = df.sort_values("Date")

    # compute features
    df["Return"] = df["Close"].pct_change()
    df["MA3"] = df["Close"].rolling(3).mean()
    df["MA7"] = df["Close"].rolling(7).mean()
    df["Volatility"] = df["Close"].rolling(7).std()

    df = df.dropna()
    if df.shape[0] == 0:
        return jsonify({"error": "not enough data to compute features"}), 500

    last = df.iloc[-1]

    features = {
        "open": float(last["Open"]),
        "high": float(last["High"]),
        "low": float(last["Low"]),
        "close": float(last["Close"]),
        "volume": float(last["Volume"]),
        "market_cap": float(last["Market Cap"]),
        "return": float(last["Return"]),
        "ma3": float(last["MA3"]),
        "ma7": float(last["MA7"]),
        "volatility": float(last["Volatility"]),
        "date": last["Date"].strftime("%Y-%m-%d") if not pd.isna(last["Date"]) else None,
    }
    return jsonify(features)

@app.route("/static/<path>", methods=["GET"])
def serve_detection_results(path: str):
    return send_from_directory(app.config["RESULTS_FOLDER"], path)


@app.route("/api/models/face-recognition", methods=["POST"])
def face_recognition():
    if not len(request.files) > 0:
        return (
            jsonify({"status": 400, "message": "missing image (you did not upload an image)"}),
            400,
        )
    image = request.files["image"]
    filepath = join(
        app.config["UPLOAD_FOLDER"],
        image.filename if image.filename is not None else f"{uuid4()}.png",
    )
    image.save(filepath)  # type: ignore
    with open(filepath, "rb") as image:
        detected_faces: List[DetectionResult] = face_client.detect(
            image.read(-1),
            detection_model=FaceDetectionModel.DETECTION03,
            recognition_model=FaceRecognitionModel.RECOGNITION04,
            return_face_id=False,
            return_face_attributes=[
                FaceAttributeTypeDetection03.HEAD_POSE,
                FaceAttributeTypeDetection01.GLASSES,
                FaceAttributeTypeDetection01.OCCLUSION,
            ],
        )  # type:ignore
        filename = generate_labelled_image(
            image,
            detected_faces,
            directory=app.config["RESULTS_FOLDER"],
            output=f"{uuid4()}.png",
        )

    return jsonify(
        {
            "resultUrl": f"http://localhost:8080/static/{filename}",
            "detectedFaces": list(map(lambda a: a.as_dict(), detected_faces)),  # type:ignore
        }
    )
@app.route("/api/audio/transcribe", methods=["POST"])
def audio_transcribe():
    """
    Endpoint para transcribir audio usando Whisper.
    Recibe un archivo de audio (wav, mp3, etc.) y devuelve el texto transcrito.
    """
    if "audio" not in request.files:
        return jsonify({"status": 400, "message": "missing audio file"}), 400

    audio_file = request.files["audio"]

    # Guardar el archivo temporalmente
    temp_path = join(
        app.config["AUDIO_FOLDER"],
        f"{uuid4()}.webm"  # El navegador suele enviar webm
    )

    try:
        audio_file.save(temp_path)

        # Transcribir con Whisper (carga perezosa)
        model = get_whisper_model()
        result = model.transcribe(temp_path, language="es")

        # Limpiar archivo temporal
        os.remove(temp_path)

        return jsonify({
            "transcript": result["text"],
            "language": result.get("language", "es")
        })
    except Exception as e:
        # Limpiar archivo si existe
        if os.path.exists(temp_path):
            os.remove(temp_path)
        return jsonify({"status": 500, "message": f"transcription error: {str(e)}"}), 500

if __name__ == "__main__":
    app.run("0.0.0.0", 8080, debug=True)
    face_client.close()
