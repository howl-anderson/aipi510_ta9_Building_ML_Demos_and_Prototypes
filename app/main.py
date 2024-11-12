from flask import Flask, jsonify, request


import numpy as np
import onnxruntime as rt

app = Flask(__name__)

# Load the model
sess = rt.InferenceSession(
    "celsius_fahrenheit.onnx",
    providers=rt.get_available_providers(),
)

# Get the inputs, a list of input tensors
input_tensors = input_name = sess.get_inputs()

# Get the first input tensor, the real input tensor
input_tensor = input_tensors[0]

# Get the name of the input tensor
input_name = input_tensor.name


@app.route("/")
def index():
    return app.send_static_file("index.html")


@app.route("/inference", methods=["GET"])
def parse():
    input = float(request.args.get("celsius"))

    # input is a list of list, so we need to create a list of list
    x = np.asarray([[input]], dtype=np.float32)

    outputs = sess.run(None, {input_name: x})

    # outputs is a list of output, the first one is the output
    output = outputs[0]

    # output is a list of list, so we need to extract the value
    y_hat = output.tolist()[0][0]

    result = {"celsius": input, "fahrenheit": y_hat}

    return jsonify(result)


if __name__ == "__main__":
    app.config["DEBUG"] = True
    app.run(host="0.0.0.0", port=5108)
