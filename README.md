# Flask PDF Chatbot

This repository contains a Flask app chatbot with PDF upload functionality. The chatbot allows users to interact with it and also provides the ability to upload PDF files. The uploaded PDFs can be processed or used for further analysis within the chatbot application.


## Features

- Interactive chatbot interface
- PDF upload functionality
- Processing and analysis of uploaded PDF files
- User-friendly interface with frontend included
- Powered by Flask web framework


## Usage

1. Clone this repository to your local machine or just copy the codes of 'flask_app.py' file
2. Enter your OpenAI API key in the code 'config.py' (where it says "YOUR_API_KEY")
3. Create a folder named 'template' in your project directory and copy 'index.html' inside this folder
4. Create a folder named 'uploads' and leave it empty (your uploaded PDF docments will store here for processing)
5. Install required libraries for the app (check 'requirements.txt' file)
6. Finally run the app
7. After running, go to your browser and type "localhost:port", for example "127.0.0.1:5000"
8. Upload any file, clicl on submit button and start asking questions about your document
