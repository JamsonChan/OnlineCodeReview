import os
from mainpath import mainpath
def create_homepage_error(hw_num):
    final_html = f"""
        <!DOCTYPE html>
        <html>
            <head>
                <meta charset="utf-8" >
                <link rel="icon" href="https://cdn-icons-png.flaticon.com/512/328/328201.png" type="image/x-icon"/> 
                <title>MESSAGE</title>
                <style type="text/css">
                    html{{width: 100%; height: 100%; overflow: hidden; font-style: sans-serif;}}   
                    body{{width: 100%;height: 100%;font-family: 'Open Sans',sans-serif;margin: 0; background-color: #37464a; background:url("/img/homepage_background.jpg");background-size: cover;background-attachment: fixed;background-position: center;}}
                    #login{{position: fixed;top: 50%;left:50%;transform: translate(-50%,-50%);background:#2329358e;text-align: center;border-radius: 40px;padding: 30px;}}  
                    #login h1{{color: #fff; text-shadow:0 0 10px; letter-spacing: 0px; text-align: center;}}  /* letter-spacing: 5px */
                    #login h2{{color: rgb(0, 0, 0); letter-spacing: 5px; text-align: center;}}
                    .but{{width: 310px;min-height: 20px;display: block;background-color: #07070785;border: 2px solid #bccdf3;color: #fff;padding: 12px 20px;font-size: 16px;line-height: normal;border-radius: 10px;cursor: pointer; font-family: consolas;}}
                    .but:hover {{background-color: #fcfcfc85;color: rgb(2, 0, 0);}}
                </style>
            </head>
            <body>
                <div id="login">
                    <h1>{{{{ message }}}}</h1> <!-- 區塊段落 -->
                    <form action="/homepage/{hw_num}">
                        <button class="but">↩️ 返回會員首頁 ↩️</button><br/>
                    </form>
                </div>
            </body>
        </html>
    """
    final_html = final_html.replace("'", "\"")
    os.chdir(mainpath)
    with open(f"templates/homepageerror.html", "w", encoding="utf-8") as file:
        file.write(final_html)
        os.chdir(mainpath)

