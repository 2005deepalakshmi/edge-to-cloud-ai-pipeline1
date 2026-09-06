from max.graph import Graph, TensorType, DeviceRef
from max.dtype import DType
import max.graph.ops as ops


def sensor_forward(x):
    # Extract sensor values
    temperature = ops.slice_tensor(x, [0])
    humidity = ops.slice_tensor(x, [1])
    vibration = ops.slice_tensor(x, [2])

    # Normalize temperature
    temp_norm = ops.div(
        temperature,
        ops.constant(
            45.0,
            dtype=DType.float32,
            device=DeviceRef.CPU()
        )
    )

    # Normalize humidity
    hum_norm = ops.div(
        humidity,
        ops.constant(
            100.0,
            dtype=DType.float32,
            device=DeviceRef.CPU()
        )
    )

    # Calculate combined feature score
    score = ops.add(
        ops.add(temp_norm, hum_norm),
        vibration
    )

    return score


# Create MAX Graph
graph = Graph(
    "ecrio_sensor_graph",
    forward=sensor_forward,
    input_types=[
        TensorType(
            DType.float32,
            shape=[3],
            device=DeviceRef.CPU()
        )
    ]
)


print("MAX Graph Created Successfully")
print(graph)