from flask import Flask, session, redirect, url_for, escape, request
from SQLFacade import SQLFacade

# flask initial
app = Flask(__name__)

# set the secret key.
app.secret_key = '\x11S>Bi\xf7\xd5}:\x90\r\xbb\xd7\x04\x91\x0e\xa6\x08o\xe6n8d\xf4'

@app.route('/')
def index():
    if 'username' in session:
        return 'Logged in as %s' % escape(session['username'])
    return 'You are not logged in'

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        sql = SQLFacade.get_singleton()
        data = dict()
        data['memberID'] = request.form['username']
        data['passwd'] = request.form['password']
        result = sql.find_member(data)
        if result:
            session['username'] = request.form['username']
        return redirect(url_for('index'))
    return '''
        <form action="" method="post">
            <p><input type=text name=username>
            <p><input type=password name=password>
            <p><input type=submit value=Login>
        </form>
    '''

@app.route('/logout')
def logout():
    # remove the username from the session if it's there
    session.pop('username', None)
    return redirect(url_for('index'))

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        sql = SQLFacade.get_singleton()
        data = dict()
        data['memberID'] = request.form['username']
        data['passwd'] = request.form['password']
        data['name'] = None
        data['address'] = None
        data['phone'] = None
        sql.create_member(data)
        return redirect(url_for('index'))
    return '''
        <form action="" method="post">
            <p><input type=text name=username>
            <p><input type=password name=password>
            <p><input type=submit value=register>
        </form>
    '''

@app.route('/order', methods=['GET', 'POST'])
def order():
    if 'username' not in session:
        return 'You are not logged in'

    if request.method == 'POST':

        return redirect(url_for('index'))
    else:
        return '''
        <form action="" method="post">
            <p><input type=text name=username>
            <p><input type=password name=password>
            <p><input type=submit value=register>
        </form>
        '''


if __name__ == "__main__":
    app.run(debug=True)