// ==================== Cookie Utilities ====================
/**
 * Set a cookie with optional expiry time
 * @param {string} name - Cookie name
 * @param {string} value - Cookie value
 * @param {number} expiryHours - Expiry time in hours (optional, default: session)
 */
function setCookie(name, value, expiryHours = null) {
    let cookieString = `${name}=${encodeURIComponent(value)}; path=/`;
    
    if (expiryHours) {
        const date = new Date();
        date.setTime(date.getTime() + expiryHours * 60 * 60 * 1000);
        cookieString += `; expires=${date.toUTCString()}`;
    }
    
    document.cookie = cookieString;
}

/**
 * Get a cookie value by name
 * @param {string} name - Cookie name
 * @returns {string|null} - Cookie value or null if not found
 */
function getCookie(name) {
    const nameEQ = name + "=";
    const cookies = document.cookie.split(';');
    
    for (let cookie of cookies) {
        cookie = cookie.trim();
        if (cookie.indexOf(nameEQ) === 0) {
            return decodeURIComponent(cookie.substring(nameEQ.length));
        }
    }
    
    return null;
}

/**
 * Delete a cookie by name
 * @param {string} name - Cookie name
 */
function deleteCookie(name) {
    setCookie(name, '', -1);
}

/**
 * Check if user is currently logged in
 * @returns {boolean} - True if user token exists in cookies
 */
function isLoggedIn() {
    return getCookie('authToken') !== null;
}

/**
 * Get logged-in username from cookie
 * @returns {string|null} - Username or null if not logged in
 */
function getUsername() {
    return getCookie('username');
}

/**
 * Log out user by clearing auth cookies
 */
function logout() {
    deleteCookie('authToken');
    deleteCookie('username');
}

// ==================== UI State Management ====================
/**
 * Update navbar to reflect login status
 */
function updateAuthUI() {
    const navLinks = document.querySelector('.nav-links');
    if (!navLinks) return;
    
    const loginItem = navLinks.querySelector('li:last-child');
    if (!loginItem) return;
    
    if (isLoggedIn()) {
        const username = getUsername();
        
        // Create user dropdown HTML
        loginItem.innerHTML = `
            <div class="user-dropdown">
                <button class="user-trigger">
                    <span class="username-text">${username}</span>
                    <span class="dropdown-arrow">▼</span>
                </button>
                <div class="dropdown-menu">
                    <a href="bookmarks.html" class="dropdown-item bookmarks-link">Bookmarks</a>
                    <button id="logoutBtn" class="dropdown-item logout-item">Logout</button>
                </div>
            </div>
        `;
        
        // Attach dropdown toggle handler
        const userTrigger = loginItem.querySelector('.user-trigger');
        const dropdownMenu = loginItem.querySelector('.dropdown-menu');
        
        userTrigger.addEventListener('click', (e) => {
            e.preventDefault();
            dropdownMenu.classList.toggle('active');
        });
        
        // Close dropdown when clicking outside
        document.addEventListener('click', (e) => {
            if (!loginItem.contains(e.target)) {
                dropdownMenu.classList.remove('active');
            }
        });
        
        // Attach logout handler
        const logoutBtn = loginItem.querySelector('#logoutBtn');
        logoutBtn.addEventListener('click', (e) => {
            e.preventDefault();
            logout();
            window.location.href = 'index.html';
        });
    } else {
        loginItem.innerHTML = `<a href="login.html" class="login-link">Login</a>`;
    }
}

/**
 * Run on page load to check and update auth status
 */
function checkAuthStatus() {
    updateAuthUI();
}
