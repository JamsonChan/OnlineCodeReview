from collections import defaultdict  # 存取學生驗證碼字典
import os, time  # 路徑, 時間
import secrets  # 生成驗證碼
from datetime import timedelta  # 登入時效
from mainpath import mainpath  # 系統初始路徑
from werkzeug.utils import secure_filename  # 過濾檔案名稱
from flask import *  # flask 伺服器
from flask_mail import Mail, Message  # 增加這行
import sendemail  # 發送信箱設置
from autoranktable import rank_table_html  # 生成排名資料
from autoheroranktable import create_hero_rank_html  # 生成英雄榜排名
from reload_grading import reload_homework_autograding  # 計算成績
from automistake import checkMistakeHtml  # 學生錯誤答案
from sql_connect import sql_connect  # 連結 MySQL 資料庫
from automemberhomepage import create_member_home_page  # 生成系統會員首頁
from automembererror import create_membererror  # 生成會員錯誤頁面
from autocodereview import create_review_html  # 生成程式碼審查清單頁面
from autouploaderror import create_upload_error  # 生成學生錯誤答案頁面
from autogoupload import create_auto_goUpload  # 生成上傳作業頁面
from outputpythonfile import read_python_file  # 生成程式碼審查頁面
from autostudentdatahtml import create_studentdata_html  # 生成學生後端數據
from autoteachingassistant import create_teaching_assistant_page  # 生成助教頁面
from autoteachingassistanterror import create_teaching_assistant_error_page  # 生成權限錯誤頁面
from autoforgetpassword import create_forget_password_html  # 生成忘記密碼頁面
from autohomepage import create_home_page  # 生成homepage
from autoleetcodehtml import create_leetcode_html  # 生成休閒題目頁面
from autototalsemestergrade import create_total_semester_grade_html  # 生成portal成績頁面
from autohomepageerror import create_homepage_error  # 生成會員首頁錯誤頁面
from outputpythonfile import PythonToHTML  # 生成留言板html (delete、add)
from autopersonaldata import create_student_personal_data_html  # 生成會員個人資料
from autocheckpersonaldata import create_check_personal_data_html  # 生成確認更改會員個人資料
from autopersonalerror import create_personal_error_html  # 生成個資錯誤頁面
from autoassignreviewnumber import assign_review_number  # 自動分配審查編號
from mainpath import mainpath, is_permissions_set  # 系統初始路徑, 權限人員

# ---------------------------------------------------- # 自定義變數
hwn = "2"  # 作業編號
Anonymous_message_dic = {"hw1":False, "hw2":True, "hw3":True, "hw4":True, "hw5":True, "hw6":True, "hw7":True, "hw8":True}  # 匿名審查字典
Verification_code_dict = defaultdict(str)  # 存取學生驗證碼
Anonymous_message = True  # 匿名開關
Code_review_comment = True  # 程式碼審查開關
Upload_file = False  # 上傳作業開關
leecode_button = False  # 休閒題目開關
ALLOWED_EXTENSIONS = set(['py'])  # 限制檔案格式
First_Path = mainpath  # 首頁目錄
# ---------------------------------------------------- # 自定義變數

# ---------------------------------------------------- # 熱更新 html 檔案
app = Flask(__name__, static_folder="public", static_url_path="/")
app.secret_key = "any string but secret"
app.jinja_env.auto_reload = True  # 更新靜態文件
app.config['TEMPLATES_AUTO_RELOAD'] = True
app.config.from_object(sendemail)
mail = Mail(app)  # 使用 flask_mail
# ---------------------------------------------------- # 熱更新 html 檔案

# ---------------------------------------------------- # 路由器
@app.route("/")  # 系統首頁
def index():
    return render_template("home.html")

@app.route("/register")  # 註冊頁面
def register():
    return render_template("register.html")

@app.route("/signUp", methods=["POST"])  # 註冊
def signUp():
    name = request.form["name"]  # 姓名
    nickname = request.form["nickname"]  # 暱稱
    studentid = request.form["studentid"]  # 學號
    password1 = request.form["password1"]  # 密碼
    password2 = request.form["password2"]  # 確認密碼
    if password1 != password2:return render_template("error.html", message = "確認密碼輸入錯誤!")
    connection = sql_connect()
    sql_cursor = connection.cursor()
    sql_cursor.execute(f"SELECT true FROM StudentData WHERE student_id = '{studentid}';")
    studentid_isexist = sql_cursor.fetchall()
    sql_cursor.execute(f"SELECT true FROM StudentData WHERE nickname = '{nickname}';")
    nickname_isexist = sql_cursor.fetchall()
    if not (studentid[1:].isdecimal() and len(studentid) == 8 and studentid[0].isalpha() and studentid[0].islower()):
        parameter = "學號錯誤(ex. s1104813)"
    elif studentid_isexist:
        parameter = "學號已註冊過!"
    elif nickname_isexist:
        parameter = "暱稱已被使用!"
    else:
        sql_cursor.execute(f"INSERT INTO StudentData VALUES('{studentid}', '{password1}', '{name}', '{nickname}', 0, 0, 0);")
        connection.commit()  # 更新資料庫
        parameter = "註冊成功!"
    sql_cursor.close()  # 關閉資料庫 / 連結
    connection.close()  # 新增資料需要新增這行
    return render_template("error.html", message = parameter)

@app.route("/forgetpassword1")  # 更改密碼頁面
def forgetpassword1():
    return render_template("forgetpassword1.html")

@app.route("/forgetpassword2/<student_id>")  # 更改密碼頁面
def forgetpassword2(student_id):
    return render_template("forgetpassword2.html")

@app.route("/reflash", methods=["POST"])  # 更改密碼處理
def reflash():
    student_id = request.form["studentid"]
    new_password = request.form["newpassword1"]
    verification_code = request.form["verification"]   
    if Verification_code_dict[student_id] != verification_code:parameter = "驗證碼錯誤!" 
    else:
        connection = sql_connect()
        sql_cursor = connection.cursor()
        sql_cursor.execute(f"UPDATE `StudentData` SET `password` = '{new_password}' WHERE `student_id` = '{student_id}';")
        parameter = "密碼變更成功!"
        connection.commit()  # 更新資料庫
        sql_cursor.close()  # 關閉資料庫 / 連結
        connection.close()  # 新增資料需要新增這行       
    return render_template("error.html", message = parameter)

@app.route("/signIn", methods=["POST"])  # 登入
def signIn():
    student_ID = request.form["studentid"]
    password = request.form["password"]
    connection = sql_connect()
    sql_cursor = connection.cursor()
    sql_cursor.execute(f"SELECT true FROM `StudentData` WHERE `student_id` = '{student_ID}' AND `password` = '{password}';")
    account_password_isexeist = sql_cursor.fetchall()
    if not account_password_isexeist:return render_template("error.html", message = "帳號或密碼錯誤!")
    else:
        session["StudentID"] = student_ID
        session.permanent = True  # 更新限制活動狀態
        app.permanent_session_lifetime = timedelta(minutes=3)  # 登入到期限制
    sql_cursor.close()
    connection.close()
    return redirect(f"/homepage/hw{hwn}")

@app.route("/signout")  # 登出  
def signout():
    if "StudentID" in session:
        del session["StudentID"]  # 移除 Session 中的會員資訊
        del session["RandomID"]
        return redirect("/")
    else:return render_template("error.html", message = "尚未登入")

@app.route("/send_email", methods=["POST"])  # 獲取信箱驗證碼
def send_email():
    student_id = request.form["studentid"]
    new_password1 = request.form["newpassword1"]
    new_password2 = request.form["newpassword2"]
    connection = sql_connect()
    sql_cursor = connection.cursor()
    sql_cursor.execute(f"SELECT `student_id`, `password` FROM StudentData WHERE `student_id` = '{student_id}';")
    id_password_isexit = sql_cursor.fetchall()
    if not id_password_isexit:return render_template("error.html", message = "學號尚未註冊!")
    if new_password1 != new_password2:return render_template("error.html", message = "兩密碼不相同!")
    if new_password1 == id_password_isexit[0][1]:return render_template("error.html", message = "密碼與舊密碼相同!")
    create_forget_password_html(student_id, new_password1, new_password2)
    verification_code = secrets.token_urlsafe()
    Verification_code_dict[student_id] = verification_code
    if student_id == "pclin":recipient = "pclin@saturn.yzu.edu.tw"
    else:recipient = f"{session['StudentID']}@mail.yzu.edu.tw"
    title = "資料結構系統-更改密碼"
    content = f"驗證碼:{verification_code}"
    message = Message(title, recipients=[recipient])
    message.body = content
    mail.send(message)
    return redirect(f"/forgetpassword2/{student_id}")

@app.route("/homepageerror/<hw_num>")  # 會員首頁錯誤頁面
def homepageerror(hw_num):
    if "StudentID" in session:
        message = request.args.get("message", "發生錯誤,請聯繫客服!")
        create_homepage_error(hw_num)
        return render_template("homepageerror.html", message = message)
    else:return render_template("error.html", message = "尚未登入")

@app.route("/membererror/<hw_num>")  # 作業首頁錯誤頁面
def membererror(hw_num):
    if "StudentID" in session:
        message = request.args.get("message", "發生錯誤,請聯繫客服!")
        Score = request.args.get("Score")
        Time = request.args.get("Time")
        Memory = request.args.get("Memory")
        create_membererror(hw_num)
        if Score:return render_template("membererror.html", message = message, Score = Score, Time = Time, Memory = Memory)
        else:return render_template("membererror.html", message = message)
    else:return render_template("error.html", message = "尚未登入")

@app.route("/uploaderror/<student_id>")  # 上傳錯誤頁面
def uploaderror(student_id):
    if "StudentID" in session:
        message = request.args.get("message", "發生錯誤,請聯繫客服!")
        Score = request.args.get("Score")
        Time = request.args.get("Time")
        Memory = request.args.get("Memory")
        create_upload_error(student_id)
        return render_template("uploaderror.html", message = message, Score = Score, Time = Time, Memory = Memory)
    else:return render_template("error.html", message = "尚未登入")

@app.route("/teachingassistanterror/<hw_num>")  # 權限錯誤頁面
def teachingassistanterror(hw_num):
    if "StudentID" in session:
        message = request.args.get("message", "發生錯誤,請聯繫客服!")
        create_teaching_assistant_error_page(hw_num)
        return render_template("teachingassistanterror.html", message = message)
    else:return render_template("error.html", message = "尚未登入")

@app.route("/homepage/<hw_num>")  # 系統會員首頁
def homepage(hw_num):
    if "StudentID" in session:
        random_id = check_student_data_create(session["StudentID"], hw_num)
        double_check_student_data(session["StudentID"], hw_num)
        create_home_page(hw_num, session["StudentID"])
        session["RandomID"] = random_id
        return render_template("homepage.html")
    else:return render_template("error.html", message = "尚未登入")

@app.route("/member_homepage/<hw_num>")  # 作業專區
def member_homepage(hw_num):
    if "StudentID" in session:
        connection = sql_connect()
        sql_cursor = connection.cursor()
        sql_cursor.execute(f"SELECT SD.`name`, H.`random_id` FROM `StudentData` AS SD, `Homework` AS H WHERE SD.`student_id` = '{session['StudentID']}' AND `homework_number` = '{hw_num}' AND SD.`student_id` = H.`student_id`;")
        name, random_id = sql_cursor.fetchall()[0]               
        create_member_home_page(hw_num, random_id)
        main_random(random_id)  # 更新session random_id
        sql_cursor.close()
        connection.close()
        return render_template(f"member_homepage.html", message1 = f"{session['StudentID'][1:]} - {name}", message2 = "作業期限:03/31 23:59", message3 = "審查期限:04/07 23:59")
    else:return render_template("error.html", message = "尚未登入")

@app.route("/personal_data/<hw_num>")  # 個人資料
def personal_data(hw_num):
    if "StudentID" in session:
        connection = sql_connect()
        sql_cursor = connection.cursor()
        sql_cursor.execute(f"SELECT `name`, `nickname`, `password` FROM `StudentData` WHERE `student_id` = '{session['StudentID']}';")
        name, nickname, password = sql_cursor.fetchall()[0]
        Len = len(password)
        password = ("*"*(Len//2)) + password[Len//2:]
        create_student_personal_data_html(hw_num, name, session["StudentID"], nickname, password)
        connection.close()
        sql_cursor.close()
        return render_template("personal_data.html")
    else:return render_template("error.html", message = "尚未登入")

@app.route("/portal_grades/<hw_num>/<student_id>")  # portal成績
def portal_grades(hw_num, student_id):
    if "StudentID" in session:
        create_total_semester_grade_html(student_id, hw_num)
        return render_template("portal_grades.html")
    else:return render_template("error.html", message = "尚未登入")

@app.route("/download_homework_file/<homework_file_name>")  # 下載作業說明
def download_homework_file(homework_file_name):  
    if "StudentID" in session:
        return send_from_directory('homework_download', homework_file_name, as_attachment=True)
    else:return render_template("error.html", message = "尚未登入")

@app.route("/display_homework/<homework_html_name>")  # 顯示作業說明
def display_homework(homework_html_name):
    if "StudentID" in session:
        return render_template(f"{homework_html_name}.html")
    else:return render_template("error.html", message = "尚未登入")

@app.route("/display_homepage_rules")  # 顯示主頁說明
def display_homepage_rules():
    if "StudentID" in session:
        return render_template("homepage_rules.html")
    else:return render_template("error.html", message = "尚未登入")

@app.route("/display_homework_rules")  # 顯示上傳作業規則
def display_homework_rules():
    if "StudentID" in session:
        return render_template("homework_rules.html")
    else:return render_template("error.html", message = "尚未登入")

@app.route("/display_leetcode/<hw_num>")  # 顯示休閒題目的題目
def display_leetcode(hw_num):
    if "StudentID" in session:
        return render_template(f"{hw_num}_description.html")
    else:return render_template("error.html", message = "尚未登入")

@app.route("/hero_rank/<hw_num>")  # 英雄榜
def hero_rank(hw_num):
    if "StudentID" in session:
        create_hero_rank_html(hw_num, session["StudentID"])
        return render_template("herorank.html")
    else:return render_template("error.html", message = "尚未登入")

@app.route("/leetcode/<hw_num>")  # 休閒題目
def leetcode(hw_num):
    if "StudentID" in session:
        if leecode_button:
            create_leetcode_html(hw_num)
            return render_template("leetcode.html")
        else:
            return redirect(f"/homepageerror/{hw_num}?message=尚未開放!")
    else:return render_template("error.html", message = "尚未登入")

@app.route("/leetcode_correction/<hw_num>", methods=["POST"])  # 儲存休閒題目之學生答案
def leetcode_correction(hw_num):
    if "StudentID" in session:
        if leecode_button:
            leetcode_comment = request.form["leetcode_comment"].replace("\n", "")
            os.chdir(First_Path)    
            with open(f"templates/{hw_num}.py", "w", encoding="utf-8") as file:
                file.write(leetcode_comment)
                os.chdir(First_Path) 
            return render_template("leetcode.html")
        else:
            return redirect(f"/homepageerror/{hw_num}?message=尚未開放!")
    else:return render_template("error.html", message = "尚未登入")

@app.route("/rank_best/<hw_num>", methods = ["GET"])  # 總表排行
def rank_best(hw_num):
    if "StudentID" in session:
        attribute = request.values.get("rank_best")  # (student_id, time, memory, upload_count)
        rank_table_html(hw_num, "best", attribute, session["StudentID"])  # 更新排行榜
        return render_template(f"rank_best.html")
    else:return render_template("error.html", message = "尚未登入")
    
@app.route("/rank_all/<hw_num>", methods = ["GET"])  # 時間排行checkMistakeHtml
def rank_all(hw_num):
    if "StudentID" in session:
        attribute = request.values.get("rank_all")  # (student_id, time, memory, upload_time)
        rank_table_html(hw_num, "all", attribute, session["StudentID"])  # 更新排行榜
        return render_template(f"rank_all.html")
    else:return render_template("error.html", message = "尚未登入")
       
@app.route("/goUpload/<hw_num>")  # 上傳作業頁面
def goUpload(hw_num):
    if "StudentID" in session:
        if Upload_file and hw_num == f"hw{hwn}":
            connection = sql_connect()
            sql_cursor = connection.cursor()
            sql_cursor.execute(f"SELECT `score`, `upload_count` FROM `Homework` WHERE `student_id` = '{session['StudentID']}' AND `homework_number` = '{hw_num}';")
            output_sql_cursor_isexist = sql_cursor.fetchall()
            parameter1,  parameter2 = str(output_sql_cursor_isexist[0][0]), str(output_sql_cursor_isexist[0][1])         
            sql_cursor.close()
            connection.close()
            create_auto_goUpload(hw_num)
            return render_template(f"goUpload.html", message1 = f"上傳次數:{parameter2}", message2 = f"最高分數:{parameter1}")
        else:return redirect(f"/membererror/{hw_num}?message=目前沒有開放~")
    else:return render_template("error.html", message = "尚未登入")

@app.route("/upload", methods=["POST"])  # 作業自動化批改
def upload():
    if "StudentID" in session:
        time_limit_exeeded_bol = False
        connection = sql_connect()
        sql_cursor = connection.cursor()
        sql_cursor.execute(f"SELECT `upload_count` FROM `Homework` WHERE `student_id` = '{session['StudentID']}' AND `homework_number` = 'hw{hwn}';")
        frequency_isexist = sql_cursor.fetchall()
        frequency = frequency_isexist[0][0]
        if frequency == 30:return redirect(f"/membererror/hw{hwn}?message=已達上傳次數!")
        check_create_student_dir(session["StudentID"])
        UPLOAD_FOLDER = f"{mainpath}\\homework_file\\hw{hwn}\\{session['StudentID']}"
        app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER  # 存放的資料夾
        app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 限制檔案大小 "16MB"
        student_file = request.files["file"]  # s1104813.py
        if student_file and allowed_file(student_file.filename) and (f"{session['StudentID']}.py" == str(student_file.filename)):  # 儲存學生上傳的檔案
            filename = secure_filename(student_file.filename)
            student_file.save(os.path.join(app.config["UPLOAD_FOLDER"], filename))
        else:return redirect(f"/membererror/hw{hwn}?message=檔案錯誤!")
        filename = check_student_file_rename(session["StudentID"], str(student_file.filename), str(frequency))
        sql_cursor.close()
        connection.close()
        upload_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        try:
            Score, Time, Memory, Sheet = reload_homework_autograding(session["StudentID"], filename, hwn)  # 計算分數 , 時間 , 記憶體
        except:
            time_limit_exeeded_bol = True
            Score, Time, Memory = 0, 0, 0
        upload_file_count(session["StudentID"])  # 計算上傳次數
        update_Time_Memory_Score_HomeworkFile(session["StudentID"], Time, Memory, Score, filename)
        if time_limit_exeeded_bol:  # 超過時間限制
            update_all_homework(f"hw{hwn}", session["StudentID"], session["RandomID"], 999999.999, 999999.999, upload_time, 0, filename)  # 全部作業資料更新
            return redirect(f"/membererror/hw{hwn}?message=time limit exceeded")
        if Score == 100:
            update_all_homework(f"hw{hwn}", session["StudentID"], session["RandomID"], Time, Memory, upload_time, Score, filename)  # 全部作業資料更新           
            return redirect(f"/membererror/hw{hwn}?message=成功上傳!&Score=分數:{Score}&Time=時間:{Time}ms&Memory=記憶體:{Memory}KB")
        else:
            update_all_homework(f"hw{hwn}", session["StudentID"], session["RandomID"], 999999.999, 999999.999, upload_time, Score, filename)  # 全部作業資料更新
            create_checkmistake_sheet(Sheet, f"hw{hwn}", session["StudentID"])
            return redirect(f"/uploaderror/{session['StudentID']}?message=成功上傳!&Score=分數:{Score}&Time=時間:----ms&Memory=記憶體:----KB")
    else:return render_template("error.html", message = "尚未登入")

@app.route("/checkMistake/<student_id>")  # 顯示學生作業錯誤答案
def checkMistake(student_id):
    if "StudentID" in session:        
        return render_template(f"checkMistake.html")
    else:return render_template("error.html", message = "尚未登入")

@app.route("/codereview/<hw_num>/<random_id>")  # 顯示程式碼審查頁面
def codereview(hw_num, random_id):
    if "StudentID" in session:
        if (hw_num != f"hw{hwn}") or (Code_review_comment or session["StudentID"] in is_permissions_set):  # 判斷是否開啟程式碼審查
            os.chdir(First_Path)
            connection = sql_connect()
            sql_cursor = connection.cursor()
            sql_cursor.execute(f"SELECT `random_id` FROM Homework WHERE student_id = '{session['StudentID']}' AND homework_number = '{hw_num}';")
            session_random_id = sql_cursor.fetchall()[0][0]
            main_random(session_random_id)  # 更新session random_id
            sql_cursor.execute(f"SELECT `student_id` FROM `Homework` WHERE `random_id` = {random_id} AND `homework_number` = '{hw_num}'")
            author_id = sql_cursor.fetchall()[0][0]
            read_python_file(hw_num, author_id, Anonymous_message_dic[hw_num], session["StudentID"], session["RandomID"])
            create_review_html(hw_num, Anonymous_message_dic[hw_num], random_id, session["StudentID"], session["RandomID"])
            return render_template(f"codereview.html")
        else:return redirect(f"/membererror/{hw_num}?message=審查尚未開放!")
    else:return render_template("error.html", message = "尚未登入")

@app.route("/codepage/<hw_num>/<random_id>")  # 顯示學生程式碼
def codepage(hw_num, random_id):
    if "StudentID" in session:
        if (hw_num != f"hw{hwn}") or (Code_review_comment or session["StudentID"] in is_permissions_set):  # 判斷是否開啟程式碼審查
            os.chdir(First_Path)
            connection = sql_connect()
            sql_cursor = connection.cursor()
            sql_cursor.execute(f"SELECT random_id FROM Homework WHERE student_id = '{session['StudentID']}' AND homework_number = '{hw_num}';")
            session_random_id = sql_cursor.fetchall()[0][0]
            main_random(session_random_id)  # 更新session random_id
            sql_cursor.execute(f"SELECT `student_id` FROM `Homework` WHERE `random_id` = {random_id} AND `homework_number` = '{hw_num}';")
            author_id = sql_cursor.fetchall()[0][0]
            sql_cursor.close()
            connection.close()
            read_python_file(hw_num, author_id, Anonymous_message_dic[hw_num], session["StudentID"], session["RandomID"])
            return render_template(f"codepage.html")
        else:return redirect(f"/membererror/{hw_num}?message=審查尚未開放!")
    else:return render_template("error.html", message = "尚未登入")

@app.route("/teachingassistant/<hw_num>")  # 顯示助教專區
def teachingassistant(hw_num):
    if "StudentID" in session:
        if session["StudentID"] in is_permissions_set:
            create_teaching_assistant_page(hw_num)
            return render_template(f"teachingassistant.html")
        else:return redirect(f"/homepageerror/{hw_num}?message=請止步謝謝~")
    else:return render_template("error.html", message = "尚未登入")

@app.route("/studentdata/<hw_num>")  # 顯示學生後台數據
def studentdata(hw_num):
    if "StudentID" in session:
        if session["StudentID"] in is_permissions_set:
            create_student_data(hw_num)  # 創建學生後臺數據
            return render_template(f"studentdata.html")
        else:return redirect(f"/membererror/{hw_num}?message=請止步謝謝~")
    else:return render_template("error.html", message = "尚未登入")

@app.route("/opensmallname/<hw_num>")  # 開啟匿名留言
def opensmallname(hw_num):
    global Anonymous_message
    if "StudentID" in session:
        if session["StudentID"] == "s1104813" and hw_num == f"hw{hwn}":
            Anonymous_message = True  # 開啟匿名留言
            return redirect(f"/teachingassistanterror/{hw_num}?message=成功開啟匿名留言~")
        else:return redirect(f"/teachingassistanterror/{hw_num}?message=沒有權限~")
    else:return render_template("error.html", message = "尚未登入")

@app.route("/unopensmallname/<hw_num>")  # 關閉匿名留言
def unopensmallname(hw_num):
    global Anonymous_message
    if "StudentID" in session:
        if session["StudentID"] == "s1104813" and hw_num == f"hw{hwn}":
            Anonymous_message = False  # 關閉匿名留言
            return redirect(f"/teachingassistanterror/{hw_num}?message=成功關閉匿名留言~")
        else:return redirect(f"/teachingassistanterror/{hw_num}?message=沒有權限~")
    else:return render_template("error.html", message = "尚未登入")

@app.route("/opencodereviewcomment/<hw_num>")  # 打開審查留言
def opencodereviewcomment(hw_num):
    global Code_review_comment
    if "StudentID" in session:
        if session["StudentID"] == "s1104813" and hw_num == f"hw{hwn}":
            Code_review_comment = True  # 開啟程式碼審查
            return redirect(f"/teachingassistanterror/{hw_num}?message=成功開啟程式碼審查~")
        else:return redirect(f"/teachingassistanterror/{hw_num}?message=沒有權限~")
    else:return render_template("error.html", message = "尚未登入")

@app.route("/unopencodereviewcomment/<hw_num>")  # 關閉審查留言
def unopencodereviewcomment(hw_num):
    global Code_review_comment
    if "StudentID" in session:
        if session["StudentID"] == "s1104813" and hw_num == f"hw{hwn}":
            Code_review_comment = False  # 關閉程式碼審查
            return redirect(f"/teachingassistanterror/{hw_num}?message=成功關閉程式碼審查~")
        else:return redirect(f"/teachingassistanterror/{hw_num}?message=沒有權限~")
    else:return render_template("error.html", message = "尚未登入")

@app.route("/openuploadfile/<hw_num>")  # 開啟上傳檔案按鈕
def openuploadfile(hw_num):
    global Upload_file
    if "StudentID" in session:
        if session["StudentID"] == "s1104813" and hw_num == f"hw{hwn}":
            Upload_file = True  # 開啟程式碼審查
            return redirect(f"/teachingassistanterror/{hw_num}?message=成功開啟上傳檔案~")
        else:return redirect(f"/teachingassistanterror/{hw_num}?message=沒有權限~")
    else:return render_template("error.html", message = "尚未登入")

@app.route("/unopenuploadfile/<hw_num>")  # 關閉上傳檔案按鈕
def unopenuploadfile(hw_num):
    global Upload_file
    if "StudentID" in session:
        if session["StudentID"] == "s1104813" and hw_num == f"hw{hwn}":
            Upload_file = False  # 關閉程式碼審查
            return redirect(f"/teachingassistanterror/{hw_num}?message=成功關閉上傳檔案~")
        else:return redirect(f"/teachingassistanterror/{hw_num}?message=沒有權限~")
    else:return render_template("error.html", message = "尚未登入")

@app.route("/Assignnumber/<hw_num>")  # 分配學生審查編號
def Assignnumber(hw_num):
    if "StudentID" in session:
        if session["StudentID"] == "s1094815" and hw_num == f"hw{hwn}":
            assign_review_number(hw_num)
            return redirect(f"/teachingassistanterror/{hw_num}?message=成功分配審查編號~")
        else:return redirect(f"/teachingassistanterror/{hw_num}?message=沒有權限~")
    else:return render_template("error.html", message = "尚未登入")

@app.route("/change_nickname/<hw_num>/<student_id>", methods=["POST"])  # 登入後更改暱稱
def change_nickname(hw_num, student_id):
    if "StudentID" in session:
        connection = sql_connect()
        sql_cursor = connection.cursor()
        sql_cursor.execute(f"SELECT `name`, `password` FROM `StudentData` WHERE `student_id` = '{session['StudentID']}';")
        name, password = sql_cursor.fetchall()[0]
        Len = len(password)
        password = ("*"*(Len//2)) + password[Len//2:]
        create_check_personal_data_html(hw_num, name, student_id, '', password, "nickname")
        connection.close()
        sql_cursor.close()
        return render_template("change_nickname.html")
    else:return render_template("error.html", message = "尚未登入")

@app.route("/change_password/<hw_num>/<student_id>", methods=["POST"])  # 登入後更改密碼
def change_password(hw_num, student_id):
    if "StudentID" in session:
        connection = sql_connect()
        sql_cursor = connection.cursor()
        sql_cursor.execute(f"SELECT `name`, `nickname` FROM `StudentData` WHERE `student_id` = '{session['StudentID']}';")
        name, nickname = sql_cursor.fetchall()[0]
        create_check_personal_data_html(hw_num, name, student_id, nickname, '', "password")
        connection.close()
        sql_cursor.close()
        return render_template("change_password.html")
    else:return render_template("error.html", message = "尚未登入")

@app.route("/check_change/<Type>/<hw_num>/<student_id>", methods=["POST"])  # 更新新密碼和暱稱
def check_change(Type, hw_num, student_id):
    if "StudentID" in session:
        connection = sql_connect()
        sql_cursor = connection.cursor()
        if Type == "nickname":
            new_nickname = request.form["new_nickname"]
            sql_cursor.execute(f"SELECT * FROM `StudentData` WHERE `nickname` = '{new_nickname}';")
            if sql_cursor.fetchall():
                connection.close()
                sql_cursor.close()
                return redirect(f"/personal_error/{hw_num}/{student_id}?message=❌暱稱已被使用❌")
            sql_cursor.execute(f"UPDATE `StudentData` SET `nickname` = '{new_nickname}' WHERE `student_id` = '{student_id}';")
        else:
            new_password = request.form["new_password"]
            sql_cursor.execute(f"SELECT * FROM `StudentData` WHERE `password` = '{new_password}' AND `student_id` = '{student_id}';")
            if sql_cursor.fetchall():
                connection.close()
                sql_cursor.close()
                return redirect(f"/personal_error/{hw_num}/{student_id}?message=❌您輸入了舊密碼❌")
            sql_cursor.execute(f"UPDATE `StudentData` SET `password` = '{new_password}' WHERE `student_id` = '{student_id}';")
        connection.commit()
        connection.close()
        sql_cursor.close()
        return redirect(f"/personal_error/{hw_num}/{student_id}?message=⭕恭喜成功更改⭕")      
    else:return render_template("error.html", message = "尚未登入")

@app.route("/personal_error/<hw_num>/<student_id>", methods=["GET"])  # 個資錯誤頁面顯示
def personal_error(hw_num, student_id):
    if "StudentID" in session:
        message = request.args.get("message")
        create_personal_error_html(hw_num)
        return render_template("personal_error.html", message = message)
    else:return render_template("error.html", message = "尚未登入")

# -------------------------------------------------------------------- # 路由器

# -------------------------------------------------------------------- # 路由器方法(javascript、ajax)
@app.route("/codelike", methods=['POST'])  # 處理'審查清單'按讚、收回讚
def codelike():
    student_id = session["StudentID"]
    count = int(request.form["count"])
    like_type = request.form["like_type"]
    hw_num = request.form["homework_number"]
    author_random_id = request.form["author_random_id"]

    connection = sql_connect()
    sql_cursor = connection.cursor()
    sql_cursor.execute(f"SELECT `student_id` FROM `Homework` WHERE `homework_number` = '{hw_num}' AND `random_id` = {author_random_id}")
    author_id = sql_cursor.fetchall()[0][0]

    if like_type == "add":
        count += 1
        sql_cursor.execute(f"INSERT INTO `CodeLike` VALUES('{student_id}', '{hw_num}', '{author_id}');")
    else:
        count -= 1
        sql_cursor.execute(f"DELETE FROM `CodeLike` WHERE student_id = '{student_id}' AND homework_number = '{hw_num}' AND author_id = '{author_id}';")
    sql_cursor.execute(f"UPDATE `Homework` SET `like_count` = {count} WHERE `student_id` = '{author_id}' AND `homework_number` = '{hw_num}';")
    connection.commit()
    sql_cursor.close()
    connection.close()
    return str(count) if count != 0 else "" 

@app.route("/commentlike", methods=['POST'])  # 處理'留言區'留言按讚、收回讚
def commentlike():
    student_id = session["StudentID"]
    count = int(request.form["count"])
    hw_num = request.form["homework_number"]
    like_type = request.form["like_type"]
    reviewer = request.form["reviewer"]
    review_time = request.form["review_time"]

    connection = sql_connect()
    sql_cursor = connection.cursor()
    sql_cursor.execute(f"SELECT `student_id` FROM `Homework` WHERE `homework_number` = '{hw_num}' AND `random_id` = {reviewer}")
    reviewer = sql_cursor.fetchall()[0][0]

    if like_type == "add":
        count += 1
        sql_cursor.execute(f"INSERT INTO `CommentLike` VALUES('{student_id}', '{reviewer}', '{review_time}');")
    else:
        count -= 1
        sql_cursor.execute(f"DELETE FROM `CommentLike` WHERE student_id = '{student_id}' AND reviewer_id = '{reviewer}' AND review_time = '{review_time}';")
    sql_cursor.execute(f"UPDATE `Comment` SET `like_count` = {count} WHERE reviewer_id = '{reviewer}' AND review_time = '{review_time}';")
    connection.commit()
    sql_cursor.close()
    connection.close()
    return str(count) if count != 0 else ""

@app.route("/addcomment", methods=['POST'])  # 留言板新增留言
def addcomment():
    os.chdir(First_Path)
    student_id = session["StudentID"]
    random_id = session["RandomID"]
    hw_num = request.form["homework_number"]
    isAnonymous = Anonymous_message_dic[hw_num]
    author_id = request.form["author_id"]
    review_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    content = request.form["content"]

    content = content.replace("<", "&lt;").replace(">", "&gt;")  # 將此符號轉換成html的符號
    content = content.replace("\n", "<br>").replace("\r", "<br>")  # 將換行轉換成html換行
    content = content.replace(" ", "&nbsp")  # 將空格轉換成html空格

    connection = sql_connect()
    sql_cursor = connection.cursor()
    sql_cursor.execute(f"INSERT INTO `Comment` VALUES ('{hw_num}', '{author_id}', '{session['StudentID']}', '{review_time}', '{content}', 0);")
    connection.commit()
    sql_cursor.close()
    connection.close()

    pth = PythonToHTML(hw_num, author_id, isAnonymous, student_id, random_id)
    return pth.to_html_msg_board()

@app.route("/deletecomment", methods=['POST'])  # 留言板刪除留言
def deletecomment():
    student_id = session["StudentID"]
    random_id = session["RandomID"]
    review_time = request.form["review_time"]

    hw_num = request.form["homework_number"]
    author_id = request.form["author_id"]

    isAnonymous = Anonymous_message_dic[hw_num]

    connection = sql_connect()
    sql_cursor = connection.cursor()
    sql_cursor.execute(f"DELETE FROM `Comment` WHERE reviewer_id = '{student_id}' AND review_time = '{review_time}';")
    sql_cursor.execute(f"DELETE FROM `CommentLike` WHERE reviewer_id = '{student_id}' AND review_time = '{review_time}';")
    connection.commit()
    sql_cursor.close()
    connection.close()
    pth = PythonToHTML(hw_num, author_id, isAnonymous, student_id, random_id)
    return pth.to_html_msg_board()
    
@app.route("/codewholike", methods=['POST'])  # '審查清單'按讚名單
def codewholike():
    hw_num = request.form["homework_number"]
    author_id = request.form["id"]
    isAnonymous = Anonymous_message_dic[hw_num]

    connection = sql_connect()
    sql_cursor = connection.cursor()

    sql_cursor.execute(f"SELECT `student_id` FROM `Homework` WHERE `homework_number` = '{hw_num}' AND `random_id` = {author_id}")
    author_id = sql_cursor.fetchall()[0][0]

    sql_cursor.execute(f"""
                        SELECT
                            s.name,
                            s.nickname
                        FROM `CodeLike` c
                        LEFT JOIN `StudentData` s ON s.student_id = c.student_id
                        WHERE c.author_id = '{author_id}' AND c.homework_number = '{hw_num}'
                        """)

    like = [x[(1 if isAnonymous else 0)] for x in sql_cursor.fetchall()]
    out = ""
    for x in like:
        out += f"{x}<br>" 
    out += ""
    connection.commit()
    sql_cursor.close()
    connection.close()
    
    return out if like else ""
    
@app.route("/commentwholike", methods=['POST'])  # '留言板'按讚名單
def commentwholike():
    hw_num = request.form["homework_number"]
    reviewer_id = request.form["id"]
    review_time = request.form["review_time"]
    isAnonymous = Anonymous_message_dic[hw_num]

    connection = sql_connect()
    sql_cursor = connection.cursor()

    sql_cursor.execute(f"SELECT `student_id` FROM `Homework` WHERE `homework_number` = '{hw_num}' AND `random_id` = {reviewer_id}")
    reviewer_id = sql_cursor.fetchall()[0][0]

    sql_cursor.execute(f"""
                        SELECT
                            s.name,
                            s.nickname
                        FROM `CommentLike` c
                        LEFT JOIN `StudentData` s ON s.student_id = c.student_id
                        WHERE c.reviewer_id = '{reviewer_id}' AND c.review_time = '{review_time}'
                        """)
    
    like = [x[(1 if isAnonymous else 0)] for x in sql_cursor.fetchall()]
    print(like)
    out = ""
    for x in like:
        out += f"{x}<br>" 
    out += ""
    connection.commit()
    sql_cursor.close()
    connection.close()
    
    return out if like else ""

# -------------------------------------------------------------------- # 路由器方法(javascript、ajax)

# -------------------------------------------------------------------- # 函式方法

def check_student_data_create(student_id, hw_num):  # 確認學生資料是否在資料庫
    connection = sql_connect()
    sql_cursor = connection.cursor()
    sql_cursor.execute(f"SELECT `student_id`, `homework_number`, `random_id` FROM `Homework` WHERE `student_id` = '{student_id}' AND `homework_number` = '{hw_num}';")
    studnet_data_isexist = sql_cursor.fetchall()
    if not studnet_data_isexist:
        sql_cursor.execute(f"SELECT COUNT(*) FROM `Homework` WHERE `homework_number` = '{hw_num}';")
        Len = sql_cursor.fetchall()[0][0]
        if student_id == "s1104813":
            random_id = 1104813
        elif student_id == "s1094815":
            random_id = 1094815
        elif student_id == "pclin":
            random_id = 9999999
        else:
            random_id = Len + 1
        sql_cursor.execute(f"INSERT INTO `Homework`(`homework_number`, `student_id`, `random_id`) VALUES('{hw_num}', '{student_id}', {random_id});")
        connection.commit()
    else:random_id = studnet_data_isexist[0][2]
    sql_cursor.close()
    connection.close()
    return random_id

def double_check_student_data(student_id, hw_num):  # 再次確認學生資料是否在資料庫
    connection = sql_connect()
    sql_cursor = connection.cursor()
    sql_cursor.execute(f"SELECT DISTINCT `homework_number` FROM `Homework` WHERE `student_id` = '{student_id}';")
    check_hwn = {i[0] for i in sql_cursor.fetchall()}
    for i in range(1, int(hw_num[2:])):
        if f"hw{i}" not in check_hwn:
            if student_id in is_permissions_set:
                sql_cursor.execute(f"INSERT INTO `Homework`(`homework_number`, `student_id`, `random_id`) VALUES('hw{i}', '{student_id}', {is_permissions_set[student_id]});")
            else:
                sql_cursor.execute(f"SELECT COUNT(*) FROM `Homework` WHERE `homework_number` = 'hw{i}';")
                random_id = sql_cursor.fetchall()[0][0]
                sql_cursor.execute(f"INSERT INTO `Homework`(`homework_number`, `student_id`, `random_id`) VALUES('hw{i}', '{student_id}', {random_id+1});")
            connection.commit()
    sql_cursor.close()
    connection.close()

def check_create_student_dir(student_file):  # 創建學生資料夾 "homework_file/hw_num/studentid"
    os.chdir(First_Path)
    lst = os.listdir(f"./homework_file/hw{hwn}")
    os.chdir(f"./homework_file/hw{hwn}")
    if student_file not in lst:os.mkdir(student_file)
    os.chdir(First_Path)

def allowed_file(filename):  # 限制檔案 (.py)
    return '.' in filename and filename.split('.', 1)[1] in ALLOWED_EXTENSIONS

def check_student_file_rename(student_id, student_file, frequency):  # 存取學生作業檔案
    os.chdir(f"./homework_file/hw{hwn}/{student_id}")
    if os.path.isfile(f"hw{hwn}_{student_id}_{frequency}.py"):  # 處理例外事件, 檔案重複
        os.remove(f"hw{hwn}_{student_id}_{frequency}.py")
    os.rename(student_file, f"hw{hwn}_{student_id}_{frequency}.py")
    os.chdir(First_Path)
    return f"hw{hwn}_{student_id}_{frequency}.py"

def create_checkmistake_sheet(checkmistake_sheet, hw_num, student_id):  # 創建學生錯誤題目的表單
    for rs in range(len(checkmistake_sheet)):
        checkmistake_sheet[rs] = tuple(checkmistake_sheet[rs])
    checkmistake_sheet = tuple(checkmistake_sheet)
    checkMistakeHtml(checkmistake_sheet, hw_num, student_id)

def upload_file_count(student_id):  # 計算上傳次數
    connection = sql_connect()
    sql_cursor = connection.cursor()
    sql_cursor.execute(f"UPDATE `Homework` SET `upload_count` = `upload_count` + 1 WHERE `student_id` = '{student_id}' AND `homework_number` = 'hw{hwn}';")
    connection.commit()
    sql_cursor.close()
    connection.close()

def update_Time_Memory_Score_HomeworkFile(student_id, Time, Memory, score, student_file):  # 作業資料儲存資料庫
    connection = sql_connect()
    sql_cursor = connection.cursor()
    if score == 100:
        sql_cursor.execute(F"UPDATE `Homework` SET `score` = {score}, `time` = {Time}, `memory` = {Memory}, `file_name` = '{student_file}' WHERE `student_id` = '{student_id}' AND `homework_number` = 'hw{hwn}' AND (`memory` >= {Memory} OR `time` >= {Time});")
    else:
        sql_cursor.execute(F"UPDATE `Homework` SET `score` = {score}, `file_name` = '{student_file}' WHERE `student_id` = '{student_id}' AND `homework_number` = 'hw{hwn}' AND `score` <= {score};")
    connection.commit()
    sql_cursor.close()
    connection.close()

def update_all_homework(hw_num, student_id, random_id, Time, Memory, upload_time, score, file_name):  # 全部作業資料新增資料庫
    connection = sql_connect()
    sql_cursor = connection.cursor()
    sql_cursor.execute(f"INSERT INTO `AllHomework` VALUES('{hw_num}', '{student_id}', {random_id}, {Time}, {Memory}, '{upload_time}', {score}, '{file_name}');")
    connection.commit()
    sql_cursor.close()
    connection.close()

def create_student_data(hw_num):  # 生成學生後端資料
    connection = sql_connect()
    sql_cursor = connection.cursor()
    sql_cursor.execute(f"""
                        SELECT t1.*, t2.`review_target1`, t2.`review_target2`, t2.`review_target3`, t2.`ok1`, t2.`ok2`, t2.`ok3`
                        FROM
                            (SELECT SD.`student_id`, SD.`name`, SD.`nickname`, H.`upload_count`, H.`score`, H.`file_name`, H.`random_id`
                            FROM `Homework` AS H, `StudentData` AS SD
                            WHERE SD.`student_id` = H.`student_id` AND H.`homework_number` = '{hw_num}') t1
                        LEFT JOIN
                            (SELECT
                                H1.`student_id`,
                                RT.`random_id`,
                                RT.`review_target1`,
                                RT.`review_target2`,
                                RT.`review_target3`,
                                (CASE WHEN H1.`student_id` IN (SELECT `reviewer_id` FROM Comment WHERE `author_id` = H2.`student_id` AND `homework_number` = '{hw_num}') THEN '✅' ELSE '❌' END) `ok1`,
                                (CASE WHEN H1.`student_id` IN (SELECT `reviewer_id` FROM Comment WHERE `author_id` = H3.`student_id` AND `homework_number` = '{hw_num}') THEN '✅' ELSE '❌' END) `ok2`,
                                (CASE WHEN H1.`student_id` IN (SELECT `reviewer_id` FROM Comment WHERE `author_id` = H4.`student_id` AND `homework_number` = '{hw_num}') THEN '✅' ELSE '❌' END) `ok3`
                            FROM `ReviewTarget` AS RT
                            LEFT JOIN `Homework` AS H1 ON RT.`random_id` = H1.`random_id`
                            LEFT JOIN `Homework` AS H2 ON RT.`review_target1` = H2.`random_id`
                            LEFT JOIN `Homework` AS H3 ON RT.`review_target2` = H3.`random_id`
                            LEFT JOIN `Homework` AS H4 ON RT.`review_target3` = H4.`random_id`
                            WHERE RT.`homework_number` = '{hw_num}' AND H1.`homework_number` = '{hw_num}' AND H2.`homework_number` = '{hw_num}' AND H3.`homework_number` = '{hw_num}' AND H4.`homework_number` = '{hw_num}') t2
                        ON t1.`student_id` = t2.`student_id`
                        ORDER BY `student_id`;
                        """)
    student_sheet = tuple(sql_cursor.fetchall())
    create_studentdata_html(student_sheet, hw_num)
    sql_cursor.close()
    connection.close()

def main_random(random_id):  # 切換作業編號
    del session["RandomID"]
    session["RandomID"] = random_id

# -------------------------------------------------------------------- # 函式方法
if __name__ == "__main__":
    # app.run(host="140.138.178.26", port=3000, debug=True)
    # app.run(host="140.138.178.26", port=3000)
    app.run(debug=True, port=3000)