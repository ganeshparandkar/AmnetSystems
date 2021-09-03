tree=et.parse('bay.xml')
root=tree.getroot()

ch_num_toc=[]
ch_page_toc=[]
ch_pgn_mt=[]

for type_tag in root.findall('front/div/list/list-item/p/b'):
    if type_tag.text is not None:
        ch_num_toc.append(type_tag.text)
        
for type_tag in root.findall('front/div/list/list-item/p/ref/display-text'):
    if type_tag.text is not None:
        ch_page_toc.append(type_tag.text)
    
print('\n',ch_num_toc,'\n')
print(ch_page_toc,'\n')

for type_tag in root.findall('div/page-start'):
        ch_pgn_mt.append(type_tag.get('number'))


ch_pgn_mt = ch_pgn_mt[1:]
for i in range(0,len(ch_pgn_mt)):
    ch_pgn_mt[i]=ch_pgn_mt[i][2:]
#print(ch_pgn_mt)

total_ch=len(ch_pgn_mt)

# I have interoduced this error intentionally
ch_pgn_mt[1]='15'
print(ch_pgn_mt)

pgn_issue=[]

for i in range(0,total_ch):
    if(ch_page_toc[i]!=ch_pgn_mt[i]):
        pgn_issue.append(i)
if(len(pgn_issue)==0):
    print("No issues with pagen numbers")
else:
    print("There is a page number issue on")
    for j in pgn_issue:
        print("On chapter : ",j+1)

ch_name_toc=[]
for type_tag in root.findall('front/div/list/list-item'):
    #print(type_tag.text)
    if type_tag.text is not None:
        ch_name_toc.append(type_tag.text)

