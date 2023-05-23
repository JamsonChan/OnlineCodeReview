import os
from mainpath import mainpath, mainpost
def create_leetcode_html(hw_num):
    html = f"""
            <!DOCTYPE html>
            <html>
            <head>
                <meta charset="UTF-8">
                <link rel="icon" href="https://cdn-icons-png.flaticon.com/512/328/328201.png" type="image/x-icon"/> 
                <title>休閒題目</title>
                <style type="text/css">
                    body, html{{width: 99.3%;height: 100%;font-family: consolas; background:url("/img/leetcode_background.jpg");background-size: cover;background-attachment: fixed;background-position: center;}}
                    form {{display:inline-block;}}
                    #sitebody{{width:100%;height:100%;font-size:13px;}}
                    #sidebar_left{{width:50%;height:64%;text-align:center;float:left;}}
                    #sidebar_right{{width:50%;height:72%;text-align:center;float:right;}}
                    #msgtextarea {{border:5px purple double; font-size:20px; color:white;background-color:black;width: 95%;height: 100%;resize: none;}}
                    .cmt {{border: 2px solid #bccdf3;color: #fff;font-size: 23px;background-color: #07070785;text-align: center;width: 150px;min-height: 40px;display: block;padding: 9px 14px;font-size: 18px;line-height: normal;border-radius: 5px;margin: 10px auto;cursor: pointer;}}
                    .cmt:hover {{background-color: #fcfcfc85;color: rgb(2, 0, 0);}}
                    .main_but{{width: 300px;min-height: 20px;display: block;background-color: #07070785;border: 2px solid #bccdf3;color: #fff;padding: 18px 20px;font-size: 18px;line-height: normal;border-radius: 10px;cursor: pointer; font-family: consolas;}}
                    .main_but:hover {{background-color: #fcfcfc85;color: rgb(2, 0, 0);}}
                </style>
            </head>
            <body>
                <!-- <script src="https://cdn.bootcss.com/marked/0.8.0/marked.js"></script> -->
                <!-- <link href="http://cdn.bootcss.com/highlight.js/8.0/styles/monokai_sublime.min.css" rel="stylesheet"> -->
                <!-- <script src="http://cdn.bootcss.com/highlight.js/8.0/highlight.min.js"></script> -->
                <!-- <script>hljs.initHighlightingOnLoad();</script> -->
                <script type="text/javascript">

                    function insertText(obj,str) {{
                    if (document.selection) {{
                        var sel = document.selection.createRange();
                        sel.text = str;
                    }} else if (typeof obj.selectionStart === 'number' && typeof obj.selectionEnd === 'number') {{
                        var startPos = obj.selectionStart,
                            endPos = obj.selectionEnd,
                            cursorPos = startPos,
                            tmpStr = obj.value;
                            // alert(tmpStr);
                        obj.value = tmpStr.substring(0, startPos) + str + tmpStr.substring(endPos, tmpStr.length);
                        cursorPos += str.length;
                        obj.selectionStart = obj.selectionEnd = cursorPos;
                    }} else {{
                        obj.value += str
                    }}
                }}

                    function moveEnd(obj){{
                        obj.focus();
                        var len = obj.value.length;
                        if (document.selection) {{
                            var sel = obj.createTextRange();
                            sel.moveStart('character',len);
                            sel.collapse();
                            sel.select();
                        }} else if (typeof obj.selectionStart == 'number' && typeof obj.selectionEnd == 'number') {{
                            obj.selectionStart = obj.selectionEnd = len;
                        }}
                    }}
                    //ctrl 是dom节点
                    function getCursortPosition(ctrl) 
                    {{
                        //获取光标位置函数 
                        var CaretPos = 0; 
                        // IE Support
                        if (document.selection) 
                        {{ 
                            ctrl.focus (); // 获取焦点
                            var Sel = document.selection.createRange (); // 创建选定区域
                            Sel.moveStart('character', -ctrl.value.length); // 移动开始点到最左边位置
                            CaretPos = Sel.text.length;                      // 获取当前选定区的文本内容长度
                        }} 
                        // Chrome、Firefox support (非ie)
                        else if (ctrl.selectionStart || ctrl.selectionStart == '0')
                        {{
                            CaretPos = ctrl.selectionStart; // 获取选定区的开始点 
                        }}
                        return CaretPos; 
                    }}
                    //ctrl 是dom节点，pos 是要定位到的位置
                    function setCaretPosition(ctrl, pos)
                    {{
                        //设置光标位置函数 
                        if(ctrl.setSelectionRange)   //非ie
                        {{
                            ctrl.focus();  // 获取焦点
                            ctrl.setSelectionRange(pos,pos);  // 设置选定区的开始和结束点
                        }} 
                        else if (ctrl.createTextRange)
                        {{ 
                            var range = ctrl.createTextRange();  // 创建选定区
                            range.collapse(true);                // 设置为折叠,即光标起点和结束点重叠在一起
                            range.moveEnd('character', pos);     // 移动结束点
                            range.moveStart('character', pos);   // 移动开始点
                            range.select();                      // 选定当前区域
                        }} 
                    }}
                    
                    function TextAreaTab(obj) {{
                        var oldPos = getCursortPosition(obj);
                        if(event.keyCode == 9){{ // tab
                            //do stm...
                            // alert(event.keyCode);
                            insertText(obj, "    ");
                            setCaretPosition(obj, oldPos+4);
                            window.setTimeout(function() {{
                                //document.getElementById("bt0").click();
                                obj.focus();
                            }}, 2);
                        }}
                        else if(event.keyCode == 13){{ // enter
                            var tab = '\\n';
                            if (obj.value[oldPos-1] == ':'){{
                                tab += "    ";
                            }}
                            var i = oldPos-1;
                            while (i != -1 && obj.value[i] != '\\n'){{
                                i -= 1;
                            }}
                            i += 1;
                            while (obj.value[i] == ' '){{
                                i += 1;
                                tab += ' ';
                            }}
                            insertText(obj, tab);
                            setCaretPosition(obj, oldPos + tab.length);
                            event.preventDefault();
                        }}
                        else if (event.keyCode == 8){{ // backspace
                            if ((obj.value[oldPos-1] == '\\"' && obj.value[oldPos] == '\\"') ||
                                (obj.value[oldPos-1] == '\\'' && obj.value[oldPos] == '\\'') ||
                                (obj.value[oldPos-1] == '(' && obj.value[oldPos] == ')') ||
                                (obj.value[oldPos-1] == '[' && obj.value[oldPos] == ']') ||
                                (obj.value[oldPos-1] == '{{' && obj.value[oldPos] == '}}')){{
                                obj.value = obj.value.slice(0, oldPos-1) + obj.value.slice(oldPos+1);
                                setCaretPosition(obj, oldPos-1);
                                event.preventDefault();
                            }}else if (obj.value[oldPos-1] == ' '){{
                                var curPos = oldPos-1;
                                var cnt = 0;
                                while (cnt != 4 && obj.value[curPos] == ' '){{
                                    cnt += 1;
                                    curPos -= 1;
                                }}
                                if (cnt == 4){{
                                    obj.value = obj.value.slice(0, oldPos-4);
                                    setCaretPosition(obj, oldPos-4);
                                    event.preventDefault();
                                }}
                            }}
                        }}
                    }}
                    
                    function TextAreaPair(obj){{
                        var oldPos = getCursortPosition(obj);
                        if(event.keyCode == 222){{ // " and '
                            var pair = obj.value[oldPos-1];
                            insertText(obj, pair);
                            setCaretPosition(obj, oldPos);
                        }}else if(event.keyCode == 219){{ // [] and {{}}
                            var pair = obj.value[oldPos-1];
                            if (pair == '[') pair = ']';
                            else if (pair == '{{') pair = '}}';
                            insertText(obj, pair);
                            setCaretPosition(obj, oldPos);
                        }}else if(event.keyCode == 57){{ // ()
                            insertText(obj, ')');
                            setCaretPosition(obj, oldPos);
                        }}
                }}
                </script>


            <!-- enter -> pre line 以幾個空格開頭，就加幾個空格；若 pre line 以:結尾，則額外加4個空格 -->

                <div id="sitebody">
                    <div style="text-align: center;padding:30px">
                        <form action="/homepage/{hw_num}"><button class="main_but">返回會員首頁</button></form>
                    </div>
                    <form id="sidebar_left" action="/leetcode_correction/{hw_num}" method="POST"></br></br>
                        <textarea id="msgtextarea" class="tabIndent" placeholder ="You can coding here..." required="required" name="leetcode_comment" onkeydown="TextAreaTab(this)" onkeyup="TextAreaPair(this)" autofocus="autofocus"></textarea></br>
                        <!-- <script>tabIndent.renderAll();</script> -->
                        <button class="cmt">Submit</button>
                    </form>
                    <div id="sidebar_right">
                        <iframe 
                                frameborder="0"
                                scrolling="yes"
                                allowtransparency="no"
                                noresize="noresize"
                                align="right"
                                style="position: relative; background: block; width: 100%; height: 100%;"
                                src="http://{mainpost}/display_leetcode/{hw_num}">
                        </iframe>
                    </div>
                </div>
            </body>
            </html>
    """
    os.chdir(mainpath)    
    with open(f"templates/leetcode.html", "w", encoding="utf-8") as file:
        file.write(html)
        os.chdir(mainpath) 