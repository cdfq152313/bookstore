from flask import Flask, session, redirect, url_for, escape, request, render_template
from SQLFacade import SQLFacade

# flask initial
app = Flask(__name__)

# set the secret key.
app.secret_key = '\x11S>Bi\xf7\xd5}:\x90\r\xbb\xd7\x04\x91\x0e\xa6\x08o\xe6n8d\xf4'

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        sql = SQLFacade()
        keyword = request.form['keyword']
        result = sql.find_book(keyword)
        if 'username' in session:
            return render_template('index.html',  name=session['username'], books=result)
        return render_template('index.html',  books=result)

    if 'username' in session:
        return render_template('index.html', name=session['username'])
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        sql = SQLFacade()
        data = dict()
        data['memberID'] = request.form['username']
        data['passwd'] = request.form['password']
        result = sql.find_member(data)
        if result:
            session['username'] = request.form['username']
        return redirect(url_for('index'))
    return render_template('login.html')

@app.route('/search')
def search():
    return 
#    return render_template('search.html')

@app.route('/logout')
def logout():
    # remove the username from the session if it's there
    session.pop('username', None)
    return redirect(url_for('index'))

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        sql = SQLFacade()
        data = dict()
        data['memberID'] = request.form['username']
        data['passwd'] = request.form['password']
        data['name'] = request.form['name']
        data['address'] = request.form['address']
        data['phone'] = request.form['phone']
        data['email'] = request.form['email']
        sql.create_member(data)
        return redirect(url_for('index'))
    return render_template('register.html')

@app.route('/order', methods=['GET', 'POST'])
def order():
    if 'username' not in session:
        return redirect(url_for('index'))

    if request.method == 'POST':
        return redirect(url_for('index'))
    else:
        return render_template('order.html')


if __name__ == "__main__":
    
    app.run(debug=True)
