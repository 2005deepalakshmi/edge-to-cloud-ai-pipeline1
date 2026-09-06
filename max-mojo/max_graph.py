from max.graph import Graph, TensorType, DeviceRef
from max.dtype import DType
import max.graph.ops as ops


def build_sensor_graph():
    graph = Graph(
        "ecrio_sensor_features",
        input_types=[
            TensorType(DType.float32, [3], DeviceRef.CPU())
        ],
    )

    with graph:
        inputs = graph.inputs[0]

        temperature = ops.slice_tensor(inputs, [0], [1])
        humidity = ops.slice_tensor(inputs, [1], [1])
        vibration = ops.slice_tensor(inputs, [2], [1])

        temperature_norm = ops.div(
            temperature,
            ops.constant(45.0, DType.float32)
        )

        humidity_norm = ops.div(
            humidity,
            ops.constant(100.0, DType.float32)
        )

        score = ops.add(
            ops.add(temperature_norm, humidity_norm),
            vibration
        )

        graph.output(score)

    return graph


if __name__ == "__main__":
    graph = build_sensor_graph()
    print("Ecrio MAX sensor feature graph created successfully.")
    print(graph)

