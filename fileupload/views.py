import PyPDF2
from PyPDF2 import pdf
from django.http.response import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, HttpResponse, redirect

from .forms import FilesUploadForm
from .models import file_upload

# Create your views here.

import io

from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.converter import TextConverter
from pdfminer.layout import LAParams
from pdfminer.pdfpage import PDFPage


def convert_pdf_to_txt(path):
    rsrcmgr = PDFResourceManager()
    retstr = io.StringIO()
    codec = 'utf-8'
    laparams = LAParams()
    device = TextConverter(rsrcmgr, retstr, codec=codec, laparams=laparams)
    fp = open(path, 'rb')
    interpreter = PDFPageInterpreter(rsrcmgr, device)
    password = ""
    maxpages = 0
    caching = True
    pagenos = set()

    for page in PDFPage.get_pages(fp, pagenos, maxpages=maxpages,
                                  password=password,
                                  caching=caching,
                                  check_extractable=True):
        interpreter.process_page(page)

    fp.close()
    device.close()
    text = retstr.getvalue()
    retstr.close()
    return text


def index(request):
    if request.method == 'POST':
        c_form = FilesUploadForm(request.POST, request.FILES)
        if c_form.is_valid():
            name = c_form.cleaned_data['file_name']
            files = c_form.cleaned_data['files']
            file_upload(file_name=name, up_file=files).save()

            return redirect('view')
        else:
            return HttpResponse("Error")

    else:
        context = {
            'form': FilesUploadForm()
        }
        return render(request, 'index.html', context)


def sendsample(request):
    return render(request, 'd1.html')


def Pageno(request):
    return render(request, 'pageNo.html')


def mdash(request):
    data = file_upload.objects.first()
    print
    a = '.' + data.up_file.url
    # file = open(a, "rb")
    print('file name is ---------------------> ', a)
    pdfData = convert_pdf_to_txt(a)

    pdfData = pdfData.replace('—', '<span class="bg-yellow">—</span>')
    pdfData = pdfData.replace('\n', '<br>')
    # print(type(pdfData))
    s = '<p>' + pdfData + '</p>'
    count = 0
    for i in pdfData:
        if i == '—':
            count = count + 1

    # s = s.split(' ')

    context = {
        # 'pdfData': pdfData,
        # 'pdfData': '<h1>hello</h1>',
        'pdfData': s,

        'count': count,
    }
    return render(request, 'mdash.html', context)


def junkChar(request):
    return render(request, 'Jcharacter.html')


def show_file(request):
    # all_data = file_upload.objects.all()
    data = file_upload.objects.first()
    print
    a = '.' + data.up_file.url
    # file = open
    # (a, "rb")
    print('file name is ---------------------> ', a)
    pdfData = convert_pdf_to_txt(a)

    # pdfReader = PyPDF2.PdfFileReader(file)
    # print(pdfReader.numPages)
    # pageObj = pdfReader.getPage(0)

    # reader = PyPDF2.PdfFileReader(file)
    # page1 = reader.getPage(4)
    # # print(page1)
    # pdfData = pageObj.extractText()
    words = pdfData.split(' ')
    print(words)
    context = {
        'data': words,
        # 'data': all_data,
        # 'pdfData': words
    }

    return render(request, 'view.html', context)
