from flask import Flask, render_template, request, redirect, flash, url_for
from flask_mysqldb import MySQL
from werkzeug.utils import secure_filename
from flask import send_from_directory
import os

app = Flask(__name__)

# MySQL 配置
app.config['MYSQL_HOST'] = '127.0.0.1'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = '1234'
app.config['MYSQL_DB'] = 'database_try'
app.secret_key = 'your_secret_key'

app.config['UPLOAD_FOLDER'] = 'uploads'  # 上传文件的存储目录
app.config['ALLOWED_EXTENSIONS'] = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}

if not os.path.exists(app.config['UPLOAD_FOLDER']):
    os.makedirs(app.config['UPLOAD_FOLDER'])

mysql = MySQL(app)

@app.route('/')
def home():
    return redirect(url_for('sign_in'))

@app.route('/create_room', methods=['GET', 'POST'])
def create_room():
    if request.method == 'POST':
        room_number = request.form['room_number'].strip()
        password = request.form['password'].strip()

        if room_number and password:
            # 检查房间号是否已经存在
            cur = mysql.connection.cursor()
            cur.execute("SELECT * FROM rooms WHERE room_number = %s", (room_number,))
            existing_room = cur.fetchone()

            if existing_room:
                flash('This room number already exists. Please choose another one.', 'error')
            else:
                try:
                    cur.execute("INSERT INTO rooms (room_number, password) VALUES (%s, %s)", (room_number, password))
                    mysql.connection.commit()
                    flash('Room created successfully!', 'success')
                    return redirect('/create_room?success=1')
                except Exception as e:
                    flash(f'Error: {str(e)}', 'error')
                finally:
                    cur.close()
        else:
            flash('Room number and password cannot be empty!', 'error')

        return redirect('/create_room')  # 重定向回创建房间页面

    return render_template('create_room.html')

@app.route('/sign_in', methods=['GET', 'POST'])
def sign_in():
    if request.method == 'POST':
        room_number = request.form['room_number'].strip()
        password = request.form['password'].strip()

        cur = mysql.connection.cursor()
        cur.execute("SELECT * FROM rooms WHERE room_number = %s AND password = %s", (room_number, password))
        room = cur.fetchone()
        cur.close()

        if room:
            print("Login successful!")
            return redirect(url_for('content', room_number=room_number))
        else:
            print("Invalid room number or password!")
            flash('Invalid room number or password!', 'error')

    return render_template('sign_in.html')

@app.route('/content/<room_number>', methods=['GET', 'POST'])
def content(room_number):
    if request.method == 'POST':
        content = request.form['content'].strip()
        if content:
            cur = mysql.connection.cursor()
            cur.execute("INSERT INTO notes(content, room_number) VALUES (%s, %s)", (content, room_number))
            mysql.connection.commit()
            cur.close()
            flash('Note added successfully!', 'success')
        else:
            flash('Note cannot be empty!', 'error')

        # 重定向到当前房间的内容页面
        return redirect(f'/content/{room_number}')

    cur = mysql.connection.cursor()
    cur.execute("SELECT content, id FROM notes WHERE room_number = %s", (room_number,))
    results = cur.fetchall()

    # 查询已上传的文件
    cur.execute("SELECT filename FROM uploaded_files WHERE room_number = %s", (room_number,))
    uploaded_files = cur.fetchall()

    cur.close()
    return render_template('content.html', notes=results, uploaded_files=uploaded_files, room_number=room_number)

@app.route('/delete_note/<int:note_id>/<room_number>', methods=['POST'])
def delete_note(note_id, room_number):
    cur = mysql.connection.cursor()
    cur.execute("DELETE FROM notes WHERE id = %s AND room_number = %s", (note_id, room_number))
    mysql.connection.commit()
    cur.close()
    return redirect(f'/content/{room_number}')  # 重定向到相应房间的联系页面

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']

@app.route('/upload/<room_number>', methods=['POST'])
def upload_file(room_number):
    if 'file' not in request.files:
        flash('No file part', 'error')
        return redirect(request.url)

    file = request.files['file']
    
    if file.filename == '':
        flash('No selected file', 'error')
        return redirect(request.url)

    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

        # 将文件信息存储到数据库
        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO uploaded_files (filename, room_number) VALUES (%s, %s)", (filename, room_number))
        mysql.connection.commit()
        cur.close()

        flash('File uploaded successfully!', 'success')
        return redirect(url_for('content', room_number=room_number))
    
    flash('File type not allowed', 'error')
    return redirect(request.url)

@app.route('/uploads/<filename>', methods=['GET'])
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

def get_uploaded_files(room_number):
    cur = mysql.connection.cursor()
    cur.execute("SELECT filename FROM uploaded_files WHERE room_number = %s", (room_number,))
    uploaded_files = cur.fetchall()
    cur.close()
    return uploaded_files

@app.route('/delete_file/<filename>/<room_number>', methods=['POST'])
def delete_file(filename, room_number):
    # 删除文件
    file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    print(f"Attempting to delete file at: {file_path}")  # 打印文件路径
    try:
        # 检查文件是否存在
        if os.path.exists(file_path):
            os.remove(file_path)
            print("File deleted successfully.")
        else:
            flash('File not found!', 'error')
            print("File not found.")

        # 从数据库中删除文件记录
        cur = mysql.connection.cursor()
        cur.execute("DELETE FROM uploaded_files WHERE filename = %s AND room_number = %s", (filename, room_number))
        mysql.connection.commit()
        cur.close()

        # 检查是否成功删除数据库中的记录
        if cur.rowcount > 0:
            print("File record deleted from database.")
        else:
            print("No file record found to delete.")
            
        flash('File deleted successfully!', 'success')
    except Exception as e:
        print(f"Error occurred: {str(e)}")  # 打印错误信息
        flash(f'Error deleting file: {str(e)}', 'error')

    # 返回更新后的文件列表
    uploaded_files = get_uploaded_files(room_number)  # 获取更新后的文件列表
    return render_template('content.html', uploaded_files=uploaded_files, room_number=room_number)

if __name__ == '__main__':
    app.run(debug=True)