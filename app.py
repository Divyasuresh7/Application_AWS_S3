from flask import Flask, request, jsonify, render_template
# from ldap3 import Server, Connection, ALL

app = Flask(__name__)

# AD_SERVER = ''
# AD_PORT = 389  # The default LDAP port for AD is 389
# AD_BASE_DN = 'DC=orient,DC=com'  

# def validate_credentials(username, password):
#     try:
#         # Creating a connection to the Active Directory server
#         server = Server(AD_SERVER, port=AD_PORT, get_info=ALL)
#         conn = Connection(server, user=f"{username}@orient.com", password=password)

#         # Binding to the server to check the credentials
#         if conn.bind():
#             return True
#         else:
#             return False
#     except Exception as e:
#         print(f"An error occurred: {e}")
#         return False

VALID_USERNAME = 'Admin'
VALID_PASSWORD = 'Admin@123'

def validate_credentials(username, password):
    return username == VALID_USERNAME and password == VALID_PASSWORD

@app.route('/')
def index():
    return render_template('new.html')

@app.route('/login', methods=['POST'])
def login():
    data = request.form  # Get the form data submitted from login.html
    username = data.get('username')
    password = data.get('password')

    if username and password:
        if validate_credentials(username, password):
            return jsonify({'success': True})
        else:
            return jsonify({'success': False, 'message': 'Invalid credentials'})

    return jsonify({'success': False, 'message': 'Username and password are required'})


@app.route('/dashboard')
def dashboard():
    return render_template('dashboard.html')

if __name__ == '__main__':
    app.run(debug=True)

