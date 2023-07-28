from flask import Flask, request, jsonify, render_template,session
import os
# from ldap3 import Server, Connection, ALL

app = Flask(__name__)
app.secret_key = 'your_secret_key_here'

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
    folders = get_upload_folders()
    return render_template('dashboard.html', folders=folders)

ALLOWED_EXTENSIONS = {'txt', 'csv', 'xlsx'}
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def get_upload_folders():
    UPLOAD_FOLDER = "C:/Users/Divya Suresh/GITHUB_UPLOAD_PROJECTS/UPLOAD"
    return [name for name in os.listdir(UPLOAD_FOLDER) if os.path.isdir(os.path.join(UPLOAD_FOLDER, name))]

@app.route('/upload', methods=['POST'])
def upload():
    if 'file' not in request.files:
        return jsonify({'message': 'No file part'}), 400

    file = request.files['file']

    if file.filename == '':
        return jsonify({'message': 'No selected file'}), 400

    if file and allowed_file(file.filename):
        selected_option = request.form.get('selected_option')

        folders = get_upload_folders()
        if not selected_option or selected_option not in folders:
            return jsonify({'message': 'Invalid selected option'}), 400

        UPLOAD_FOLDER = "C:/Users/Divya Suresh/GITHUB_UPLOAD_PROJECTS/UPLOAD"
        folder_path = os.path.join(UPLOAD_FOLDER, selected_option)
        os.makedirs(folder_path, exist_ok=True)

        file_path = os.path.join(folder_path, file.filename)
        file.save(file_path)

        return jsonify({'message': 'File uploaded successfully'}), 200
    else:
        return jsonify({'message': 'Invalid file format. Allowed formats are txt, csv, and xlsx.'}), 400
    
def get_upload_folders():
    UPLOAD_FOLDER = "C:/Users/Divya Suresh/GITHUB_UPLOAD_PROJECTS/UPLOAD"
    return [name for name in os.listdir(UPLOAD_FOLDER) if os.path.isdir(os.path.join(UPLOAD_FOLDER, name))]

if __name__ == '__main__':
    app.run(debug=True)