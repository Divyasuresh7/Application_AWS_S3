from flask import Flask, request, jsonify, render_template
import ldap3

app = Flask(__name__)

# Replace these values with your Active Directory server and domain details
# AD_SERVER = 'ldap://your_ad_server_address'
# AD_SERVER = 'ldap://OTMUMACKADC.orient.com'
AD_SERVER = 'ldap://OTMUMBDCPRD.orient.com/'
BASE_DN = 'OU=Users,DC=orient,DC=com'

def validate_credentials(username, password):
    try:
        conn = ldap3.Connection(
            AD_SERVER, user=f'{username}', password=password, auto_bind=True
        )
        conn.search(
            search_base=BASE_DN,
            search_filter=f'(sAMAccountName={username})',
            attributes=['cn'],
        )

        if conn.entries:
            # Authentication successful
            return True
        else:
            # Authentication failed
            return False
    except ldap3.core.exceptions.LDAPBindError:
        # Connection error or invalid credentials
        return False
    except Exception as e:
        print(f"An error occurred: {e}")
        return False

@app.route('/')
def index():
    return render_template('login.html')

@app.route('/login', methods=['GET','POST'])
def login():
    username = request.json.get('username')
    password = request.json.get('password')

    if username and password:
        if validate_credentials(username, password):
            return jsonify({'success': True})
        else:
            return jsonify({'success': False})

    return jsonify({'success': False})

@app.route('/dashboard', methods=['GET','POST'])
def dashboard():
    return render_template('dashboard.html')

if __name__ == '__main__':
    app.debug = True
    app.run()
