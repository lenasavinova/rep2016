
# coding: utf-8

# In[17]:

import requests
import json
import re, html
import matplotlib.pyplot as plt
 
def vk_api(method, **kwargs):
    api_request = 'https://api.vk.com/method/'+ method + '?'
    api_request += '&'.join(['{}={}'.format(key, kwargs[key]) for key in kwargs])
    return json.loads(requests.get(api_request).text)

def cleaner(text):
    text1 = re.sub('<.*>', '', text)
    text2 = re.sub(' ?http([0-9a-zA-Z/.\_=;:?-])*', '', text1)
    text3= re.sub('([\[\|\]]|\xad)', '', text2)
    text4 = re.sub('(id|club)[0-9]*', '', text3)
    text5 = re.sub('("?[.,)?!(:])("?[А-ЯЁA-Za-zа-яё])', r'\1 \2', text4)
    text6 = html.unescape(text5)
    return text6

def length(text):
    i = len(text.split(' '))
    return i

def write(d, path):
    f = open(path,'a', encoding = 'utf-8')
    for el in d:
        f.write(str(el) + ' : ' + str(d[el]) + '\n')
    f.close()
    
def write2(d, path):
    f = open(path,'a', encoding = 'utf-8')
    for key in d:
        for ind, com in enumerate(d[key]):
            f.write(str(key) + ' : ' + d[key][ind]+ '\n')
    f.close()
    

posts_ids = set()
offsets = [0,100]
d_posts = {}
posts = {}
for el in offsets:
    data = vk_api('wall.get', domain = 'voicekids', count = 100, offset = str(el))
    k = 1
    while k < len(data["response"]):
        posts_ids.add(data["response"][k]['id'])
        posts[data["response"][k]['id']] = cleaner(data["response"][k]['text'])
        if cleaner(data["response"][k]['text']) == '':
             d_posts[data["response"][k]['id']] == 0
        else:
            d_posts[data["response"][k]['id']] = length(cleaner(data["response"][k]['text']))
        k += 1
        
write(posts, r'C:\program_lena\voicekids_posts.txt') 



# In[5]:

d_comments = {}
id_com = {}
comments = {}
for el in posts_ids:
    d_comments[el] = []
    comments[el] = []
    for offs in offsets:
        data = vk_api('wall.getComments', owner_id=-55157869, post_id = str(el), count = 100, offset = str(offs))
        k = 1
        while k < len(data["response"]):
            comments[el].append(cleaner(data["response"][k]['text']))
            if cleaner(data["response"][k]['text']) == '':
                d_comments[el].append(0)
                if data["response"][k]['from_id'] in id_com:
                    id_com[data["response"][k]['from_id']].append(0)
                else:
                    id_com[data["response"][k]['from_id']] = [0]
            else:
                d_comments[el].append(length(cleaner(data["response"][k]['text'])))
                if data["response"][k]['from_id'] in id_com:
                    id_com[data["response"][k]['from_id']].append(length(cleaner(data["response"][k]['text'])))
                else:
                    id_com[data["response"][k]['from_id']] = [length(cleaner(data["response"][k]['text']))]
                
            k += 1
      


                


# In[8]:

write2(comments, r'C:\program_lena\voicekids_comments.txt')

id_city = {}
for el in id_com:
    user_info = vk_api('users.get', user_ids = el, fields = 'city')
    try:
        inf = user_info["response"][0]
        if 'city' in inf:
            id_city[el] = inf['city']    
        else:
            continue
    except:
        continue
         


# In[9]:

id_ages = {}
for el in id_com:
    user_info = vk_api('users.get', user_ids = el, fields = 'bdate')
    try:
        inf = user_info["response"][0]
        if 'bdate' in inf:
            res = re.search('\.([0-9]{4})', inf['bdate'])
            if res:
                id_ages[el] = 2017 - int(res.group(1))
            else:
                continue
        else:
            continue
    except:
        continue


# In[24]:

def dict_gen(d1, d2, d3):
    for el in d1:
        for ele in d2:
            if el == ele:
                if d2[ele] in d3:
                    d3[d2[ele]].append(d1[el])
                else:
                    d3[d2[ele]] = [d1[el]]
            else:
                continue
    return d3

def dict_mean(d1, d2):
    d2 = {el: round(sum(d1[el])/len(d1[el])) for el in d1}
    return d2

id_comlen = {}
id_comlen = dict_mean(id_com, id_comlen)


# In[25]:

post_comlen = {}
post_comlen = dict_mean(d_comments, post_comlen)


# In[26]:

city_comlen = {}
city_meanlen = {}
city_comlen = dict_gen(id_comlen, id_city, city_comlen)
city_meanlen = dict_mean(city_comlen, city_meanlen)
          


# In[27]:

age_comlen = {}
age_meanlen = {}
age_comlen = dict_gen(id_comlen, id_ages, age_comlen)
age_meanlen = dict_mean(age_comlen, age_meanlen)


# In[29]:

postlen_comlen = {}
postlen_meanlen = {}
postlen_comlen = dict_gen(post_comlen, d_posts, postlen_comlen)
postlen_meanlen = dict_mean(postlen_comlen, postlen_meanlen)


# In[30]:


cityname_meanlen = {}

for el in city_meanlen:
    data = vk_api('database.getCitiesById',  city_ids = str(el))
    if data['response'] != [] and data["response"][0]['name'] != '':
        cityname_meanlen[data["response"][0]['name']] = city_meanlen[el]
    else:
        continue



# In[83]:

import matplotlib
from matplotlib import rc
matplotlib.rcdefaults()
font = {'family': 'Courier New', 'weight': 'normal'} 
rc('font', **font)

def graf_citymost():
    citiesall = []
    comlenall = []
    for city in sorted(cityname_meanlen, key = cityname_meanlen.get, reverse = True):
        citiesall.append(city)
        comlenall.append(cityname_meanlen[city])
    cities = citiesall[1:51:1]
    comlen = comlenall[1:51:1]
    plt.bar(range(len(cities)), comlen)
    plt.title('Зависимость длины комментария от города')
    plt.ylabel('Средняя длина комментария в словах')
    plt.xlabel('Города')
    plt.xticks(range(len(cities)), cities, rotation=90)
    plt.tight_layout()
    plt.savefig('citiesmost.png')
    plt.show()


graf_citymost() #первые 50 городов с самой большой средней длиной комментов, всех городов больше 1000


# In[82]:

def graf_age():
    age = []
    comlen = []
    for el in age_meanlen:
        age.append(el)
        comlen.append(age_meanlen[el])
    plt.bar(range(len(age)), comlen)
    plt.title('Зависимость длины комментария от возраста')
    plt.ylabel('Средняя длина комментария в словах')
    plt.xlabel('Возраст пользователя (по данным ВК)')
    plt.xticks(range(len(age)), age, rotation=90)
    plt.tight_layout()
    plt.savefig('ages.png')
    plt.show()

graf_age()


# In[87]:

def graf_post():
    post = []
    comlen = []
    for el in postlen_meanlen:
        post.append(el)
        comlen.append(postlen_meanlen[el])
    plt.bar(range(len(post)), comlen)
    plt.title('Зависимость длины комментария от длины поста')
    plt.ylabel('Средняя длина комментария в словах')
    plt.xlabel('Средняя длина поста')
    plt.xticks(range(len(post)), post)
    plt.tight_layout()
    plt.savefig('posts.png')
    plt.show()
    
graf_post()


# In[ ]:



