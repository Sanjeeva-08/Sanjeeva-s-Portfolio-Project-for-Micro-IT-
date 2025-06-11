// Get references to HTML elements
const internshipForm = document.getElementById('internshipForm');
const submitButton = document.getElementById('submitButton');
const buttonText = document.getElementById('buttonText');
const loadingSpinner = document.getElementById('loadingSpinner');
const formMessage = document.getElementById('formMessage');

// Add an event listener for the form submission
internshipForm.addEventListener('submit', async (event) => {
    event.preventDefault(); // Prevent the default form submission (which reloads the page)

    // Clear any previously displayed messages (success or error)
    formMessage.classList.add('hidden');
    formMessage.classList.remove('success', 'error');
    formMessage.textContent = '';

    // Show the loading state: disable button, change text, and show spinner
    submitButton.disabled = true;
    buttonText.textContent = 'Submitting...';
    loadingSpinner.classList.remove('hidden');

    // Gather the form data from the input fields, including new 'phone' and 'year'
    const formData = {
        fullName: document.getElementById('fullName').value,
        email: document.getElementById('email').value,
        phone: document.getElementById('phone').value, // Added phone number
        university: document.getElementById('university').value,
        program: document.getElementById('program').value,
        year: document.getElementById('year').value, // Added year from dropdown
        // Split skills by comma, trim whitespace, and filter out empty strings
        skills: document.getElementById('skills').value.split(',').map(s => s.trim()).filter(s => s.length > 0)
    };

    try {
       
        await new Promise(resolve => setTimeout(resolve, 2000));

        // Simulate a random success or failure (70% chance of success)
        const isSuccess = Math.random() > 0.3;

        if (isSuccess) {
            // Display success message
            formMessage.classList.remove('hidden');
            formMessage.classList.add('success');
            formMessage.textContent = 'Application submitted successfully! We will be in touch shortly.';
            internshipForm.reset(); // Clear all form fields after successful submission
        } else {
            // Throw an error to trigger the catch block for simulated failure
            throw new Error('Failed to submit application. Please check your inputs and try again.');
        }

    } catch (error) {
        // Handle any errors that occur during the API call or simulation
        formMessage.classList.remove('hidden');
        formMessage.classList.add('error');
        formMessage.textContent = `Error: ${error.message}`;
        console.error('Submission error:', error); // Log the error to the console for debugging
    } finally {
        // This block runs regardless of success or failure
        // Reset the button state: re-enable, change text back, and hide spinner
        submitButton.disabled = false;
        buttonText.textContent = 'Submit Application';
        loadingSpinner.classList.add('hidden');
    }
});
