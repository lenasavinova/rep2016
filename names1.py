from flask import Flask
from flask import render_template, request
import json

def dictsimple(path):
    f = open(path, 'r', encoding = 'utf-8')
    d = {'Ася':[],'Леся':[],'Жора':[],'Гоша':[],'Дуся':[],'Тима':[],'Дуня':[],'Маруся':[],'Гера':[],'Гриша':[]}
    for line in f:
        line1 = line.replace('\n', '')
        line3 = line1.split('\t')
        d['Ася'].append(line3[0].capitalize())
        d['Леся'].append(line3[1].capitalize())
        d['Жора'].append(line3[2].capitalize())
        d['Гоша'].append(line3[3].capitalize())
        d['Дуся'].append(line3[4].capitalize())
        d['Тима'].append(line3[5].capitalize())
        d['Дуня'].append(line3[6].capitalize())
        d['Маруся'].append(line3[7].capitalize())
        d['Гера'].append(line3[8].capitalize())
        d['Гриша'].append(line3[9].capitalize())
    f.close()
    return d

def dictfreq(d):
    new = {}
    for key in d:
        a = []
        d1 = {}
        for el in d[key]:
            if el != '':
                if el in d1:
                    d1[el] += 1
                else:
                    d1[el] = 1
            else:
                continue
        a.append(d1)
        new[key] = a
    return new

app = Flask(__name__)

@app.route('/')
def form():
    global d
    global new
    if request.args:
        s = request.args['name1'] + '\t' + request.args['name2'] + '\t' + request.args['name3'] + '\t' + request.args['name4'] + '\t' + request.args['name5'] + '\t' + \
            request.args['name6'] + '\t' + request.args['name7'] + '\t' + request.args['name8'] + '\t' + request.args['name9'] + '\t' + request.args['name10'] + '\n'
        f = open(r'D:\\name_contraction\\data.txt', 'a', encoding = 'utf-8')
        f.write(s)
        f.close()
        d = dictsimple(r'D:\\name_contraction\\data.txt')
        new = dictfreq(d)
        return render_template('after.html')
    else:
        return render_template('mainform.html')
    

@app.route('/json/')
def jsond():
    global d
    s = json.dumps(d, sort_keys = True, indent = 4, separators = (',', ': '), ensure_ascii = False)
    return render_template('json.html', js = s)

@app.route('/stats/')
def stats():
    global new
    return render_template('stats.html', dicti = new)

@app.route('/search/')
def search():
    return render_template('search.html')
    
@app.route('/results/')
def res():
    global new
    if request.args:
        for key in new:
            if key == request.args['namesh']:
                name = str(key)
                res = new[key]
            else:
                continue
        return render_template('results.html', name = name, res = res)
    else:
        return render_template('search.html')

    
if __name__ == '__main__':
    app.run()
