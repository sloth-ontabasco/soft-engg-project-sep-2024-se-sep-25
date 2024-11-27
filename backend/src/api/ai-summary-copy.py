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
    clean_directory("extracted_files/images")
    clean_directory("extracted_files/text")
    with zipfile.ZipFile(file_path, 'r') as zip_ref:
        zip_ref.extractall("extracted_files")
    files = []
    for root, _, filenames in os.walk("extracted_files"):
        for filename in filenames:
            files.append(os.path.relpath(os.path.join(root, filename), "extracted_files"))
    return files

def convert_images_to_jpg(image, output_path):
    image = image.convert("RGB")
    image.save(output_path, "JPEG")

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
                    content += image_text #image text is added to the content
                    image_output_path = f"extracted_files/images/image_{image_count}.jpg"
                    convert_images_to_jpg(image, image_output_path)
    elif file_path.endswith('.docx'):
        doc = docx.Document(file_path)
        for para in doc.paragraphs:
            content += para.text
        # Extract images and perform OCR
        for rel in doc.part.rels.values():
            if "image" in rel.target_ref:
                image_count += 1
                image = Image.open(io.BytesIO(rel.target_part.blob))
                image_output_path = f"extracted_files/images/image_{image_count}.jpg"
                convert_images_to_jpg(image, image_output_path)
                image_text = pytesseract.image_to_string(image)
                image_texts.append(image_text)
                content += image_text #image text is added to the content
    elif file_path.endswith('.csv'):
        content = pd.read_csv(file_path).to_string()
    elif file_path.endswith('.xlsx'):
        content = pd.read_excel(file_path).to_string()
    # else:
    #     with open(file_path, 'r') as file:
    #         content = file.read()
    
    # Save text content to text folder
    if content:
        text_output_path = f"extracted_files/text/{os.path.basename(file_path)}.txt"
        with open(text_output_path, 'w') as text_file:
            text_file.write(content)

    return content, image_texts

def count_words(text):
    return len(text.split())

def split_text(text, max_length):
    sentences = text.split('. ') #converts the text into sentences
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

def summarize_files(zip_file_path, milestone_title, milestone_description):
    files = extract_zip(zip_file_path)
    summarizer = pipeline("summarization", model="facebook/bart-large-cnn")
    image_captioner = pipeline("image-to-text", model="Salesforce/blip-image-captioning-large") 
    model = SentenceTransformer('paraphrase-MiniLM-L6-v2')  # for similarity checking
    summaries = []
    image_text_combined = ""

    print("Extracted Files : ", files)
    for file_name in files:
        file_path = os.path.join("extracted_files", file_name)
        content = read_file_content(file_path, model) #this reads the content of the file and the classifies into text and images
        
        subFiles = []
        for root, _, filenames in os.walk("extracted_files\\text"):
            for filename in filenames:
                subFiles.append(os.path.relpath(os.path.join(root, filename), "extracted_files\\text"))
        for root, _, filenames in os.walk("extracted_files\\images"):
            for filename in filenames:
                subFiles.append(os.path.relpath(os.path.join(root, filename), "extracted_files\\images"))

        for files in subFiles:
            if files.endswith(('.jpg', '.jpeg', '.png')):
                # Generate summary for images
                image_summary = image_captioner(Image.open(os.getcwd() + "\\extracted_files\\images\\" + files), max_new_tokens=1024)
                print("Image Summary : ", image_summary[0]['generated_text'])
                summaries.append("Image Summary : " + image_summary[0]['generated_text'])
                image_text_combined += str(image_summary[0]['generated_text']) + ". "
            else:
                # Count the number of words in the file content
                total_words = count_words(content[0])
                print("Total number of text file words in the file:", total_words)
                # Determine the chunk size based on the total number of words
                if total_words < 1000:
                    chunk_size = 200
                elif total_words < 5000:
                    chunk_size = 500
                else:
                    chunk_size = 1000
                
                print("Chunk size:", chunk_size)
                # Split content into chunks of the determined size
                chunks = split_text(content[0], max_length=chunk_size)
                
                summary = ""
                for chunk in chunks:
                    summary_chunk = summarizer(chunk, max_length=200, min_length=25, do_sample=False)[0]['summary_text']
                    summary += summary_chunk + " "

                print("Text summary : ", summary.strip())
                summaries.append("Summary of all texts : " + summary.strip())

        #generate a summary for the images text
        print(image_text_combined)
        if image_text_combined:
            summary_2 = summarizer(image_text_combined, max_length=200, min_length=50, do_sample=False)[0]['summary_text']
            print("Image text summary : ", summary_2)
            summaries.append("Summary of Images : " + summary_2)

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

# Example usage
zip_file_path = r"C:\\Users\\Balakumaran S\\Documents\\milestone_2.zip"

milestone_title = "User Interfaces"
milestone_description = "Create a storyboard for the application - it can be a ppt or even a video. Embed the ppt/video in the PDF submission of this week. Take each user story and create low-fidelity wireframes. Apply usability design guidelines and heuristics discussed in lectures to come up with the wireframes.";

start_time = time.time()
summaries, similarity_score, evaluation = summarize_files(zip_file_path, milestone_title, milestone_description)
end_time = time.time()

print("Summaries of Files:", summaries)
print("Similarity Score:", similarity_score)
print(f"Time taken to generate response: {end_time - start_time} seconds")

# Save summaries and similarity score to PDF
output_pdf_path = r"C:\\Users\\Balakumaran S\\Documents\\soft-engg-project-sep-2024-se-sep-25\\summary_report.pdf"
save_summary_to_pdf(summaries, similarity_score, evaluation, output_pdf_path)