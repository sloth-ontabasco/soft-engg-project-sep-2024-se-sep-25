import time
import zipfile
import os
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
import textwrap
import shutil
import google.generativeai as genai
import os

# genai.configure(api_key=os.environ["API_KEY"])
genai.configure(api_key="AIzaSyD2SrL0lIQjWz9s_-k-CDYAJEl5C4SXbCo")

def generate_evaluation_prompt(milestone_title, milestone_description):
    prompt = f"Milestone Title: {milestone_title}\nMilestone Description: {milestone_description}\n\n"
    prompt += "\nBased on the milestone title and description. Given the context below, provide an overall summary of the submission and detail what was completed and what was not completed. Be lenient in your evaluation and provide constructive feedback.\n\n Also, group the images based on the context and describe what those sequence of images are about in brief (if any, by giving an appropriate heading).\n\n If the evaluation rubrix is provided, provide your scores based on the submission made by the candidate for each criteria. Else, mention evaluation cannot be done becacuse of no rubric available.\n\n"
    return prompt

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

def draw_bullets(c, text, x, y, max_width):
    """Draw bullet points on the PDF canvas."""
    wrapped_text = textwrap.wrap(text, width=100)
    for line in wrapped_text:
        c.drawString(x, y, f"• {line}")
        y -= 12
        if y < 40:
            c.showPage()
            c.setFont("Helvetica", 12)
            y = letter[1] - 40
    return y

def draw_bold_text(c, text, x, y, max_width):
    """Draw bold text on the PDF canvas."""
    wrapped_text = textwrap.wrap(text, width=100)
    for line in wrapped_text:
        c.setFont("Helvetica-Bold", 12)
        c.drawString(x, y, line)
        c.setFont("Helvetica", 12)
        y -= 12
        if y < 40:
            c.showPage()
            c.setFont("Helvetica", 12)
            y = letter[1] - 40
    return y

def save_summary_to_pdf(summaries, output_path):
    """Save the summaries to a PDF file."""
    c = canvas.Canvas(output_path, pagesize=letter)
    width, height = letter
    c.setFont("Helvetica", 12)
    c.drawString(100, height - 40, "Summaries of Files")
    y_position = height - 60
    max_width = width - 80  # Adjust the width to fit within the page margins

    lines = summaries.split('\n')
    for line in lines:
        if line.startswith('* '):
            y_position = draw_bullets(c, line[2:], 40, y_position, max_width)
        elif line.startswith('**') and line.endswith('**'):
            y_position = draw_bold_text(c, line[2:-2], 40, y_position, max_width)
        else:
            wrapped_text = textwrap.wrap(line, width=100)
            for wrapped_line in wrapped_text:
                c.drawString(40, y_position, wrapped_line)
                y_position -= 12
                if y_position < 40:
                    c.showPage()
                    c.setFont("Helvetica", 12)
                    y_position = height - 40
        y_position -= 20

    c.save()

def generate_content(prompt, context):
    content = prompt + "\n " + context
    model = genai.GenerativeModel("gemini-1.5-flash")
    response = model.generate_content(content)
    return response.text

def upload_file_to_gemini(image_path, context):
    image = genai.upload_file(image_path)
    context.append(image)
    print("Image Uploaded : ", image.name)
            
def summarize_files(zip_file_path, rubrix_file_path, milestone_title, milestone_description):
    prompt = generate_evaluation_prompt(milestone_title, milestone_description);
    files = extract_zip(zip_file_path)
    context = [prompt];
    
    if(rubrix_file_path):
        file_path = os.path.join("submissions", rubrix_file_path)
        upload_file_to_gemini(file_path, context)
    
    for file_name in files:
        file_path = os.path.join("extracted_files", file_name)
        sample_pdf = genai.upload_file(file_path)
        context.append(sample_pdf)
        model = genai.GenerativeModel(model_name="gemini-1.5-flash")
        response = model.generate_content(context)

    return response.text

# Example usage
zip_file_path = os.path.join(os.getcwd(), "backend\\src\\api\\submissions", "milestone_1.zip")
# rubrix_file_path = ""; # No rubrix file provided
rubrix_file_path = os.path.join(os.getcwd(), "backend\\src\\api\\submissions", "milestone_1_rubrix.png")

milestone_title = "Identify User Requirements"
milestone_description = "Identify users of the application - primary, secondary and tertiary users. Write user stories for the requirements, based on the SMART guidelines discussed in the lectures.";

# milestone_title = "User Interfaces"
# milestone_description = "Create storyboards and low-fidelity wireframes.";

# milestone_title = "Scheduling and Design"
# milestone_description = "Project Schedule - come up with a schedule of your overall project based on the user stories created in the previous milestones. Create a schedule for your sprints and iterations, timings of your scrum meetings etc. Trello board, Gantt chart - specifying your tasks and contributions. Project Scheduling Tools - which tools are you using? E.g. Pivotal Tracker, Jira. Design of Components - Describe different components of your system based on the user stories created in the previous milestones. Software Design - Basic class diagrams of your proposed system. Details/Minutes of a few scrum meetings. Most of the pages in the UI."


start_time = time.time()
generative_summary = summarize_files(zip_file_path, rubrix_file_path, milestone_title, milestone_description)
end_time = time.time()

print(f"Time taken to generate response: {end_time - start_time} seconds")

# Save summaries and similarity score to PDF
output_pdf_path = os.path.join(os.getcwd(), "backend\\src\\api\\reports", "summary_report.pdf")
save_summary_to_pdf(generative_summary, output_pdf_path)