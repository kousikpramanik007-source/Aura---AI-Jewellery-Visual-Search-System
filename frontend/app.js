document.addEventListener('DOMContentLoaded', () => {
    // DOM Elements
    const dropZone = document.getElementById('drop-zone');
    const fileInput = document.getElementById('file-input');
    const uploadPlaceholder = document.getElementById('upload-placeholder');
    const previewContainer = document.getElementById('preview-container');
    const imagePreview = document.getElementById('image-preview');
    const removeBtn = document.getElementById('remove-btn');
    const searchBtn = document.getElementById('search-btn');
    const btnSpinner = document.getElementById('btn-spinner');
    const loaderSection = document.getElementById('loader-section');
    const resultsSection = document.getElementById('results-section');
    const resultsGrid = document.getElementById('results-grid');
    const resultsCount = document.getElementById('results-count');
    
    // Modal Elements
    const detailModal = document.getElementById('detail-modal');
    const modalImage = document.getElementById('modal-image');
    const modalTitle = document.getElementById('modal-title');
    const modalPath = document.getElementById('modal-path');
    const modalSimilarity = document.getElementById('modal-similarity');
    const modalDistance = document.getElementById('modal-distance');
    const modalClose = document.getElementById('modal-close');
    const modalOverlay = document.getElementById('modal-overlay');

    let selectedFile = null;

    // --- Drag & Drop Event Listeners ---
    ['dragenter', 'dragover'].forEach(eventName => {
        dropZone.addEventListener(eventName, (e) => {
            e.preventDefault();
            e.stopPropagation();
            dropZone.classList.add('dragover');
        }, false);
    });

    ['dragleave', 'drop'].forEach(eventName => {
        dropZone.addEventListener(eventName, (e) => {
            e.preventDefault();
            e.stopPropagation();
            dropZone.classList.remove('dragover');
        }, false);
    });

    dropZone.addEventListener('drop', (e) => {
        const dt = e.dataTransfer;
        const files = dt.files;
        if (files.length > 0) {
            handleFile(files[0]);
        }
    });

    dropZone.addEventListener('click', () => {
        if (!selectedFile) {
            fileInput.click();
        }
    });

    fileInput.addEventListener('change', (e) => {
        if (e.target.files.length > 0) {
            handleFile(e.target.files[0]);
        }
    });

    removeBtn.addEventListener('click', (e) => {
        e.stopPropagation();
        resetUpload();
    });

    searchBtn.addEventListener('click', () => {
        if (selectedFile) {
            performSearch(selectedFile);
        }
    });

    // --- Core Functions ---
    function handleFile(file) {
        if (!file.type.startsWith('image/')) {
            alert('Please upload an image file.');
            return;
        }

        selectedFile = file;
        
        // Show image preview
        const reader = new FileReader();
        reader.onload = (e) => {
            imagePreview.src = e.target.result;
            uploadPlaceholder.classList.add('hidden');
            previewContainer.classList.remove('hidden');
            searchBtn.disabled = false;
        };
        reader.readAsDataURL(file);
    }

    function resetUpload() {
        selectedFile = null;
        fileInput.value = '';
        imagePreview.src = '#';
        previewContainer.classList.add('hidden');
        uploadPlaceholder.classList.remove('hidden');
        searchBtn.disabled = true;
        resultsSection.classList.add('hidden');
    }

    async function performSearch(file) {
        // UI Updates for loading state
        searchBtn.disabled = true;
        btnSpinner.classList.remove('hidden');
        loaderSection.classList.remove('hidden');
        resultsSection.classList.add('hidden');

        const formData = new FormData();
        formData.append('file', file);

        try {
            const response = await fetch('/search', {
                method: 'POST',
                body: formData
            });

            if (!response.ok) {
                const errData = await response.json();
                throw new Error(errData.detail || 'Visual search failed.');
            }

            const data = await response.json();
            displayResults(data.results);
        } catch (error) {
            console.error('Error searching:', error);
            alert(`Error: ${error.message}`);
        } finally {
            // UI Updates for completed state
            searchBtn.disabled = false;
            btnSpinner.classList.add('hidden');
            loaderSection.classList.add('hidden');
        }
    }

    function displayResults(results) {
        resultsGrid.innerHTML = '';
        
        if (!results || results.length === 0) {
            resultsCount.textContent = '0 designs found';
            resultsGrid.innerHTML = '<p class="no-results">No matches found in the database.</p>';
            resultsSection.classList.remove('hidden');
            return;
        }

        resultsCount.textContent = `${results.length} designs found`;

        results.forEach((item, index) => {
            // Generate a clean filename for display, e.g., "001_001.png"
            const filename = item.image_path.split('/').pop();
            const displayName = filename.split('.')[0].replace('_', ' #');
            
            // Build the card element
            const card = document.createElement('div');
            card.className = 'result-card';
            card.innerHTML = `
                <div class="card-img-container">
                    <img src="/${item.image_path}" alt="Jewellery match ${index+1}">
                    <span class="similarity-badge">${item.similarity}% Match</span>
                </div>
                <div class="card-details">
                    <h3 class="card-title">Earring ${displayName}</h3>
                    <div class="card-meta">
                        <span>Rank: <strong class="card-meta-val">#${index+1}</strong></span>
                        <span>Distance: <strong class="card-meta-val">${item.distance.toFixed(4)}</strong></span>
                    </div>
                </div>
            `;

            // Card click handler for opening modal
            card.addEventListener('click', () => {
                openModal(item, displayName);
            });

            resultsGrid.appendChild(card);
        });

        resultsSection.classList.remove('hidden');
        // Scroll to results
        resultsSection.scrollIntoView({ behavior: 'smooth', block: 'start' });
    }

    // --- Modal Functions ---
    function openModal(item, displayName) {
        modalImage.src = `/${item.image_path}`;
        modalTitle.textContent = `Earring ${displayName}`;
        modalPath.textContent = item.image_path;
        modalSimilarity.textContent = `${item.similarity}% Match`;
        modalDistance.textContent = item.distance.toFixed(6);

        detailModal.classList.remove('hidden');
        document.body.style.overflow = 'hidden'; // Disable page scroll
    }

    function closeModal() {
        detailModal.classList.add('hidden');
        document.body.style.overflow = ''; // Re-enable page scroll
        // Clear modal elements
        modalImage.src = '';
    }

    modalClose.addEventListener('click', closeModal);
    modalOverlay.addEventListener('click', closeModal);
    
    // Close modal on Esc key
    document.addEventListener('keydown', (e) => {
        if (e.key === 'Escape' && !detailModal.classList.contains('hidden')) {
            closeModal();
        }
    });
});
