import time
import zipfile
import os
import pandas as pd
import docx
import fitz  # PyMuPDF
from transformers import pipeline
from sentence_transformers import SentenceTransformer, util
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.lib.units import inch
import textwrap
from PIL import Image
import pytesseract
import io
import shutil

# Set the tesseract_cmd to the installed location
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

def generate_evaluation_prompt(milestone_title, milestone_description):
    prompt = f"Milestone: {milestone_title}\nDescription: {milestone_description}\n\n"
    prompt += "\nBased on the milestone and the description, please detail what was completed and what was not completed."
    return prompt

def get_evaluation_from_ai(prompt, context):
    # Use the question-answering pipeline
    ai_model = pipeline("question-answering", model="deepset/roberta-base-squad2")
    qa_input = {
        'question': prompt,
        'context': context
    }
    evaluation = ai_model(qa_input)['answer']
    return evaluation

def clean_directory(directory_path):
    if os.path.exists(directory_path):
        shutil.rmtree(directory_path)
    os.makedirs(directory_path)

def extract_zip(file_path):
    clean_directory("extracted_files")
    with zipfile.ZipFile(file_path, 'r') as zip_ref:
        zip_ref.extractall("extracted_files")
    return os.listdir("extracted_files")

def read_file_content(file_path, model):
    content = ""
    image_texts = []
    image_count = 0
    if file_path.endswith('.pdf'):
        with open(file_path, 'rb') as f:
            doc = fitz.open(f)
            for page in doc:
                content += page.get_text()
                # Extract images and perform OCR
                for img in page.get_images(full=True):
                    image_count += 1
                    xref = img[0]
                    base_image = doc.extract_image(xref)
                    image_bytes = base_image["image"]
                    image = Image.open(io.BytesIO(image_bytes))
                    image_text = pytesseract.image_to_string(image)
                    image_texts.append(image_text)
                    print(f"Image {image_count} text: {image_text}")
    elif file_path.endswith('.docx'):
        doc = docx.Document(file_path)
        for para in doc.paragraphs:
            content += para.text
        # Extract images and perform OCR
        for rel in doc.part.rels.values():
            if "image" in rel.target_ref:
                image_count += 1
                image = Image.open(io.BytesIO(rel.target_part.blob))
                image_text = pytesseract.image_to_string(image)
                image_texts.append(image_text)
                print(f"Image {image_count} text: {image_text}")
    elif file_path.endswith('.csv'):
        content = pd.read_csv(file_path).to_string()
    elif file_path.endswith('.xlsx'):
        content = pd.read_excel(file_path).to_string()
    # Add more format handlers as necessary
    print(f"Total number of images detected: {image_count}")

    # Group similar image texts into paragraphs
    grouped_texts = []
    current_paragraph = ""
    for i, text in enumerate(image_texts):
        if i == 0:
            current_paragraph = text
        else:
            similarity = calculate_similarity(current_paragraph, text, model)
            if similarity > 0.7:  # Adjust the threshold as needed
                current_paragraph += " " + text
            else:
                grouped_texts.append(current_paragraph)
                current_paragraph = text
    if current_paragraph:
        grouped_texts.append(current_paragraph)

    # Append grouped image texts to content
    for paragraph in grouped_texts:
        content += "\n\n" + paragraph

    return content

def calculate_similarity(text1, text2, model):
    embedding1 = model.encode(text1, convert_to_tensor=True)
    embedding2 = model.encode(text2, convert_to_tensor=True)
    similarity = util.pytorch_cos_sim(embedding1, embedding2).item()
    return similarity

def split_text(text, max_length):
    sentences = text.split('. ')
    chunks = []
    current_chunk = []
    current_length = 0

    for sentence in sentences:
        sentence_length = len(sentence.split())
        if current_length + sentence_length > max_length:
            chunks.append('. '.join(current_chunk) + '.')
            current_chunk = [sentence]
            current_length = sentence_length
        else:
            current_chunk.append(sentence)
            current_length += sentence_length

    if current_chunk:
        chunks.append('. '.join(current_chunk) + '.')

    return chunks

def count_words(text):
    return len(text.split())

# def summarize_files(zip_file_path, milestone_title, milestone_description):
#     files = extract_zip(zip_file_path)
#     summarizer = pipeline("summarization", model="facebook/bart-large-cnn")
#     model = SentenceTransformer('paraphrase-MiniLM-L6-v2')  # for similarity checking

#     summaries = []
#     for file_name in files:
#         file_path = os.path.join("extracted_files", file_name)
#         content = read_file_content(file_path, model)
        
#         # Count the number of words in the file content
#         total_words = count_words(content)
#         print("Total number of words in the file:", total_words)

#         # Determine the chunk size based on the total number of words
#         if total_words < 1000:
#             chunk_size = 200
#         elif total_words < 5000:
#             chunk_size = 500
#         else:
#             chunk_size = 1000
        
#         print("Chunk size:", chunk_size)
#         # Split content into chunks of the determined size
#         chunks = split_text(content, max_length=chunk_size)
        
#         summary = ""
#         for chunk in chunks:
#             summary_chunk = summarizer(chunk, max_length=100, min_length=25, do_sample=False)[0]['summary_text']
#             summary += summary_chunk + " "
#         summaries.append(summary.strip())

#     # Validate closeness of summaries to milestone
#     combined_summary = " ".join(summaries)
#     milestone_text = milestone_title + " " + milestone_description
#     milestone_embedding = model.encode(milestone_text, convert_to_tensor=True)
#     summary_embedding = model.encode(combined_summary, convert_to_tensor=True)
#     similarity = util.pytorch_cos_sim(milestone_embedding, summary_embedding).item()

#     return summaries, similarity

def summarize_files(zip_file_path, milestone_title, milestone_description):
    files = extract_zip(zip_file_path)
    summarizer = pipeline("summarization", model="facebook/bart-large-cnn")
    model = SentenceTransformer('paraphrase-MiniLM-L6-v2')  # for similarity checking
    summaries = []
    for file_name in files:
        file_path = os.path.join("extracted_files", file_name)
        content = read_file_content(file_path, model)
        
        # Count the number of words in the file content
        total_words = count_words(content)
        print("Total number of words in the file:", total_words)
        # Determine the chunk size based on the total number of words
        if total_words < 1000:
            chunk_size = 200
        elif total_words < 5000:
            chunk_size = 500
        else:
            chunk_size = 1000
        
        print("Chunk size:", chunk_size)
        # Split content into chunks of the determined size
        chunks = split_text(content, max_length=chunk_size)
        
        summary = ""
        for chunk in chunks:
            summary_chunk = summarizer(chunk, max_length=200, min_length=100, do_sample=False)[0]['summary_text']
            summary += summary_chunk + " "
        summaries.append(summary.strip())

    # Validate closeness of summaries to milestone
    combined_summary = " ".join(summaries)
    milestone_text = milestone_title + " " + milestone_description
    milestone_embedding = model.encode(milestone_text, convert_to_tensor=True)
    summary_embedding = model.encode(combined_summary, convert_to_tensor=True)
    similarity = util.pytorch_cos_sim(milestone_embedding, summary_embedding).item()

    # Generate evaluation prompt
    evaluation_prompt = generate_evaluation_prompt(milestone_title, milestone_description)
    evaluation = get_evaluation_from_ai(evaluation_prompt, combined_summary)

    return summaries, similarity, evaluation

# def save_summary_to_pdf(summaries, similarity_score, output_path):
#     c = canvas.Canvas(output_path, pagesize=letter)
#     width, height = letter

#     c.setFont("Helvetica", 12)
#     c.drawString(100, height - 40, "Summaries of Files")

#     y_position = height - 60
#     max_width = width - 80  # Adjust the width to fit within the page margins

#     for i, summary in enumerate(summaries, 1):
#         wrapped_text = textwrap.wrap(f"Summary {i}: {summary}", width=100)  # Adjust width as needed
#         text = c.beginText(40, y_position)
#         text.setFont("Helvetica", 10)
#         for line in wrapped_text:
#             text.textLine(line)
#             y_position -= 12  # Adjust line height as needed
#             if y_position < 40:
#                 c.drawText(text)
#                 c.showPage()
#                 c.setFont("Helvetica", 12)
#                 y_position = height - 40
#                 text = c.beginText(40, y_position)
#                 text.setFont("Helvetica", 10)
#         c.drawText(text)
#         y_position -= 20

#     c.drawString(100, y_position - 20, f"Similarity Score: {similarity_score}")
#     c.save()

def save_summary_to_pdf(summaries, similarity_score, evaluation, output_path):
    c = canvas.Canvas(output_path, pagesize=letter)
    width, height = letter
    c.setFont("Helvetica", 12)
    c.drawString(100, height - 40, "Summaries of Files")
    y_position = height - 60
    max_width = width - 80  # Adjust the width to fit within the page margins
    for i, summary in enumerate(summaries, 1):
        wrapped_text = textwrap.wrap(f"Summary {i}: {summary}", width=100)  # Adjust width as needed
        text = c.beginText(40, y_position)
        text.setFont("Helvetica", 10)
        for line in wrapped_text:
            text.textLine(line)
            y_position -= 12  # Adjust line height as needed
            if y_position < 40:
                c.drawText(text)
                c.showPage()
                c.setFont("Helvetica", 12)
                y_position = height - 40
                text = c.beginText(40, y_position)
                text.setFont("Helvetica", 10)
        c.drawText(text)
        y_position -= 20
    c.drawString(100, y_position - 20, f"Similarity Score: {similarity_score}")
    y_position -= 40
    c.drawString(100, y_position, "Evaluation:")
    y_position -= 20
    wrapped_evaluation = textwrap.wrap(evaluation, width=100)
    text = c.beginText(40, y_position)
    text.setFont("Helvetica", 10)
    for line in wrapped_evaluation:
        text.textLine(line)
        y_position -= 12
        if y_position < 40:
            c.drawText(text)
            c.showPage()
            c.setFont("Helvetica", 12)
            y_position = height - 40
            text = c.beginText(40, y_position)
            text.setFont("Helvetica", 10)
    c.drawText(text)
    c.save()

# zip_file_path = r"C:\\Users\\Balakumaran S\\Documents\\milestone_1.zip"

# milestone_title = "Identify User Requirements"
# milestone_description = "Identify users of the application - primary, secondary and tertiary users. Write user stories for the requirements, based on the SMART guidelines discussed in the lectures.";

# zip_file_path = r"C:\\Users\\Balakumaran S\\Documents\\milestone_2.zip"

# milestone_title = "User Interfaces"
# milestone_description = "Create a storyboard for the application - it can be a ppt or even a video. Embed the ppt/video in the PDF submission of this week. Take each user story and create low-fidelity wireframes. Apply usability design guidelines and heuristics discussed in lectures to come up with the wireframes.";

zip_file_path = r"C:\\Users\\Balakumaran S\\Documents\\milestone_2.zip"

milestone_title = "Scheduling and Design"
milestone_description = "Project Schedule - come up with a schedule of your overall project based on the user stories created in the previous milestones. Create a schedule for your sprints and iterations, timings of your scrum meetings etc. Trello board, Gantt chart - specifying your tasks and contributions. Project Scheduling Tools - which tools are you using? E.g. Pivotal Tracker, Jira. Design of Components - Describe different components of your system based on the user stories created in the previous milestones. Software Design - Basic class diagrams of your proposed system. Details/Minutes of a few scrum meetings. Most of the pages in the UI (It may be modified (up to a certain limit) at a later time if necessary) - E.g.: HTML/CSS/Javascript (if you are using a framework like Vue.js or React.js, pages should be connected and redirection also implemented, have to submit the frontend folder without integration with backend API’s. Additionally provide a Readme file to run the frontend code)."

start_time = time.time()
summaries, similarity_score, evaluation = summarize_files(zip_file_path, milestone_title, milestone_description)
end_time = time.time()

print("Summaries of Files:", summaries)
print("Similarity Score:", similarity_score)
print(f"Time taken to generate response: {end_time - start_time} seconds")

# Save summaries and similarity score to PDF
output_pdf_path = r"C:\\Users\\Balakumaran S\\Documents\\soft-engg-project-sep-2024-se-sep-25\\summary_report.pdf"
save_summary_to_pdf(summaries, similarity_score, evaluation, output_pdf_path)