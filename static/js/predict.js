document.getElementById('prediction-form').addEventListener('submit', async function(event) {
    event.preventDefault();

    const formData = new FormData(event.target);
    const formObject = Object.fromEntries(formData.entries());

    // send input features to flask backend
    try {
        const response = await fetch('/predict', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(formObject)
        });

        const modal = document.getElementById('prediction-modal');
        const modalResult = document.getElementById('modal-result');
        const closeModalButton = document.querySelector('.close');

        // helps refresh modal 
        modalResult.innerHTML = '';

        // get predictions and display model output 
        if (response.ok) {
            const result = await response.json();
            modalResult.innerHTML = `
                <h3 class="prediction-heading">Prediction: ${result.prediction} Tumor </h3>
                <p>Benign Classification Probability: <span class="probability">${(result.probabilities.Benign * 100).toFixed(2)}%</span></p>
                <p>Malignant Classification Probability: <span class="probability">${(result.probabilities.Malignant * 100).toFixed(2)}%</span></p>
            `;
        } else {
            const error = await response.json();
            modalResult.innerHTML = `<p>Error: ${error.error}</p>`;
        }

        // modal functions 
        modal.style.display = 'block';

        closeModalButton.onclick = function() {
            modal.style.display = 'none';
        };

        window.onclick = function(event) {
            if (event.target === modal) {
                modal.style.display = 'none';
            }
        };

    } catch (error) {
        console.error("Error:", error);
    }
});
