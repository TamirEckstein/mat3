# -*- coding: utf-8 -*-
"""
Created on Thu Mar 25 19:50:24 2021

@author: User
"""
import re
import json

def check_text(text):
    
    not_wanted = ['נוצרה על ידי', 'מוצפנות מקצה-לקצה', 'הוסיף/ה את', 'הוסיף/ה אותך', 'עזב/ה', 'יצרת קבוצה זו', '<המדיה לא נכללה>']
    for words in not_wanted:
        if text.find(words)!= -1:
            return False
    
    return True


def extract_data(file):
    
    data = []
    
    time_p = '([0-9]{2}|[0-9]{1}):[0-9]{2}'
    date_p = '(([0-9]{2}|[0-9])\.([0][1-9]|[1][0-2]|[0-9])\.[0-9]{4})'
    phone_p  = '\+[0-9]{3}\s[0-9]{2}-[0-9]{3}-[0-9]{4}'
    
    for text in file:
        
        if check_text(text):
            if re.search(time_p,text) and re.search(date_p,text) :
                time = re.search(time_p,text)[0]
                date = re.search(date_p,text)[0]
                
                if re.search(phone_p,text):
                    id_label = re.search(phone_p,text)[0]
                else:
                   Start_name= text.find(" - ")+3
                   End_name= text.find(": ")
                   id_label =  text[Start_name:End_name] 
                   
          
                text_copy = text
                text_copy.replace(time,"")
                text_copy.replace(date,"")
                text_copy.replace(id_label,"")
                
                
                dict_data = {'id':id_label,'datetime':time + " " + date,'text':text_copy}
                data.append(dict_data)
                last_row = dict_data.copy()
                
            else:
                dict_data = last_row
                dict_data['text'] = text
                
 
    return data
    
def make_private_id(data):
    
    ids =[]
    for d in data:
        ids.append(data['id'])
    ids = set(ids)
    
    private_id = {id_o:index for index,id_o in enumerate(ids)}

    for d in data:
        d['id'] = private_id[d['id']]
        
        
def metadata(firstline,data):
    
    ids =[]
    for d in data:
        ids.append(data['id'])
    participents_number = len(set(ids))
    
    return ids
            
def megaDiction(data,meta) :
    mega_Data={'messages':data,'metadata':meta}
    return mega_Data
                  
           
name='WhatsApp.txt'    
fhand=open(name,'r',encoding='utf-8')
File=fhand.readlines()
data= extract_data(File)
make_private_id(data)
meta=metadata(File[0],File)
json.dump(megaDiction(data,meta),File,ensure_ascii=False,indent=6)
print(json.load(File))

