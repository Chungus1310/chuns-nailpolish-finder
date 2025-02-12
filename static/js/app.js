document.addEventListener('DOMContentLoaded', function() {
    // DOM Elements
    const colorPicker = document.getElementById('colorPicker');
    const colorName = document.getElementById('colorName');
    const colorHex = document.getElementById('colorHex');
    const searchButton = document.getElementById('searchButton');
    const loadingSpinner = document.getElementById('loadingSpinner');
    const productsGrid = document.getElementById('productsGrid');
    const noResults = document.getElementById('noResults');
    const itemTypeInput = document.getElementById('itemType');
    const marketButtons = document.querySelectorAll('.market-btn');
    const body = document.body;

    // State
    let currentMarket = 'amazon';

    // Theme colors
    const themes = {
        amazon: {
            primary: '#FFE6E6',
            secondary: '#E1AFD1',
            tertiary: '#AD88C6',
            quaternary: '#7469B6'
        },
        yandex: {
            primary: '#DEAA79',
            secondary: '#FFE6A9',
            tertiary: '#B1C29E',
            quaternary: '#659287'
        }
    };

    // Market Button Event Listeners
    marketButtons.forEach(btn => {
        btn.addEventListener('click', function() {
            const market = this.getAttribute('data-market');
            switchMarketplace(market);
        });
    });

    function switchMarketplace(market) {
        // Update active state of buttons
        marketButtons.forEach(btn => {
            btn.classList.remove('active');
            if (btn.getAttribute('data-market') === market) {
                btn.classList.add('active');
            }
        });

        // Update theme
        body.classList.remove('amazon-theme', 'yandex-theme');
        body.classList.add(`${market}-theme`);
        
        // Update state
        currentMarket = market;

        // Clear results
        productsGrid.innerHTML = '';
        noResults.classList.add('d-none');

        // Update button gradient based on new theme
        updateSearchButtonGradient(colorPicker.value);
    }

    // Update color information when color is picked
    colorPicker.addEventListener('input', function(e) {
        const hex = e.target.value;
        updateColorInfo(hex);
    });

    function updateColorInfo(hex) {
        const colorMatch = ntc.name(hex);
        colorName.textContent = colorMatch[1];
        colorHex.textContent = hex.toUpperCase();
        updateSearchButtonGradient(hex);
    }

    function updateSearchButtonGradient(hex) {
        const theme = themes[currentMarket];
        searchButton.style.background = `linear-gradient(135deg, ${hex}, ${theme.quaternary})`;
    }

    function formatSearchQuery(color, itemType, market) {
        // Different query formats for each marketplace
        if (market === 'amazon') {
            return `"${color}" colored ${itemType}`;  // Exact match with quotes for Amazon
        } else {
            return `${color} colored ${itemType}`;    // Simple format for Yandex
        }
    }

    // Handle search button click
    searchButton.addEventListener('click', async function() {
        const selectedColor = colorName.textContent;
        const itemType = itemTypeInput.value.trim() || 'nail polish';
        
        // Format search query based on marketplace
        const searchQuery = formatSearchQuery(selectedColor, itemType, currentMarket);
        
        // Show loading spinner, hide other elements
        loadingSpinner.classList.remove('d-none');
        productsGrid.innerHTML = '';
        noResults.classList.add('d-none');

        try {
            // Fetch products from selected marketplace
            const response = await fetch(`/search?q=${encodeURIComponent(searchQuery)}&market=${currentMarket}`);
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
        productsGrid.innerHTML = '';

        products.forEach((product, index) => {
            const productCard = document.createElement('div');
            productCard.className = 'col-12 col-md-6 col-lg-4';
            productCard.style.animationDelay = `${index * 0.1}s`;
            
            productCard.innerHTML = `
                <div class="product-card">
                    <a href="${product.product_url}" target="_blank" class="text-decoration-none">
                        <img src="${product.image_url}" alt="${product.title}" class="product-image">
                        <div class="product-info">
                            <h5 class="product-title">${shortenTitle(product.title)}</h5>
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

    function shortenTitle(title) {
        const words = title.split(' ');
        // Keep more of the original title for better context
        return title.length > 50 ? title.substring(0, 50) + '...' : title;
    }

    // Trigger initial color update
    colorPicker.dispatchEvent(new Event('input'));
});
