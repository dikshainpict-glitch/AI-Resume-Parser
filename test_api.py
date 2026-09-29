import requests

url = "http://127.0.0.1:5000/parse-resume"

file_path = "uploads/resume.pdf"

with open(file_path, "rb") as file:
    response = requests.post(
        url,
        files={"resume": file}
    )

print("Status Code:", response.status_code)
print("Response:")
print(response.json())