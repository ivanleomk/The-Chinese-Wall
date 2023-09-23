from modal import Image, Secret, Stub, method, gpu, web_endpoint


MODEL_NAME = "meta-llama/Llama-2-13b-chat-hf"
EMBEDDING_MODEl = "thenlper/gte-large"


def download_model_to_folder():
    from huggingface_hub import snapshot_download
    from transformers.utils import move_cache
    import os

    snapshot_download(
        MODEL_NAME,
        token=os.environ["HUGGINGFACE_TOKEN"],
    )
    snapshot_download(EMBEDDING_MODEl)
    move_cache()


image = (
    Image.from_registry("nvcr.io/nvidia/pytorch:22.12-py3")
    .pip_install("torch==2.0.1", index_url="https://download.pytorch.org/whl/cu118")
    # Pinned to 08/15/2023
    .pip_install(
        "vllm @ git+https://github.com/vllm-project/vllm.git@805de738f618f8b47ab0d450423d23db1e636fa2",
        "typing-extensions==4.5.0",  # >=4.6 causes typing issues
    )
    .pip_install("pinecone-client")
    .pip_install("sentence_transformers")
    # Use the barebones hf-transfer package for maximum download speeds. No progress bar, but expect 700MB/s.
    .pip_install("hf-transfer~=0.1")
    .env({"HF_HUB_ENABLE_HF_TRANSFER": "1"})
    .run_function(
        download_model_to_folder,
        secret=Secret.from_name("my-huggingface-secret"),
        timeout=60 * 20,
    )
)

stub = Stub("llama-13b-discord", image=image)
GPU_CONFIG = gpu.L4()


template = """<s>[INST]<<SYS>>
{system}
<</SYS>>

{user} [/INST] """
system_template = "You are a helpful, respectful and honest assistant here to help participants with a challenge called the Chinese Wall for a Coding Competition organised by UBS. Here is some useful information that will help you respond to the query by the partcipant. \n-{context}"


@stub.function(
    gpu=GPU_CONFIG,
    secrets=[Secret.from_name("my-huggingface-secret"), Secret.from_name("pinecone")],
)
@web_endpoint()
def respond(prompt: str):
    from vllm import LLM, SamplingParams
    import os
    import pinecone

    from sentence_transformers import SentenceTransformer

    model = SentenceTransformer("thenlper/gte-large")
    embedding = model.encode([prompt])[0].tolist()
    print("---Generated embedding of query")

    pinecone.init(
        api_key=os.environ["PINECONE_API_KEY"], environment="asia-northeast1-gcp"
    )
    index = pinecone.Index("chinesewall")
    match = index.query(embedding, top_k=2, include_metadata=True)
    results = [i["metadata"]["text"] for i in match["matches"]]
    print(results)
    model = LLM(model=MODEL_NAME)
    sampling_params = SamplingParams(
        temperature=0.5,
        top_p=0.95,
        max_tokens=1200,
        presence_penalty=1.15,
    )

    formatted_system_prompt = system_template.format(context="\n-".join(results))
    print(formatted_system_prompt)

    result = model.generate(
        [template.format(system=formatted_system_prompt, user=prompt)], sampling_params
    )
    response = result[0].outputs[0].text

    return {"response": response}
