from maplewikiskillbox import *

with open('src.txt','r',encoding='utf8') as file:
    src = file.read()

replace_all_skills_in_page(src,'result.txt')