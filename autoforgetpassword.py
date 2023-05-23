import os
from mainpath import mainpath
def create_forget_password_html(student_id, new_password1, new_password2):
    html = f"""
        <!DOCTYPE html>
        <html>

        <head>
            <meta charset="utf-8">
            <title>Forget Password</title>
            <style type="text/css">
                html{{   width: 100%;   height: 100%;   overflow: hidden;   font-style: sans-serif;   }}   
                body{{width: 100%;height: 100%;padding: 0;font-family:'Open Sans',sans-serif;margin: 0;background: url("/img/Background.jpg");background-size: cover;background-attachment: fixed;background-position: center;}} 
                #login{{position: fixed;top: 50%;left:50%;transform: translate(-50%,-50%);background:rgba(0, 0, 0, 0.5);text-align: center;border-radius: 10px;padding: 30px;}}   
                #login h1{{   color: #fff;   text-shadow:0 0 10px;   letter-spacing: 1px;   text-align: center;   }}   
                h1{{   font-size: 2em;   margin: 0.67em 0;   }}   
                input{{   width: 278px;   height: 18px;   margin-bottom: 10px;   outline: none;   padding: 10px;   font-size: 13px;   color: #fff;   border-top: 1px solid #312E3D;   border-left: 1px solid #312E3D;   border-right: 1px solid #312E3D;   border-bottom: 1px solid #56536A;   border-radius: 4px;   background-color: #2D2D3F;   }}   
                .but{{width: 310px;min-height: 20px;display: block;background-color: #07070785;border: 2px solid #bccdf3;color: #fff;padding: 12px 20px;font-size: 16px;line-height: normal;border-radius: 10px;cursor: pointer; font-family: consolas;}}
                .but:hover {{background-color: #fcfcfc85;color: rgb(2, 0, 0);}}
                .select_style select{{ padding:5px;background:transparent; width:268px; font-size:16px; border:none; height:30px; -webkit-appearance:none; /*for Webkit browsers*/ }} 
            </style>
        </head>

        <body>
            <div id="login">
                <h1>忘記密碼</h1>
                <form action="/reflash" , method="POST">
                    <input type="text" placeholder="帳號" required="required" name="studentid" value="{student_id}"/><br/>
                    <input type="password" placeholder="新密碼" required="required" name="newpassword1" value="{new_password1}"/><br/>
                    <input type="password" placeholder="確認新密碼" required="required" name="newpassword2" value="{new_password2}"/><br/>
                    <input type="text" placeholder="驗證碼" required="required" name="verification"/><br/>
                    <button class="but">確定更改密碼</button><br/>
                </form>
                <form action="/">
                    <button class="but">返回</button>
                </form>
            </div>
        </body>

        </html>
    """
    html = html.replace("'", "\"")
    os.chdir(mainpath)
    with open(f"templates/forgetpassword2.html", "w", encoding="utf-8") as file:
        file.write(html)
        os.chdir(mainpath)
