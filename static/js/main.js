document.addEventListener('DOMContentLoaded', function() {
    const sidebarToggle = document.getElementById('sidebarToggle');
    
    if (sidebarToggle) {
        sidebarToggle.addEventListener('click', function(e) {
            e.preventDefault();
            document.querySelector('#wrapper').classList.toggle('toggled');
        });
    }
    
    const passwordField = document.getElementById('id_password1');
    
    if (passwordField) {
        passwordField.addEventListener('input', function() {
            const password = this.value;
            let strength = 0;
            
            if (password.length >= 8) {
                strength += 1;
            }
            
            if (/[A-Z]/.test(password)) {
                strength += 1;
            }
            
            if (/[a-z]/.test(password)) {
                strength += 1;
            }
            
            if (/[0-9]/.test(password)) {
                strength += 1;
            }
            
            if (/[^A-Za-z0-9]/.test(password)) {
                strength += 1;
            }
            
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
                feedbackElement.innerHTML = '<div class="progress" style="height: 5px;"><div class="progress-bar bg-danger" style="width: 40%"></div></div><small class="text-danger">Contraseña debil</small>';
            } else if (strength <= 4) {
                feedbackElement.innerHTML = '<div class="progress" style="height: 5px;"><div class="progress-bar bg-warning" style="width: 70%"></div></div><small class="text-warning">Contraseña media</small>';
            } else {
                feedbackElement.innerHTML = '<div class="progress" style="height: 5px;"><div class="progress-bar bg-success" style="width: 100%"></div></div><small class="text-success">Contraseña fuerte</small>';
            }
        });
    }
    
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
