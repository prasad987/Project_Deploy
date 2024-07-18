document.addEventListener("DOMContentLoaded", function() {
    const fileInput = document.getElementById('file-input');
    const fileNameDisplay = document.getElementById('file-name');
    const imageDisplay = document.getElementById('image-display');

    fileInput.addEventListener('change', function() {
        const file = fileInput.files[0];
        const fileName = file ? file.name : 'No file chosen';
        fileNameDisplay.textContent = fileName;

        if (file) {
            const reader = new FileReader();
            reader.onload = function(e) {
                imageDisplay.src = e.target.result;
                imageDisplay.style.display = 'block';
            };
            reader.readAsDataURL(file);
        } else {
            imageDisplay.style.display = 'none';
        }
    });
});
