import os
from mainpath import mainpath, mainpost
def create_auto_goUpload(hw_num):
    final_html = f"""
        <!DOCTYPE html>
        <html>
            <head>
                <link rel="icon" href="https://cdn-icons-png.flaticon.com/512/328/328201.png" type="image/x-icon"/> 
                <meta charset="UTF-8">
                <title>作業檔案上傳</title>
                <style type="text/css">
                    html{{   width: 100%;   height: 100%;   overflow: hidden;   font-style: sans-serif;   }}   
                    body{{width: 100%;height: 100%;font-family: 'Open Sans',sans-serif;margin: 0; background-color: #37464a; background:url("/img/upload_background.png");background-size: cover;background-attachment: fixed;background-position: center;}}
                    #login{{position: fixed;top: 50%;left:31%;transform: translate(-50%,-50%);background:#2329358e;text-align: center;border-radius: 40px;padding: 30px;}}  
                    #login h1{{   color: #fff;   text-shadow:0 0 10px;   letter-spacing: 5px;   text-align: center;white-space:nowrap;}}   
                    .but{{width: 310px;min-height: 20px;display: block;background-color: #07070785;border: 2px solid #bccdf3;color: #fff;padding: 12px 20px;font-size: 16px;line-height: normal;border-radius: 100px;cursor: pointer; font-family: consolas;}}
                    .but:hover {{background-color: #fcfcfc85;color: rgb(2, 0, 0);}}
                    input{{border: 2px solid #ccc; border-radius: 20px;padding: 6px; width: 200px; font-size: 15px; font-family:consolas; background-color:rgba(255, 255, 255, 0.486); color:red; font-family:consolas;}}                 
                </style>
            </head>
            <body>
                <div id="login">
                    <h1>{{{{ message1 }}}}</h1>
                    <h1>{{{{ message2 }}}}</h1>
                    <form action="/upload" enctype="multipart/form-data" method="POST">
                        <input type="file" name="file"><br/>
                        <br/>
                        <button class="but">👌 送出 👌</button><br/>
                    </form>
                    <form action="/member_homepage/{hw_num}">
                        <button class="but">返回作業專區</button>
                    </form>
                </div>
                <div class="main" style="float:top; height: 7%;"></div>
                <div class="main" style="float:right; width:3%; height: 100%;"></div>
                <div style="white-space:nowrap; float:right; width: 50%;">
                    <iframe 
                            frameborder="0"
                            scrolling="yes"
                            allowtransparency="no"
                            noresize="noresize"
                            align="right"
                            style="position: relative; background: block; width: 100%; height: 85vh;"
                            src="http://{mainpost}/display_homework_rules">
                    </iframe>
                </div>
            </body>
        </html>
    """
    final_html = final_html.replace("'", "\"")
    os.chdir(mainpath)
    with open(f"templates/goUpload.html", "w", encoding="utf-8") as file:
        file.write(final_html)
        os.chdir(mainpath)

