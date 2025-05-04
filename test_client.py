import requests

url = "http://127.0.0.1:5000/api/get_tax_info"
payload = {
    "user_query": "What is the corporate tax rate in Alaska?"
}

response = requests.post(url, json=payload)
print("Status Code:", response.status_code)
print("Raw Response Text:", response.text)  # <== Show the actual content

try:
    print("JSON:", response.json())
except Exception as e:
    print("Failed to parse JSON:", str(e))
