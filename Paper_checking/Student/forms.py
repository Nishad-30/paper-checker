from django import forms

class PdfForm(forms.Form):
    pdf_file = forms.FileField()