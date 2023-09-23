from modal import Stub, web_endpoint, Image, Secret
from pydantic import BaseModel

"""
This is a function which take a string and return it's embedding
"""

MODEL_NAME = "thenlper/gte-large"


def download_model_weights() -> None:
    from huggingface_hub import snapshot_download
    from transformers.utils import move_cache
    from sentence_transformers import SentenceTransformer

    snapshot_download(repo_id=MODEL_NAME)

    # We also download the onnx model by running this
    model = SentenceTransformer(MODEL_NAME)

    move_cache()


image = (
    Image.debian_slim()
    .pip_install(
        "transformers",
        "torch",
        "huggingface_hub",
        "sentence_transformers",
        "pinecone-client",
        "replicate",
    )
    .run_function(download_model_weights)
)


stub = Stub("embedding", image=image)


class PromptInput(BaseModel):
    prompt: str
    prev_messages: str


@stub.function(secrets=[Secret.from_name("pinecone"), Secret.from_name("replicate")])
@web_endpoint(method="POST")
def embed(input: PromptInput):
    from sentence_transformers import SentenceTransformer
    import pinecone
    import os
    import replicate

    pinecone.init(
        api_key=os.environ["PINECONE_API_KEY"], environment="asia-northeast1-gcp"
    )
    index = pinecone.Index("chinesewall")

    model = SentenceTransformer(MODEL_NAME)
    embedding = model.encode([input.prompt])[0].tolist()
    results = index.query(embedding, top_k=2, include_metadata=True)

    context = [i["metadata"]["text"] for i in results["matches"]]
    combined_context = "\n-".join(context)

    formatted_system_prompt = f"As an AI assistant for the Chinese Wall Coding Competition organized by UBS, respond to participants' questions with concise, 2-sentence answers. Start with 'Hi there!' and only use information from the provided context.{combined_context}\n If unsure, reply with 'I don't have a good answer'. here are the past 3 messages the user has sent: {input.prev_messages}."

    print(formatted_system_prompt)
    output = replicate.run(
        "meta/llama-2-13b-chat:f4e2de70d66816a838a89eeeb621910adffb0dd0baba3976c96980970978018d",
        input={
            "system_prompt": formatted_system_prompt,
            "prompt": f"Please generate a response to this question : {input.prompt}",
        },
        max_tokens=2000,
        temperature=0.75,
    )

    list_output = "".join(list(output))

    return {"results": list_output}
