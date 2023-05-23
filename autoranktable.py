import os
from sql_connect import sql_connect  # 連結 MySQL 資料庫
import sqlquries
from mainpath import mainpath

def rank_table_html(hw_num, rank_type, attribute, session_id):  # 生成html排行榜表格
    upload_type = "count" if rank_type == "best" else "time"
    upload_type_zh = "上傳次數" if rank_type == "best" else "上傳時間"
    connection = sql_connect()
    sql_cursor = connection.cursor()
    sql_queries = sqlquries.rank_best_sql(hw_num, attribute) if rank_type == "best" else sqlquries.rank_all_sql(hw_num, attribute)
    sql_cursor.execute(sql_queries)  # 取得表格所有資料
    result = sql_cursor.fetchall()
    html = f"""
            <!DOCTYPE html>
            <head>
                <meta charset='UTF-8'>
                <link rel="icon" href="https://cdn-icons-png.flaticon.com/512/328/328201.png" type="image/x-icon"/> 
                <title>排名</title>
                <style type="text/css">
                    body{{width: 100%;height: 100%;padding: 0;font-family:'consolas',sans-serif;margin: 0;background:url("/img/rank_background.jpeg");background-size: cover;background-attachment: fixed;background-position: center;}}
                    .main_but{{width: 300px;min-height: 20px;display: block;background-color: #07070785;border: 2px solid #bccdf3;color: #fff;padding: 18px 20px;font-size: 18px;line-height: normal;border-radius: 10px;cursor: pointer; font-family: consolas;}}
                    .main_but:hover {{background-color: #fcfcfc85;color: rgb(2, 0, 0);}}
                    .sort_but{{border-width:0px; text-align: center;display: block;background-color:#FF5F5F;color:#fff;font-size: 23px;cursor: pointer;}}
                    .sort_but:hover {{background-color: #fcfcfc85;color: rgb(2, 0, 0);}}
                    .main {{font-family:consolas;}}
                    form {{display:inline-block;}}
                    table {{background-color: #ffffffa9;border-collapse:collapse;word-break:keep-all;white-space:nowrap;font-size:22px;margin-left: auto; margin-right: auto; width:80%; border-spacing: 0; border:7px #FFD382 groove;}}
                    tr {{text-align: center;color:#fff;font-size:22px;}}
                    th {{position:sticky;top:0;font-weight:normal;background-color:#FF5F5F;border-color:#000;border-width:1px;border-style:solid;padding:15px;font-size:23px;}}
                    td {{color:black;border-color:#000;border-width:1px;border-style:solid;padding:5px;}}
                </style>
            </head>

            <body>
                <div style = "text-align: center;padding:30px">
                    <form action="/rank_best/{hw_num}" method="GET"><button type="submit" class="main_but" name="rank_best" value="student_id">最佳排行</button></form>
                    <form action="/rank_all/{hw_num}" method="GET"><button type="submit" class="main_but" name="rank_all" value="upload_time">總體排行</button></form>
                    <form action="/member_homepage/{hw_num}"><button class="main_but">返回作業專區</button></form>
                </div>

                <div class='main'>
                    <table>
                        <tr>
                """
    html += f"""
                <th>編號</th>
                <th><form action="/rank_{rank_type}/{hw_num}" method="GET"><button type="submit" class="sort_but" name="rank_{rank_type}" value="student_id">學號姓名🔽</button></form></th>
                <th><form action="/rank_{rank_type}/{hw_num}" method="GET"><button type="submit" class="sort_but" name="rank_{rank_type}" value="time">花費時間(ms)🔽</button></form></th>
                <th><form action="/rank_{rank_type}/{hw_num}" method="GET"><button type="submit" class="sort_but" name="rank_{rank_type}" value="memory">記憶體使用量(MB)🔽</button></form></th>
                <th><form action="/rank_{rank_type}/{hw_num}" method="GET"><button type="submit" class="sort_but" name="rank_{rank_type}" value="upload_{upload_type}">{upload_type_zh}🔽</button></form></th>
            """
    if rank_type == "all":
        html += f"""
                <th>檔名</th>
                <th><form action="/rank_{rank_type}/{hw_num}" method="GET"><button type="submit" class="sort_but" name="rank_{rank_type}" value="score">分數🔽</button></form></th>
                """
  
    for row in result:
        html += "<tr style = 'background-color:#53FF5366'>" if row[1][:7] == session_id[1:] else "<tr>"
        html += f"<td>{row[0]}</td><td>{row[1]}</td><td>{row[2]}</td><td>{row[3]}</td><td>{row[4]}</td>"
        if rank_type == "all":
            html += f"<td>{row[5]}</td><td>{row[6]}</td>"
        html += "</tr>"

    html += "</table></div></br></br></body></html>"
    html = html.replace("'", "\"")
    os.chdir(mainpath)
    with open(f"templates/rank_{rank_type}.html", "w", encoding="utf-8") as file:
        file.write(html)
        os.chdir(mainpath) 
    sql_cursor.close()
    connection.close()