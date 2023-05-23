import os
from sql_connect import sql_connect  # 連結 MySQL 資料庫
import sqlquries
from mainpath import mainpath

def create_hero_rank_html(hw_num, session_id):  # 生成html排行榜表格
    connection = sql_connect()
    sql_cursor = connection.cursor()
    sql_queries = sqlquries.hero_rank_sql()
    sql_cursor.execute(sql_queries)  # 取得表格所有資料
    result = sql_cursor.fetchall()
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
                    table {{background-color: #ffffffa9;border-collapse:collapse;word-break:keep-all;white-space:nowrap;font-size:22px;margin-left: auto; margin-right: auto; width:80%; border-spacing: 0; border:7px #FFD382 groove;}}
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
    # # 三種獎牌分別顯示
    # <th>金牌</th>
    # <th>銀牌</th>
    # <th>銅牌</th>
    html += f"""
                <th>編號</th>
                <th>學號姓名</th>
                <th>獎牌</th>
                <th>總分</th>
                <th>上傳次數</th>
            """
  
    for row in result:
        html += "<tr style = 'background-color:#53FF5366'>" if row[1] == session_id else "<tr>"
        html += f"<td>{row[0]}</td><td>{row[1][1:]} {row[2]}</td><td>{row[3]}</td><td>{row[4]}</td><td>{row[5]}</td></tr>"

    html += "</table></div></br></br></body></html>"
    html = html.replace("'", "\"")
    os.chdir(mainpath)
    with open(f"templates/herorank.html", "w", encoding="utf-8") as file:
        file.write(html)
        os.chdir(mainpath) 
    sql_cursor.close()
    connection.close()