from contextlib import asynccontextmanager

from fastapi import FastAPI, HTTPException, Request
from pydantic import BaseModel, ConfigDict, Field
from transformers import pipeline


@asynccontextmanager
async def lifespan(app: FastAPI):
    app.state.generator = pipeline("text-generation", model="openai-community/gpt2", device=-1)
    yield


app = FastAPI(title="Geração de texto com GPT-2", lifespan=lifespan)


class GenerationInput(BaseModel):
    model_config = ConfigDict(str_strip_whitespace=True)

    prompt: str = Field(min_length=1, max_length=2000)


class GenerationOutput(BaseModel):
    generated_text: str


@app.post("/generate", response_model=GenerationOutput)
def generate(body: GenerationInput, request: Request):
    generator = request.app.state.generator
    max_new_tokens = 48
    available_tokens = generator.model.config.n_positions - max_new_tokens
    if len(generator.tokenizer.encode(body.prompt, verbose=False)) > available_tokens:
        raise HTTPException(status_code=422, detail="A frase excede o contexto do GPT-2.")

    result = generator(
        body.prompt,
        max_new_tokens=max_new_tokens,
        do_sample=True,
        top_p=0.9,
        pad_token_id=generator.tokenizer.eos_token_id,
        return_full_text=True,
    )
    return {"generated_text": result[0]["generated_text"]}
