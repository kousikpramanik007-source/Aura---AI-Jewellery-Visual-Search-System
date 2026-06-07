import os
import sys
import logging
import numpy as np
import faiss

# Set up logging configuration
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(sys.stdout)
    ]
)

def main():
    features_file = "features.npy"
    index_file = "faiss_index.bin"
    
    logging.info("Starting FAISS indexing process...")
    
    # Check if features file exists
    if not os.path.exists(features_file):
        logging.error(f"Features file '{features_file}' not found. Please run feature extraction first.")
        sys.exit(1)
        
    try:
        logging.info(f"Loading embeddings from {features_file}...")
        embeddings = np.load(features_file)
        logging.info(f"Loaded embeddings array of shape {embeddings.shape}")
        
        # FAISS requires float32 datatype
        if embeddings.dtype != np.float32:
            logging.info("Converting embeddings to float32...")
            embeddings = embeddings.astype('float32')
            
        # Get dimensions
        num_vectors, dimension = embeddings.shape
        logging.info(f"Number of vectors: {num_vectors}, Vector dimension: {dimension}")
        
        # Build index
        logging.info("Building FAISS IndexFlatL2...")
        index = faiss.IndexFlatL2(dimension)
        
        # Add vectors to index
        logging.info("Adding embeddings to the index...")
        index.add(embeddings)
        logging.info(f"Index built successfully. Total vectors in index: {index.ntotal}")
        
        # Save index to file
        logging.info(f"Saving FAISS index to {index_file}...")
        faiss.write_index(index, index_file)
        logging.info("FAISS indexing completed successfully!")
        
    except Exception as e:
        logging.error(f"An error occurred during FAISS indexing: {e}", exc_info=True)
        sys.exit(1)

if __name__ == "__main__":
    main()
