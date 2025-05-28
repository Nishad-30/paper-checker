from django.shortcuts import render, redirect
# from django.contrib import messages
# from django.core.files.storage import FileSystemStorage
# import os
# from Result.models import *

# def upload_model_answers(request):
#     if request.method == 'POST':
#         # Get form data
#         subject_code = request.POST['subject_code']

#         # Set upload directory and file name
#         target_dir = "uploads/"
#         file_name = f"{subject_code}_model_answers.pdf"
#         target_file = os.path.join(target_dir, file_name)

#         # Check if the file was uploaded
#         if request.FILES:
#             # Save the file to the upload directory
#             with open(target_file, 'wb+') as f:
#                 for chunk in request.FILES['model_answers'].chunks():
#                     f.write(chunk)

#             # Save the file details to the database
#             # models.ModelAnswer.objects.create(
#             #     subject_code=subject_code,
#             #     file_name=file_name,
#             #     file_path=target_file
#             # )

#             # Display success message
#             messages.success(request, 'File uploaded successfully!')

#             return redirect('teacher_dashboard')

#         # Display error message
#         messages.error(request, 'File upload failed. Please check the file syntax and try again.')

#     return redirect('teacher_dashboard')


# def submit_answers(request):
#     if request.method == 'POST':
#         # Get form data
#         subject_code = request.POST['subject_code']
#         roll_number = request.POST['roll_number']

#         # Save student answers sheet to uploads directory
#         target_dir = "uploads/"
#         tar = target_dir
#         student_answers = request.FILES['student_answers']
#         student_answers_filename = os.path.join(target_dir, student_answers.name)
#         with open(student_answers_filename, 'wb+') as f:
#             for chunk in student_answers.chunks():
#                 f.write(chunk)

#         # Run Python code and capture output
#         model_answers_path = os.path.join(tar, f"{subject_code}_model_answers.pdf")
#         student_answers_path = student_answers_filename

#         # Call external Python script
#         # cmd = ["python3", "process_answers.py", model_answers_path, student_answers_path]
#         # output = subprocess.run(cmd, capture_output=True, text=True)

#         # # Save student answers and Python code output to database
#         # StudentAnswer.objects.create(
#         #     subject_code=subject_code,
#         #     roll_number=roll_number,
#         #     answers_text=output.stdout
#         # )

#         # Display success message
#         messages.success(request, 'Student answers submitted successfully!')

#         return redirect('student_dashboard')

#     return redirect('student_dashboard')
from Result.tests import *
from Dashboard.models import *
# import io

def Checking(code):
    answer_paper = selection_search("teacher_answers","Subject_code",code)
    answer_sheet = selection_search("student_answers","Subject_code",code)
    data1 = answer_paper[0][1]
    data2 = answer_sheet[0][2]
    # buffer1 = io.BytesIO(data1)
    # buffer2 = io.BytesIO(data2)
    # data1 =r"C:\Users\nisha\Downloads\Answer_paper.pdf"
    # data2 = r"C:\Users\nisha\Downloads\Answer_sheet.pdf"
    reader1 = PdfReader(data1)
    reader2 = PdfReader(data2)
    # printing number of pages in pdf file 

    # getting a specific page from the pdf file
    page1 = reader1.pages[0] #getting first page
    page2 = reader2.pages[0]

    # extracting text from page
    text1 = page1.extract_text()
    text2 = page2.extract_text()
    que_mark = [2,2,2]
    total = 6
    que=len(que_mark)
    textls1 = []
    textls2 = []
    textls1 = text1.split(" ")
    textls2 = text2.split(" ")
    sum = 0
    result = {}
    for i in range(1,que+1):
        record = []
        # print(" ---------------")
        # print("| Question no. "+str(i)+"|")
        sent1 = []
        sent2 = []
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
        mrk = que_mark[i-1]*score(sentence1,sentence2)
        sum = sum+mrk
        # print("||Score for this question :-----> "+str(mrk)+"/"+str(que_mark[i-1]))
        # print("------------------------------------------------------")
        record = [sentence1, sentence2, mrk]
        result[i]=record
        
        # print("\n\n")
    # print("\nTotal score:- "+str(sum)+"/"+str(total))
    # Process the extracted text with SBERT model
    return result

# def answer(request):
#     # code="32"
#     # context = Checking(code)
#     return render(request,"answer.html", context)