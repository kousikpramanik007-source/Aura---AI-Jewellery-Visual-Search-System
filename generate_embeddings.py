import os
import pickle
import numpy as np
import tensorflow as tf
from tensorflow.keras.applications.efficientnet import EfficientNetB0, preprocess_input
from tensorflow.keras.preprocessing import image
from tqdm import tqdm

def main():
    print("Initializing EfficientNetB0 model (include_top=False, pooling='avg')...")
    # Load model pre-trained on ImageNet
    model = EfficientNetB0(weights='imagenet', include_top=False, pooling='avg')
    
    # Path to dataset
    dataset_dir = "data/RingFIR"
    if not os.path.exists(dataset_dir):
        print(f"Error: Dataset directory '{dataset_dir}' not found.")
        return

    print("Traversing dataset directory to find images...")
    image_paths = []
    # Allowed image extensions
    allowed_extensions = ('.png', '.jpg', '.jpeg', '.webp')
    
    for root, dirs, files in os.walk(dataset_dir):
        for file in files:
            if file.lower().endswith(allowed_extensions):
                # Save path relative to the project root
                relative_path = os.path.relpath(os.path.join(root, file), start=os.getcwd())
                image_paths.append(relative_path)
                
    # Sort image paths to keep the order deterministic
    image_paths.sort()
    
    num_images = len(image_paths)
    print(f"Found {num_images} images to process.")
    
    if num_images == 0:
        print("No images found. Exiting.")
        return

    # Extract features in batches for speed
    batch_size = 32
    embeddings = []
    
    print("Extracting features (embeddings) using EfficientNetB0...")
    for i in tqdm(range(0, num_images, batch_size)):
        batch_paths = image_paths[i:i+batch_size]
        batch_images = []
        
        for img_path in batch_paths:
            try:
                # Load image and resize to 224x224 (EfficientNetB0 default size)
                img = image.load_img(img_path, target_size=(224, 224))
                x = image.img_to_array(img)
                batch_images.append(x)
            except Exception as e:
                print(f"\nError loading image {img_path}: {e}")
                # Fallback: append zero-array of correct shape so indexing matches
                batch_images.append(np.zeros((224, 224, 3)))
        
        # Convert batch to numpy array
        batch_x = np.array(batch_images)
        # Preprocess input (normalization for EfficientNet)
        batch_x = preprocess_input(batch_x)
        
        # Predict embeddings
        batch_embeddings = model.predict(batch_x, verbose=0)
        embeddings.extend(batch_embeddings)
        
    # Convert list of embeddings to a numpy array
    embeddings = np.array(embeddings)
    
    print(f"Embeddings shape: {embeddings.shape}")
    
    # Save embeddings to features.npy
    features_file = "features.npy"
    np.save(features_file, embeddings)
    print(f"Saved embeddings to {features_file}")
    
    # Save image paths to image_paths.pkl
    paths_file = "image_paths.pkl"
    with open(paths_file, "wb") as f:
        pickle.dump(image_paths, f)
    print(f"Saved image paths to {paths_file}")
    print("Feature extraction completed successfully!")

if __name__ == "__main__":
    main()
