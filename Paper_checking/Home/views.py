from django.shortcuts import render, redirect
from Home.models import *
# Create your views here.

def home(request):
    return render(request, 'home.html')



# def error(request):
#     context = {}
#     context['data'] = "there is an error"
#     return render(request,"error.html", context)

# def my_redirect_view(request):
#     target_url = 'home/'
#     return render(request, 'myapp/index.html', {'target_url': target_url})

# def teacher_dashboard(request):
#     context = {}
#     teacher_username = str(request.POST.get('teacher_username'))
#     teacher_password = str(request.POST.get('teacher_password'))
#     teacher_login = display_table("teacher_login")
#     if request.method == 'POST':
#         for i in teacher_login:
#             if i[0]==teacher_username:
#                 if i[1]==teacher_password:
#                     return redirect('teacher-dashboard')
#                 else:
#                     context['data'] = "Wrong Name"
#                     return redirect('error')
#             else:
#                 context['data'] = "Wrong Roll No"
#                 return redirect('error')
#         # subject_code = request.POST['subject_code']
#         # model_answers = request.FILES['model_answers']
#         # fs = FileSystemStorage()
#         # filename = fs.save(model_answers.name, model_answers)
#         # messages.success(request, f'Model answers for subject code {subject_code} uploaded successfully.')
        
#     return render(request,'teacher_dashboard.html')



# def student_dashboard(request):
#     student_RN = str(request.POST.get('student_roll_number'))
#     student_name = str(request.POST.get('student_name'))
#     context = {'student_RN': student_RN, 'student_name': student_name, }
#     student_login = display_table("student_login")
#     if request.method == 'POST':
#         for i in student_login:
#             if i[0]==student_RN:
#                 if i[1]==student_name:
#                     return render(request, 'student_dashboard.html', context)
#                 else:
#                     context['data'] = "Wrong Password"
#                     return redirect('error')
#             else:
#                 context['data'] = "Wrong Name"
#                 return redirect('error')
#     return render(request, 'student_dashboard.html', context)