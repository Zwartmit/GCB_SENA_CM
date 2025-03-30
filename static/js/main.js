document.addEventListener('DOMContentLoaded', function() {
    // Sidebar toggle
    const sidebarToggle = document.getElementById('sidebarToggle');
    
    if (sidebarToggle) {
        sidebarToggle.addEventListener('click', function(e) {
            e.preventDefault();
            document.querySelector('#wrapper').classList.toggle('toggled');
        });
    }
    
    // Password field validation
    const passwordField = document.getElementById('id_password1');
    
    if (passwordField) {
        passwordField.addEventListener('input', function() {
            const password = this.value;
            let strength = 0;
            
            // Check length
            if (password.length >= 8) {
                strength += 1;
            }
            
            // Check for uppercase
            if (/[A-Z]/.test(password)) {
                strength += 1;
            }
            
            // Check for lowercase
            if (/[a-z]/.test(password)) {
                strength += 1;
            }
            
            // Check for numbers
            if (/[0-9]/.test(password)) {
                strength += 1;
            }
            
            // Check for special characters
            if (/[^A-Za-z0-9]/.test(password)) {
                strength += 1;
            }
            
            // Update feedback
            let feedbackElement = document.getElementById('password-strength');
            
            if (!feedbackElement) {
                feedbackElement = document.createElement('div');
                feedbackElement.id = 'password-strength';
                feedbackElement.classList.add('mt-2');
                this.parentNode.appendChild(feedbackElement);
            }
            
            if (strength === 0) {
                feedbackElement.innerHTML = '';
            } else if (strength <= 2) {
                feedbackElement.innerHTML = '<div class="progress" style="height: 5px;"><div class="progress-bar bg-danger" style="width: 40%"></div></div><small class="text-danger">Weak password</small>';
            } else if (strength <= 4) {
                feedbackElement.innerHTML = '<div class="progress" style="height: 5px;"><div class="progress-bar bg-warning" style="width: 70%"></div></div><small class="text-warning">Medium password</small>';
            } else {
                feedbackElement.innerHTML = '<div class="progress" style="height: 5px;"><div class="progress-bar bg-success" style="width: 100%"></div></div><small class="text-success">Strong password</small>';
            }
        });
    }
    
    // Auto-dismiss alerts after 5 seconds
    const alerts = document.querySelectorAll('.alert:not(.alert-permanent)');
    
    alerts.forEach(function(alert) {
        setTimeout(function() {
            const closeButton = alert.querySelector('.btn-close');
            if (closeButton) {
                closeButton.click();
            } else {
                alert.remove();
            }
        }, 5000);
    });
});
