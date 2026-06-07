# Aura - AI-Powered Jewellery Visual Search Engine

Aura is a luxury-themed, AI-powered jewellery visual search engine. It allows users to upload a photo of a jewellery piece (e.g. an earring) and instantly find the top 10 most visually similar designs from the RingFIR dataset.

The system uses a pre-trained **EfficientNetB0** model (ImageNet weights) to extract deep visual features and **FAISS** (Facebook AI Similarity Search) to build an efficient index for near-instant L2 similarity matching.

---

## Architecture

```
                       +-------------------------+
                       |   RingFIR Dataset       |
                       +------------+------------+
                                    |
                                    v (Traverse files)
                       +------------+------------+
                       |  generate_embeddings.py | <-- EfficientNetB0 (No training)
                       +------------+------------+
                                    |
                                    v (features.npy & image_paths.pkl)
                       +------------+------------+
                       |      build_index.py     | <-- FAISS IndexFlatL2
                       +------------+------------+
                                    |
                                    v (faiss_index.bin)
                       +------------+------------+
                       |        FastAPI          | <-- main.py & search.py
                       +------------+------------+
                                    ^
                                    | (Upload query / Return matches)
                       +------------+------------+
                       |   Glassmorphic UI (Web) | <-- HTML5 / Vanilla CSS / JS
                       +-------------------------+
```

---

## Directory Structure

```
.
├── data/
│   └── RingFIR/               # Dataset directory containing folders 001 to 046
├── frontend/
│   ├── index.html             # Premium user interface
│   ├── style.css              # Glassmorphism dark mode with gold accents
│   └── app.js                 # Drag & drop upload, API caller, and DOM renderer
├── .venv/                     # Virtual environment
├── .gitignore                 # Files excluded from git tracking
├── Dockerfile                 # Production build configuration
├── requirements.txt           # Project dependencies
├── generate_embeddings.py     # Stage 1: Feature extraction script
├── build_index.py             # Stage 2: FAISS indexing script
├── search.py                  # Search engine module
└── main.py                    # FastAPI server entrypoint
```

---

## Setup & Execution

### 1. Virtual Environment Setup

Create a virtual environment and install the required dependencies:

```bash
# Create virtual environment (if not already created)
python3 -m venv .venv

# Activate virtual environment
source .venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### 2. Extract Embeddings (Stage 1)

Traverse the dataset and generate visual embeddings for each jewellery image:

```bash
python generate_embeddings.py
```

This will generate:

- `features.npy`: Numpy array containing the extracted vectors.
- `image_paths.pkl`: Serialized list of relative file paths.

### 3. Build FAISS Index (Stage 2)

Index the extracted embeddings into FAISS for fast query matching:

```bash
python build_index.py
```

This will create:

- `faiss_index.bin`: The binary FAISS index file.

### 4. Run the Visual Search Web Application

Start the FastAPI server:

```bash
python main.py
```

The server will start at `http://localhost:8000`. 
Open `http://localhost:8000` in your web browser to use the premium visual search interface.

---

## Docker Deployment

You can build and run the entire application inside a Docker container:

```bash
# Build the Docker image
docker build -t aura-jewellery-search .

# Run the container (Make sure you have generated features/index files locally, or let them copy)
docker run -p 8000:8000 aura-jewellery-search
```

---

## Design Highlights

- **Luxury Dark Mode**: Sleek glassmorphism style using champagne gold accents (`#d4af37` / `#c5a880`) for a premium jewellery feel.
- **Micro-Animations**: Hover transitions, card scalings, inline skeleton spinners, and image detail modals for a responsive, interactive user experience.
- **Fast and Scalable**: Performs high-performance search queries in milliseconds using FAISS IndexFlatL2.

# Aura---AI-Jewellery-Visual-Search-System
