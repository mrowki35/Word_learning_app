import kivy
from kivy.app import App


import json
import random
from kivy.lang import Builder
from pathlib import Path
from kivy.properties import ObjectProperty

from kivy.uix.screenmanager import ScreenManager
from kivy.uix.screenmanager import Screen
import fileinput
from kivy.config import Config

from kivy.uix.button import Button
from kivy.uix.label import Label

from kivy.graphics import RoundedRectangle

Config.set('graphics', 'resizable', True)




wordslist=[]
wordsbackuplist=[]
with open('data.txt','r',encoding="utf-8") as randomwordslistfile:
    for line in randomwordslistfile:
        randomwords1=line
        randomwords2=randomwords1.replace("\n", "").split(", ")
        wordslist.append(randomwords2[0])
        wordsbackuplist.append(randomwords2[0])
       
randomwordslistfile.close()


def checkiftheowordalreadyexists(whattocheck):
    #str(whattocheck)
    existingwordslist=[]
    with open('data.txt','r', encoding="utf-8") as exisitngwordfile:
        for line in exisitngwordfile:
            existingwords1=line
            existingwords2=existingwords1.replace("\n", "")
            existingwordsfulllist=existingwords2.split(",")
            existingwordslist.append(existingwordsfulllist[0])
        #print(whattocheck)
        if whattocheck in existingwordslist:
            #print("This world already exists")
            exisitngwordfile.close()
            return 1
        else:
            exisitngwordfile.close() 
    exisitngwordfile.close()    


class word:

    polish =''
    english = ''
    deutsch =''
    def add(self,pl,eng,de):
        word.polish=pl
        if(checkiftheowordalreadyexists(word.polish)==1):
            return
        word.english=eng
        word.deutsch=de
        with open('data.txt','a', encoding = 'utf-8') as my_data_file:
            my_data_file.write("\n" + word.polish + ', ')
            my_data_file.write(word.english + ', ')
            my_data_file.write(word.deutsch)
        my_data_file.close()

#word2=word()
#losowanie słowek

def chooserandomwords():
    randomwordslist=[]
    with open('data.txt','r',encoding="utf-8") as randomwordslistfile:
        for line in randomwordslistfile:
            randomwords1=line
            randomwords2=randomwords1.replace("\n", "")
            randomwordsfulllist=randomwords2.split(", ")
            randomwordslist.append(randomwordsfulllist[0])
       
    randomwordslistfile.close()
    if (len(randomwordslist)==0):
        return ['']
    else:
        return randomwordslist

def randomchoice():
    z=random.choice(chooserandomwords())
    return z
    
    
def givewordeng():
    print("Podaj tłumaczenie po angielsku: ")
    poangielsku=input()
    return poangielsku
def givewordde():
    print("Podaj tłumaczenie po niemiecku: ")
    poniemiecku=input()
    return poniemiecku


def checkanswer(x,y,z):
    fullanswerlist=[]
    with open('data.txt','r',encoding="utf-8") as basefile_answers:
        for line in basefile_answers: 
            answermirror=line
            answerwithenter=answermirror.replace("\n", "")
            answerlist=answerwithenter.rsplit(", ")
            fullanswerlist.append(answerlist)
            
        if [x,y,z] in fullanswerlist:
            return "DOBRZE"

        else:
            return "ŹLE"
            

    basefile_answers.close()

def cloninglist(list1):
    list2=list1[:]
    return list2

def resetwordlist():
    global wordslist
    wordslist=cloninglist(wordsbackuplist)
    

def worddeletion(h):
    items=[]
    if(checkiftheowordalreadyexists(h)==1):
        with open('data.txt','r',encoding="utf-8") as existingwordfile2:
            for line in existingwordfile2:
                items.append(line)
            for string in items:
                if h in string:
                    items.remove(string)
        existingwordfile2.close()
        with open('data.txt','w',encoding='utf-8') as f:
            for item in items: 
                f.write(item)
        f.close()


def deletewholedata():
    with open ('data.txt','w+',encoding="utf-8") as f:
        pass
    f.close() 


def colorupdater(good_or_bad):
    if (good_or_bad=="DOBRZE"):
        return [.5,1,.2,0.1]
    elif (good_or_bad=="ŹLE"):
        return [1,0,0,0.1]
    else:
        pass

#def test(self,good_or_bad):
   # if (good_or_bad=="DOBRZE"):
      #  return self.add_widget(Button(text="Następne słówko",size=[10,20],pos=[200,100],size_hint =(.2, .2)))
   # elif (good_or_bad=="ŹLE"):
      #  return self.add_widget(Button(text="Następne słówko",size=[10,20],pos_hint = {'center_x':0.5, 'center_y':0.8},size_hint =(.2, .2)))
   

#mainmenu

class FirstWindow(Screen):
    pass

#deleteword

class SecondWindow(Screen):
    wordtodelete=ObjectProperty(None)
    def presstosubmit(self):
        deletedword=self.wordtodelete.text
        worddeletion(deletedword)

    def cleanall(self):
        deletewholedata()
        exchange="Wyczyszczono całą listę słówek"
        self.ids.my_label.text= exchange
        
        

#myshufflelayout-quiz  

class ThirdWindow(Screen):
    popolsku=ObjectProperty(None)
    ang=ObjectProperty(None)
    niem=ObjectProperty(None)


    def showwhatword(self):
        popolsku=randomchoice()
        if (popolsku==''):
            return "Lista jest pusta"
        else:
            return popolsku

    def resetingpress(self):
        resetwordlist()
        self.popolsku.text="Zresetowano listę słów"
    
    def functioncheckanswer(self):
        c=self.popolsku.text
        a=self.ang.text
        b=self.niem.text
        #self.ids.cowyswietlic.text=checkanswer(c, a, b)
        answer_holding=checkanswer(c, a, b)
        self.rgba=colorupdater(answer_holding)
        self.ids.cowyswietlic.text=answer_holding
    
    def newword(self):
        global wordlslist
        global wordsbackuplist
        try:
            wordslist.remove(self.popolsku.text)
        except IndexError:
            self.popolsku.text="Lista jest pusta"
            pass
        except ValueError:
            pass

        if (len(wordslist)==0):
            self.popolsku.text="Lista jest pusta"
           # self.ids.thisone.add_widget(myButton)
        else:
            #wordslist.remove(self.popolsku.text)
            self.popolsku.text=random.choice(wordslist)
            self.rgba=[0,0,0,0]
            self.ids.cowyswietlic.text=""
    def showtherightanswer(self):
        fullanswerlist=[]
        fullanswerlist1=[]
        fullanswerlist2=[]
        with open('data.txt','r',encoding="utf-8") as basefile_answers:
            for line in basefile_answers: 
                answermirror=line
                answerlist=answermirror.replace("\n", "").rsplit(", ")
                fullanswerlist.append(answerlist[0])
                fullanswerlist1.append(answerlist[1])
                fullanswerlist2.append(answerlist[2])
            try:
                index=fullanswerlist.index(self.popolsku.text)
                self.ids.cowyswietlic.text= self.popolsku.text+"   "+fullanswerlist1[index]+"   "+fullanswerlist2[index]
                self.rgba=[0,0,0,0.1]
            except ValueError:
                self.ids.cowyswietlic.text=""
                self.rgba=[0,0,0,0]
                
            
            
            
        basefile_answers.close()



#maygrdalyout-addword

class FourthWindow(Screen):
    
    pl=ObjectProperty(None)
    eng=ObjectProperty(None)
    de=ObjectProperty(None)
    
    
        
    def press(self):
        
    
        word2=word()
        x=self.pl.text
        y=self.eng.text
        z=self.de.text
        word2.add(x,y,z)
        self.pl.text=""
        self.eng.text=""
        self.de.text=""



class WindowManager(ScreenManager):
    pass

kv = Builder.load_file('my.kv')


class MyApp(App):
    def build(self):
        return kv



if __name__=='__main__':
    MyApp().run()



