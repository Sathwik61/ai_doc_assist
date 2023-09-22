from flask import Flask, render_template, request, jsonify
from werkzeug.utils import secure_filename
from functions import learn_pdf, Answer_from_documents, remove_pdf_from_json
import os
import openai

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads/'
app.config['SECRET_KEY'] = os.getenv("SECRET_KEY", "default_secret_key")
openai.api_key = os.getenv("OPENAI_API_KEY")

# Ensure the uploads folder exists
if not os.path.exists(app.config['UPLOAD_FOLDER']):
    os.makedirs(app.config['UPLOAD_FOLDER'])


@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')


@app.route('/upload', methods=['POST'])
def upload_pdf():
    uploaded_file = request.files.get('pdf_file')
    if uploaded_file and uploaded_file.filename.endswith('.pdf'):
        filename = secure_filename(uploaded_file.filename)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        uploaded_file.save(filepath)
        learn_pdf(filepath)
        os.remove(filepath)
        return jsonify({"success": "PDF uploaded and read successfully!"})
    else:
        return jsonify({"error": "Invalid file type. Please upload a PDF."}), 400


@app.route('/query', methods=['POST'])
def query_bot():
    user_input = request.form.get('query')
    if user_input:
        response = Answer_from_documents(user_input)
        # Return the bot's response as a JSON object
        return jsonify({"response": response})
    else:
        # Return an error message
        return jsonify({"error": "Please enter a valid query."}), 400


@app.route('/remove_pdf', methods=['POST'])
def remove_pdf():
    file_name = request.form.get('name')
    file_size = int(request.form.get('size'))
    removed = remove_pdf_from_json(file_name, file_size)
    if removed:
        return jsonify({"message": "PDF removed successfully!"})
    else:
        return jsonify({"error": "Failed to remove PDF."}), 400


if __name__ == "__main__":
    app.run(debug=True)
