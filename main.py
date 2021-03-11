from flask import Flask , render_template , request , redirect
import json

with open("config.json", 'r') as c:
    params = json.load(c)['params']

app = Flask(__name__)

@app.route('/')
def base():       
    return render_template('base.html',params=params)
    

@app.route('/index' , methods=['GET', 'POST'] ) 
def index(): 
    if request.method == 'POST':
        text = request.form.get('word')
        mean = params[text][0]
        uses = params[text][1]
        rword = params[text][2]
        print(text)     
    return render_template('index.html' , text=text , uses=uses , mean=mean , rword=rword)
    

@app.route('/add' , methods=['GET', 'POST'] )
def add():
    if request.method == 'POST':
        word = request.form.get('word')
        hword = request.form.get('hword')
        uses = request.form.get('use')
        rword = request.form.get('rword')
        with open("config.json", "r+") as f:
            data = json.load(f)
            data["params"][word] =[hword,uses,rword]
            data.update(data)
            f.seek(0)
            json.dump(data , f , indent=4 , sort_keys=True)
        with open("config.json", 'r') as f:
            data = json.load(f)["params"]
            data.update(data)
    return render_template('add.html' , params = params )

@app.route('/delete/<string:word>' , methods=['GET' , 'POST'] )
def delete(word):
    if request.method == 'POST':
        word =  request.form.get('word')
        with open('config.json') as data_file:
            data = json.load(data_file)
            data1 = json.dumps(data)
            for word in data1:
                del data1["params"][word]
    return redirect('/', word=word )
app.run(debug=True)