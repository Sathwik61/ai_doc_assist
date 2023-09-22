import os
import uuid
import json
import PyPDF2
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import linear_kernel
import openai


def learn_pdf(file_path):
    content_chunks = []
    # Extract file name and size
    file_name = os.path.basename(file_path)
    file_size = os.path.getsize(file_path)

    with open(file_path, 'rb') as pdf_file:
        pdf_reader = PyPDF2.PdfReader(pdf_file)
        for page in pdf_reader.pages:
            content = page.extract_text()
            obj = {
                "id": str(uuid.uuid4()),
                "text": content,
                "name": file_name,  # Add file name
                "size": file_size   # Add file size
            }
            content_chunks.append(obj)

    json_file_path = 'my_knowledgebase.json'
    with open(json_file_path, 'r', encoding='utf-8') as f:
        data = json.load(f)

    # Remove existing entries with the same text, name, and size
    data = [entry for entry in data if not (
        entry['text'] == content and entry['name'] == file_name and entry['size'] == file_size)]

    data.extend(content_chunks)
    with open(json_file_path, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)


def Answer_from_documents(user_query):
    with open('my_knowledgebase.json', 'r', encoding="utf-8") as jsonfile:
        data = json.load(jsonfile)
        documents = [item['text'] for item in data]
        documents.append(user_query)

        tfidf = TfidfVectorizer().fit_transform(documents)
        cosine_similarities = linear_kernel(tfidf[-1], tfidf).flatten()
        related_docs_indices = cosine_similarities.argsort()[:-3:-1]

        context = ''.join([documents[index] for index in related_docs_indices])

        myMessages = [
            {"role": "system", "content": "You're a helpful Assistant."},
            {"role": "user", "content": f"The following is a Context:\n{context}\n\n Answer the following user query according to the above given context.\n\nquery: {user_query}"}
        ]
        response = openai.ChatCompletion.create(
            model='gpt-3.5-turbo',
            messages=myMessages,
            max_tokens=200,
        )

    return response['choices'][0]['message']['content']


def remove_pdf_from_json(file_name, file_size):
    json_file_path = 'my_knowledgebase.json'
    with open(json_file_path, 'r', encoding='utf-8') as f:
        data = json.load(f)

    # Filter out the entry with the given name and size
    new_data = [entry for entry in data if not (
        entry['name'] == file_name and entry['size'] == file_size)]

    if len(new_data) == len(data):
        return False  # No entry was removed

    with open(json_file_path, 'w', encoding='utf-8') as f:
        json.dump(new_data, f, ensure_ascii=False, indent=4)

    return True
