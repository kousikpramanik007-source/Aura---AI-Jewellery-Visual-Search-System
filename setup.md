Step 1: Repository analyze
Analyze this RingFIR repository.

Tasks:
1. Understand the dataset structure.
2. Identify how images and labels are organized.
3. Review all image retrieval notebooks.
4. Recommend the best pretrained model for a fast MVP.
5. Create a development plan for a Jewellery Image Search Website.

Do not write code yet.
Generate a detailed implementation roadmap.
Step 2: Feature extraction system
Implement a feature extraction pipeline.

Requirements:
- Use EfficientNetB0 pretrained on ImageNet.
- Do not train any model.
- Use include_top=False and pooling='avg'.
- Traverse all images inside the RingFIR dataset.
- Generate embeddings for every image.
- Save embeddings to features.npy.
- Save image paths to image_paths.pkl.
- Create a script named generate_embeddings.py.

Use clean, production-ready code.
Step 3: FAISS indexing
Create a FAISS indexing pipeline.

Requirements:
- Load features.npy.
- Build a FAISS IndexFlatL2 index.
- Store the index as faiss_index.bin.
- Create build_index.py.
- Add logging and error handling.
Step 4: Search engine
Create an image search module.

Requirements:
- Accept a query image.
- Extract its EfficientNetB0 embedding.
- Search FAISS index.
- Return top 10 similar images.
- Return image path and similarity score.
- Create search.py.

Code must be modular and reusable.
Step 5: FastAPI backend
Build a FastAPI backend.

Requirements:
- POST /search endpoint.
- Accept uploaded image.
- Run similarity search.
- Return top 10 matching images.
- Enable CORS.
- Organize project structure properly.
Step 6: Frontend
Create a modern frontend.

Requirements:
- HTML
- CSS
- JavaScript

Features:
- Upload image.
- Preview uploaded image.
- Display top 10 similar earrings.
- Responsive design.
- Dark mode styling.
Step 7: Connect everything
Integrate all modules.

Requirements:
- Feature extraction.
- FAISS search.
- FastAPI backend.
- Frontend UI.

Ensure the application runs end-to-end.

Provide:
- Complete folder structure.
- requirements.txt
- setup instructions.
Step 8: Deployment
Prepare the project for deployment.

Requirements:
- Dockerfile
- .gitignore
- README.md
- Environment setup instructions

Target:
- Local machine
- Render deployment
- Railway deployment
Final Prompt (One-shot)
Jodi ekbare shob korte chao:

Build a complete AI-powered Jewellery Visual Search Engine using the RingFIR dataset.

Requirements:
- EfficientNetB0 pretrained model
- No training
- Feature extraction pipeline
- FAISS vector search
- FastAPI backend
- HTML/CSS/JS frontend
- Top 10 similar image retrieval
- Modular architecture
- Production-ready code
- requirements.txt
- Dockerfile
- README.md
- Deployment instructions

Generate all source files with complete code.