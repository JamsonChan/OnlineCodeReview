import os
from sql_connect import sql_connect  # 連結 MySQL 資料庫
import sqlquries
from mainpath import mainpath

def create_total_semester_grade_html(student_id, hw_num):  # 生成html排行榜表格
    connection = sql_connect()
    sql_cursor = connection.cursor()

    html = f"""
            <!DOCTYPE html>
            <head>
                <meta charset='UTF-8'>
                <link rel="icon" href="https://cdn-icons-png.flaticon.com/512/328/328201.png" type="image/x-icon"/> 
                <title>英雄榜</title>
                <style type="text/css">
                    body{{width: 100%;height: 100%;padding: 0;font-family:'consolas',sans-serif;margin: 0;background:url("/img/herorank_background.jpg");background-size: cover;background-attachment: fixed;background-position: center;}}
                    .main_but{{width: 300px;min-height: 20px;display: block;background-color: #07070785;border: 2px solid #bccdf3;color: #fff;padding: 18px 20px;font-size: 18px;line-height: normal;border-radius: 10px;cursor: pointer; font-family: consolas;}}
                    .main_but:hover {{background-color: #fcfcfc85;color: rgb(2, 0, 0);}}
                    .sort_but{{border-width:0px; text-align: center;display: block;background-color:#FF5F5F;color:#fff;font-size: 23px;cursor: pointer;}}
                    .main {{font-family:consolas;}}
                    form {{display:inline-block;}}
                    table {{background-color: #ffffffa9;border-collapse:collapse;word-break:keep-all;white-space:nowrap;font-size:22px;margin-left: auto; margin-right: auto; width:60%; border-spacing: 0; border:7px #FFD382 groove;}}
                    tr {{text-align: center;color:#fff;font-size:22px;}}
                    th {{position:sticky;top:0;font-weight:normal;background-color:#FF5F5F;border-color:#000;border-width:1px;border-style:solid;padding:15px;font-size:23px;}}
                    td {{color:black;border-color:#000;border-width:1px;border-style:solid;padding:5px;}}
                </style>
            </head>

            <body>
                <div style = "text-align: center;padding:30px">
                    <form action="/homepage/{hw_num}"><button class="main_but">返回會員首頁</button></form>
                </div>

                <div class='main'>
                    <table>
                        <tr>
                """

    html += f"""
                <th>Homework Number</th>
                <th>死線</th>
                <th>上傳次數</th>
                <th>分數</th>
                <th>累計平均</th>
                </tr>
            """
    sql_queries = sqlquries.homework_score(student_id)
    sql_cursor.execute(sql_queries)  # 取得表格所有資料
    result = sql_cursor.fetchall()
    for row in result:
        html += f"<tr><td>{row[0]}</td><td>{row[1]}</td><td>{row[2]}</td><td>{row[3]}</td><td>{row[4]}</td></tr>"
    
    html += "</table><table></br></br><tr>"

    sql_queries = sqlquries.total_semester_grade(student_id)
    sql_cursor.execute(sql_queries)  # 取得表格所有資料
    result = sql_cursor.fetchall()

    html += f"""
                <th>作業總平均</th>
                <th>期中考</th>
                <th>期末考</th>
                </tr>
            """
    
    for row in result:
        html += f"<tr><td>{row[0]}</td><td>{row[1]}</td><td>{row[2]}</td></tr>"
    
    html += "</table></div></br></br></body></html>"
    html = html.replace("'", "\"")
    sql_cursor.close()
    connection.close()
    os.chdir(mainpath)
    with open(f"templates/portal_grades.html", "w", encoding="utf-8") as file:
        file.write(html)
        os.chdir(mainpath) 
