# import os
# import sys
# from PyPDF2 import PdfReader
# from sentence_transformers import SentenceTransformer, util
# import numpy as np

# # Load the pre-trained SBERT model
# model = SentenceTransformer('stsb-roberta-large')

# # Actual Evaluation using Transformers
# def score(sentence1, sentence2):
#     embedding1 = model.encode(sentence1, convert_to_tensor=True)
#     embedding2 = model.encode(sentence2, convert_to_tensor=True)
#     # compute similarity scores of two embeddings
#     cosine_scores = util.pytorch_cos_sim(embedding1, embedding2)
#     sc = cosine_scores.item()
#     if sc < 0.4:
#         return 0
#     elif sc > 0.4 and sc < 0.65:
#         return 0.5
#     else:
#         return 1

# # Function to extract text from PDF file
# def extract_text_from_pdf(file_path):
#     with open(file_path, 'rb') as file:
#         reader = PdfReader(file)
#         text = ""
#         for page in reader.pages:
#             text += page.extract_text()
#     return text

# # Function to process student and model answers
# def process_answers(model_answers_file_path, student_answers_file_path):
#     # Extract text from PDF files
#     model_answers_text = extract_text_from_pdf(model_answers_file_path)
#     student_answers_text = extract_text_from_pdf(student_answers_file_path)

#     # Process each question and calculate score
#     que_mark = [2,2,2,2,2,2,2,2,2]
#     total = 18
#     i = 1
#     sum = 0
#     while True:
#         # Find the start indices of the current question
#         mystr = f"\nAns{i}"
#         if mystr in student_answers_text:
#             start = student_answers_text.index(mystr)
#             student_text = student_answers_text[start+len(mystr):].strip().split("\n")

#             # Find the end index of the current question
#             if i < len(que_mark):
#                 end = student_answers_text.index(f"\nAns{i+1}")
#             else:
#                 end = len(student_answers_text)

#             student_text = student_answers_text[start+len(mystr):end]

#             # Find the corresponding model answer
#             model_start = model_answers_text.index(f"Question {i}:") + len("Question {i}:")
#             if i < len(que_mark):
#                 model_end = model_answers_text.index(f"Question {i+1}:", model_start)
#             else:
#                 model_end = len(model_answers_text)

#             model_text = model_answers_text[model_start:model_end].strip()

#             # Extract sentences from student and model answers
#             student_sentences = [util.split_sentences(text)[0] for text in student_text]
#             model_sentences = util.split_sentences(model_text)

#             # Calculate score
#             sentence1, sentence2 = student_sentences[0], model_sentences[0]
#             sc = score(sentence1, sentence2)
#             mark = que_mark[i-1] * sc
#             sum += mark

#             print("Question {}: ".format(i))
#             print("Student answer: {}".format(student_text))
#             print("Model answer: {}".format(model_text))
#             print("Score: {}".format(mark))

#             i += 1

#     print("Total score: {}/{}".format(sum, total))

# # Get file paths from arguments
# process_answers(sys.argv[1], sys.argv[2])