# PDF Answer AI

This project allows users to upload PDF files, extract their content, and store the information in a JSON file. Users can then query the stored information using ChatGPT.

## Features

- Upload PDF files and extract their content.
- Store extracted content in a JSON file.
- Query the stored information using ChatGPT.
- Remove uploaded PDF information based on file name and size.

## Installation

1. Clone the repository:

```
git clone https://github.com/Anuswar/Pdf-Answer-AI.git
```

2. Navigate to the project directory:

```
cd Pdf-Answer-AI
```

3. Install the required packages:

```
pip install -r requirements.txt
```

## Usage

1. Start the Flask application:

```
python app.py
```

2. Open a web browser and navigate to `http://127.0.0.1:5000/`.

3. Use the web interface to upload PDF files and query the stored information.

## Dependencies

- Flask: Web framework used to build the application.
- Werkzeug: Used for the `secure_filename` function.
- PyPDF2: Library to read PDF files.
- OpenAI: Library to interact with the OpenAI API.
- Scikit-learn: Used for the `TfidfVectorizer` and `linear_kernel` functions.

## Contributing

Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.