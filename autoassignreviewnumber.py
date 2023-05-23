from sql_connect import sql_connect  # 連結 MySQL 資料庫
from random import sample  # 生成審查編號
def assign_review_number(hw_num):
    connection = sql_connect()
    sql_cursor = connection.cursor()
    # ---------------------------------------------------------------------------- # 分配審查編號
    
    sql_cursor.execute(f"SELECT `student_id` FROM `Homework` WHERE homework_number = '{hw_num}';")
    student_data = sql_cursor.fetchall()
    student_data = [i[0] for i in student_data if i[0] not in {"s1104813", "s1094815", "pclin"}]
    student_count = len(student_data)
    random_lst = sample([i for i in range(1, student_count+1)], student_count)
    for i, e in enumerate(random_lst):
        sql_cursor.execute(f"UPDATE `Homework` SET `random_id` = {e} WHERE `student_id` = '{student_data[i]}' AND `homework_number` = '{hw_num}';")
    connection.commit()

    # connection.close()
    # sql_cursor.close()
    # ---------------------------------------------------------------------------- # 分配審查編號

    # ---------------------------------------------------------------------------- # 確認審查編號
    # sql_cursor.execute(f"SELECT `random_id` FROM `Homework` WHERE `homework_number` = '{hw_num}';")
    # random_total = sql_cursor.fetchall()
    # check = [i for i in range(1, 71)]
    # print(check)
    # for i in random_total:
    #     if i[0] in check:
    #         check.remove(i[0])
    #     else:
    #         print(i[0])
    # print(check)
    # ---------------------------------------------------------------------------- # 確認審查編號

    
    # ---------------------------------------------------------------------------- # 輸出學生作業分數
    sql_cursor.execute(f"SELECT `random_id`, `score` FROM `Homework` WHERE `homework_number` = '{hw_num}';")
    student_score = sql_cursor.fetchall()
    Score_list = [[x, y] for x, y in student_score if x not in {1094815, 1104813, 9999999}]
    # print(Score_list, len(Score_list))
    # ---------------------------------------------------------------------------- # 輸出學生作業分數

    # ---------------------------------------------------------------------------- # 分配學生3個審查者
    from random import randint
    def alloc(g, L):
        while True:
            try:
                n = randint(0,len(L)-1)
            except ValueError: break
            if L[n] not in g:
                g.append(L[n])
                del L[n]
                break
    from random import randint
    subLen = len(Score_list)//3
    # 區分成高中低三群，複製加長3倍並排序
    high = [s[0] for s in sorted(Score_list[:subLen]*3, key=lambda x: x[1], reverse=True)]
    mid =  [s[0] for s in sorted(Score_list[subLen:subLen*2]*3, key=lambda x: x[1], reverse=True)]
    low =  [s[0] for s in sorted(Score_list[subLen*2:]*3, key=lambda x: x[1], reverse=True)]
    # 開始分配評分對象
    Rating_list=[]
    level=["high", "mid", "low"]
    for s in Score_list:
    # 洗亂高中低3者的順序，要不然各自分數級距的都在同一排
        order=[]
        while len(order)!=3:
            n=randint(0,2)
            if n not in order:
                order.append(n)
    # 分別分配高中低3級距被評者，若某級距使用完了，就去找別的級距的被評者，直到所有人都被分配完(繳交作業人數非3倍數時)
        group = [s[0]] # 先把評分者加入第一項
        while len(group)!=4: # 確認評分者有被分配到3位被評者才結束
            for i in range(3): # 照打亂的高中低3級距順序分配
                exec(f"alloc(group, {level[order[i]]})")
    #             Alloc.alloc(group, level[order[i]])
                
        Rating_list.append(group)

    Rating_list = sorted(Rating_list) # 依照評分者學號排序
    # print(Rating_list)
    # print(len(Rating_list))
    # ---------------------------------------------------------------------------- # 分配學生3個審查者

    # ---------------------------------------------------------------------------- # 將分配好的審查清單加入資料庫
    for random_id, review_target1, review_target2, review_target3 in Rating_list:
        # print(random_id, review_target1, review_target2, review_target3)
        print("=========================================================")
        print(f"INSERT INTO `ReviewTarget` VALUES('{hw_num}', {random_id}, {review_target1}, {review_target2}, {review_target3});")
        sql_cursor.execute(f"INSERT INTO `ReviewTarget` VALUES('{hw_num}', {random_id}, {review_target1}, {review_target2}, {review_target3});")
    connection.commit()
    connection.close()
    sql_cursor.close()
    # ---------------------------------------------------------------------------- # 將分配好的審查清單加入資料庫