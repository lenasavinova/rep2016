import re, os, sys
from flask import Flask, render_template, request

def get_words(path, new_path):
    f = open(path, 'r', encoding = 'utf-8')
    text = f.read()
    f.close()
    words = text.split(' ')
    for word in words:
        word = word.strip('\n')
        if word != '-':
            fl = open(new_path, 'a', encoding = 'utf-8')
            fl.write(word + '\n')
            fl.close()
            

def word_lemma(path):
    f = open(path, 'r', encoding = 'utf-8')
    arr = f.readlines()
    f.close()
    x = set()
    for line in arr:
        res = re.search('(.+?){', line)
        tok = res.group(1)
        resl = re.search('{(.+?)=', line)
        lemma = resl.group(1)
        elem = tok.lower() + ':' + lemma
        x.add(elem)
    return x
    
def code1(x, path):
    i = 0
    for el in sorted(x):
        res = re.search('(.+?):', el)
        tok = res.group(1)
        resl = re.search(':(.+)', el)
        lemma = resl.group(1)
        f = open(path, 'a', encoding = 'utf-8')
        f.write('INSERT INTO lemmas(id, word, lemma) values("' + str(i) + '", "' + tok + '", "' + lemma + '");\n')
        f.close()
        i += 1    

def code2(path1, path2):
    f = open(path1, 'r', encoding = 'utf-8')
    arr = f.readlines()
    f.close()
    f1 = open(path2, 'r', encoding = 'utf-8')
    text = f1.readlines()
    f1.close()
    for ind,line in enumerate(arr):
        resl = re.search('^(\W+?)\w', line)
        if resl:
            if resl.group(1) == '"':
                punct_l = '«'
            else:
                punct_l = resl.group(1)        
        else:
            punct_l = ''
        resr = re.search('(\W+?)\n', line)
        if resr:
            if '"' in resr.group(1):
                punct_r = resr.group(1).replace('"', '»')
            else:
                punct_r = resr.group(1)
        else:
            punct_r = ''
        word = arr[ind].strip('\n"!.:;,()?')
        st = '"(\d+)", "' + word.lower()+ '"'
        for el in text:
            res = re.search(st, el)
            if res:
                lemm_id = res.group(1)
                f1 = open(path2, 'a', encoding = 'utf-8')
                f1.write('INSERT INTO fulltext(id, word_token, punct_left, punct_right, posit_in_text, lemma_id) values("' + str(ind) + '", "' + word + '", "' + punct_l + '", "' + punct_r + '", "' + str(ind + 1) + '", "' + lemm_id + '");\n')
                f1.close()
                break

def main():
    if not os.path.exists(r'D:\\datab\\words_for_db.txt'):
        get_words(r'dary_volhvov.txt', r'words_for_db.txt')
        os.system(r'D:\\mystem.exe -nid ' + 'D:\\datab\\words_for_db.txt' + ' D:\\datab\\words_with_lemmas.txt') 
        x = word_lemma(r'words_with_lemmas.txt')
        code1(x, r'code.txt')
        code2(r'words_for_db.txt', r'code.txt')
       
main()

app = Flask(__name__)
        
@app.route('/')
def page_main():
    if request.args:
        f = open(r'D:\\datab\\forapp\\raw_input.txt', 'w', encoding = 'utf-8')
        f.write(request.args['rawtext'])
        f.close()
        get_words(r'D:\\datab\\forapp\\raw_input.txt', r'D:\\datab\\forapp\\raw_words.txt')
        os.system(r'D:\\mystem.exe -nid ' + 'D:\\datab\\forapp\\raw_words.txt' + ' D:\\datab\\forapp\\words_and_lemmas.txt') 
        y = word_lemma(r'D:\\datab\\forapp\\words_and_lemmas.txt')
        if not os.path.exists(r'D:\\datab\\forapp\\' + request.args['filename'] + '.txt'):
            code1(y, r'D:\\datab\\forapp\\' + request.args['filename'] + '.txt')
            code2(r'D:\\datab\\forapp\\raw_words.txt', r'D:\\datab\\forapp\\' + request.args['filename'] + '.txt')
        return render_template('result.html', path = 'D:\\datab\\forapp\\' + request.args['filename'] + '.txt')
    else:
        return render_template('main.html')

if __name__ == '__main__':    
    app.run()
    


    

