from django.shortcuts import render, redirect
from django.contrib import messages
from django.core.files.storage import FileSystemStorage
from Dashboard.models import *
import PyPDF2
from .forms import PdfForm

def error(request):
    return render(request,"error.html")

def login(request):
    return render(request,"login.html")

def teacher_dashboard(request):
    context = {'b': '0'}
    teacher_username = str(request.POST.get('teacher_username'))
    teacher_password = str(request.POST.get('teacher_password'))
    teacher_login = display_table("teacher_login")
    if request.method == 'POST':
        for i in teacher_login:
            if i[0]==teacher_username:
                if i[1]==teacher_password:
                    a=1
                    return redirect('teacher-dashboard')
                else:
                    context['message'] = "Wrong Password"
                    return redirect('error')
            else:
                context['message'] = "Wrong Username"
                return redirect('error')
        # subject_code = request.POST['subject_code']
        # model_answers = request.FILES['model_answers']
        # fs = FileSystemStorage()
        # filename = fs.save(model_answers.name, model_answers)
        # messages.success(request, f'Model answers for subject code {subject_code} uploaded successfully.')
        
    return render(request,'teacher_dashboard.html')

# def pdf_view(request):
#     context= {}
#     subject_code = request.POST.get('subject_code')
#     model_paper = request.POST.get('model_answers')
#     data = display_table("Teacher_paper")
#     if request.method == 'POST':
#         # for code in data:
#         #     if code[0] == subject_code:
#         #         context["message"]= "Answer Sheet already exists"
#         #         return render(request,'upload.html', context)
#         form = PdfForm(request.POST, request.FILES)
#         text = ""
#         pdf_file = request.FILES['model_answers']
#         pdf_reader = PyPDF2.PdfReader(model_paper)
#         text = ""
#         for page in range(len(pdf_reader.pages)):
#             text += pdf_reader.pages[page].extract_text()
#         val = (subject_code, text)
#         sql = "%s,%s"
#         inserting("Teacher_answers", sql, val)
#         context["message"]= "Answer Sheet Uploaded"
#     return render(request,'upload.html', context)

def upload_model_answers(request):
    context= {}
    subject_code = request.POST.get('subject_code')
    Question = request.POST.get('Question')
    marks = request.POST.get('marks')
    data = display_table("Teacher_paper")
    if request.method == 'POST':
        for code in data:
            if code[0] == subject_code:
                context["message"]= "Answer Sheet already exists"
                return render(request,'upload.html', context)
        form = PdfForm(request.POST, request.FILES)
        if form.is_valid():
            pdf_file = request.FILES['pdf_file']
            pdf_reader = PyPDF2.PdfReader(pdf_file)
            text = ""
            for page in range(len(pdf_reader.pages)):
                text += pdf_reader.pages[page].extract_text()
            val = (subject_code, text)
            sql = "%s,%s"
            inserting("Teacher_paper", sql, val)
            val1 = (subject_code, Question, marks)
            sql1 = "%s,%s,%s"
            inserting("paper", sql1, val1)
            context["message"]= "Answer Sheet Uploaded"
            return render(request, 'upload.html', context)
        
    else:
        form = PdfForm()
    return render(request, 'upload.html', context)
