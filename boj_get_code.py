import requests
from urllib.request import urlretrieve
from urllib.request import urlopen
from bs4 import BeautifulSoup
import os
import ctypes

#확장자 가져오기
def get_extension(lang):
    dict = {
        "C" : 'c',
        "C11" : 'c',
        "C++" : 'cpp',
        "C++11" : 'cpp',
        "C++14" : 'cpp',
        "Java" : 'java',
        "Python" : 'py',
        "Python3" : "py",
        "Ruby 2.2" : "rb",
        "C# 4.0" : "cs",
        "Text" : 'txt',
        'Go' : 'go',
        'F#' : 'fs',
        'Pascal' : 'pas',
        'Lua' : 'lua',
        'Perl' : 'pl',
        'C(Clang)' : 'c',
        'C++(Clang)' : 'c',
        'C++(Clang)' : 'cc',
        'C++14(Clang)' : 'cc',
        'Fortran' : 'f95',
        'Ada' : 'ada',
        'awk' : 'awk',
        'Ocaml' : 'ml',
        'Whitespace' : 'ws',
        'Tcl' : 'tcl',
        'Assembly (32bit)' : 'asm',
        'D' : 'd',
        'Clojure' : 'clj',
        'Rhino' : 'js',
        'Cobol' : 'cob',
        'SpiderMonkey' : 'js',
        'Pike' : 'pike',
        'sed' : 'sed',
        'Rust' : 'rs',
        'Intercal' : 'i',
        'bc' : 'bc',
        'VB.NET 4.0' : 'vb',
        }
    for x in dict.keys():
        if x.lower() == lang.lower():
            return dict[x]

USERNAME = input("ID  : ")
PASSWORD = input("PASSWORD  : ")
NEWFOLDER = input("폴더 명 : ")

if not os.path.exists(NEWFOLDER):
    os.makedirs(NEWFOLDER)
else:
    ctypes.windll.user32.MessageBoxW(0, "이미 폴더가 존재합니다", " ", 1)
    quit()

#세션 연결
with requests.Session() as c:
    #파일저장 함수
    def save_file(file_name, source, extension):
        download = c.get("https://www.acmicpc.net/source/download/" + source).text
        with open(os.path.join(NEWFOLDER, str(file_name)+"."+extension), "w") as code:
            code.write(download)
        
    url = "https://www.acmicpc.net/signin/?next=/"
    c.get(url)
    login_data = {
        'login_user_id' : USERNAME,
        'login_password' : PASSWORD,
        'next' : '/'
            }
    
    c.post(url, data=login_data, headers={"Referer":"https://www.acmicpc.net/"})

    user_page = c.get("https://www.acmicpc.net/user/" + USERNAME)

    bsObj = BeautifulSoup(user_page.text, "html.parser")
    problem_list = bsObj.findAll("span", {"class":"problem_number"})
    
    problem_number_list = []
    #list 안에 있는 내용을 뽑기
    for number in problem_list:
        problem_number_list.append(number.get_text())

    for number in problem_number_list:
        problem_page = c.get("https://www.acmicpc.net/status/?from_mine=1&problem_id="+ number +
                             "&user_id=" + USERNAME)
        bsObj = BeautifulSoup(problem_page.text, "html.parser")
        table = []
        #result_problem = bsObj.findAll("span", {"class":"result-text"})
        #result_problem = bsObj.find("table", {"id":"status-table"}).tbody.children
        for child in bsObj.find("table", {"id":"status-table"}).tbody.findAll("tr"):
            correct = child.find("span", {"class":"result-text"}).get_text().strip()
            if correct != "맞았습니다!!":
                continue
            source = child.td.get_text()
            language = child.findAll("td")[6].a.get_text().strip()
            table_info = [number, source, language]
            table.append(table_info)

        file_count = 1
        first_ck = True
        
        for info in table:
            if first_ck == True:
                file_name = str(info[0])
                first_ck = False
            else:
                file_name = str(info[0]) + "-" + str(file_count)
            extension = get_extension(info[2])
            save_file(file_name, info[1], extension)
            file_count += 1

    

    
    
    
        
    
    
