import requests
import json
import os
import subprocess
import time
import sys

class HomeAssistant:
    def __init__(self, host, token, device_name):
        self.host = host.rstrip('/')
        self.headers = {
            'Authorization': f'Bearer {token}',
            'Content-Type': 'application/json',
        }
        self.device_name = device_name

    def set_sensor_value(self, entity_id, value):
        """Set a sensor value.
        
        Args:
            entity_id (str): The sensor entity ID
            value (float): The sensor value
        """
        return self.set_state(entity_id, value)

    def set_state(self, entity_id, state, attributes=None):
        url = f"{self.host}/api/states/{entity_id}"
        data = {'state': state}
        if attributes:
            data['attributes'] = attributes
        
        response = requests.post(url, headers=self.headers, json=data)
        response.raise_for_status()
        return response.json()

    def get_state(self, entity_id):
        url = f"{self.host}/api/states/{entity_id}"
        response = requests.get(url, headers=self.headers)
        response.raise_for_status()
        return response.json()
    
    def set_all(self, temperature, humidity, co2):
        self.set_sensor_value(f"sensor.{self.device_name}_co2", co2)
        self.set_sensor_value(f"sensor.{self.device_name}_temperature", temperature)
        self.set_sensor_value(f"sensor.{self.device_name}_humidity", humidity)
        
        
        
def read_values(binary, hidraw_device):
    out = subprocess.run([binary, hidraw_device], capture_output=True, text=True)
    print(out.stdout)
    print(out.stderr)
    stdout = out.stdout.strip()
    tokens = stdout.split(",")
    if len(tokens) != 5:
        raise ValueError(f"Expected 5 tokens, got {len(tokens)}: {stdout}")
    _, _, temperature, humidity, co2 = tokens
    return float(temperature), float(humidity), float(co2)

def get_mandatory_env(name):
    value = os.getenv(name)
    if not value:
        raise ValueError(f"Environment variable {name} is not set")
    return value

# Example usage
if __name__ == "__main__":
    HA_HOST = get_mandatory_env("HA_HOST")
    HA_TOKEN = get_mandatory_env("HA_TOKEN")
    HA_DEVICE_NAME = get_mandatory_env("HA_DEVICE_NAME")
    HIDRAW_DEVICE = get_mandatory_env("HIDRAW_DEVICE")

    ha = HomeAssistant(HA_HOST, HA_TOKEN, HA_DEVICE_NAME)
    
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    binary = "./ht2000"
    
    print(f"Starting Home Assistant client for device {HA_DEVICE_NAME} on {HA_HOST}")

    while True:
        error = False
        try:
            temperature, humidity, co2 = read_values(binary, HIDRAW_DEVICE)
            ha.set_all(temperature, humidity, co2)
            print("Sensor values updated successfully")

        except requests.exceptions.RequestException as e:
            print(f"Error connecting to Home Assistant: {e}")
            error = True
        except Exception as e:
            print(f"Error reading sensor values: {e}")
            error = True
    
        sys.stdout.flush()
        if error:
            # HT2000 starts misbehaving if it is pinged too often during
            # startup.
            time.sleep(60)
        else:
            time.sleep(1)
