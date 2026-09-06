def calculate_risk(temperature: Float64, humidity: Float64, vibration: Float64) -> Float64:
    return (temperature / 45.0) + (humidity / 100.0) + vibration


def main():
    var temperature: Float64 = 37.5
    var humidity: Float64 = 70.0
    var vibration: Float64 = 0.6

    var risk = calculate_risk(temperature, humidity, vibration)

    print("Ecrio Mojo Test")
    print("Temperature:", temperature)
    print("Humidity:", humidity)
    print("Vibration:", vibration)
    print("Calculated risk:", risk)