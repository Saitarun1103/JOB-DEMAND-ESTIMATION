import pandas as pd 
import numpy as np

#=================flask code starts here
from flask import Flask, render_template, request, redirect, url_for, session,send_from_directory

app = Flask(__name__)
app.secret_key = 'welcome'

def manhattan_similarity(vec1, vec2):
    return sum(abs(v1 - v2) for v1, v2 in zip(vec1, vec2))

task_embed = np.load("model/task_link_mistral.npy")
dataset = pd.read_csv("Dataset/dataset.csv")
job_name = dataset['Title']

@app.route('/Predict', methods=['GET', 'POST'])
def predictView():
    return render_template('Predict.html', msg='')
 
@app.route('/index', methods=['GET', 'POST'])
def index():
    return render_template('index.html', msg='')

@app.route('/UserLogin', methods=['GET', 'POST'])
def UserLogin():
    return render_template('UserLogin.html', msg='')

@app.route('/UserLoginAction', methods=['GET', 'POST'])
def UserLoginAction():
    if request.method == 'POST' and 't1' in request.form and 't2' in request.form:
        user = request.form['t1']
        password = request.form['t2']
        if user == "admin" and password == "admin":
            return render_template('UserScreen.html', msg="<font size=3 color=blue>Welcome "+user+"</font>")
        else:
            return render_template('UserLogin.html', msg="<font size=3 color=red>Invalid login details</font>")

@app.route('/Logout')
def Logout():
    return render_template('index.html', msg='')

@app.route('/PredictAction', methods=['GET', 'POST'])
def PredictAction():
    if request.method == 'POST':
        global task_embed, job_name
        testData = pd.read_csv("Dataset/testData.csv")
        task = testData['task']
        index = testData['index']
        output = '<table border=1 align=center width=100%><tr>'
        output += '<th><font size="3" color="black">Task Description</font></th>'
        output += '<th><font size="3" color="blue">Predicted Job Demand</font></th>'
        output += '<th><font size="3" color="red">Manhattan Similarity</font></th></tr>'
        for i in range(len(index)):#loop all test description index
            similarity_score = 1000000
            match_job = ""
            for j in range(len(task_embed)):#loop all job task description 
                if j != index[i]:
                    similarity = manhattan_similarity(task_embed[j], task_embed[index[i]])#use extension similarity to find similarity
                    if similarity < similarity_score:#take job with highest similarity
                        similarity_score = similarity
                        match_job = job_name[j]
            output += "<tr>"
            output += '<td><font size="3" color="black">'+task[i]+'</font></td>'
            output += '<td><font size="4" color="blue">'+match_job+'</font></td>'  
            output += '<td><font size="4" color="red">'+str(round(similarity_score,2))+'</font></td></tr>'  
        output += "</table><br/><br/><br/><br/>"             
        return render_template('UserScreen.html', msg=output)

if __name__ == '__main__':
    app.run()    
