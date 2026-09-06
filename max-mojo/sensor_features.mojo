def calculate_feature_score(
    temperature: Float64,
    humidity: Float64,
    vibration: Float64
) -> Float64:
    var temperature_norm = temperature / 45.0
    var humidity_norm = humidity / 100.0
    var vibration_norm = vibration

    return (
        temperature_norm
        + humidity_norm
        + vibration_norm
    )


def main():
    var temperature: Float64 = 37.5
    var humidity: Float64 = 70.0
    var vibration: Float64 = 0.6

    var score = calculate_feature_score(
        temperature,
        humidity,
        vibration
    )

    print("Ecrio Mojo Feature Processing")
    print("Feature score:", score)
