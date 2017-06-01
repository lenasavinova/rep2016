import flask
import telebot
import conf
import re
import random
from pymorphy2 import MorphAnalyzer
morph = MorphAnalyzer()

def dict_maker():
    f = open(r'/home/savinovalena/mysite/wordsforbot.txt', 'r', encoding = 'utf-8')
    d = {}
    for line in f:
        wordraw = line.split('\t')[1].strip('\n')
        an = morph.parse(wordraw)[0]
        char = str(an.tag).split(' ')[0]
        if len(str(an.tag).split(' ')) < 2:
            lemma = str(an.word)
        else:
            lemma = str(an.normal_form)
        if char not in d:
            d[char] = [lemma]
        else:
            if lemma not in d[char]:
                d[char].append(lemma)
    f.close()
    return d

def inflct(char, infl, d, output):
    for el in d:
        if el == char:
            new_word = random.choice(d[el])
            ana_for_word = morph.parse(new_word)[0]
            new_word_raw = ana_for_word.inflect(infl)
            if new_word_raw != None:
                output = str(new_word_raw.word)
            else:
                continue
        else:
            continue
    return output

def not_inflct(char, d, output):
    if char not in ['UNKN', 'LATN', 'PNCT', 'NUMB,intg', 'NUMB,real', 'CONJ', 'PREP', 'PRCL']:
        for el in d:
            if el == char:
                output = random.choice(d[el])
            else:
                continue
    return output

def pnct(orig_word, output):
    res_r = re.search('([!,:.?*)}";]+$)', orig_word)
    res_l = re.search('(^[(*{"#]+)', orig_word)
    if res_l:
        pnc_l = res_l.group(1)
        output = pnc_l + output
    if res_r:
        pnc_r = res_r.group(1)
        output = output + pnc_r
    return output

d = dict_maker()

WEBHOOK_URL_BASE = "https://{}:{}".format(conf.WEBHOOK_HOST, conf.WEBHOOK_PORT)
WEBHOOK_URL_PATH = "/{}/".format(conf.TOKEN2)

bot = telebot.TeleBot(conf.TOKEN2, threaded=False)

bot.remove_webhook()
bot.set_webhook(url=WEBHOOK_URL_BASE+WEBHOOK_URL_PATH)

app = flask.Flask(__name__)

@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
	bot.send_message(message.chat.id, 'Привет! Я бот, который генерирует сообщения в ответ на твои фразы. Пиши все, что хочешь - '                     'я знаю, что ответить)')

@bot.message_handler(content_types=['document', 'audio', 'video', 'sticker', 'photo', 'voice'])
def send_mistake(message):
	bot.send_message(message.chat.id, 'Ой, что-то непонятное. Я умею отвечать только на текстовые сообщения:(')

@bot.message_handler(func=lambda m: True)
def random_phrase(message):
    mes = message.text
    orig_words = mes.split()
    for ind,orig_word in enumerate(orig_words):
        orig = orig_word.strip('!,:.?*#^"@)(}{][;')
        first = morph.parse(orig)[0]
        char = str(first.tag).split(' ')[0]
        try:
            infl = set(str(first.tag).split(' ')[1].split(','))
            orig_words[ind] = inflct(char, infl, d, orig)
        except:
            orig_words[ind] = not_inflct(char, d, orig)
        orig_words[ind] = pnct(orig_word, orig_words[ind])
    reply = ' '.join(orig_words).capitalize()
    bot.send_message(message.chat.id, reply)

@app.route('/', methods=['GET', 'HEAD'])
def index():
    return 'ok'

@app.route(WEBHOOK_URL_PATH, methods=['POST'])
def webhook():
    if flask.request.headers.get('content-type') == 'application/json':
        json_string = flask.request.get_data().decode('utf-8')
        update = telebot.types.Update.de_json(json_string)
        bot.process_new_updates([update])
        return ''
    else:
        flask.abort(403)

