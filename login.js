// ==================== Login Form Handling ====================
const loginForm = document.getElementById('loginForm');
const usernameInput = document.getElementById('username');
const passwordInput = document.getElementById('password');
const errorMessage = document.getElementById('errorMessage');
const submitBtn = document.querySelector('.submit-btn');

// ==================== Form Validation ====================
/**
 * Validate login form inputs
 * @returns {boolean} - True if form is valid, false otherwise
 */
function validateForm() {
    const username = usernameInput.value.trim();
    const password = passwordInput.value.trim();
    
    if (!username || !password) {
        showError('Username and password are required');
        return false;
    }
    
    if (username.length < 3) {
        showError('Username must be at least 3 characters');
        return false;
    }
    
    if (password.length < 1) {
        showError('Password cannot be empty');
        return false;
    }
    
    return true;
}

/**
 * Display error message
 * @param {string} message - Error message to display
 */
function showError(message) {
    errorMessage.textContent = message;
    errorMessage.style.display = 'block';
}

/**
 * Hide error message
 */
function hideError() {
    errorMessage.style.display = 'none';
    errorMessage.textContent = '';
}

/**
 * Simulate login - in production, this would call your API
 */
function handleLogin(e) {
    e.preventDefault();
    
    // Clear previous errors
    hideError();
    
    // Validate form
    if (!validateForm()) {
        return;
    }
    
    const username = usernameInput.value.trim();
    const password = passwordInput.value.trim();
    
    // Disable submit button during processing
    submitBtn.disabled = true;
    submitBtn.textContent = 'Logging in...';
    
    // Simulate API call delay
    setTimeout(() => {
        // TODO: Replace with actual API call to /api/login
        // For now, accept any non-empty username/password combination
        // In production:
        // fetch('/api/login', {
        //     method: 'POST',
        //     headers: { 'Content-Type': 'application/json' },
        //     body: JSON.stringify({ username, password })
        // })
        // .then(res => res.json())
        // .then(data => {
        //     if (data.success) {
        //         setCookie('authToken', data.token);
        //         setCookie('username', username);
        //         // Redirect after short delay
        //         setTimeout(() => {
        //             window.location.href = 'index.html';
        //         }, 500);
        //     } else {
        //         showError(data.message || 'Login failed');
        //         submitBtn.disabled = false;
        //         submitBtn.textContent = 'Login';
        //     }
        // });
        
        // Mock login: set cookies and redirect
        setCookie('authToken', 'mock_token_' + Date.now());
        setCookie('username', username);
        
        // Redirect after short delay for UX feedback
        setTimeout(() => {
            window.location.href = 'index.html';
        }, 500);
        
    }, 1000); // Simulate network delay
}

// ==================== Event Listeners ====================
if (loginForm) {
    loginForm.addEventListener('submit', handleLogin);
}

// Clear error on input
if (usernameInput) {
    usernameInput.addEventListener('focus', hideError);
}

if (passwordInput) {
    passwordInput.addEventListener('focus', hideError);
}
