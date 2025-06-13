import requests


def get_user_input():
    ph = float(input("Enter pH value: "))
    hardness = float(input("Enter Hardness value: "))
    solids = float(input("Enter Solids value: "))
    chloramines = float(input("Enter Chloramines value: "))
    sulfate = float(input("Enter Sulfate value: "))
    conductivity = float(input("Enter Conductivity value: "))
    organic_carbon = float(input("Enter Organic Carbon value: "))
    trihalomethanes = float(input("Enter Trihalomethanes value: "))
    turbidity = float(input("Enter Turbidity value: "))
    return [ph, hardness, solids, chloramines, sulfate, conductivity, organic_carbon, trihalomethanes, turbidity]


def make_prediction(values):
    API_KEY = "Y20GSzqSee0FtrKo34MlM5umSJvSeGmah1VGaT8PF1fW"

    try:
        # Get access token
        token_response = requests.post(
            'https://iam.cloud.ibm.com/identity/token',
            data={"apikey": API_KEY, "grant_type": 'urn:ibm:params:oauth:grant-type:apikey'}
        )
        token_response.raise_for_status()
        mltoken = token_response.json()["access_token"]
    except Exception as e:
        print("Failed to get access token:", e)
        return {"error": "Token fetch failed"}

    # Set up headers and payload
    headers = {
        'Content-Type': 'application/json',
        'Authorization': 'Bearer ' + mltoken
    }

    payload_scoring = {
        "input_data": [
            {
                "fields": [
                    "ph", "Hardness", "Solids", "Chloramines", "Sulfate",
                    "Conductivity", "Organic_carbon", "Trihalomethanes", "Turbidity"
                ],
                "values": [values]
            }
        ]
    }

    try:
        response = requests.post(
            'https://us-south.ml.cloud.ibm.com/ml/v4/deployments/88badb8e-e3e1-4fcd-844d-04e882b6fbc2/predictions?version=2021-05-01',
            json=payload_scoring,
            headers=headers
        )
        response.raise_for_status()
        print("Prediction request successful")
        print("Full Response:", response.text)  # Debug output
        return response.json()
    except Exception as e:
        print("Failed to get prediction:", e)
        print("Response text:", response.text)
        return {"error": "Prediction request failed"}


def interpret_response(response):
    if 'predictions' not in response:
        print("No predictions found in the response.")
        print("⚠Full response:", response)
        return

    prediction = response['predictions'][0]['values'][0][0]
    probabilities = response['predictions'][0]['values'][0][1]

    labels = {0.0: "Not Drinkable", 1.0: "Safe to Drink"}
    drink_status = labels[prediction]
    not_safe_prob = probabilities[0] * 100
    safe_prob = probabilities[1] * 100

    print("\n💧 Water Quality Prediction Result 💧")
    print("====================================")
    print(f"🔎 Final Verdict     : {drink_status}")
    print(f"🧪 Probability (Not Safe): {not_safe_prob:.2f}%")
    print(f"✅ Probability (Safe)    : {safe_prob:.2f}%")
    print("====================================")



def main():
    values = get_user_input()
    response = make_prediction(values)
    interpret_response(response)

if __name__ == "__main__":
    main()
