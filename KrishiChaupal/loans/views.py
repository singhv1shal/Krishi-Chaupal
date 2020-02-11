from __future__ import unicode_literals
from django.shortcuts import render
from django.views.generic import TemplateView
# Create your views here.
from selenium.webdriver.chrome.options import Options
from prompt_toolkit import print_formatted_text
from selenium import webdriver
from bs4 import BeautifulSoup
import time
import re
import os

class loans():
    def __init__(self):
        self.name=""
        self.link=""

class loan_content():
    def __init__(self):
        self.col1=""
        self.col2=""


class loan(TemplateView):
    template_name='loan.html'

class canara(TemplateView):
    template_name='loan.html'

def cbi(request):
    options=Options()
    options.add_argument("--headless")
    context={}
    loan_list=[]
    loan_links=[]
    driver=webdriver.Chrome(executable_path=r'chromedriver',chrome_options=options)
    driver.get('https://www.centralbankofindia.co.in/English/Kisan_Tatkal.aspx')

    soup=BeautifulSoup(driver.page_source,'lxml')

    divi=soup.find('ul',class_='nav nav-list tree open is-active')
    for li in divi.find_all('li'):
        for A in li.find_all('a'):
            x=loans()
            x.name=A.text
            x.link="https://www.centralbankofindia.co.in/English/"+A['href']
            loan_list.append(x.name)
            loan_links.append(x.link)
    context.update({'loan_list':loan_list})

    driver.quit()

    driver=webdriver.Chrome(executable_path=r'chromedriver',chrome_options=options)
    context.update({'loan_links':loan_links})

    details={}
    m=0
    for url in loan_links:
        driver.get(url)
        soup=BeautifulSoup(driver.page_source,'lxml')
        div=soup.find('div',id='content')
        time.sleep(1)
        TR=div.find_all('tr')
        content=[]
        for tr in TR:
            i=0
            x=loan_content()
            for td in tr.find_all('td'):
                if i%2==0:
                    x.col1=td.get_text()
                    x.col1 = os.linesep.join([s for s in x.col1.splitlines() if s])
                    i=i+1
                else:
                    x.col2=td.get_text()
                    x.col2 = os.linesep.join([s for s in x.col2.splitlines() if s])
            content.append(x)
        final={}
        k=0
        for j in range(len(content)):
            final.update({content[k].col1:content[k].col2})
            k+=1
        details.update({loan_list[m]:final})
        m+=1
    context.update({'details':details})
    driver.quit()
    return render(request,'cbi.html',context=context)

def iob(request):
    options=Options()
    options.add_argument("--headless")
    context={}
    loan_list=[]
    loan_links=[]
    driver=webdriver.Chrome(executable_path=r'chromedriver',chrome_options=options)
    driver.get('https://www.iob.in/Rural')

    soup=BeautifulSoup(driver.page_source,'lxml')

    UL=soup.find('li',class_='mega-drop-down')

    for i in range(3):
        UL=UL.findNextSibling()

    div=UL.find('div',class_='col-md-2')

    for j in range(3):
        div=div.findNextSibling()



    li=div.find_all('li')
    for LI in li:
        # print(LI)
        for A in LI.find_all('a'):
             x=loans()
             x.name=A.text
             x.link="https://www.iob.in/"+A['href']
             loan_list.append(x.name)
             loan_links.append(x.link)

    # for loan in loans:
    #     print(loan.name)

    driver.quit()
    context.update({'loan_list':loan_list})
    driver=webdriver.Chrome(executable_path=r'chromedriver',chrome_options=options)
    details={}
    # for i in range(len(loans)):
    m=0
    for url in loan_links:
        # url="https://www.iob.in/"+loans[i].link
        # url="https://www.iob.in/Agri-clinic"
        # print(url)
        driver.get(url)
        soup=BeautifulSoup(driver.page_source,'lxml')
        div=soup.find('div',id='ctl00_ContentPlaceHolder1_ohtr_descrp')
        # print(div)
        TR=div.find('tr')
        TR=TR.findNextSibling()

        content=[]
        for j in range(8):
            x=loan_content()
            z=0
            for td in TR.find_all('td'):
                if z%2==0:
                    x.col1=td.get_text()
                    z=z+1
                else:
                    x.col2=td.get_text()
                    x.col2 = os.linesep.join([s for s in x.col2.splitlines() if s])
            content.append(x)
            TR=TR.findNextSibling()
        final={}
        k=0
        for p in range(len(content)):
            final.update({content[k].col1:content[k].col2})
            k+=1
        details.update({loan_list[m]:final})
        m+=1
        context.update({'details':details})
        driver.quit()
        return render(request,'cbi.html',context=context)
