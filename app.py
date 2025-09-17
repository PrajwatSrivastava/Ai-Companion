# Import necessary libraries
import pandas as pd  # Used for data handling, though not used here
import torch  # Used for tensor operations, required for working with models
import pickle  # For serializing objects, though not used here
from flask import Flask, render_template, request, jsonify  # Flask for web app and HTTP handling
from transformers import AutoModelForQuestionAnswering, AutoTokenizer  # For pre-trained models and tokenizers
from flask_cors import CORS  # To handle Cross-Origin Resource Sharing (CORS) for web requests

# Initialize Flask app
app = Flask(__name__)

# Enable CORS to allow the app to make cross-origin requests
CORS(app)

# Define the route for the home page, renders the HTML template
@app.route('/', methods=["GET", "POST"])
def home():
    return render_template('index.html')  # Return the index.html template when accessed

# Define the route for handling the question-answering request
@app.route('/evaluate', methods=['POST', 'GET'])
def evaluate():

    # Use when showing front end
    text_input = request.form.get('textInput')
    question_input = request.form.get('questionInput')

    # Use when using chrome extension
    # Receive JSON data from the POST request
    # data = request.get_json()
    # text_input = data.get('textInput')
    # question_input = data.get('questionInput')

    # Print inputs for debugging purposes
    print(text_input)
    print(question_input)

    # If either text or question input is not provided, return an error message
    if text_input and question_input is None:
        return jsonify({'answer': 'Input text not provided.'})

    # Prepare the input for the model: question and context (text)
    QA_input = [{'question': f'{question_input}',
                 'context': f'{text_input}'}]

    # Specify the pre-trained model name
    model_name = 'deepset/roberta-base-squad2'

    # Load the pre-trained model and tokenizer for question answering
    model = AutoModelForQuestionAnswering.from_pretrained(model_name)
    tokenizer = AutoTokenizer.from_pretrained(model_name)

    # Tokenize the question and context (text) for the model
    inputs0 = tokenizer(QA_input[0]['question'], QA_input[0]['context'], return_tensors="pt")

    # Get the model output (start and end logits for the answer)
    output0 = model(**inputs0)

    # Find the start and end positions of the answer in the tokenized input
    answer_start_idx = torch.argmax(output0.start_logits)
    answer_end_idx = torch.argmax(output0.end_logits)

    # Extract the tokens corresponding to the answer
    answer_tokens = inputs0.input_ids[0, answer_start_idx:answer_end_idx+1]

    # Decode the tokens back to a human-readable answer
    answer = tokenizer.decode(answer_tokens)

    # Print the answer for debugging purposes
    print(answer)

    # Return the predicted answer as a JSON response
    return jsonify({'prediction': answer}) # when using chrome ext

    return jsonify({'answer': answer}) # when using template index.html for front-end porpuse

# Start the Flask app when the script is run
if __name__ == '__main__':
    app.run(debug=True)
