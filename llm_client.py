import asyncio
from groq import AsyncGroq
from config import GROQ_API_KEY, DEFAULT_LLM_MODEL, DEFAULT_TEMPERATURE


async def call_llm_async(prompt, model=DEFAULT_LLM_MODEL, temperature=DEFAULT_TEMPERATURE):
    """Call Groq LLM asynchronously."""
    client = AsyncGroq(api_key=GROQ_API_KEY)
    response = await client.chat.completions.create(
        model=model,
        messages=[{"role": "user", "content": prompt}],
        temperature=temperature
    )
    return response.choices[0].message.content.strip()


def call_llm(prompt, model=DEFAULT_LLM_MODEL, temperature=DEFAULT_TEMPERATURE):
    """Call Groq LLM synchronously."""
    return asyncio.run(call_llm_async(prompt, model, temperature))
