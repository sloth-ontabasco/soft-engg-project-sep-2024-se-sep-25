import torch
from PIL import Image
from transformers import MllamaForConditionalGeneration, AutoProcessor
import time

model_id = "meta-llama/Llama-3.2-11B-Vision-Instruct"

model = MllamaForConditionalGeneration.from_pretrained(
    model_id,
    torch_dtype=torch.bfloat16,
    device_map="auto",
)
processor = AutoProcessor.from_pretrained(model_id)

image = Image.open("./extracted_files/images/image_1.jpg");

messages = [
    {"role": "user", "content": [
        {"type": "image"},
        {"type": "text", "text": "Based on the milestone requirements which is to create a storyboard for the application. Take each user story and create low-fidelity wireframes. Apply usability design guidelines and heuristics discussed in lectures to come up with the wireframes. Is the image submission relevant to the milestone requirements?"}
    ]}
]
input_text = processor.apply_chat_template(messages, add_generation_prompt=True)
inputs = processor(
    image,
    input_text,
    add_special_tokens=False,
    return_tensors="pt"
).to(model.device)

start_time = time.time()
output = model.generate(**inputs, max_new_tokens=1024)
end_time = time.time()
print(f"Time taken: {end_time - start_time}")
print(processor.decode(output[0]))
