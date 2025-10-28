from fastapi import FastAPI
from pydantic import BaseModel  # Import BaseModel
from classify import classify_image
import uvicorn
# shutil is no longer needed

app = FastAPI()

# 1. Define a model for the incoming JSON
class ImagePath(BaseModel):
    path: str

# 2. Change the endpoint to expect this JSON model
@app.post("/classify")
async def classify(item: ImagePath):
    # 3. No more temp files. Pass the path from the JSON directly.
    print(f"Processing path: {item.path}")
    result = classify_image(item.path) 
    return result

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)