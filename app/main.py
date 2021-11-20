import uvicorn
import asyncio

async def main():
    uvicorn.run("api:app", host="0.0.0.0", port=8000, reload=True)
    
if __name__ == "__main__":
    asyncio.run(main())