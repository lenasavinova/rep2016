import urllib.request, re

def download_page(path):
    page = urllib.request.urlopen(path)
    raw = page.read().decode('utf-8')
    return raw

def get_text(raw):
    res = re.search('</h1>(.*?)p>(.*?)<div', raw, flags = re.DOTALL)
    raw_text = res.group(2)
    return raw_text

def cleaner(raw_text):
    cl1 = re.sub('<span(.*?)</span>', '', raw_text, flags = re.DOTALL)
    cl2 = re.sub('<.*?>', '', cl1, flags = re.DOTALL)
    cl3 = re.sub('&(.*?);', '', cl2, flags = re.DOTALL)
    cl4 = re.sub('([\w"]\.)(\w)', r'\1 \2', cl3, flags = re.DOTALL)
    text = re.sub('[\n\t]', '', cl4, flags = re.DOTALL)
    return text

def get_words(text):
    words = text.split(' ')
    a = []
    for el in words:
        el = el.strip('.,«»"?!:;')
        el = el.lower()
        if el != '' and el != '—':
            a.append(el)    
    return a
            
def common(texts):
    x1 = set(get_words(texts[0]))
    x2 = set(get_words(texts[1]))
    x3 = set(get_words(texts[2]))
    x4 = set(get_words(texts[3]))
    com = x1 & x2 & x3 & x4
    f = open('Общие словоформы для сюжета', 'a', encoding = 'utf-8')
    for el in sorted(com):
        f.write(el + '\n')
    f.close()
    
def unique(texts):
    x1 = set(get_words(texts[0]))
    x2 = set(get_words(texts[1]))
    x3 = set(get_words(texts[2]))
    x4 = set(get_words(texts[3]))
    uniq = (x1 | x2 | x3 | x4) - ((x1 & x2) | (x1 & x3) | (x1 & x4) | (x3 & x2) | (x4 & x2) | (x3 & x4))
    return uniq

def frequency(texts):
    d = {}
    for text in texts:
        for el in get_words(text):
            if el not in d:
                d[el] = 1
            else:
                d[el] += 1
    freq = set()
    for el in d:
        if d[el] > 1:
            freq.add(el)
    return freq

def check(uniq, freq):
    uni = uniq & freq
    f = open('Уникальные словоформы для заметок сюжета', 'a', encoding = 'utf-8')
    for el in sorted(uni):
        f.write(el + '\n')
    f.close()
                   
def main():
    links = ['http://www.m24.ru/articles/123718', 'http://www.metronews.ru/novosti/mjortvyj-poljak-ochnulsja-v-morge-i-pozhalovalsja-na-holod/Tpopla---1oHJs2UR5902m1pqGCzI1A/', 'http://izvestia.ru/news/648859', 'https://regnum.ru/news/accidents/2212408.html']
    texts = []
    for el in links:
        raw = download_page(el)
        raw_text = get_text(raw)
        text = cleaner(raw_text)
        texts.append(text)
    common(texts)
    uniq = unique(texts)
    freq = frequency(texts)
    check(uniq, freq)
    
main()
    
