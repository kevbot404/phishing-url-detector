let session;

async function loadModel(){
    session=await ort.InferenceSession.create("./model/model.onnx");
    console.log("Model loaded");
}

loadModel();

async function predict(){
    const url=document.getElementById("urlInput").value.trim();
    const result=document.getElementById("result");

    if(!url){
        result.innerHTML="Enter a URL";
        return;
    }

    if(!session){
        result.innerHTML="Model loading...";
        return;
    }

    try{
        const input=new ort.Tensor(
            "float32",
            Float32Array.from(extractFeatures(url)),
            [1,16]
        );

        const output=await session.run({
            [session.inputNames[0]]:input
        });

        const probs=output.probabilities.data;

        const prediction=probs[0]>probs[1]?0:1;

        const confidence=Math.max(...probs);

        result.innerHTML=`
        <b>URL:</b> ${url}<br><br>
        <b>Prediction:</b> ${prediction===0?"PHISHING":"LEGITIMATE"}<br>
        <b>Confidence:</b> ${(confidence*100).toFixed(2)}%
        `;
    }
    catch(e){
        console.error(e);
        result.innerHTML="Error: "+e.message;
    }
}