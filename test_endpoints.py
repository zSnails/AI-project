import requests
from urllib.parse import quote_plus

BASE = "http://localhost:8080"
TIMEOUT = 6

ENDPOINTS = {
    "aguacate": (
        "/api/models/aguacate",
        {
            "total-volume": "64236.62",
            "4046": "1036.74",
            "4225": "54454.85",
            "4770": "48.16",
            "total-bags": "8696.87",
            "small-bags": "8603.62",
            "large-bags": "93.25",
            "xlarge-bags": "0.0",
            "type": "conventional",
            "year": "2015",
            "region": "Albany",
        },
    ),
    "bitcoin": (
        "/api/models/bitcoin",
        {
            "open": "2763.24",
            "high": "2889.62",
            "low": "2720.61",
            "close": "2875.34",
            "volume": "860575000",
            "market-cap": "45535800000",
            "return": "0.01",
            "ma3": "2800",
            "ma7": "2750",
            "volatility": "10",
        },
    ),
    "grasa": (
        "/api/models/grasa",
        {
            "age": "23",
            "weight": "154.25",
            "height": "67.75",
            "neck": "36.2",
            "chest": "93.1",
            "abdomen": "85.2",
            "hip": "94.5",
            "thigh": "59.0",
            "knee": "37.3",
            "ankle": "21.9",
            "biceps": "32.0",
            "forearm": "27.4",
            "wrist": "17.1",
        },
    ),
    "telecomunicaciones": (
        "/api/models/telecomunicaciones",
        {
            "gender": "Female",
            "senior-citizen": "0",
            "partner": "Yes",
            "dependents": "No",
            "tenure": "1",
            "phone-service": "No",
            "multiple-lines": "No phone service",
            "internet-service": "DSL",
            "online-security": "No",
            "online-backup": "Yes",
            "device-protection": "No",
            "tech-support": "No",
            "streaming-tv": "No",
            "streaming-movies": "No",
            "contract": "Month-to-month",
            "paperless-billing": "Yes",
            "payment-method": "Electronic check",
            "monthly-charges": "29.85",
            "total-charges": "29.85",
        },
    ),
    "vino": (
        "/api/models/vino",
        {
            "type": "white",
            "fixed-acidity": "7",
            "volatile-acidity": "0.27",
            "citric-acid": "0.36",
            "residual-sugar": "20.7",
            "chlorides": "0.045",
            "free-sulfur-dioxide": "45",
            "total-sulfur-dioxide": "170",
            "density": "1.001",
            "pH": "3",
            "sulphates": "0.45",
            "alcohol": "8.8",
        },
    ),
}


def build_url(path, params):
    if not params:
        return BASE + path
    qs = "&".join(f"{quote_plus(k)}={quote_plus(str(v))}" for k, v in params.items())
    return BASE + path + "?" + qs


def try_call(name, path, params):
    url = build_url(path, params)
    print(f"--- {name} -> {url}")
    try:
        r = requests.get(url, timeout=TIMEOUT)
    except requests.exceptions.RequestException as e:
        print(f"ERROR: request failed: {e}\n")
        return
    print(f"HTTP {r.status_code}")
    ct = r.headers.get("content-type", "")
    try:
        if "application/json" in ct:
            print(r.json())
        else:
            print(r.text)
    except Exception:
        print(r.text)
    print("\n")


if __name__ == "__main__":
    print("Starting automated endpoint tests. Make sure server is running at http://localhost:8080")
    for name, (path, params) in ENDPOINTS.items():
        try_call(name, path, params)
    print("Done")
