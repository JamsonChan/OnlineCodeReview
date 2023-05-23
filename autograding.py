import os, sys, time, copy, gc
from guppy import hpy
from mainpath import mainpath

try:    
    first = mainpath
    os.chdir(first)
    button = False
    sheet = []  # html用
    studentwrongans = []  # 學生錯誤答案, 特殊 error
    #---------------------------------------------------------# vscode 加入環境變數
    os.chdir(f"{mainpath}\\homework_file")
    sys.dont_write_bytecode = True
    sys.path.append(os.getcwd())
    exec(f"from question import hw{hw_num}_IN as In, hw{hw_num}_ANS as Ans")
    topic = copy.deepcopy(In)
    #---------------------------------------------------------# vscode 加入環境變數
    os.chdir(first)
    os.chdir(f"./homework_file/hw{hw_num}/{id}")
    last = os.getcwd()
    function_name = f"Homework_{hw_num}"
    #---------------------------------------------------------# vscode 加入環境變數
    sys.dont_write_bytecode = True
    sys.path.append(os.getcwd())
    try:
        exec(f"from {student_file} import {function_name} as func")
    except Exception as ex:  # 顯示 error 名稱:
        for i in range(len(In)):studentwrongans.append(f"{ex.__class__.__name__}")
        Score = 0
        Time = 0
        Memory = 0
        count = 0
        for i in range(len(In)):
            sheet.append([f"第{i+1}題", str(In[i]), str(studentwrongans[count]), str(Ans[i])])
            # sheet.append([f"第{i+1}題", f"{In[i][0]}, {In[i][1]}", studentwrongans[count], Ans[i]])
            count += 1
        os.chdir(first)
        button = True
    if button != True:
        frequency = 1  # 循環次數
        score = 0  # 基本分
        avg = 4  # 一題幾分
        error = []  # 錯誤題號   
        now = time.time()  # 時間複雜度
        heap = hpy()
        heap.setref()
        heap_status1 = heap.heap()  # 堆疊起點
        for f in range(frequency):
            for i in range(len(In)):
                try:
                    student_Ans = func(topic[i][0], topic[i][1], topic[i][2])
                except Exception as ex:  # 顯示 error 名稱
                    if f == 0:
                        error.append(i)
                        studentwrongans.append(f"{ex.__class__.__name__}:{str(ex)}")  # 加入特殊 error
                    continue
                if f == 0:
                    if student_Ans == Ans[i]:
                        score += avg
                    else:
                        error.append(i)
                        studentwrongans.append(str(student_Ans))
        heap_status2 = heap.heap()  # 堆疊終點
        os.chdir(first)
        Score = int(score)
        Time = round((time.time()-now)*1000, 1)
        Memory = round(heap_status2.size/1024**1, 3)
        # print(f"error:{len(error)}, stu:{len(studentwrongans)}")
        gc.collect()
        if Score != 100:
            count = 0
            for i in error:
                sheet.append([f"第{i+1}題", str(In[i]), str(studentwrongans[count]), str(Ans[i])])
                # sheet.append([f"第{i+1}題", f"{In[i][0]}, {In[i][1]}", studentwrongans[count], Ans[i]])
                count += 1
except NameError:
    def receive(studentid, filename, hwnum):
        global id, student_file, hw_num
        student_file = filename.split('.py')[0]
        hw_num = hwnum
        id = studentid