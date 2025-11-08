// CleanEarth Community - Complete JavaScript

document.addEventListener('DOMContentLoaded', function() {
    initializeApplication();
});

function initializeApplication() {
    // Auto-hide flash messages after 5 seconds
    initializeFlashMessages();
    
    // Initialize form validations
    initializeFormValidations();
    
    // Initialize tooltips
    initializeTooltips();
    
    console.log('✅ CleanEarth Community initialized successfully!');
}

function initializeFlashMessages() {
    const flashMessages = document.querySelectorAll('.alert');
    flashMessages.forEach(alert => {
        setTimeout(() => {
            const bsAlert = new bootstrap.Alert(alert);
            bsAlert.close();
        }, 5000);
    });
}

function initializeFormValidations() {
    // File upload validation
    const fileInputs = document.querySelectorAll('input[type="file"]');
    fileInputs.forEach(input => {
        input.addEventListener('change', function(e) {
            validateFileUpload(this);
        });
    });

    // Form submission loading states
    const forms = document.querySelectorAll('form');
    forms.forEach(form => {
        form.addEventListener('submit', function(e) {
            const submitBtn = this.querySelector('button[type="submit"]');
            if (submitBtn && this.checkValidity()) {
                showLoadingState(submitBtn);
            }
        });
    });

    // Upload form specific validation
    const uploadForm = document.getElementById('uploadForm');
    if (uploadForm) {
        uploadForm.addEventListener('submit', function(e) {
            if (!validateUploadForm()) {
                e.preventDefault();
            }
        });
    }
}

function initializeTooltips() {
    const tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    const tooltipList = tooltipTriggerList.map(function (tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl);
    });
}

function validateFileUpload(input) {
    const file = input.files[0];
    if (!file) return;

    const maxSize = 16 * 1024 * 1024; // 16MB
    const allowedTypes = ['image/jpeg', 'image/jpg', 'image/png', 'image/gif', 'image/webp'];

    if (file.size > maxSize) {
        showNotification('File size must be less than 16MB.', 'error');
        input.value = '';
        return;
    }

    if (!allowedTypes.includes(file.type)) {
        showNotification('Please upload only image files (JPG, PNG, GIF, WebP).', 'error');
        input.value = '';
        return;
    }

    // Show file preview
    showFilePreview(input, file);
}

function validateUploadForm() {
    const beforePhoto = document.querySelector('input[name="before_photo"]');
    const afterPhoto = document.querySelector('input[name="after_photo"]');
    const wasteKg = document.querySelector('input[name="waste_kg"]');
    
    if (!beforePhoto.files[0] || !afterPhoto.files[0]) {
        showNotification('Please upload BOTH images to earn points.', 'error');
        return false;
    }
    
    if (parseFloat(wasteKg.value) <= 0) {
        showNotification('Please enter a valid waste amount (greater than 0).', 'error');
        return false;
    }
    
    return true;
}

function showFilePreview(input, file) {
    // Remove existing preview
    const existingPreview = input.parentNode.querySelector('.file-preview');
    if (existingPreview) {
        existingPreview.remove();
    }

    // Create preview element
    const preview = document.createElement('div');
    preview.className = 'file-preview mt-2';
    
    if (file.type.startsWith('image/')) {
        const reader = new FileReader();
        reader.onload = function(e) {
            preview.innerHTML = `
                <div class="border rounded p-2 bg-light text-center">
                    <img src="${e.target.result}" class="img-thumbnail" style="max-height: 100px; max-width: 100%;">
                    <div class="mt-1 small text-muted">${file.name}</div>
                    <div class="small text-muted">${(file.size / 1024 / 1024).toFixed(2)} MB</div>
                </div>
            `;
        };
        reader.readAsDataURL(file);
    }
    
    input.parentNode.appendChild(preview);
}

function showLoadingState(button) {
    const originalText = button.innerHTML;
    button.setAttribute('data-original-text', originalText);
    button.disabled = true;
    button.innerHTML = `
        <span class="spinner-border spinner-border-sm me-2" role="status"></span>
        Processing...
    `;
    
    // Re-enable after 30 seconds (safety measure)
    setTimeout(() => {
        resetButtonState(button);
    }, 30000);
}

function resetButtonState(button) {
    const originalText = button.getAttribute('data-original-text');
    if (originalText) {
        button.innerHTML = originalText;
        button.disabled = false;
    }
}

function showNotification(message, type = 'info') {
    // Remove existing notifications
    const existingNotifications = document.querySelectorAll('.custom-notification');
    existingNotifications.forEach(notification => notification.remove());

    // Create notification element
    const notification = document.createElement('div');
    notification.className = `custom-notification alert alert-${type === 'error' ? 'danger' : 'success'} alert-dismissible fade show`;
    notification.style.cssText = `
        position: fixed;
        top: 20px;
        right: 20px;
        z-index: 1060;
        min-width: 300px;
        box-shadow: 0 5px 15px rgba(0,0,0,0.2);
    `;
    notification.innerHTML = `
        <div class="d-flex align-items-center">
            <i class="fas fa-${type === 'error' ? 'exclamation-triangle' : 'check-circle'} me-2"></i>
            <span>${message}</span>
            <button type="button" class="btn-close ms-auto" data-bs-dismiss="alert"></button>
        </div>
    `;
    
    document.body.appendChild(notification);
    
    // Auto remove after 5 seconds
    setTimeout(() => {
        if (notification.parentNode) {
            notification.parentNode.removeChild(notification);
        }
    }, 5000);
}

// Mobile sidebar toggle
function toggleSidebar() {
    const sidebar = document.querySelector('.sidebar');
    sidebar.classList.toggle('show');
}

// Points calculator for upload form
function calculatePointsPreview() {
    const wasteKgInput = document.querySelector('input[name="waste_kg"]');
    if (wasteKgInput) {
        wasteKgInput.addEventListener('input', function() {
            const wasteKg = parseFloat(this.value) || 0;
            const basePoints = 10;
            const totalPoints = basePoints;
            
            const pointsElement = document.getElementById('points-preview');
            if (pointsElement) {
                pointsElement.textContent = `Estimated points: ${totalPoints}`;
            }
        });
    }
}

// Initialize points calculator
calculatePointsPreview();

// Export functions for global access
window.toggleSidebar = toggleSidebar;
window.showNotification = showNotification;