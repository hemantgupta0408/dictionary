from flask import Flask , render_template , request , redirect , flash
import json
import os

with open("config.json", 'r') as c:
    params = json.load(c)['params']

app = Flask(__name__)

app.secret_key = 'the-random-string'

@app.route('/')
def base():        
    return render_template('base.html',params=params)
    

@app.route('/index' , methods=['GET', 'POST'] ) 
def index(): 
    with open("config.json") as c:
        params = json.load(c)['params']
    text = request.form.get('word')
    if text in params:
        if request.method == 'POST':
            text = request.form.get('word')
            mean = params[text][0]
            uses = params[text][1]
            rword = params[text][2]  
    else:
        return ("Word dictionary mein nhi hai re bhawa....") 
    return render_template('index.html' , params=params , text=text , uses=uses , mean=mean , rword=rword)
    

@app.route('/add' , methods=['GET', 'POST'] )
def add():
    if request.method == 'POST':
        text = request.form.get('word')
        hword = request.form.get('hword')
        uses = request.form.get('use')
        rword = request.form.get('rword')
        with open("config.json", "r+") as f:
            data = json.load(f)
            data["params"][text] =[hword,uses,rword]
            data.update(data)
            f.seek(0)
            json.dump(data , f , indent=4 , sort_keys=True)
        flash("Word Added Successfully", "success")
    return render_template('add.html' , params = params )


@app.route('/edit/<string:text>' , methods=['GET' , 'POST'] )
def edit(text):
    filename = os.path.join('config.json')
    with open(filename) as c:
        params = json.load(c)['params']
        mean = params[text][0]
        usess = params[text][1]
        rwords = params[text][2]  
    if request.method == 'POST':
        text = request.form.get('word')
        hword = request.form.get('hword')
        uses = request.form.get('use')
        rword = request.form.get('rword')
        with open("config.json", "r+") as f:
            data = json.load(f)
            data['params'][text] =[hword,uses,rword]
            data.update(data)
            f.seek(0)
            f.truncate()
            json.dump(data , f , indent=4 , sort_keys=True)
        flash("Word Edit Successfully", "success")
        
    return render_template('edit.html' , params = params  , text=text , usess=usess , mean=mean , rwords=rwords)

@app.route('/delete/<string:text>' , methods=['GET' , 'POST'] )
def delete(text):
    filename = os.path.join('config.json')
    with open(filename, "r") as f:
        data = json.load(f)

    if text in data['params']:
        del data['params'][text]

    with open(filename, "w") as file:
        json.dump(data, file , indent=4 , sort_keys=True)
    flash("Word Delete Successfully", "success")   
    return redirect('/')
app.run( use_reloader=True,debug=True, port=5000 )