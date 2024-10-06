// (function () {
//     'use strict'
//     var forms = document.querySelectorAll('.needs-validation')
//     Array.prototype.slice.call(forms)
//         .forEach(function (form) {
//             form.addEventListener('submit', function (event) {
//                 if (!form.checkValidity()) {
//                     event.preventDefault()
//                     event.stopPropagation()
//                 }
//                 form.classList.add('was-validated')
//             }, false)
//         })
// })();

// (function () {
//     'use strict'
//     var forms = document.querySelectorAll('.needs-validation')
//     Array.prototype.slice.call(forms)
//         .forEach(function (form) {
//             form.addEventListener('submit', function (event) {
//                 if (!form.checkValidity()) {
//                     event.preventDefault()
//                     event.stopPropagation()
//                 }
//                 form.classList.add('was-validated')
//             }, false)
//         })
// })();


//     document.getElementById('myForm').addEventListener('submit', function(event) {
//         event.preventDefault(); // Prevent default form submission

//         if (!this.checkValidity()) {
//             event.stopPropagation();
//             this.classList.add('was-validated');
//             return;
//         }

//         const formData = new FormData(this);

//         fetch(this.action, {
//             method: 'POST',
//             body: formData
//         })
//         .then(response => response.json()) // Handle the server response
//         .then(data => {
//             alert('Form submitted successfully!');
//             this.reset();
//             this.classList.remove('was-validated');
//         })
//         .catch(error => {
//             console.error('Error:', error);
//             alert('An error occurred. Please try again.');
//         });
//     });


//     function previewLogo(event) {
//         const file = event.target.files[0];
//         const preview = document.getElementById('profileImagePreview');
        
//         if (file) {
//             const reader = new FileReader();
//             reader.onload = function(e) {
//                 preview.src = e.target.result;
//             }
//             reader.readAsDataURL(file);
//         } else {
//             preview.src = '';
//         }
//     }

//     function toggleEdit() {
//         const formElements = document.querySelectorAll('#instituteForm input, #instituteForm textarea');
//         const isReadonly = formElements[0].hasAttribute('readonly');

//         formElements.forEach(element => {
//             if (isReadonly) {
//                 element.removeAttribute('readonly');
//             } else {
//                 element.setAttribute('readonly', true);
//             }
//         });

//         document.getElementById('saveButton').classList.toggle('d-none');
//     }

//     document.getElementById('instituteForm').addEventListener('submit', function(event) {
//         event.preventDefault();
//         // Here, you can gather form data and send it to the server if needed
//         window.location.href = 'invoice.html'; // Redirect to the new page
//     });

//     function previewLogo(event) {
//         const file = event.target.files[0];
//         const preview = document.getElementById('profileImagePreview');
        
//         if (file) {
//             const reader = new FileReader();
//             reader.onload = function(e) {
//                 preview.src = e.target.result;
//             }
//             reader.readAsDataURL(file);
//         } else {
//             preview.src = '';
//         }
//     }

//     function toggleEdit() {
//         const formElements = document.querySelectorAll('#instituteForm input, #instituteForm textarea');
//         const isReadonly = formElements[0].hasAttribute('readonly');

//         formElements.forEach(element => {
//             if (isReadonly) {
//                 element.removeAttribute('readonly');
//             } else {
//                 element.setAttribute('readonly', true);
//             }
//         });

//         document.getElementById('saveButton').classList.toggle('d-none');
//     }

//     document.getElementById('instituteForm').addEventListener('submit', function(event) {
//         event.preventDefault();
//         // Here, you can gather form data and send it to the server if needed
//         window.location.href = 'details-institute.html'; // Redirect to the new page
//     });