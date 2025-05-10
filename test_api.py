# backend/test_api.py
import requests

API_URL = "http://localhost:5000/upload"

def test_image_upload(image_path):
    with open(image_path, 'rb') as file:
        files = {'file': file}
        response = requests.post(API_URL, files=files)
        print(response.json())

if __name__ == "__main__":
    test_image_upload("2.jpg")  # Replace with your test image