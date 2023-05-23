import os
from mainpath import mainpath, is_permissions_set
def create_studentdata_html(student_sheet, hw_num):
    html = f"""
    <!DOCTYPE html>
    <head>
        <meta charset='UTF-8'>
        <link rel="icon" href="https://cdn-icons-png.flaticon.com/512/328/328201.png" type="image/x-icon"/> 
        <title>學生後台數據</title>
        <style type="text/css">
            body{{width: 100%;height: 100%;font-family: 'Open Sans',sans-serif;margin: 0; background-color: #37464a; background:url("/img/picture.png");background-size: cover;background-attachment: fixed;background-position: center;}}
            .main {{font-family:consolas;}}
            table {{background-color: #ffffffa9;border-collapse:collapse;word-break:keep-all;white-space:nowrap;font-size:22px;margin-left: auto; margin-right: auto; width:80%; border-spacing: 0; border:7px #FFD382 groove;}}
            tr {{text-align: center;color:#fff;font-size:22px;}}
            th {{position:sticky;top:0;font-weight:normal;background-color:#FF5F5F;border-color:#000;border-width:1px;border-style:solid;padding:15px;font-size:23px;}}
            td {{color:black;border-color:#000;border-width:1px;border-style:solid;padding:5px;}}
            .but{{width: 310px;min-height: 20px;display: block;background-color: #07070785;border: 2px solid #bccdf3;color: #fff;padding: 12px 20px;font-size: 16px;line-height: normal;border-radius: 10px;cursor: pointer; font-family: consolas;}}
            .but:hover {{background-color: #fcfcfc85;color: rgb(2, 0, 0);}}
        </style>
    </head>
    <body style='background-color: #315e49;'>
        <div style = "text-align: center;padding:30px">
            <form action="/teachingassistant/{hw_num}" style="display:inline-block;"><button class="but"style="font-size: 23px;">返回助教頁面</button></form>
        </div>
        <div class='main'>
        <table style="border-collapse:collapse;word-break:keep-all;white-space:nowrap;font-size:22px;">
        <tr style="color:#fff;background-color:#48a6fb;font-size:22px;">
    """
    html += "<th>學號</th><th>姓名</th><th>暱稱</th><th>上傳次數</th><th>最佳分數</th><th>最佳程式碼</th><th>審查編號</th><th>目標1</th><th>目標2</th><th>目標3</th></tr>"
    student, teacher = "", ""
    for row in student_sheet:
        tar1 = f"{row[7]}{row[10]}" if row[7] else ""
        tar2 = f"{row[8]}{row[11]}" if row[8] else ""
        tar3 = f"{row[9]}{row[12]}" if row[9] else ""
        if row[0] in is_permissions_set:
            teacher += f"<tr><td>{row[0]}</td><td>{row[1]}</td><td>{row[2]}</td><td>{row[3]}</td><td>{row[4]}</td><td>{row[5]}</td><td>{row[6]}</td><td>{tar1}</td><td>{tar2}</td><td>{tar3}</td></tr>"
        else:
            student += f"<tr><td>{row[0]}</td><td>{row[1]}</td><td>{row[2]}</td><td>{row[3]}</td><td>{row[4]}</td><td>{row[5]}</td><td>{row[6]}</td><td>{tar1}</td><td>{tar2}</td><td>{tar3}</td></tr>"
    html += student + teacher
    html += "</table></div></body></html>"
    html = html.replace("'", "\"")
    os.chdir(mainpath)
    with open(f"templates/studentdata.html", "w", encoding="utf-8") as file:
        file.write(html)
        os.chdir(mainpath) 