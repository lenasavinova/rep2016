import time, re, os, urllib.request, html, shutil
def get_text(raw):
    res = re.search('</dl>(.+?)<div', raw, flags = re.DOTALL)
    if res:
        raw_text = res.group(1)
        check = re.search('[а-яёА-ЯЁ]{3,}', raw_text, flags = re.DOTALL)
        if check == None:
            res1 = re.search('</dl>(.+?)</p>', raw, flags = re.DOTALL)
            if res1:
                raw_text = res1.group(1)
            else:
                raw_text = 'no text'
    else:
        raw_text = 'no text'
    return raw_text

def cleaner(raw_text):
    cl = re.sub('[\n\t]+', '', raw_text, flags = re.DOTALL)
    cl1 = re.sub('(</p>|<br />)', '\n', cl, flags = re.DOTALL)
    cl2 = re.sub('<.*?>', '', cl1, flags = re.DOTALL)
    cl3 = html.unescape(cl2)
    text = re.sub('([а-яё])-([а-яё])', r'\1\2', cl3, flags = re.DOTALL) #здесь происходит чистка знаков переноса, потому что они портят разбор майстема (конечно, оба варианта, и с чисткой и без чистки, неидеальны и у каждого есть издержки, но, кажется, больше издержек в уродском майстеме с переносами)
    return text

def date_find(raw):
    res = re.search('Опубликовано (\d{2}\.\d{2}\.\d{4})', raw)
    if res:
        date_full = res.group(1)
    else:
        date_full = 'No date'
    return date_full

def title_find(raw):
    res = re.search('<h2>(.+?)</h2>', raw, flags = re.DOTALL)
    if res:
        title = res.group(1)
        title = re.sub('[\n\t]+', '', title)
    else:
        titlle = 'No title'
    return title

def formystem(i, text):
    f = open(r'D:\\susaninskaya_nov\\for_mystem\\' + str(i) + '.txt', 'w', encoding = 'utf-8')
    f.write(text)
    
def dirs(year, month, i, title, date_full, pageUrl, text):
    if not os.path.exists(r'D:\\susaninskaya_nov\\plain\\' + year + os.sep + month):
        os.makedirs(r'D:\\susaninskaya_nov\\plain\\' + year + os.sep + month)
    f = open(r'D:\\susaninskaya_nov\\plain\\' + year + os.sep + month + os.sep + str(i) + '.txt', 'w', encoding = 'utf-8')
    f.write('@au Noname\n' +'@ti ' + title + '\n'  + '@da ' + date_full + '\n' + '@topic Nocategory' + '\n' + '@url ' + pageUrl + '\n' + text)
    f.close()
    
def meta_data(path, title, date_full, pageUrl, year):
    row = '%s\tNo author\t\t\t%s\t%s\tпублицистика\t\t\tNo category\t\tнейтральный\tн-возраст\tн-уровень\tрайонная\t%s\tСусанинская новь\t\t%s\tгазета\tРоссия\tКостромская область\tru'
    string = row % (path, title, date_full, pageUrl, year)
    f = open(r'D:\\susaninskaya_nov\\metadata.csv', 'a', encoding = 'utf-8')
    f.write(string + '\n')
    f.close()
    
def mystem_txt(year, month, i):
    if not os.path.exists(r'D:\\susaninskaya_nov\\mystem-plain\\' + year + os.sep + month):
        os.makedirs(r'D:\\susaninskaya_nov\\mystem-plain\\' + year + os.sep + month)
    os.system(r'D:\\mystem.exe -cid ' + 'D:\\susaninskaya_nov\\for_mystem\\' + str(i) + '.txt' + ' D:\\susaninskaya_nov\\mystem-plain\\' + year + os.sep + month + os.sep + str(i) + '.txt')
    
def mystem_xml(year, month, i):
    if not os.path.exists(r'D:\\susaninskaya_nov\\mystem-xml\\' + year + os.sep + month):
        os.makedirs(r'D:\\susaninskaya_nov\\mystem-xml\\' + year + os.sep + month)
    os.system(r'D:\\mystem.exe -cid --format xml ' + 'D:\\susaninskaya_nov\\for_mystem\\' + str(i) + '.txt' + ' D:\\susaninskaya_nov\\mystem-xml\\' + year + os.sep + month + os.sep + str(i) + '.xml')
        
def download_page(pageUrl):
    time.sleep(2)
    try:
        page = urllib.request.urlopen(pageUrl)
        raw = page.read().decode('utf-8')
    except:
        print('Error at', pageUrl)
        raw = 'no page'
    return raw

def main():
    commonUrl = 'http://susnov.ru/chitat-gazetu/'
    if not os.path.exists(r'D:\\susaninskaya_nov\\for_mystem'):
        os.makedirs(r'D:\\susaninskaya_nov\\for_mystem')
    for i in range(149, 4123):
        pageUrl = commonUrl + str(i)
        raw = download_page(pageUrl)
        if raw != 'no page':
            raw_text = get_text(raw)
        else:
            continue
        if raw_text != 'no text':
            text = cleaner(raw_text)
        else:
            continue
        if text != '':
            title = title_find(raw)
            date_full = date_find(raw)
        else:
            continue
        if date_full != 'No date':
            month = date_full[3:5:1]
            year = date_full[6:]
            formystem(i, text)
            mystem_txt(year, month, i)
            mystem_xml(year, month, i)
            dirs(year, month, i, title, date_full, pageUrl, text)
            path = 'D:\\susaninskaya_nov\\plain\\' + year + '\\' + month + '\\' + str(i) + '.txt'
            meta_data(path, title, date_full, pageUrl, year)
        else:
            continue
    shutil.rmtree(r'D:\\susaninskaya_nov\\for_mystem')
main() 
                   

        
        
        
        
        
        



   
