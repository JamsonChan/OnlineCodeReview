import os
from mainpath import mainpath
def checkMistakeHtml(result, hw_num, student_id):
    html = f"""
    <!DOCTYPE html>
    <head>
        <meta charset='UTF-8'>
        <link rel="icon" href="https://cdn-icons-png.flaticon.com/512/328/328201.png" type="image/x-icon"/> 
        <title>錯誤題目</title>
        <style type="text/css">
            .main {{font-family:consolas;}}
            form {{dispaly:inline-block;}}
            body {{width: 100%;height: 100%;padding: 0;font-family:'consolas',sans-serif;margin: 0;background:url("/img/upload_background.png");background-size: cover;background-attachment: fixed;background-position: center;}}
            table {{word-wrap:break-word; word-break:break-all;background-color: #ffffffa9;border-collapse:collapse;word-break:keep-all;font-size:22px;margin-left: auto; margin-right: auto; width:80%; border-spacing: 0; border:7px #FFD382 groove;}}
            tr {{text-align: center;color:#fff;font-size:22px;}}
            th {{position:sticky;top:0;font-weight:normal;background-color:#FF5F5F;border-color:#000;border-width:1px;border-style:solid;padding:15px;font-size:23px;}}
            td {{word-break: break-all;color:black;border-color:#000;border-width:1px;border-style:solid;padding:5px;}}
            .but {{width: 310px;min-height: 20px;display: block;background-color: #07070785;border: 2px solid #bccdf3;color: #fff;padding: 12px 20px;font-size: 16px;line-height: normal;border-radius: 10px;cursor: pointer; font-family: consolas;}}
            .but:hover {{background-color: #fcfcfc85;color: rgb(2, 0, 0);}}
        </style>
    </head>
    <body style='background-color: #37464a;'>
        <div style = "text-align:center; padding:30px">
            <form action="/goUpload/{hw_num}" style="display:inline-block;"><button class="but"style="font-size: 23px;">返回上傳</button></form>
            <form action="/member_homepage/{hw_num}" style="display:inline-block;"><button class="but"style="font-size: 23px;">返回作業專區</button></form>
        </div>
        <div class='main'>
        <table style="border-collapse:collapse;word-break:keep-all;font-size:22px;table-layout:fixed;">
        <tr style="color:#fff;background-color:#48a6fb;font-size:22px;">
    """
    html += "<th>錯誤題號</th><th>錯誤題目</th><th>您的答案</th><th>正確答案</th></tr>"
    for row in result:
        html += f"<tr><td>{row[0]}</td><td>{row[1]}</td><td>{row[2]}</td><td>{row[3]}</td></tr>"
    html += "</table></div></br></br></body></html>"
    html = html.replace("'", "\"")
    os.chdir(mainpath)
    with open(f"templates/checkMistake.html", "w", encoding="utf-8") as file:
        file.write(html)
        os.chdir(mainpath) 