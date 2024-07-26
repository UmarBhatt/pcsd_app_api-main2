from fastapi import FastAPI, File, UploadFile
from fastapi.responses import JSONResponse
from PIL import Image
import io
import numpy as np
import vgg16_  # Assuming this module contains necessary image processing functions

app = FastAPI()

@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.post("/upload-image/")
async def upload_image(file: UploadFile = File(...)):
    try:
        # Read the uploaded image file
        image = Image.open(io.BytesIO(await file.read()))
        
        # Process the image using the vgg16_ module (assumed to be defined in vgg16_.py)
        result = vgg16_.process_image(image)  # Replace with actual function
        
        # Ensure the result is JSON serializable
        def convert_to_serializable(obj):
            if isinstance(obj, np.ndarray):
                return obj.tolist()
            elif isinstance(obj, np.float32):
                return float(obj)
            elif isinstance(obj, (list, tuple)):
                return [convert_to_serializable(item) for item in obj]
            elif isinstance(obj, dict):
                return {key: convert_to_serializable(value) for key, value in obj.items()}
            return obj

        result = convert_to_serializable(result)
        
        # Return the result as JSON
        return JSONResponse(content={"result": result})
    except Exception as e:
        return JSONResponse(content={"error": str(e)}, status_code=400)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
