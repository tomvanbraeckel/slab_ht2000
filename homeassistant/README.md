# Home Assistant integration for HT2000

This is a Home Assistant integration for the HT2000 CO2 sensor.

[Home Assistant](https://www.home-assistant.io/) is a popular open source home automation platform.

## Usage

1. Genrate a token from Home Assistant.

2. Add the following to your Home Assistant configuration:

```yaml
template:
 - sensor:
   - name: "HT2000 CO2"
     unique_id: ht2000_co2_sensor
     unit_of_measurement: "ppm"
     device_class: carbon_dioxide
     state: "{{ states('sensor.ht2000_co2')|float(default=0) }}"
     availability: >-
       {{ (as_timestamp(now()) - as_timestamp(states.sensor.ht2000_co2.last_updated)) < 120 }}
   - name: "HT2000 Temperature"
     unique_id: ht2000_temperature_sensor
     unit_of_measurement: "°C"
     device_class: temperature
     state: "{{ states('sensor.ht2000_temperature')|float(default=0) }}"
     availability: >-
       {{ (as_timestamp(now()) - as_timestamp(states.sensor.ht2000_temperature.last_updated)) < 120 }}
   - name: "HT2000 Humidity"
     unique_id: ht2000_humidity_sensor
     unit_of_measurement: "%"
     device_class: humidity
     state: "{{ states('sensor.ht2000_humidity')|float(default=0) }}"
     availability: >-
       {{ (as_timestamp(now()) - as_timestamp(states.sensor.ht2000_humidity.last_updated)) < 120 }}
```

3. Create file `private.env` with the following content:
```
HA_HOST=http://homeassistant.local:8123
HA_TOKEN=YOUR_HA_TOKEN
HA_DEVICE_NAME=ht2000
```

NOTE: HA_DEVICE_NAME must be consistent with `ht2000` in the `state` and
`availability` fields.

4. Check you have the right hidraw devince in `docker-compose.yaml`.

5. Run the container:
```
cd ha
docker compose up -d --build
```
