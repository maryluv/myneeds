# myneeds

##!!!!!!!!!!!!!!!!!!!!!!!!!!reshenie_nasti1
import re

def opentext(text):
    with open (text, 'r', encoding = 'utf-8') as t:
        text = t.read()
    return(text)
        
def anawords(text):
    t = opentext(text)
    nwords = re.findall(r'<w>', t)
    nana = re.findall(r'<ana', t)
    k = len(nana)/len(nwords)
    print('Среднее количество разборов на слово =', str(k), '.')

def dictionary(text):
    t = opentext(text)
    d = {}
    part = 'gr="(\w+)'
    strings = t.split('\n')
    for s in strings:
        sd = {}
        for i in re.findall(part, s):
            sd[i] = ''
        for key in sd:
            if key not in d:
                d[key] = '1'
            else:
                d[key] = str(int(d[key]) + 1)
    return(d)

def makefreq(text):
    d = dictionary(text)
    with open ('freqtext.txt', 'w', encoding = 'utf-8') as f:
        for key in d:
            f.write('{}\t{}\n'.format(key, d[key]))

def SIns(text):
    t = opentext(text)
    strings = re.findall('<w>(.*?)</w>', t) 
    reg = '<.*=ins.*>'
    com = '(\w+)<'
    cont = []
    words = []
    for s in range(len(strings)):
        if re.search(reg, strings[s]):
            word = strings[s-3]+strings[s-2]+strings[s-1]+strings[s]+strings[s+1]+strings[s+2]+strings[s+3]
            cont.append(word)
    for i in cont:
        three = ''
        for j in re.findall(com, i):
            three = three+j+' '
        words.append(three)
    return words

def makeins(text):
    words = SIns(text)
    with open ('ins.txt', 'w', encoding = 'utf-8') as f:
        for w in words:
            seven = w.split()
            f.write(seven[0]+' '+seven[1]+' '+seven[2]+'\t'+seven[3]+'\t'+seven[4]+' '+seven[5]+' '+seven[6]+'\n')
    
def main():
    anawords('text.xml')
    makefreq('text.xml')
    makeins('text.xml')

if __name__ == '__main__':
    main()
    
##!!!!!!!!!!!!!!!!!!!!!reshenie_nasti2
import re

def open_xml():
    ##читать по строкам
    with open('text.xml', 'r', encoding = 'utf-8') as f:
        text = f.readlines()
    return text


def open_xml_as_string():
    ##читать в одну строку
    with open('text.xml', 'r', encoding = 'utf-8') as f:
        text = f.read()
    return text


def write(string, filename):
    ##записать строку куда-нибудь
    with open(filename, 'w', encoding = 'utf-8') as f:
        f.write(string)


def count_ana_word(line_arr):
    ## считает число разборов на число словоформ
    n_arr = []
    for line in line_arr:
        if '<w' in line:
            num = len(re.findall('<ana ', line))
            n_arr.append(num)
    counter = sum(n_arr)/len(n_arr)
    return counter


def find_lex(text_str):
    ## Делает словарь типа "Часть речи: число вхожджений"
    lex_arr = [i.group(1) for i in re.finditer(r'gr=\"(.*?)(,|=)', text_str)]
    lex_d = {i: str(lex_arr.count(i)) for i in lex_arr}
    return lex_d
        

def get_text(text_str):
    ##убирает из текста все теги и переносы строк, возвращает массив слов с сохраненным регистром и знаками препинания
    text = re.sub('<.*?>', '', text_str)
    text = re.sub('\n', '', text)
    text_arr = text.split(' ')
    return text_arr


def find_ins(text_lines):
    ## находит в тексте слова которых есть разборы с творительным падежом и складывает их в массив
    words_ins = []
    for line in text_lines:
        if '=ins' in line:
            word = re.match('<w>(.*?)<', line).group(1)
            words_ins.append(word)
    return words_ins

def get_idx(words_ins, text_arr):
    text_arr_e = [i.strip('&.,?:"«»;!()') for i in text_arr] ##делает массив слов без знаков препинания
    idx_array = []
    for word in words_ins:
        for i in range(len(text_arr_e)):
            if text_arr_e[i] == word and i not in idx_array:
                idx_array.append(i)
    return idx_array

def make_string(idx_arr, text_arr):
    line_arr = []
    ## возвращает массив строк, как в задании
    for i in idx_arr:
        left_context = [] ## делаю по отдельности левый и правый контекст
        for l in range(i-3, i):
            if l >= 0:
                left_context.append(text_arr[l])
        right_context = []
        for l in range(i+1, i+4):
            if l <= len(text_arr):
                right_context.append(text_arr[l])
        line = ' '.join(left_context)+'\t'+text_arr[i]+'\t'+' '.join(right_context)
        line_arr.append(line)
    return line_arr

def main():
    ## Задание 1
    n = (count_ana_word(open_xml()))
    print(n)
    ## Задание 2
    gr_dict = find_lex(open_xml_as_string())
    array = [i+'\t'+gr_dict[i] for i in gr_dict.keys()]
    write('\n'.join(array), 'frq_gr.txt')
    ## Задание 3
    text_arr = get_text(open_xml_as_string())
    idx_arr = get_idx(find_ins(open_xml()), text_arr)
    line_arr = make_string(idx_arr, text_arr)
    with open('words_ins.txt', 'w', encoding='utf-8') as f:
        for line in line_arr:
            f.write(line+'\n')
    print('Я сделаль!')


if __name__ == '__main__':
    main()

##!!!!!!!!!!!!!!!!!!!!!!!!!!reshenie_mashi
import re
part_of_sp = 'gr=\w{,10},'
def preprocessing(text): # функция предобработки текста
    text_no_n = re.sub ('[\n]', '', text)
    words = text_no_n.split('<w>')
    return words

def gettext():
    with open('text.xml', 'r', encoding='utf-8') as f:
        words = preprocessing(f.read())
        words = words [1:len(words)]
    return words

def anacount(text):
    words_new = []  #массив слов без 1-го корявого элемента
    ana_count = []  #массив количеств ana для каждого слова
    anas = 0        #сумма ana
    ana_per_word = 0 # среднее кол-во ana
    for word in words:
        if word.find('<ana') != -1:
            words_new.append(word)
    for word in words_new:
        ana_count.append(word.count('<ana'))
    for n in ana_count:
        anas += n
    ana_per_word = anas/len(ana_count)

def partsofsp():
    words = gettext()
    parts = []
    for word in words:
        parts.append(re.findall (r'gr="\w+[,=]',word))      
    return parts

def countparts():
    parts = partsofsp()
    parts_for_count = [ re.sub('gr="|=|,','',part[0]) for part in parts ]
    list_of_parts = []
    for n in parts_for_count:
        if list_of_parts.count(n) == 0:
            list_of_parts.append(n)       
    countparts = { part: parts_for_count.count(part) for part in list_of_parts}
    template = '{}\t{}'
    for part in countparts:
        print (template.format(part, countparts[part]))

def justwords():
    words = gettext() 
    just_words = [word[:word.find('<')] for word in words ]
    return just_words

def word_dict():
    just_words = justwords()
    words = gettext()
    w_dict = { word[:word.find('<')] : re.findall('gr="\S+"', word) for word in words}
    template = '{} {} {}\t{}\t{} {} {}'
    for word in w_dict:
       if re.search('gr="S,', str(w_dict[word])) != None:
           if re.search('=ins,', str(w_dict[word])) != None:
               print (template.format(just_words[just_words.index(word)-3],just_words[just_words.index(word)-2],just_words[just_words.index(word)-1],word,just_words[just_words.index(word)+1],just_words[just_words.index(word)+2], just_words[just_words.index(word)+3]))
               
            


word_dict()
