from modal import Stub, web_endpoint, Image
import os


MODEL_NAME = "ivanleomk/bert_password_sniffer"


def download_model_weights() -> None:
    from huggingface_hub import snapshot_download
    from transformers.utils import move_cache

    snapshot_download(repo_id=MODEL_NAME)
    move_cache()


image = (
    Image.debian_slim()
    .pip_install("transformers", "torch", "huggingface_hub")
    .run_function(download_model_weights)
)

stub = Stub("bert-classifier", image=image)


@stub.function()
@web_endpoint()
def classify(prompt: str):
    from transformers import pipeline

    prediction = pipeline(
        "text-classification", model="ivanleomk/bert_password_sniffer"
    )
    return prediction.predict(prompt)[0]
