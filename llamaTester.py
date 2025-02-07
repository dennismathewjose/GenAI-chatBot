import asyncio
import httpx
 
async def process_chunk(system_prompt, chunk):
    async with httpx.AsyncClient(timeout=30.0) as client:
        response = await client.post(
            "http://127.0.0.1:11434/api/generate",
            json={
                "model": "llama3.2:3b",
                "prompt": f"{system_prompt}\n\nContent:\n{chunk}",
                "stream": False
            }
        )
        response.raise_for_status()
        result = response.json()
        print(result["response"])
 
if __name__ == "__main__":
    system_prompt = "Provide a summary of the given content."
    chunk = "This is a sample text chunk from the document that needs processing..." * 20  # Sample text
    asyncio.run(process_chunk(system_prompt, chunk))
