// ==================== DOM Elements ====================
const searchBar = document.getElementById('searchBar');
const searchBtn = document.querySelector('.search-btn');
const reviewTiles = document.querySelectorAll('.review-tile');
const navLinks = document.querySelectorAll('.nav-links a');

// ==================== Search Functionality ====================
/**
 * Handle search button click and Enter key press
 */
function handleSearch() {
    const query = searchBar.value.trim();
    if (query) {
        console.log('Search query:', query);
        // Placeholder for future database query integration
        // This will be replaced with actual API call to fetch data
        alert(`Searching for: "${query}"\n\nThis will connect to your database later!`);
        searchBar.value = '';
    }
}

// Search button click listener
searchBtn.addEventListener('click', handleSearch);

// Search on Enter key press
searchBar.addEventListener('keypress', (e) => {
    if (e.key === 'Enter') {
        handleSearch();
    }
});

// ==================== Review Tile Interactions ====================
/**
 * Add click and hover handlers to review tiles
 */
reviewTiles.forEach((tile) => {
    // Click handler - could expand to show full review detail
    tile.addEventListener('click', function() {
        console.log('Review tile clicked:', this);
        // Placeholder for future detail view
        // Could add modal or navigate to detail page here
    });

    // Optional: Add smooth scale animation on click
    tile.addEventListener('mousedown', function() {
        this.style.transform = 'translateY(-6px) scale(0.98)';
    });

    tile.addEventListener('mouseup', function() {
        this.style.transform = 'translateY(-8px)';
    });

    tile.addEventListener('mouseleave', function() {
        this.style.transform = 'translateY(0)';
    });
});

// ==================== Smooth Scroll Navigation ====================
/**
 * Handle navigation link clicks with smooth scrolling
 */
navLinks.forEach((link) => {
    link.addEventListener('click', (e) => {
        e.preventDefault();
        const targetId = link.getAttribute('href');
        const targetSection = document.querySelector(targetId);

        if (targetSection) {
            targetSection.scrollIntoView({
                behavior: 'smooth',
                block: 'start',
            });
        }
    });
});

// ==================== Initialization ====================
/**
 * Initialize the page on load
 */
document.addEventListener('DOMContentLoaded', () => {
    console.log('ReviewHub homepage loaded!');
    // Check and update authentication status
    checkAuthStatus();
    // Placeholder for any other initialization logic
    // e.g., fetch initial data from database, set up event listeners, etc.
});
