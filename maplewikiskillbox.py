import re
import urllib.request

class Skill:
    def __init__(self, image = "",name = "",typ = "Passive",reqlv = 0,masterlv = 1,desc = '',effect ='', i = 0):
        self.image = image
        self.name = name
        self.type = typ
        self.reqlv = reqlv
        self.masterlv = masterlv
        self.desc = desc
        self.effect = effect
        self.id = i
    
    def skillbox(self):
        if self.reqlv:
            text = "{{{{Skillbox<!--{id}-->\n|image={image}\n|name={name}\n|type={type}\n|reqlv={reqlv}\n|masterlv={masterlv}\n|desc={desc}\n|effect={effect}\n}}}}".format(
        name=self.name,image=self.image,type=self.type,id=self.id,reqlv=self.reqlv,masterlv = self.masterlv,desc = self.desc,effect=self.effect)
        else:
            text = "{{{{Skillbox<!--{id}-->\n|image={image}\n|name={name}\n|type={type}\n|masterlv={masterlv}\n|desc={desc}\n|effect={effect}\n}}}}".format(
        name=self.name,image=self.image,type=self.type,id=self.id,masterlv = self.masterlv,desc = self.desc,effect=self.effect)
        return text
    

def replace_skill(skilltuple):
    if len(skilltuple) >= 5:
        skillinfo = tuple([i.replace('\n','') for i in skilltuple])
        skillid = int(re.findall('[0-9]+',skillinfo[0])[0]) if len(re.findall('[0-9]+',skillinfo[0])) > 0 else 0
        skillimg = re.findall('\[\[.*\]\]',skillinfo[1])[0]
        skillname = skillinfo[2].strip('|')
        skilltype = skillinfo[3].strip('|')
        skilldesc = skillinfo[4].strip('|')
        if re.search('\[\[',skillname):
            matcher = re.compile('\[\[([^\|\]]*)')
            pagename = matcher.findall(skillname)[0]
            print(pagename)
            url = urllib.request.urlopen(('https://maplestory.fandom.com/wiki/'+pagename).replace(' ','_'))
            sourcecode = str(url.read().decode('utf-8'))
            skillmaxlv = int(re.findall('Maximum Level:\s*</b>\s*([0-9]+)',sourcecode)[0])
            skillreqlv = int(re.findall('Level Requirement:\s*</b>\s*([0-9]+)',sourcecode)[0]) if re.search('Level Requirement',sourcecode) else 0
            descmatches = [i for i in re.findall('\<tr\>.*?\</tr\>',sourcecode,flags=re.DOTALL) if '>'+str(skillmaxlv) in i]
            for descmatch in descmatches:
                try:
                    skilleff2 = re.findall('\<td(.*)?\</td\>',descmatch,flags=re.DOTALL)[0].replace('\\n','\n')
                    skilleff = re.findall('^[^\>]*\>(.*)',skilleff2,flags=re.DOTALL)[0]
                    break
                except:
                    continue
            skill = Skill(image = skillimg,name = skillname, typ = skilltype, reqlv = skillreqlv, masterlv = skillmaxlv, desc = skilldesc,effect = skilleff,i = skillid)
            lines = list(filter(lambda x: x != '',skill.skillbox().split('\n')))
            replacementlines = [i + '\n' for i in lines]
        else:
            raise ValueError
    else:
        skillinfo = tuple([i.replace('\n','') for i in skilltuple])
        skillid = int(re.findall('[0-9]+',skillinfo[0])[0])
        templatename = re.findall('\{\{(.*)\}\}',skillinfo[1])[0]
        replacementlines = ['<!--'+str(skillid)+'-->\n','{{'+templatename+'2}}\n']
    return replacementlines

def replace_all_skills_in_page(sourcecode,writetarget = None):
    """
    Finds all skills in the page under the old skill table format and replaces them with the new skillboxes.

    v1: ignores all v skills.

    :param sourcecode (str): A single string that is the sourcecode of a wiki page, assumed to be under Fandom wiki markup format.
    :param writetarget (str): If specified, will write the new source code at the target location given here.
    
    return: A string that is another source code.
    """
    result = sourcecode

    text = [i+'\n' for i in result.split('\n')]
    if text[len(text)-1] == '\n':
        text.pop()

    starts = [i for i, x in enumerate(text) if (x == "{{Skill Table Styling}}\n") or len(re.findall('^\{\|',x)) > 0]
    ends = [i for i, x in enumerate(text) if x == "|}\n"]

    for a,b in list(zip(starts,ends)):
        err = 0
        print(a,b)
        targetstring = ''.join(text[slice(a,b+1)])
        fragment = text[slice(a,b+1)]
        replacementstring = ''
        skillindex = [i for i,x in enumerate(fragment) if re.search('\|-[0-9]*',x)]
        skillindex.append(len(fragment)-1)
        skills = [[i for i in fragment[slice(skillindex[j],skillindex[j+1])]] for j in range(len(skillindex)-1)]
        skillboxes = []
        for skilltuple in skills:
            try:
                replacementlines = replace_skill(skilltuple) 
            except ValueError:
                err = 1
                break
            skillboxes.extend(replacementlines)
        if err:
            continue
        replacementstring = replacementstring.join(skillboxes)
        result = result.replace(targetstring,replacementstring)
    
    if writetarget:
        with open(writetarget,'w+',encoding="utf8") as file:
            file.write(result)
    return(result)