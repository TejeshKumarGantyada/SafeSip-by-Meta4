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
    API_KEY = "fh3c-iGWuo91Ibmbz_oYy4orKtfKS45UXfFqY9zWI2D2"
    token_response = requests.post('https://iam.cloud.ibm.com/identity/token', data={"apikey": API_KEY, "grant_type": 'urn:ibm:params:oauth:grant-type:apikey'})
    mltoken = token_response.json()["access_token"]

    header = {'Content-Type': 'application/json', 'Authorization': 'Bearer ' + mltoken}

    payload_scoring = {
        "input_data": [
            {
                "fields": ["ph", "Hardness", "Solids", "Chloramines", "Sulfate", "Conductivity", "Organic_carbon", "Trihalomethanes", "Turbidity"],
                "values": [values]
            }
        ]
    }

    response_scoring = requests.post(
        'https://us-south.ml.cloud.ibm.com/ml/v4/deployments/c9279248-db7c-41d9-945f-536771b01f5e/predictions?version=2021-05-01',
        json=payload_scoring,
        headers=header
    )

    return response_scoring.json()


def interpret_response(response):
    prediction = response['predictions'][0]['values'][0][0]
    probabilities = response['predictions'][0]['values'][0][1]

    labels = {0.0: "not drinkable", 1.0: "drinkable"}

    print(f"Prediction: The water is {labels[prediction]}.")
    print(f"Contamination level: {probabilities[0]*100:.2f}%")


def main():
    values = get_user_input()
    response = make_prediction(values)
    interpret_response(response)

if __name__ == "__main__":
    main()
