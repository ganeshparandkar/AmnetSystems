# import io

# from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
# from pdfminer.converter import TextConverter
# from pdfminer.layout import LAParams
# from pdfminer.pdfpage import PDFPage


# def convert_pdf_to_txt(path):
#     rsrcmgr = PDFResourceManager()
#     retstr = io.StringIO()
#     codec = 'utf-8'
#     laparams = LAParams()
#     device = TextConverter(rsrcmgr, retstr, codec=codec, laparams=laparams)
#     fp = open(path, 'rb')
#     interpreter = PDFPageInterpreter(rsrcmgr, device)
#     password = ""
#     maxpages = 0
#     caching = True
#     pagenos = set()

#     for page in PDFPage.get_pages(fp, pagenos, maxpages=maxpages,
#                                   password=password,
#                                   caching=caching,
#                                   check_extractable=True):
#         interpreter.process_page(page)

    

#     fp.close()
#     device.close()
#     text = retstr.getvalue()
#     retstr.close()
#     return text

# data = convert_pdf_to_txt('./media/Ritika_Keni_Resume.pdf')
# print(data)
a = 'alsdfjalk sdfaf hi'
print(a)
print(type(a))
a = a.replace('hi','bye')
print(a)