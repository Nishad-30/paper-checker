from django.shortcuts import render, redirect

# Create your views here.

from Dashboard.models import *
from .forms import PdfForm
# import io
from sentence_transformers import SentenceTransformer
from scipy.spatial.distance import cosine
import PyPDF2
import sys
from PyPDF2 import PdfReader
# Load the pre-trained SBERT model
from sentence_transformers import SentenceTransformer, util
import numpy as np

code = ""
roll = ""

def score(sentence1,sentence2):
    model = SentenceTransformer('stsb-roberta-large')
    embedding1 = model.encode(sentence1, convert_to_tensor=True)
    embedding2 = model.encode(sentence2, convert_to_tensor=True)
    # compute similarity scores of two embeddings
    cosine_scores = util.pytorch_cos_sim(embedding1, embedding2)
    sc = cosine_scores.item()
    # return float(sc)
    if sc < 0.1:
        return 0
    elif sc > 0.1 and sc < 0.2:
        return 0.1
    elif sc > 0.2 and sc < 0.3:
        return 0.2
    elif sc > 0.3 and sc < 0.4:
        return 0.3
    elif sc > 0.4 and sc < 0.5:
        return 0.4
    elif sc > 0.5 and sc < 0.6:
        return 0.5
    elif sc > 0.6 and sc < 0.7:
        return 0.6
    elif sc > 0.7 and sc < 0.8:
        return 0.7
    elif sc > 0.8 and sc < 0.9:
        return 0.8
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
# import io

def student_dashboard(request):
    a= "0"
    student_RN = request.POST.get('student_roll_number')
    student_name = request.POST.get('student_name')
    context = {'student_RN': student_RN, 'student_name': student_name, 'a': a }
    # student_login = display_table("student_login")
    # if request.method == 'POST':
    #     for i in student_login:
    #         if i[0]==student_RN:
    #             if i[1]==student_name:
    #                 return render(request, 'student_dashboard.html', context)
    #             else:
    #                 context['message'] = "wrong name"
    #                 return redirect('error')
    #         else:
    #             context['message'] = "wrong Roll no"
    #             return redirect('error')
            
    pass
    return render(request, 'student_dashboard.html', context)



def upload_student_answers(request):
    global code
    global roll
    student_SC = str(request.POST.get('subject_code'))
    student_RN = str(request.POST.get('roll_number'))
    student_name = str(request.POST.get('student_name'))
    code = student_SC
    roll = student_RN
    context = {'student_RN': student_RN, 'student_name': student_name , 'Student_code':student_SC}
    data = display_table("Teacher_paper")
    if request.method == 'POST':
        form = PdfForm(request.POST, request.FILES)
        if form.is_valid():
            pdf_file = request.FILES['pdf_file']
            pdf_reader = PyPDF2.PdfReader(pdf_file)
            text = ""
            for page in range(len(pdf_reader.pages)):
                text += pdf_reader.pages[page].extract_text()
            val = (student_SC, text, student_RN ,student_name)
            sql = "%s,%s,%s,%s"
            inserting("student_sheet", sql, val)
            context["message"]= "Answer Sheet Uploaded"
            return render(request, 'upload.html', context)
    else:
        form = PdfForm()
    return render(request, 'upload.html', {'form': form})



def Checking(code):
    answer_paper = selection_search("teacher_paper","Subject_code",code)
    answer_sheet = selection_searchs("student_sheet","Subject_code",code, "roll_no", roll)
    data1 = answer_paper[0][1]
    data2 = answer_sheet[0][1]
    marks = selection_search("paper","Subject_code",code)
    que_mark = int(marks[0][2])
    que= int(marks[0][1])
    textls1 = []
    textls2 = []
    textls1 = data1.split(" ")
    textls2 = data2.split(" ")
    sum = 0
    result = {}
    for i in range(1,que+1):
        record = []
        sent1 = []
        sent2 = []
        if i ==1:
            mystr = "Ans1"
        else:
            mystr = "\n"+"Ans"+str(i)
        if mystr in textls1:
            mystr2 = "\n"+"Ans"+str(i+1)
            ind = textls1.index(mystr)
            for j in range(ind+1,len(textls1)):
                if textls1[j]!=mystr2:
                    sent1.append(textls1[j])
                else:
                    break
        sentence1 = listToString(sent1)
        # print("Student answer"+str(i)+"---> "+sentence1)
        if mystr in textls2:
            mystr2 = "\n"+"Ans"+str(i+1)
            ind = textls2.index(mystr)
            for j in range(ind+1,len(textls2)):
                if textls2[j]!=mystr2:
                    sent2.append(textls2[j])
                else:
                    break
        sentence2 = listToString(sent2)
        # print("Actual Answer"+str(i)+"---> " +sentence2)
        # print("------------------------------------------------------")
        
        
        mrk = que_mark*score(sentence1,sentence2)
        
        # print("||Score for this question :-----> "+str(mrk)+"/"+str(que_mark[i-1]))
        # print("------------------------------------------------------")
        record = [sentence1, sentence2, mrk]
        result[i]=record
        
        # print("\n\n")
    # print("\nTotal score:- "+str(sum)+"/"+str(total))
    # Process the extracted text with SBERT model
    return result

def answer(request):
    context = {'code': code}
    sum = 0
    content = {}
    # code="32"
    result = Checking(code)
    context['keys'] = result.keys()
    context['values'] = result.values()
    context['result'] = result
    valu = result.values()
    if request.method == 'POST':
        for i in valu: 
            get = "marks_"+str(i)
            marks = str(request.POST.get(get))
            sum = sum + float(marks)
        Sum = str(sum)
        val = (roll, code, Sum)
        sql = "%s,%s,%s"
        inserting("result", sql, val)
        content['message'] = "Marks added successfully"
        return render(request, "upload.html", content)
    else:
        pass
    return render(request,"answer.html", context)

def result(request):
    context = {}
    data = display_table("result")
    subject_dict = {}
    for item in data:
        roll_no = item[0]
        subject_code = item[1]
        marks = item[2]
        if subject_code not in subject_dict:
            subject_dict[subject_code] = []
        val = [roll_no, marks]
        subject_dict[subject_code].append(val)
    context['record'] = subject_dict
    return render(request,"result.html", context)