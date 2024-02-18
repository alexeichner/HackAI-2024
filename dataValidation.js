// document.addEventListener('DOMContentLoaded', function() {
//     const form = document.getElementById('form');
//     // const submitButton = document.getElementById('submitButton');

//     form.addEventListener('submit', preventRefresh) {
//         //event.preventDefault(); // Prevent the default form submission
        
//         const areaInput = document.getElementById('area');
//         const areaValue = parseInt(areaInput.value);
        
//         // Check if the area value is a valid integer
//         if (isNaN(areaValue)) {
//             alert('Please enter a valid integer for the area.');
//             areaInput.focus();
//             return; // Stop further execution
//         }
//     });
// });

document.querySelector('form').addEventListener('submit', preventRefresh);

function preventRefresh(event) {
    event.preventDefault();
    getPredictedPrice(); 

}

async function getPredictedPrice() {

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
//output.innerHTML = jsonData;

// Send data to the server
try {
    const response = await fetch('http://localhost:3000/submitData', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify(formData),
    });
    
    const result = await response.json();

    

    // Fetch predicted price from a new endpoint
    const predictedPriceResponse = await fetch('http://localhost:3000/getPredictedPrice');
    const predictedPriceResult = await predictedPriceResponse.json();
    console.log("front end pp: ", predictedPriceResult.predicted_price);

    // Update output.innerHTML with the predicted price
    alert(`Predicted Price: $${predictedPriceResult.predicted_price}`)
    } catch (error) {
        console.error('Error sending data to the server:', error.message);
    }
}
