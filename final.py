import flask
import telebot
import urllib.request as ur
import urllib.parse as prs
import re, html
import os

def first_page(raw):
    regexp = '<ul>(.*?)\[омонимия не снята\]'
    fragments = re.findall(regexp, raw, flags = re.DOTALL)
    examples = ''
    for ind,el in enumerate(fragments):
        el1 = re.sub('<br>', '\n', el)
        el2 = re.sub('   ?', ' ', el1)
        el3 = re.sub('<(.*?)>', '', el2)
        fragments[ind] = str(ind + 1) + '.\n' + html.unescape(el3) + '\n\n'
        examples += fragments[ind]
    return examples

def doc_token_num(raw):
    regexp = 'Найдено(.*?)>(.+?)<(.*?),(.*?)>(.+?)<'
    res = re.search(regexp, raw, flags = re.DOTALL)
    if res:
        doc_num = res.group(2)
        token_num = res.group(5)
        info = 'Найдено ' + str(doc_num) + ' документов, ' + str(token_num) + ' вхождений.\n\nВот первые несколько примеров:'
    else:
        info = 'По этому запросу ничего не найдено.'
    return info

def get_output(raw):
    info = doc_token_num(raw)
    if 'документов' in info:
        examples = first_page(raw)
        output = info + '\n\n' + examples
    else:
        output = info
    return output
    

def exact_form(req):
    url = 'http://search2.ruscorpora.ru/search.xml?env=alpha&mycorp=&mysent=&mysize=&mysentsize=&mydocsize=&dpp=10&spp=50&sp'\
    'd=10&text=lexform&mode=accent&sort=gr_grsphere&ext=10&accent=1&req=' + str(req)
    page = ur.urlopen(url)
    raw = page.read().decode('cp1251')
    output = get_output(raw)
    return output

def lemma_params(word, params):
    url = 'http://search2.ruscorpora.ru/search.xml?env=alpha&mycorp=&mysent=&mysize=&mysentsize=&mydocsize=&dpp=10&spp=50&spd=10&te'\
    'xt=lexgramm&mode=accent&sort=gr_grsphere&ext=10&accent=1&parent1=0&level1=0&lex1=' + str(word) + '&gramm1=' + str(params) + '&se'\
    'm1=&flags1=&parent2=0&level2=0&min2=1&max2=1&lex2=&gramm2=&sem2=&flags2='
    page = ur.urlopen(url)
    raw = page.read().decode('cp1251')
    output = get_output(raw)
    return output

def lemma_params_check(req):
    word = req[0]
    word = prs.quote(word)
    if len(req) > 2:
        output = 'В этом запросе что-то не так, загляни в /help.\nВот подсказка:\n\n'\
        'Грамматические признаки разделяются только запятыми без пробелов (инструкции в /requestrules).\n'
    elif len(req) == 2:
        params = req[1]
        params = prs.quote(params)
        output = lemma_params(word, params)
    else:
        params = ''
        output = lemma_params(word, params)
    return output

def two_words_search(word1, params1, word2, params2):
    url = 'http://search2.ruscorpora.ru/search.xml?env=alpha&mycorp=&mysent=&mysize=&mysentsize=&mydocsize=&dpp=10&spp=50&sp'\
    'd=10&text=lexgramm&mode=accent&sort=gr_grsphere&ext=10&accent=1&parent1=0&level1=0&lex1=' + str(word1) + '&gra'\
    'mm1=' + str(params1) + '&sem1=&flags1=&parent2=0&level2=0&min2=1&max2=1&lex2=' + str(word2) + '&gramm2=' + str(params2) + '&sem'\
    '2=&flags2='
    page = ur.urlopen(url)
    raw = page.read().decode('cp1251')
    output = get_output(raw)
    return output

def two_words_check(req):
    if len(req) != 4:
         output = 'В этом запросе что-то не так, загляни в /help.\nВот подсказки:\n\n'\
        '1. Не забывай ставить 0 вместо грамматических признаков слова, если они не нужны.\n2. Грамматические признаки раздел'\
        'яются только запятыми без пробелов (инструкции в /requestrules).\n'
    else:
        word1 = prs.quote(req[0])
        word2 = prs.quote(req[2])
        params1 = req[1]
        params2 = req[3]
        if params1 != '0':
            params1 =  prs.quote(params1)
        else:
            params1 = ''
        if params2 != '0':
            params2 =  prs.quote(params2)
        else:
            params2 = ''
        output = two_words_search(word1, params1, word2, params2)
    return output 

TOKEN = os.environ["TOKEN"]

bot = telebot.TeleBot(TOKEN, threaded=False)

bot.remove_webhook()
bot.set_webhook(url="https://accentcorpusbot.herokuapp.com/bot")

app = flask.Flask(__name__)

@bot.message_handler(commands=['start'])
def send_welcome(message):
	bot.send_message(message.chat.id, 'Привет! Я бот, который посылает запросы в акцентологический корпус НКРЯ и возвраща'\
    'ет результаты выдачи и первую страницу примеров. Чтобы узнать, какие запросы я понимаю, отправь /help.')

@bot.message_handler(commands=['help'])
def send_options(message):
	bot.send_message(message.chat.id, 'Я умею делать такие запросы:\n\n/exact - поиск по конкретной форме.\nПример 1: а\'мфора'\
                     '\nПример 2: на\' руку\n\n/lex'\
                    ' - поиск по одной лексеме или лексеме с указанными грамматическими признаками.\nПример 1: '\
                     'сильный\nПример 2: корова sg,gen'\
                    '\n\n/2lex - поиск по двум словам с указанными грамматическими признаками.\nПример: дом sg,nom отец sg,gen\n'\
                    'Если грамматические признаки слова не нужны, поставь вместо них 0.\nПример: дом 0 отец gen\n\n'\
                    'Все запросы пишутся через пробел после нужной команды.\n\n'
                    'Список грамматических признаков и инструкции по их написанию ищи по команде /requestrules.')

@bot.message_handler(commands=['exact'])
def get_form(message):
    raw_req = message.text
    req = raw_req.split()[1:]
    if req != []:
        req = ' '.join(req)
        req = prs.quote(req)
        output = exact_form(req)
    else:
        output = 'Чтобы я смог прочитать запрос, напиши его через пробел после команды.'
    bot.send_message(message.chat.id, output)
    
@bot.message_handler(commands=['lex'])
def get_word(message):
    raw_req = message.text
    req = raw_req.split()[1:]
    if req != []:
        output = lemma_params_check(req)
    else:
        output = 'Чтобы я смог прочитать запрос, напиши его через пробел после команды.'
    bot.send_message(message.chat.id, output)
    
@bot.message_handler(commands=['2lex'])
def get_words(message):
    raw_req = message.text
    req = raw_req.split()[1:]
    if req != []:
        output = two_words_check(req)
    else:
        output = 'Чтобы я смог прочитать запрос, напиши его через пробел после команды.'
    bot.send_message(message.chat.id, output)
    
@bot.message_handler(commands=['requestrules'])
def send_rules(message):
    f = open(r'request_rules.txt', 'r', encoding = 'utf-8')
    rules = f.read()
    bot.send_message(message.chat.id, rules)
    
@bot.message_handler(content_types=['text','document', 'audio', 'video', 'sticker', 'photo', 'voice'])
def req_get(message):
    bot.send_message(message.chat.id, 'Я умею работать только с командами, описанными в /help. Не забывай писать назва'\
                    'ние нужной команды перед запросом :)')

@app.route('/', methods=['GET', 'HEAD'])
def index():
    return 'ok'

@app.route("/bot", methods=['POST'])
def webhook():
    if flask.request.headers.get('content-type') == 'application/json':
        json_string = flask.request.get_data().decode('utf-8')
        update = telebot.types.Update.de_json(json_string)
        bot.process_new_updates([update])
        return ''
    else:
        flask.abort(403)

if __name__ == '__main__':
    import os
    app.debug = True
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)  
