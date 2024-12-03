from flask import Flask, render_template, request, jsonify, redirect, url_for
import pg8000

app = Flask(__name__, template_folder= 'src')

global db
global signedIn 
signedIn = False # Default


@app.route('/', methods=['GET', 'POST'])
def home():

    if request.method == 'POST':
        global signedIn
        global db
        username = request.form.get('username')
        password = request.form.get('password')
        try:
            db = pg8000.connect(user=username, password=password, host='codd.mines.edu', port=5433, database='csci403')
            signedIn = True
            return redirect(url_for('form'))
        except Exception as e: 
            signedIn = False
            return redirect(url_for('error'))
        
    return render_template('index.html')

@app.route('/form', methods=['GET', 'POST'])
def form():
    if(signedIn == False):
        return redirect(url_for('home'))
    if request.method == 'POST':
        return redirect(url_for(results))
    return render_template('form.html')

@app.route('/results', methods=['GET'])
def results():
    return render_template('results.html')

@app.route('/error')
def error():
    return render_template('error.html')

# Run the app
if __name__ == '__main__':
    app.run()
