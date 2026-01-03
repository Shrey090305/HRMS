// Global JavaScript for DayFlow HRMS

document.addEventListener('DOMContentLoaded', function() {
    // Auto-dismiss alerts after 5 seconds
    const alerts = document.querySelectorAll('.alert');
    alerts.forEach(alert => {
        setTimeout(() => {
            const bsAlert = new bootstrap.Alert(alert);
            bsAlert.close();
        }, 5000);
    });

    // Confirm delete actions
    const deleteButtons = document.querySelectorAll('.btn-delete');
    deleteButtons.forEach(button => {
        button.addEventListener('click', function(e) {
            if (!confirm('Are you sure you want to delete this item?')) {
                e.preventDefault();
            }
        });
    });

    // Form validation feedback
    const forms = document.querySelectorAll('.needs-validation');
    forms.forEach(form => {
        form.addEventListener('submit', function(event) {
            if (!form.checkValidity()) {
                event.preventDefault();
                event.stopPropagation();
            }
            form.classList.add('was-validated');
        });
    });

    // Initialize tooltips
    const tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    tooltipTriggerList.map(function (tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl);
    });

    // Date input - set max to today for date of birth
    const dobInputs = document.querySelectorAll('input[name="date_of_birth"]');
    const today = new Date().toISOString().split('T')[0];
    dobInputs.forEach(input => {
        input.setAttribute('max', today);
    });

    // File input preview for profile pictures
    const profilePictureInput = document.getElementById('profile_picture');
    if (profilePictureInput) {
        profilePictureInput.addEventListener('change', function(e) {
            const file = e.target.files[0];
            if (file) {
                if (file.size > 5 * 1024 * 1024) {
                    alert('File size must be less than 5MB');
                    e.target.value = '';
                    return;
                }
                
                // Show preview if there's an image element
                const reader = new FileReader();
                reader.onload = function(e) {
                    const preview = document.getElementById('profile-preview');
                    if (preview) {
                        preview.src = e.target.result;
                    }
                };
                reader.readAsDataURL(file);
            }
        });
    }

    // Password confirmation validation
    const passwordInput = document.getElementById('password');
    const confirmPasswordInput = document.getElementById('confirm_password');
    
    if (passwordInput && confirmPasswordInput) {
        confirmPasswordInput.addEventListener('input', function() {
            if (passwordInput.value !== confirmPasswordInput.value) {
                confirmPasswordInput.setCustomValidity('Passwords do not match');
            } else {
                confirmPasswordInput.setCustomValidity('');
            }
        });
    }

    // Calculate leave days automatically
    const startDateInput = document.getElementById('start_date');
    const endDateInput = document.getElementById('end_date');
    
    if (startDateInput && endDateInput) {
        function calculateDays() {
            const startDate = new Date(startDateInput.value);
            const endDate = new Date(endDateInput.value);
            
            if (startDate && endDate && endDate >= startDate) {
                const diffTime = Math.abs(endDate - startDate);
                const diffDays = Math.ceil(diffTime / (1000 * 60 * 60 * 24)) + 1;
                
                const daysDisplay = document.getElementById('days-display');
                if (daysDisplay) {
                    daysDisplay.textContent = `Total days: ${diffDays}`;
                }
            }
        }
        
        startDateInput.addEventListener('change', calculateDays);
        endDateInput.addEventListener('change', calculateDays);
    }

    // Real-time search with debounce
    const searchInput = document.querySelector('input[name="search"]');
    if (searchInput) {
        let timeout;
        searchInput.addEventListener('input', function() {
            clearTimeout(timeout);
            timeout = setTimeout(() => {
                // You can implement AJAX search here
                console.log('Searching for:', this.value);
            }, 500);
        });
    }

    // Auto-calculate net salary in payroll
    const basicSalaryInput = document.getElementById('basic_salary');
    const allowancesInput = document.getElementById('allowances');
    const deductionsInput = document.getElementById('deductions');
    
    if (basicSalaryInput && allowancesInput && deductionsInput) {
        function calculateNetSalary() {
            const basic = parseFloat(basicSalaryInput.value) || 0;
            const allowances = parseFloat(allowancesInput.value) || 0;
            const deductions = parseFloat(deductionsInput.value) || 0;
            const net = basic + allowances - deductions;
            
            const netSalaryDisplay = document.getElementById('net-salary-display');
            if (netSalaryDisplay) {
                netSalaryDisplay.textContent = `Net Salary: $${net.toFixed(2)}`;
            }
        }
        
        basicSalaryInput.addEventListener('input', calculateNetSalary);
        allowancesInput.addEventListener('input', calculateNetSalary);
        deductionsInput.addEventListener('input', calculateNetSalary);
    }
});

// Utility function for AJAX requests
function makeRequest(url, method = 'GET', data = null) {
    const options = {
        method: method,
        headers: {
            'Content-Type': 'application/json',
        }
    };
    
    if (data) {
        options.body = JSON.stringify(data);
    }
    
    return fetch(url, options)
        .then(response => response.json())
        .catch(error => {
            console.error('Error:', error);
            throw error;
        });
}

// Export for use in other scripts
window.hrmsUtils = {
    makeRequest
};
