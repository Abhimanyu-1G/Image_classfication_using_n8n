
from fastapi import FastAPI
from pydantic import BaseModel 
from classify import classify_image
import uvicorn

app = FastAPI()
class ImagePath(BaseModel):
    path: str
@app.post("/classify")
async def classify(item: ImagePath):
    print(f"Processing path: {item.path}")
    result = classify_image(item.path) 
    return result

if __name__ == "__main__":

    uvicorn.run(app, host="0.0.0.0", port=8000)

