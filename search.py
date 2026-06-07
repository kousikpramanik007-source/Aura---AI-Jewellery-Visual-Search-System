import os
import pickle
import numpy as np
import tensorflow as tf
from tensorflow.keras.applications.efficientnet import EfficientNetB0, preprocess_input
from tensorflow.keras.preprocessing import image
import faiss

class JewellerySearchEngine:
    def __init__(self, index_path="faiss_index.bin", paths_path="image_paths.pkl"):
        """
        Initializes the Search Engine by loading the model, FAISS index, and image paths.
        """
        self.index_path = index_path
        self.paths_path = paths_path
        
        # Load EfficientNetB0 for extracting query features
        print("Loading feature extraction model...")
        self.model = EfficientNetB0(weights='imagenet', include_top=False, pooling='avg')
        
        # Load FAISS index
        if not os.path.exists(index_path):
            raise FileNotFoundError(f"FAISS index file '{index_path}' not found. Please build the index first.")
        print(f"Loading FAISS index from {index_path}...")
        self.index = faiss.read_index(index_path)
        
        # Load image paths
        if not os.path.exists(paths_path):
            raise FileNotFoundError(f"Image paths file '{paths_path}' not found. Please run feature extraction first.")
        print(f"Loading image paths from {paths_path}...")
        with open(paths_path, "rb") as f:
            self.image_paths = pickle.load(f)
            
        print("Search engine initialized successfully!")

    def extract_features(self, img_path_or_file):
        """
        Extracts features (embedding) from a single image.
        Accepts either a file path (str) or a file-like object / PIL Image.
        """
        # If it's a string, load from path. Otherwise assume it's loaded PIL image or file-like object
        if isinstance(img_path_or_file, str):
            img = image.load_img(img_path_or_file, target_size=(224, 224))
        else:
            # Assume PIL Image or file-like object
            img = image.load_img(img_path_or_file, target_size=(224, 224))
            
        x = image.img_to_array(img)
        x = np.expand_dims(x, axis=0)
        x = preprocess_input(x)
        
        # Extract features
        embedding = self.model.predict(x, verbose=0)
        # Convert to float32 for FAISS
        return embedding.astype('float32')

    def search(self, query_img_path_or_file, top_k=10):
        """
        Searches the FAISS index for the top_k most similar images to the query image.
        Returns a list of dictionaries with image_path and score (L2 distance).
        """
        # Extract query embedding
        query_vector = self.extract_features(query_img_path_or_file)
        
        # Search index
        # index.search returns (distances, indices)
        distances, indices = self.index.search(query_vector, top_k)
        
        results = []
        # distances and indices are 2D arrays, since we only queried 1 vector, get the 0th elements
        for dist, idx in zip(distances[0], indices[0]):
            if idx < len(self.image_paths):
                img_path = self.image_paths[idx]
                results.append({
                    "image_path": img_path,
                    "distance": float(dist),
                    # Convert L2 distance to a simple similarity percentage score
                    # For L2, 0 distance is 100% match. We can use 1 / (1 + dist) as similarity.
                    "similarity": round(1 / (1 + float(dist)) * 100, 2)
                })
        return results

if __name__ == "__main__":
    import sys
    if len(sys.argv) < 2:
        print("Usage: python search.py <path_to_query_image>")
        sys.exit(1)
        
    query_path = sys.argv[1]
    if not os.path.exists(query_path):
        print(f"Error: Query image '{query_path}' not found.")
        sys.exit(1)
        
    try:
        engine = JewellerySearchEngine()
        results = engine.search(query_path, top_k=10)
        print("\n--- Search Results ---")
        for i, res in enumerate(results):
            print(f"{i+1}. Path: {res['image_path']}, Similarity: {res['similarity']}%, Distance: {res['distance']:.4f}")
    except Exception as e:
        print(f"Error during search: {e}")
