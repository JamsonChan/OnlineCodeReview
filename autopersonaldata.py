import os
from mainpath import mainpath
def create_student_personal_data_html(hw_num, name, student_id, nickname, password):
    html = f"""
            <!DOCTYPE html>
            <html lang="en">
            <head>
                <meta charset="UTF-8">
                <link rel="icon" href="https://cdn-icons-png.flaticon.com/512/328/328201.png" type="image/x-icon"/> 
                <title>會員個人資料</title>
                <style type="text/css">
                    body{{width: 100%;height: 100%;font-family:"consolas",sans-serif;margin: 0;background:url("/img/picture.png");background-size: cover;background-attachment: fixed;background-position: center;}}
                    .main_but{{width: 300px;min-height: 20px;display: block;background-color: #07070785;border: 2px solid #bccdf3;color: #fff;padding: 18px 20px;font-size: 18px;line-height: normal;border-radius: 10px;cursor: pointer; font-family: consolas;}}
                    .main_but:hover {{background-color: #fcfcfc85;color: rgb(2, 0, 0);}}
                    #login{{background:rgba(0, 0, 0, 0.5);text-align: center;border-radius: 10px; width: 100%;height: 100%;}}
                    input{{width: 55%; outline: none;padding: 20px;font-size: 28px;color: #fff;border-radius: 4px;background-color: #2d2d3f88;}}
                    .but{{width: 40%;height:50px;background-color: #07070785;border: 2px solid #bccdf3;color: #fff;font-size: 16px;border-radius: 10px;cursor: pointer; font-family: consolas;}}
                    .but:hover{{background-color: #fcfcfc85;color: rgb(2, 0, 0);}}
                </style>
            </head>
            <body>
                <div style = "text-align: center;padding:30px">
                    <form action="/homepage/{hw_num}" style="display:inline-block;"><button class="main_but">返回會員首頁</button></form>
                </div>
                <div id="login"></br></br>
                    <div style="color: rgb(117, 7, 136); font-size: 30px; font-family: consolas;">姓名: <input type="text" disabled="disabled" value="{name}" /></div><br>
                    <div style="color: rgb(117, 7, 136); font-size: 30px; font-family: consolas;">學號: <input type="text" disabled="disabled" value="{student_id}" /></div><br>
                    <form action="/change_nickname/{hw_num}/{student_id}" method="POST">
                        <div style="color: rgb(117, 7, 136); font-size: 30px; font-family: consolas;">暱稱: <input type="text" disabled="disabled" value="{nickname}" /></div><br><button type="button" class="but" onclick="nickname_check(this.form)">更改暱稱</button><br><br>
                    </form>
                    <form action="/change_password/{hw_num}/{student_id}" method="POST">
                        <div style="color: rgb(117, 7, 136); font-size: 30px; font-family: consolas;">密碼: <input type="text" disabled="disabled" value="{password}"/> </div><br><button type="button" class="but" onclick="password_check(this.form)">更改密碼</button><br><br><br>
                    </form>
                </div>
                <script>
                    function nickname_check(form){{
                        if (confirm('確定要更改暱稱嗎?')){{
                            form.submit();
                        }}
                    }}
                    function password_check(form){{
                        if (confirm('確定要更改密碼嗎?')){{
                            form.submit();
                        }}
                    }}
                </script>
            </body>
            </html>
    """
    html = html.replace("'", "\"")
    os.chdir(mainpath)
    with open(f"templates/personal_data.html", "w", encoding="utf-8") as file:
        file.write(html)
        os.chdir(mainpath)