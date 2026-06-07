import os
import shutil
from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pydantic import BaseModel
from typing import List

from search import JewellerySearchEngine

# Initialize FastAPI
app = FastAPI(
    title="Jewellery Visual Search API",
    description="Backend API for similarity search on the RingFIR dataset using EfficientNetB0 and FAISS.",
    version="1.0.0"
)

# Enable CORS (Cross-Origin Resource Sharing)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify actual frontend origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Global search engine variable
search_engine = None

# Create temp directory for uploaded queries
TEMP_DIR = "temp_queries"
os.makedirs(TEMP_DIR, exist_ok=True)

@app.on_event("startup")
def startup_event():
    global search_engine
    index_file = "faiss_index.bin"
    paths_file = "image_paths.pkl"
    
    if not os.path.exists(index_file) or not os.path.exists(paths_path := paths_file):
        print("WARNING: FAISS index or image paths not found! Search endpoints will fail until index is built.")
    else:
        try:
            search_engine = JewellerySearchEngine(index_path=index_file, paths_path=paths_file)
        except Exception as e:
            print(f"Error loading search engine: {e}")

# Serve the data directory so the frontend can display the images
if os.path.exists("data"):
    app.mount("/data", StaticFiles(directory="data"), name="data")

# Serve the frontend directory for static assets
if os.path.exists("frontend"):
    app.mount("/frontend", StaticFiles(directory="frontend"), name="frontend")

# Route for serving the frontend index.html at root
@app.get("/")
def read_root():
    index_path = os.path.join("frontend", "index.html")
    if os.path.exists(index_path):
        return FileResponse(index_path)
    return {"message": "Jewellery Visual Search API is running. Build index and place frontend files to see the UI."}

class SearchResult(BaseModel):
    image_path: str
    distance: float
    similarity: float

class SearchResponse(BaseModel):
    success: bool
    results: List[SearchResult]
    query_image: str = None

@app.post("/search", response_model=SearchResponse)
async def search_images(file: UploadFile = File(...)):
    global search_engine
    
    # Check if search engine is initialized
    if search_engine is None:
        # Try to initialize again in case index was created post-startup
        index_file = "faiss_index.bin"
        paths_file = "image_paths.pkl"
        if os.path.exists(index_file) and os.path.exists(paths_file):
            try:
                search_engine = JewellerySearchEngine(index_path=index_file, paths_path=paths_file)
            except Exception as e:
                raise HTTPException(status_code=500, detail=f"Failed to load search engine: {e}")
        else:
            raise HTTPException(
                status_code=503, 
                detail="Search engine not ready. FAISS index or image paths not found on server."
            )
            
    # Check if uploaded file is an image
    if not file.content_type.startswith("image/"):
        raise HTTPException(status_code=400, detail="Uploaded file must be an image.")
        
    try:
        # Save uploaded file to temp directory
        temp_file_path = os.path.join(TEMP_DIR, file.filename)
        with open(temp_file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
            
        # Run similarity search
        results = search_engine.search(temp_file_path, top_k=10)
        
        # Clean up temp file
        # Optional: We could keep the last queried image to show on frontend, 
        # but serving it would require mounting the temp directory. Let's do that!
        
        # Format results (normalize paths for URL access)
        formatted_results = []
        for res in results:
            formatted_results.append(SearchResult(
                image_path=res["image_path"],
                distance=res["distance"],
                similarity=res["similarity"]
            ))
            
        return SearchResponse(
            success=True,
            results=formatted_results,
            query_image=f"/temp/{file.filename}"
        )
        
    except Exception as e:
        print(f"Error handling search request: {e}")
        raise HTTPException(status_code=500, detail=f"Search failed: {str(e)}")

# Mount the temp directory to serve uploaded images (useful for showing user query in UI)
app.mount("/temp", StaticFiles(directory=TEMP_DIR), name="temp")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="localhost", port=8000, reload=True)
