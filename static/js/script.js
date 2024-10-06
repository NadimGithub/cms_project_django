document.addEventListener('DOMContentLoaded', function() {
    // Sidebar Toggle
    const sidebarToggle = document.querySelector("#sidebar-toggle");
    sidebarToggle.addEventListener("click", function() {
        document.querySelector("#sidebar").classList.toggle("collapsed");
    });

    // Theme Toggle
    document.querySelector(".theme-toggle").addEventListener("click", () => {
        toggleLocalStorage();
        toggleRootClass();
    });

    function toggleLocalStorage() {
        if (isLight()) {
            localStorage.removeItem("light");
        } else {
            localStorage.setItem("light", "set");
        }
    }

    function isLight() {
        return localStorage.getItem("light");
    }

    if (isLight()) {
        toggleRootClass();
    }

    // Form Validation
    const form = document.getElementById('myForm');
    const validationModal = new bootstrap.Modal(document.getElementById('validationModal'));
    const modalBody = document.getElementById('modalBody');

    form.addEventListener('submit', function(event) {
        if (!form.checkValidity()) {
            event.preventDefault(); // Prevent form from submitting
            event.stopPropagation(); // Stop event propagation

            // Collect invalid fields and display error messages
            modalBody.innerHTML = '';
            const invalidFields = form.querySelectorAll(':invalid');
            invalidFields.forEach(field => {
                const label = form.querySelector(`label[for="${field.id}"]`);
                const errorMessage = label ? label.innerText : 'Invalid field';
                modalBody.innerHTML += `<p>${errorMessage}</p>`;
            });

            validationModal.show();
            form.classList.add('was-validated'); // Add validation class
        } else {
            form.classList.remove('was-validated');
        }
    });

    // Input Feedback
    form.addEventListener('input', function(event) {
        const input = event.target;
        if (input.checkValidity()) {
            input.classList.remove('is-invalid');
            input.classList.add('is-valid');
        } else {
            input.classList.remove('is-valid');
            input.classList.add('is-invalid');
        }
    });

    // State and District Handling
    const districts = {
        Delhi: ['North Delhi', 'South Delhi', 'East Delhi', 'West Delhi'],
        Maharashtra: ['Mumbai', 'Pune', 'Nagpur', 'Aurangabad'],
        Karnataka: ['Bengaluru', 'Mysuru', 'Hubballi', 'Belagavi']
        // Add more states and districts as needed
    };

    document.getElementById('state').addEventListener('change', function() {
        const state = this.value;
        const districtSelect = document.getElementById('district');
        
        // Clear existing options
        districtSelect.innerHTML = '<option value="" disabled selected>Select a district</option>';
        
        // Populate new options
        if (state && districts[state]) {
            districts[state].forEach(district => {
                const option = document.createElement('option');
                option.value = district;
                option.textContent = district;
                districtSelect.appendChild(option);
            });
            districtSelect.disabled = false;
        } else {
            districtSelect.disabled = true;
        }
    });

    // Toggle Edit Mode
    document.getElementById('toggleEditButton').addEventListener('click', function() {
        toggleEditMode();
    });

    function toggleEditMode() {
        const formElements = document.querySelectorAll('#myForm input, #myForm textarea, #myForm select');
        const saveButton = document.getElementById('saveButton');
        const toggleButton = document.getElementById('toggleEditButton');

        formElements.forEach(element => {
            if (element.tagName === 'SELECT') {
                element.toggleAttribute('disabled');
            } else {
                element.toggleAttribute('readonly');
            }
        });

        saveButton.classList.toggle('d-none');
        toggleButton.textContent = toggleButton.textContent === 'Edit' ? 'Cancel' : 'Edit';
    }
});

// Initialize Datepicker
$(document).ready(function() {
    $('#duration').datepicker({
        format: 'mm/yyyy',
        startView: 1,
        minViewMode: 1,
        autoclose: true
    });
});


////

document.addEventListener('DOMContentLoaded', function() {
    document.getElementById('myForm').addEventListener('submit', function(event) {
        var form = event.target;
        if (!form.checkValidity()) {
            event.preventDefault(); // Prevent form from submitting
            event.stopPropagation(); // Stop event propagation
        }
        form.classList.add('was-validated'); // Add validation class
    });

    document.getElementById('myForm').addEventListener('input', function(event) {
        const input = event.target;
        if (input.checkValidity()) {
            input.classList.remove('is-invalid');
            input.classList.add('is-valid');
        } else {
            input.classList.remove('is-valid');
            input.classList.add('is-invalid');
        }
    });
});
