document.addEventListener('DOMContentLoaded', function() {
    // Get DOM elements
    const colorPicker = document.getElementById('colorPicker');
    const colorName = document.getElementById('colorName');
    const colorHex = document.getElementById('colorHex');
    const searchButton = document.getElementById('searchButton');
    const loadingSpinner = document.getElementById('loadingSpinner');
    const productsGrid = document.getElementById('productsGrid');
    const noResults = document.getElementById('noResults');

    // Update color information when color is picked
    colorPicker.addEventListener('input', function(e) {
        const hex = e.target.value;
        const colorMatch = ntc.name(hex);
        colorName.textContent = colorMatch[1]; // Get the color name
        colorHex.textContent = hex.toUpperCase();
        
        // Update button gradient based on selected color
        searchButton.style.background = `linear-gradient(135deg, ${hex}, var(--color-deep-purple))`;
    });

    // Function to extract relevant part of product title
    function extractBrandName(title) {
        // Split the title by common separators
        const words = title.split(/[\s-]/);
        
        // Get the first word (usually the brand name)
        let brandName = words[0];
        
        // If the first word is very short, include the second word
        if (brandName.length < 3 && words.length > 1) {
            brandName = words.slice(0, 2).join(' ');
        }
        
        // Return brand name + "Nail Polish"
        return `${brandName} Nail Polish`;
    }

    // Handle search button click
    searchButton.addEventListener('click', async function() {
        const selectedColor = colorName.textContent;
        // Create a more direct search query with the color name
        const searchQuery = `${selectedColor} color nail polish`;
        
        // Show loading spinner, hide other elements
        loadingSpinner.classList.remove('d-none');
        productsGrid.innerHTML = '';
        noResults.classList.add('d-none');

        try {
            // Fetch products from Flask endpoint
            const response = await fetch(`/search?q=${encodeURIComponent(searchQuery)}`);
            const products = await response.json();

            // Hide loading spinner
            loadingSpinner.classList.add('d-none');

            // Display products or no results message
            if (products.length > 0) {
                displayProducts(products);
            } else {
                noResults.classList.remove('d-none');
            }
        } catch (error) {
            console.error('Error fetching products:', error);
            loadingSpinner.classList.add('d-none');
            productsGrid.innerHTML = '<div class="col-12 text-center text-danger">Error loading products. Please try again.</div>';
        }
    });

    // Function to display products in grid
    function displayProducts(products) {
        productsGrid.innerHTML = ''; // Clear existing products

        products.forEach((product, index) => {
            const productCard = document.createElement('div');
            productCard.className = 'col-12 col-md-6 col-lg-4';
            productCard.style.animationDelay = `${index * 0.1}s`;
            
            // Extract short title
            const shortTitle = extractBrandName(product.title);
            
            productCard.innerHTML = `
                <div class="product-card">
                    <a href="${product.product_url}" target="_blank" class="text-decoration-none">
                        <img src="${product.image_url}" alt="${shortTitle}" class="product-image">
                        <div class="product-info">
                            <h5 class="product-title">${shortTitle}</h5>
                            ${product.price ? `<div class="product-price">${product.price}</div>` : ''}
                            ${product.rating ? `
                                <div class="product-rating">
                                    <i class="bi bi-star-fill text-warning"></i>
                                    ${product.rating}/5 
                                    ${product.reviews_count ? `(${product.reviews_count} reviews)` : ''}
                                </div>
                            ` : ''}
                        </div>
                    </a>
                </div>
            `;
            productsGrid.appendChild(productCard);
        });

        // Smooth scroll to products section
        const productsSection = document.querySelector('.products-section');
        setTimeout(() => {
            productsSection.scrollIntoView({ behavior: 'smooth', block: 'start' });
        }, 100);
    }

    // Trigger initial color update
    colorPicker.dispatchEvent(new Event('input'));
});
