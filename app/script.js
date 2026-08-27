let session;

async function loadModel() {
    session = await ort.InferenceSession.create(
        "model.onnx"
    );
}

async function predict() {
    const url = document.getElementById("url").value;

    const features = extractFeatures(url);

    const tensor = new ort.Tensor(
        "float32",
        Float32Array.from(features),
        [1, features.length]
    );

    const output = await session.run({
        float_input: tensor
    });

    console.log(output);
}