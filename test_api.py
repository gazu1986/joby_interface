import requests
import json
from datetime import datetime

def test_sensor_data():
    url = "http://localhost:8000/api/v1/sensor/ingest"
    
    test_data = {
        "device_id": "test_device_001",
        "temperature": 25.0,
        "pressure": 1013.25,
        "timestamp": datetime.now().isoformat()
    }
    
    try:
        response = requests.post(url, json=test_data, timeout=10)
        print(f"Status Code: {response.status_code}")
        print(f"Response: {json.dumps(response.json(), indent=2)}")
        
        if response.status_code == 200:
            print("✅ Test passed!")
        else:
            print("❌ Test failed!")
            
    except Exception as e:
        print(f"❌ Test failed with error: {str(e)}")

if __name__ == "__main__":
    test_sensor_data() 