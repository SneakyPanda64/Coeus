import json

import marko
import os
from bs4 import BeautifulSoup

import regex as re

import gpt

def ReadDocument(id):
    path = os.path.join("output", id + ".md")
    with open(path, "r") as f:
        markdown_text = f.read()
        soup = BeautifulSoup(marko.convert(markdown_text), 'html.parser')
        headers = [header.text.strip() for header in soup.find_all('h2')]
    return headers, markdown_text
def GetContext(id, index):
    headers, markdown_text = ReadDocument(id)
    if index + 1 < len(headers):
        body_text = re.findall(f"(?s)(?<=## {headers[index]}).*?(?=## {headers[index + 1]})", markdown_text)[0].strip()
    else:
        body_text = markdown_text.split(f"## {headers[index]}")[-1]
    return headers[index], body_text.strip()
def GenerateQuestion(id, index):
    header, body = GetContext(id, index)
    full_text = (header + "\n\n" + body).strip()
    questions = gpt.ChatCompletion([
        {"role": "system", "content": "You are an AI used for teaching business to A level students."},
        {"role": "user",
         f"content": f"Write a list of questions worth 2-4 marks using information from the following passage. Difficulty is in a range between 1 and 10, 10 being the hardest:\n\nformat: [{{\"question\": \"\", \"difficulty\": 0}}]\n\npassage:\n\n{full_text}"},
    ], 250, 0.7)
    return json.loads(questions)
def CheckQuestion(id, index, question, answer):
    header, body = GetContext(id, index)
    context = (header + "\n\n" + body).strip()
    answer = gpt.ChatCompletion([
        {"role": "system", "content": "You are an AI used for teaching business to students"},
        {"role": "user", "content": f"Judge the correctness on the following answer using the question and context provided also provide the model answer if the correctness is below 0.9 and respond using the format specified.\n\nQuestion: {question}\n\nAnswer: {answer}.\n\nformat: {{\"correctness\": 0.00, \"comments\": [], \"model_answer\": \"\"}}\n\nContext:\n\n{context}"}
    ], 256, 0)
    return json.loads(answer)
