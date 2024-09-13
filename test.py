import requests

response = requests.post(
     "http://localhost:1234/v1/completions",  # Make sure this matches your local server setup
    json={"prompt": "Tell me a joke"}
)

print(response.json())  # This should give you the response from your local server
