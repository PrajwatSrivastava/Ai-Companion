// Get the form element by its ID ('text-form')
const form = document.getElementById('text-form');

// Add an event listener for when the form is submitted
form.addEventListener('submit', async (event) => {

  // Prevent the default form submission behavior (which would reload the page)
  event.preventDefault();

  // Get the input elements by their IDs ('textInput' and 'questionInput')
  const textinput = document.getElementById('textInput');
  const quesinput = document.getElementById('questionInput');

  // Log the input elements to the console for debugging purposes
  console.log(textinput)
  console.log(quesinput)

  try {
    // Send a POST request to the server with the input values as JSON
    const response = await fetch('http://localhost:5000/evaluate', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json', // Set content type as JSON
      },
      body: JSON.stringify({ textInput: textinput.value, questionInput: quesinput.value }), // Convert inputs to JSON
    });

    // Check if the response from the server is successful (status code 200-299)
    if (response.ok) {
      // Parse the JSON response to get the 'prediction' value
      const answer = (await response.json()).prediction;

      // Get the div element where the result will be displayed ('prediction-answer')
      const resultDiv = document.getElementById('prediction-answer');
      
      // Log the answer to the console
      console.log(answer);

      // Display the result (answer) inside the div
      resultDiv.innerText = answer;
    } else {
      // If the request failed, log the error with the status code
      console.error('Request failed:', response.status);
    }
  } catch (error) {
    // If an error occurred during the request, log the error
    console.error('Request failed:', error);
  }
});
