import re, os
def words():
    f = open('page.txt', 'r', encoding = 'utf-8')
    text = f.read()
    f.close()
    text1 = re.sub('<.*?>', '', text, flags = re.DOTALL)
    text2 = re.sub('[{(].*?[})]', '', text1, flags = re.DOTALL)
    text3 = re.sub('[\n\t]+', '', text2, flags = re.DOTALL)
    text4 = re.sub('(&#(?:\d)+|\d+)', '', text3, flags = re.DOTALL)
    words = text4.split(' ')
    x = set()
    for el in words:
        el = el.strip(',.?!\/"«» ()')
        el = el.lower()
        if el != '':
            x.add(el)
    return x
def inters(x):
    f = open('adyg.txt', 'r', encoding = 'utf-8')
    text = f.read()
    f.close()
    text1 = text.split('\n')
    a = set(text1)
    inf = x & a   
    f1 = open('wordlist.txt', 'a', encoding = 'utf-8')
    for el in inf:
        f1.write(el + '\n')
    f1.close()

    
def analyses():
    os.system(r'C:\\Users\\student\\Desktop\\mystem.exe -ni ' + 'C:\\Users\\student\\Desktop\\exam\\adyg.txt' + ' C:\\Users\\student\\Desktop\\exam\\formystem.txt')
    
def ruswords():
    f = open('adyg.txt', 'r', encoding = 'utf-8')
    text = f.read()
    f.close()
    text1 = text.split('\n')
    a = set(text1)
    f1 = open('formystem.txt', 'r', encoding = 'utf-8')
    b = set()
    for line in f1:
        res = re.search('[^?]=S.*?(неод|од)=им,ед', line)
        if res:
            res1 = re.search('(.+?)[{]', line)
            word = res1.group(1)
            b.add(word)
    f1.close()
    result = a & b
    f2 = open('rusnouns.txt', 'a', encoding = 'utf-8')
    for el in result:
        f2.write(el + '\n')
    f2.close()
def fordb():
    f1 = open('formystem.txt', 'r', encoding = 'utf-8')
    d = {}
    for line in f1:
        res = re.search('[^?]=S.*?(неод|од)=им,ед', line)
        if res:
            res1 = re.search('(.+?)[{]', line)
            word = res1.group(1)
            res2 = re.findall('[|{]([a-яё]+?)=S', line)
            d[word] = set(res2)
    f1.close()
    f2 = open('sql.txt', 'a', encoding = 'utf-8')
    for k in d:
        if len(d[k]) != 0:
            for el in d[k]:
                f2.write('INSERT INTO rus_words(wordform, lemma) values("' + k + '", "' + el + '");\n')
    f2.close()
        
                
                                
            
def main():
    inters(words())
    analyses()
    ruswords()
    fordb()

main()
