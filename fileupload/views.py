import PyPDF2
from PyPDF2 import pdf
from django.http.response import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, HttpResponse, redirect
from django.contrib import messages

from .forms import FilesUploadForm
from .models import file_upload

# Create your views here.

import io

from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.converter import TextConverter
from pdfminer.layout import LAParams
from pdfminer.pdfpage import PDFPage
import xml.etree.ElementTree as et
import re
from xml.dom import minidom

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
def missmatch(path):
        
    mytree = minidom.parse(path)

    lang_termSetElem = mytree.getElementsByTagName('term')


    ch=''
    odd=''
    even=''


    for x in lang_termSetElem:

            ch=x.firstChild.nodeValue

            break


    i=0

    arr = []

    for x in lang_termSetElem:

        if (ch == x.firstChild.nodeValue):
            pass
        else:
            i=i+1
            # print(i, " ", x.firstChild.nodeValue)
            if(i%2==0):
                even=x.firstChild.nodeValue
                even = even[:-2]

            else:
                odd=x.firstChild.nodeValue
                odd= odd[:-2]

            if(i%2==0):
                if odd>even:
                    count=i
                    arr.append((even,odd))
                    # print(even, "<<miss match  >>", odd)

                    # break
            else:
                if even>odd:
                    count = i
                    arr.append((even,odd))
                    # print(even, "<<miss match >> ", odd)
                    # break
    return arr



def index(request):
    data = file_upload.objects.all()

    if request.method == 'POST':
        c_form = FilesUploadForm(request.POST, request.FILES)
        if c_form.is_valid():
            files = c_form.cleaned_data['files']
            name = files.name

            if (files.name.endswith('.xml') or files.name.endswith('.pdf')):
                flag = 0
                if (files.name.endswith('.pdf')):

                    for i in data:
                        if (i.file_name.endswith('.pdf')):
                            flag = 1
                            messages.info(
                                request, 'You already uploaded the PDF! You cant upload more than one PDF')

                    if flag == 0:
                        file_upload(file_name=name, up_file=files).save()

                if (files.name.endswith('.xml')):

                    for i in data:
                        if (i.file_name.endswith('.xml')):
                            flag = 1
                            messages.info(
                                request, 'You already uploaded the xml! You cant upload more than one XML')

                    if flag == 0:
                        file_upload(file_name=name, up_file=files).save()

            return redirect('home')
        else:
            return HttpResponse("Error")

    else:
        context = {
            'form': FilesUploadForm(),
            'data': data
        }

        return render(request, 'index.html', context)


def deleteAll(request):
    data = file_upload.objects.all()
    for document in data:
        document.delete()
    return redirect('home')


def sendsample(request):
    return render(request, 'd1.html')


def Pageno(request):
    
    all_data = file_upload.objects.all()
    xmlFileAvailable = False

    for i in all_data:
        if (i.file_name.endswith('.xml')):
            xmlFileAvailable = True
            xmlFile = i

    if xmlFileAvailable:

        a = '.' + xmlFile.up_file.url
        chapterData = pageNoChapterWise(a)
        #!alsldfkasdflasdjf
        tree = et.parse(a)
        root = tree.getroot()

        ch_num_toc = []
        ch_page_toc = []
        ch_pgn_mt = []
        result = []

        for type_tag in root.findall('front/div/list/list-item/p/b'):
            if type_tag.text is not None:
                ch_num_toc.append(type_tag.text)

        for type_tag in root.findall('front/div/list/list-item/p/ref/display-text'):
            if type_tag.text is not None:
                ch_page_toc.append(type_tag.text)

        result.append(ch_num_toc)
        result.append(ch_page_toc)
        # print('\n',ch_num_toc,'\n')
        # print(ch_page_toc,'\n')

        for type_tag in root.findall('div/page-start'):
            ch_pgn_mt.append(type_tag.get('number'))

        ch_pgn_mt = ch_pgn_mt[1:]
        for i in range(0, len(ch_pgn_mt)):
            ch_pgn_mt[i] = ch_pgn_mt[i][2:]
        # print(ch_pgn_mt)

        total_ch = len(ch_pgn_mt)

        # I have introduced this error intentionally
        # ch_pgn_mt[1]='15'
        # print(ch_pgn_mt)

        pgn_issue = []

        for i in range(0, total_ch):
            if(ch_page_toc[i] != ch_pgn_mt[i]):
                pgn_issue.append(i)
        if(len(pgn_issue) == 0):
            print("No issues with pagen numbers")
        else:
            print("There is a page number issue on")
            for j in pgn_issue:
                print("On chapter : ", j+1)

        ch_name_toc = []
        for type_tag in root.findall('front/div/list/list-item'):
            # print(type_tag.text)
            if type_tag.text is not None:
                ch_name_toc.append(type_tag.text)

        chapterData = result
        #
        #!alsldfkasdflasdjf
        print(chapterData)
        tree = et.parse(a)
        root = tree.getroot()
        ch_page_toc = []
        ch_pgn_mt = []
        result = []
        flag = 0
        for type_tag in root.findall('front/div/list/list-item/p/ref/display-text'):
            # print(type_tag.text)
            if type_tag.text is not None:
                ch_page_toc.append(type_tag.text)
        print(ch_page_toc)

        for type_tag in root.findall('div/page-start'):
            ch_pgn_mt.append(type_tag.get('number'))
        print(ch_pgn_mt)
        ch_pgn_mt = ch_pgn_mt[1:]
        for i in range(0, len(ch_pgn_mt)):
            ch_pgn_mt[i] = ch_pgn_mt[i][2:]

        pgn_issue = []
        total_ch = len(ch_pgn_mt)
        for i in range(0, total_ch):
            if(ch_page_toc[i] != ch_pgn_mt[i]):
                pgn_issue.append(i)
        if(len(pgn_issue) == 0):
            # print("No issues with pagen numbers")
            result.append('No issues with pagen numbers')
        else:
            # print("T")
            result.append('There is a page number issue on')
            for j in pgn_issue:
                result.append(['On chapter :', j+1])
                # print("On chapter : ",j+1)

        if len(result) > 1:
            flag = 1
            result = ''.join(result)
        else:
            result = result[0]

        chapterNames = chapterData[0]
        chapterPageNo = chapterData[1]
        arr = zip(chapterNames, chapterPageNo)
        context = {
            'xmlAvailable': xmlFileAvailable,
            'chapterData': arr,
            'data': result,
            'check': flag,
            'cNames': chapterNames,
            'cPageNo': chapterPageNo
        }
    else:
        context = {
            'xmlAvailable': xmlFileAvailable,
        }

    return render(request, 'pageNo.html', context)
def alphaOrder(request):

    all_data = file_upload.objects.all()
    xmlFileAvailable = False

    for i in all_data:
        if (i.file_name.endswith('.xml')):
            xmlFileAvailable = True
            xmlFile = i

    if xmlFileAvailable:

        a = '.' + xmlFile.up_file.url
        alphaOrder = missmatch(a)
        col1 =  [x[0] for x in alphaOrder]
        col2 =  [x[1] for x in alphaOrder]
        arr = zip(col1, col2)

        context = {
            'xmlAvailable': xmlFileAvailable,
            'alphaOrder': arr,
            'col1':col1,
            'col2':col2
        }
    else:
        context = {
            'xmlAvailable': xmlFileAvailable,
        }

    return render(request, 'orderwiseChapters.html', context)


def mdash(request):
    myContext = {}
    all_data = file_upload.objects.all()
    pdfFile = False

    for i in all_data:
        if (i.file_name.endswith('.pdf')):
            pdfFile = i

        if (i.file_name.endswith('.xml')):
            xmlFile = i

    if pdfFile:
        pdfAvailable = True

        # print('there is pdf')
        a = '.' + pdfFile.up_file.url
        print('file name is ---------------------> ', a)
        pdfData = convert_pdf_to_txt(a)

        pdfData = pdfData.replace('—', '<span class="bg-yellow">—</span>')
        pdfData = pdfData.replace('\n', '<br>')
        s = '<p>' + pdfData + '</p>'
        count = 0
        for i in pdfData:
            if i == '—':
                count = count + 1

        context = {
            'pdfData': s,
            'pdfAvailable': pdfAvailable,
            'count': count,
        }
        return render(request, 'mdash.html', context)
    else:
        pdfAvailable = False
        print('there is no pdf')
    return render(request,
                  'mdash.html', myContext)


def junkChar(request):
    myContext = {}
    context ={}
    all_data = file_upload.objects.all()
    pdfFile = False

    for i in all_data:
        if (i.file_name.endswith('.pdf')):
            pdfFile = i

        if (i.file_name.endswith('.xml')):
            xmlFile = i

    if pdfFile:
        pdfAvailable = True

        # print('there is pdf')
        a = '.' + pdfFile.up_file.url
        print('file name is ---------------------> ', a)
        pdfData = convert_pdf_to_txt(a)

        resource_manager = PDFResourceManager()
        fake_file_handle = io.StringIO()
        converter = TextConverter(resource_manager, fake_file_handle)
        page_interpreter = PDFPageInterpreter(resource_manager, converter)

        with open(a, 'rb') as fh:
            for page in PDFPage.get_pages(fh, caching=True, check_extractable=True):
                page_interpreter.process_page(page)

            text = fake_file_handle.getvalue()
            pattern = '☒'
            for i in text:
                r = re.search(pattern, i)
                if bool(r):
                    # print(r)
                    # print(type(r))
                    continue

        converter.close()
        fake_file_handle.close()

        if text:
            pdfData = text
            pdfData = pdfData.replace('☒', '<span class="bg-yellow">☒</span>')
            pdfData = pdfData.replace('\n', '<br>')
            s = '<p>' + pdfData + '</p>'
            count = 0
            for i in pdfData:
                if i == '☒':
                    count = count + 1

            if count > 0:
                context['Junk_count'] = count
                context['JunkAvailable'] = True
                context['pdfData'] = s
                context['pdfAvailable']= pdfAvailable

            print(context)
            return render(request, 'Jcharacter.html', context)


        else:
            pdfAvailable = False
            print('there is no pdf')
            return render(request,
                    'Jcharacter.html', myContext)



def pageNoChapterWise(path):
    result = 0
    return result


# def show_file(request):

#     data = file_upload.objects.first()
#     print
#     a = '.' + data.up_file.url
#     # file = open
#     # (a, "rb")
#     print('file name is ---------------------> ', a)
#     pdfData = convert_pdf_to_txt(a)

#     # pdfReader = PyPDF2.PdfFileReader(file)
#     # print(pdfReader.numPages)
#     # pageObj = pdfReader.getPage(0)

#     # reader = PyPDF2.PdfFileReader(file)
#     # page1 = reader.getPage(4)
#     # # print(page1)
#     # pdfData = pageObj.extractText()
#     words = pdfData.split(' ')
#     print(words)
#     context = {
#         'data': words,
#         # 'data': all_data,
#         # 'pdfData': words
#     }

#     return render(request, 'view.html', context)
