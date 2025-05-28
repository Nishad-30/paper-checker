from sentence_transformers import SentenceTransformer
from scipy.spatial.distance import cosine
import PyPDF2
import sys
from PyPDF2 import PdfReader
# Load the pre-trained SBERT model
from sentence_transformers import SentenceTransformer, util
import numpy as np




# Actual Evaluation using Transformers
def score(sentence1,sentence2):
    model = SentenceTransformer('stsb-roberta-large')
    embedding1 = model.encode(sentence1, convert_to_tensor=True)
    embedding2 = model.encode(sentence2, convert_to_tensor=True)
    # compute similarity scores of two embeddings
    cosine_scores = util.pytorch_cos_sim(embedding1, embedding2)
    sc = cosine_scores.item()
    if sc < 0.4:
        return 0
    elif sc > 0.4 and sc < 0.65:
        return 0.5
    else:
        return 1

# Function to extract text from PDF file
def extract_text_from_pdf(file_path):
    with open(file_path, 'rb') as file:
        reader = PyPDF2.PdfReader(file)
        text = ""
        for page in reader.pages:
            text += page.extract_text()
    return text

def listToString(s):
    str1 = ""
    for ele in s:
        str1 += ele+" "
    return str1