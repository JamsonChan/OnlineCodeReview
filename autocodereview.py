from sql_connect import sql_connect
import os
from mainpath import mainpath, mainpost, is_permissions_set
from sqlquries import auto_code_review
def create_review_html(homework_number, isAnonymous, auther_random_id, session_student_id, session_random_id):
    connection = sql_connect()
    sql_cursor = connection.cursor()
    sql_cursor.execute(auto_code_review(homework_number, session_student_id, session_random_id, isAnonymous))
    result = sql_cursor.fetchall()
    sql_cursor.execute(f"SELECT * FROM ReviewTarget WHERE homework_number = '{homework_number}' AND random_id = {session_random_id}")
    
    review_targets = sql_cursor.fetchall()
    review_targets = review_targets[0][2:] if review_targets else []
    sql_cursor.close()
    connection.close()

    html = f"""
    <!DOCTYPE html>
    <head>
        <meta charset='UTF-8'>
        <link rel="icon" href="https://cdn-icons-png.flaticon.com/512/328/328201.png" type="image/x-icon"/> 
        <title>程式碼審查</title>
        <style type="text/css">
                body, html{{font-family:consolas;width: 99.7%;height: 100%; background:url("/img/codereview_background.jpg");background-size: cover;background-attachment: fixed;background-position: center;}}
                .main {{width: 80%;margin: 20px auto;background-color: #ffffff88;}}
                form {{display:inline-block;}}
                table {{border-spacing: 0;width: 100%; border:7px #FFD382 groove;}}
                tr {{text-align: center;}}
                th {{border-color:#000;border-width:1px;border-style:solid;padding:15px;}}
                td {{border-color:#000;border-width:1px;border-style:solid;padding:5px;}}
                table thead {{background-color: blue;color: white;}}
                table thead th:first-child {{border-radius: 5px 0 0 0;border: 1px solid blue;}}
                .but{{font-size: 23px;width: 300px;min-height: 20px;display: block;background-color: #07070785;border: 2px solid #bccdf3;color: #fff;padding: 14px;font-size: 19px;line-height: normal;border-radius: 10px;cursor: pointer; font-family: consolas;}}
                .but:hover {{background-color: #fcfcfc85;color: rgb(2, 0, 0);}}
                a:hover {{font-size:22px; font-weight: bolder;}}
                .x{{}}
        </style>
        <script type="text/javascript">

            function switch_like(hwn, author_random_id) {{
            
                var like_obj = document.getElementById('like_' + author_random_id.toString());
                var like = like_obj.innerHTML;
                var count_obj = document.getElementById('count_' + author_random_id.toString());
                var count = Number(count_obj.innerHTML);

                var req = new XMLHttpRequest();
                req.onreadystatechange = function(){{
                    if(this.readyState == 4 && this.status == 200){{
                        count_obj.innerHTML = this.responseText;
                    }}
                }}

                req.open('POST', '/codelike', true);
                req.setRequestHeader('content-type', 'application/x-www-form-urlencoded;charset=UTF-8');

                if (like == '👍🏿'){{
                    like_obj.innerHTML = '👍';
                    req.send("count=" + count
                            + "&like_type=add"
                            + "&homework_number=" + hwn
                            + "&author_random_id=" + author_random_id);
                }}
                else{{
                    like_obj.innerHTML = '👍🏿';
                    req.send("count=" + count
                            + "&like_type=minus"
                            + "&homework_number=" + hwn
                            + "&author_random_id=" + author_random_id);
                }}
            }}

            function who_like(hwn, id){{
                var obj = document.getElementById('who_like_' + id.toString());
                var req = new XMLHttpRequest();
                req.onreadystatechange = function(){{
                    if(this.readyState == 4 && this.status == 200){{
                        obj.innerHTML = this.responseText;
                    }}
                }}
                req.open('POST', '/codewholike', true);
                req.setRequestHeader('content-type', 'application/x-www-form-urlencoded;charset=UTF-8');
                req.send("homework_number=" + hwn
                        + "&id=" + id);
            }}
        </script>
    </head>
    <body>
        <div style = "text-align: center; padding:30px">
            <form action="/member_homepage/{homework_number}"><button class="but">返回作業專區</button></form>
        </div>
        <div class="main" style="float:left; width: 2%;"></div>
            <div class="main" style="float:left; width: 26%; height:72%; overflow-y:auto; margin-top: 1.5%; background-size: cover;">
                <table style="border-collapse:collapse;word-break:keep-all;white-space:nowrap;font-size:20px;">
                    <tr style="color:#fff;background-color:#FF5F5F;font-size:22px;">
    """
    html += "<th>狀態</th><th>" + ("編號" if isAnonymous else "審查名單") + "</th><th>讚數</th><th>留言</th></tr>"
    codes = ["", "", ""] # 自己的code, 被分配到的code, 其他的code
    dialog = "<script type='text/javascript'>"
    for i, row in enumerate(result):
        sql_student_id, sql_name, sql_random_id, sql_file_name, sql_like_count, sql_islike, sql_comment_num = row

        # 第1行為自己的code，234行為要review的code，其他行照random_id排後面
        if sql_random_id == session_random_id: # 第1行:自己的code
            style = "style = 'background-color:rgba(58, 233, 58, 0.459);'"
            code_type = 0
        elif sql_random_id in review_targets: # 第234行:被分配到的code
            style = "style = 'background-color:rgba(49, 134, 245, 0.514);'"
            code_type = 1
        else: # 其他的code
            style = ""
            code_type = 2

        # 作業有無100
        accept = bool(sql_file_name)
        # 作業連結(100分才有)
        code_review_page = f"href='/codereview/{homework_number}/{sql_random_id}'" # if accept else ""

        codes[code_type] += f"<tr {style}>"
        # ✅:100分 ❌:沒100
        codes[code_type] += f"<td>✅</td>" if accept else f"<td>❌</td>"
        if isAnonymous: codes[code_type] += f"<td><a {code_review_page} style='text-decoration:none;color:black;'>{sql_random_id}</a></td>"
        else:           codes[code_type] += f"<td><a {code_review_page} style='text-decoration:none;color:black;'>{sql_student_id[1:]} {sql_name}</a></td>"
        # 顯示該學生對所有程式碼的按讚狀態(👍或👍🏿)
        codes[code_type] += f"""<td><a style = 'cursor:pointer' id='like_{sql_random_id}' onclick="switch_like('{homework_number}', {sql_random_id})">{'👍' if sql_islike else '👍🏿'}</a>"""
        # 顯示該程式碼被按讚次數(若0讚則不顯示數字)
        sql_like_count = sql_like_count if sql_like_count != 0 else ""
        codes[code_type] += f"""<a style = 'cursor:pointer' id='count_{sql_random_id}' onclick="who_like('{homework_number}', {sql_random_id})">{sql_like_count}</a>"""
        # 製作按讚人dialog列表
        codes[code_type] += f"""
                <dialog style="border-width:0px;padding:10px;font-size:30px;background-color:#232935ee;border-radius:25px;" id="infoModal_{sql_random_id}">
                    <div><button style = "cursor:pointer;float:right;background-color:#00000000;color:white;border-width:0px;font-size:30px;padding:0px" id="close_{sql_random_id}">x</button></div><br>
                    <div style="text-align:center;color:white;" id="who_like_{sql_random_id}"></div>
                </dialog></td>
        """
        codes[code_type] += f"<td>{sql_comment_num}</td>"
        # print(sql_student_id, sql_comment_num)
        codes[code_type] += "</tr>"
        # dialog javascript 定義
        dialog += f"""
                var num_{sql_random_id} = {sql_random_id};
                var btn_{sql_random_id} = document.getElementById("count_" + num_{sql_random_id}.toString());
                var infoModal_{sql_random_id} = document.getElementById("infoModal_" + num_{sql_random_id}.toString());
                btn_{sql_random_id}.addEventListener("click", () => {{
                    infoModal_{sql_random_id}.showModal();
                }})
                var close_{sql_random_id} = document.getElementById("close_" + num_{sql_random_id}.toString());
                close_{sql_random_id}.addEventListener("click", () => {{
                    infoModal_{sql_random_id}.close();
                }})"""
    # for xxx in codes:
    #     print(xxx)
    html += "".join(codes)
    dialog += "</script>"

    # iframe 程式碼頁面
    html += f"""
        </table></div>
            <div style="white-space:nowrap; float:right; width: 70%;">
                <iframe 
                        frameborder="0"
                        scrolling="yes"
                        allowtransparency="no"
                        noresize="noresize"
                        align="right"
                        style="position: relative; background: block; width: 100%; height: 82vh;"
                        src="http://{mainpost}/codepage/{homework_number}/{auther_random_id}">
                </iframe>
            </div>
            <div class="main" style="float:right; width: 3%;"></div>
        """ + dialog + """
        </body></html>
    """
    os.chdir(mainpath)    
    with open(f"templates/codereview.html", "w", encoding="utf-8") as file:
        file.write(html)
        os.chdir(mainpath) 