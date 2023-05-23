import os
from mainpath import mainpath, mainpost
def create_member_home_page(hw_num ,random_id):
    final_html = f"""
    <!DOCTYPE html>
    <html>
        <head>
            <meta charset="utf-8" >
            <link rel="icon" href="https://cdn-icons-png.flaticon.com/512/328/328201.png" type="image/x-icon"/> 
            <title>會員作業頁面</title>
            <style type="text/css">       
                html{{width: 100%;height: 100%;overflow: hidden;font-style: sans-serif; }}   
                body{{width: 100%;height: 100%;font-family: 'Open Sans',sans-serif;margin: 0; background-color: #37464a; background:url("/img/homepage_background.jpg");background-size: cover;background-attachment: fixed;background-position: center;}}
                #login{{position: fixed;top: 50%;left:31%;transform: translate(-50%,-50%);background:#2329358e;text-align: center;border-radius: 40px;padding: 30px;}}  
                #login h1{{color: #fff;   text-shadow:0 0 10px;   letter-spacing: 5px;   text-align: center;white-space:nowrap;}}
                #login h3{{color: #fff;   text-shadow:0 0 10px;   letter-spacing: 5px;   text-align: center;white-space:nowrap;}} 
                .but{{width: 310px;min-height: 20px;display: block;background-color: #07070785;border: 2px solid #bccdf3;color: #fff;padding: 12px 20px;font-size: 16px;line-height: normal;border-radius: 100px;cursor: pointer; font-family: consolas;}}
                .but:hover {{background-color: #fcfcfc85;color: rgb(2, 0, 0);}}
                .but_old{{width: 267px;min-height: 50px;display: block;background-color: #52747a78;border: 2px solid #f0f0ed;color: rgb(26, 24, 24);padding: 9px 14px;font-size: 15px;margin-left:1%;cursor: pointer; border-radius: 10px;}}
                ul {{margin: 0;padding: 0;list-style: none;}}/* 取消ul預設的內縮及樣式*/ 
                ul.drop-down-menu {{border: rgba(245, 241, 241, 0.548) 2px solid;display: inline-block;font-family: 'Open Sans', consolas, sans-serif;font-size: 13px;}}
                ul.drop-down-menu li {{position: relative;white-space: nowrap;border-right: #ccc 1px solid;}}
                ul.drop-down-menu > li:last-child {{border-right: none;}}
                ul.drop-down-menu > li {{float: left;}} /* 只有第一層是靠左對齊*/ 
                ul.drop-down-menu a {{background-color: rgba(20, 20, 20, 0.466);color: rgb(253, 161, 22);display: block;padding: 0 40px;text-decoration: none;line-height: 70px;font-size: 200%; font-family: consolas;font-weight:bold;}}
                ul.drop-down-menu a:hover {{background-color: #ef5c28;color: #fff;}} /* 滑鼠滑入按鈕變色*/
                ul.drop-down-menu li:hover > a {{background-color: #ef5c28;color: #fff;}} /* 滑鼠移入次選單上層按鈕保持變色*/
                ul.drop-down-menu button {{background-color: rgba(7, 1, 1, 0.616);color: rgb(245, 244, 244);display: block;padding: 0 40px;text-decoration: none;line-height: 40px;cursor:pointer;font-family: consolas;font-size: 150%;}}
                ul.drop-down-menu button:hover {{background-color: #ef5c28;color: #fff;}} /* 滑鼠滑入按鈕變色*/
                ul.drop-down-menu li:hover > button {{background-color: #ef5c28;color: #fff;}} /* 滑鼠移入次選單上層按鈕保持變色*/
                ul.drop-down-menu ul {{display: none;left: 99999px;opacity: 0;-webkit-transition: opacity 0.3s;transition: opacity 0.3s;}} /*隱藏次選單*/
                ul.drop-down-menu li:hover > ul {{display: block;opacity: 1;-webkit-transition: opacity 0.3s;transition: opacity 0.3s;left: -1px;border-right: 5px;}} /* 滑鼠滑入展開次選單*/
                ul.drop-down-menu li:hover > ul ul {{left: 99999px;}} /* 滑鼠滑入之後、次選單之後的選單依舊隱藏*/
                ul.drop-down-menu ul li:hover > ul {{left: 90%;}} /* 第二層之後的選單展開位置*/
            </style>
        </head>
        <body></br></br>
            <div style="float:left; width: 1%; height: 100%;"></div>
            <ul class="drop-down-menu">
                <li><a href="#">Homework {hw_num[2:]} ⏬</a>
                    <ul></br>                       
                        <li><form action="/member_homepage/hw1"><button class="but_old">Homework 1</button></form></li></br>                        
                        <li><form action="/member_homepage/hw2"><button class="but_old">Homework 2</button></form></li></br>
                   <!-- <li><form action="/member_homepage/hw3"><button class="but_old">Homework 3</button></form></li> -->
                   <!-- <li><form action="/member_homepage/hw4"><button class="but_old">Homework 4</button></form></li> -->
                        <li><button class="but_old">Comeing Soon</button></li></br>
                    </ul>
                </li>
            </ul>
            <div id="login">
                <h1>{{{{ message1 }}}}</h1>
                <h3>{{{{ message2 }}}}</h3>
                <h3>{{{{ message3 }}}}</h3>
                <form action="/goUpload/{hw_num}">
                    <button class="but">🚀 上傳檔案 🚀</button><br/>
                </form>
                <form action="/rank_best/{hw_num}", method="GET">
                    <button type="submit" class="but" name="rank_best" value="student_id">🏆 排行榜 🏆</button><br/>
                </form>
                <form action="/codereview/{hw_num}/{random_id}">
                    <button class="but">📄 程式碼審查 📄</button><br/>
                </form>
                <form action="/homepage/{hw_num}">
                    <button class="but">🏠 返回會員首頁 🏠</button><br/>
                </form>
           <!-- <form action="/signout">
                    <button class="but">👋 登出 👋</button><br/>
                </form> -->
            </div>
            <div class="main" style="float:right; width: 3%; height: 100%;"></div>
            <div style="white-space:nowrap; float:right; width: 50%;">
                <iframe 
                        frameborder="0"
                        scrolling="yes"
                        allowtransparency="no"
                        noresize="noresize"
                        align="right"
                        style="position: relative; background: block; width: 100%; height: 88vh;"
                        src="http://{mainpost}/display_homework/{hw_num}_description">
                </iframe>
            </div>
        </body>
    </html>
    """
    final_html = final_html.replace("'", "\"")
    os.chdir(mainpath)
    with open(f"templates/member_homepage.html", "w", encoding="utf-8") as file:
        file.write(final_html)
        os.chdir(mainpath)

