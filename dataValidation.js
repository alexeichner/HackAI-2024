document.addEventListener('DOMContentLoaded', function() {
    const form = document.getElementById('form');

    form.addEventListener('submit', function(event) {
        event.preventDefault(); // Prevent the default form submission
        
        const areaInput = document.getElementById('area');
        const areaValue = parseInt(areaInput.value);
        
        // Check if the area value is a valid integer
        if (isNaN(areaValue)) {
            alert('Please enter a valid integer for the area.');
            areaInput.focus();
            return; // Stop further execution
        }

        // Collect all the form data
        const formData = {
            area: document.getElementById('area').value,
            bedrooms: document.getElementById('bedrooms').value,
            bathrooms: document.getElementById('bathrooms').value,
            stories: document.getElementById('stories').value,
            mainroad: document.querySelector('input[name="mainroad"]:checked').value,
            guestroom: document.querySelector('input[name="guestroom"]:checked').value,
            basement: document.querySelector('input[name="basement"]:checked').value,
            hotwaterheating: document.querySelector('input[name="hotwaterheating"]:checked').value,
            airconditioning: document.querySelector('input[name="airconditioning"]:checked').value,
            parking: document.getElementById('parking').value,
            prefarea: document.querySelector('input[name="prefarea"]:checked').value,
            furnishingstatus: document.querySelector('input[name="furnishingstatus"]:checked').value
        };
        
        // Output the collected data (you can modify this part based on your needs)
        const output = document.getElementById('output');
        const jsonData = JSON.stringify(formData);
        output.innerHTML = jsonData;
    });
});

