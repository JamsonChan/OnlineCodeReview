from sql_connect import sql_connect

def auto_code_review(homework_number, student_id, random_id, isAnonymous):
    return f"""
            SELECT
                t1.student_id,
                t1.name,
                t1.random_id,
                t1.file_name,
                t1.like_count,
                (CASE WHEN ISNULL(cl.student_id) THEN 0 ELSE 1 END) islike,
                (CASE WHEN ISNULL(c.comment_num) THEN 0 ELSE c.comment_num END) comment_num
            FROM
                (SELECT
                    s.student_id,
                    s.name,
                    h.random_id,
                    h.file_name,
                    h.like_count
                FROM StudentData s LEFT JOIN Homework h ON h.student_id = s.student_id
                WHERE h.homework_number = '{homework_number}') t1
            LEFT JOIN (SELECT * FROM CodeLike c1 WHERE c1.student_id = '{student_id}' AND c1.homework_number = '{homework_number}') cl
            ON t1.student_id = cl.author_id
            LEFT JOIN (SELECT author_id, COUNT(author_id) comment_num FROM Comment WHERE homework_number = '{homework_number}' GROUP BY author_id) c
            ON c.author_id = t1.student_id
            ORDER BY """ + ("3" if isAnonymous else "1") + f""";
        """

def rank_best_sql(homework_number, attribute):
    return f"""
            SELECT
                {attribute}_rank 編號,
                CONCAT(SUBSTRING(t.student_id, 2, 7), ' ', t.name) 學號姓名,
                (CASE
                    WHEN t.time_rank = 1 THEN CONCAT(t.time, '🥇')
                    WHEN t.time_rank = 2 THEN CONCAT(t.time, '🥈')
                    WHEN t.time_rank = 3 THEN CONCAT(t.time, '🥉')
                    ELSE t.time
                END) 時間,
                (CASE
                    WHEN t.memory_rank = 1 THEN CONCAT(t.memory, '🥇')
                    WHEN t.memory_rank = 2 THEN CONCAT(t.memory, '🥈')
                    WHEN t.memory_rank = 3 THEN CONCAT(t.memory, '🥉')
                    ELSE t.memory
                END) 記憶體,
                (CASE
                    WHEN t.upload_count_rank = 1 THEN CONCAT(t.upload_count, '🤡')
                    WHEN t.upload_count_rank = 2 THEN CONCAT(t.upload_count, '👹')
                    WHEN t.upload_count_rank = 3 THEN CONCAT(t.upload_count, '👻')
                    ELSE t.upload_count
                END) 上傳次數
            FROM
                (SELECT
                    s.student_id student_id,
                    s.name name,
                    h.time time,
                    h.memory memory,
                    h.upload_count upload_count,
                    RANK() OVER(ORDER BY s.student_id) student_id_rank,
                    RANK() OVER(ORDER BY h.time) time_rank,
                    RANK() OVER(ORDER BY h.memory) memory_rank,
                    RANK() OVER(ORDER BY h.upload_count DESC) upload_count_rank
                FROM Homework h INNER JOIN StudentData s
                ON s.student_id = h.student_id AND h.homework_number = '{homework_number}' AND h.score = 100) t
            ORDER BY 1;
            """

def rank_all_sql(homework_number, attribute):
    return f"""
            SELECT
                {attribute}_rank 編號,
                CONCAT(SUBSTRING(student_id, 2, 7), ' ', name) 學號姓名,
                (CASE WHEN time = 999999.999 THEN NULL ELSE time END) 時間,
                (CASE WHEN memory = 999999.999 THEN NULL ELSE memory END) 記憶體,
                upload_time 上傳時間,
                file_name 檔名,
                score 分數
            FROM
                (SELECT
                    t1.*,
                    RANK() OVER(ORDER BY t1.student_id) student_id_rank,
                    RANK() OVER(ORDER BY t1.time) time_rank,
                    RANK() OVER(ORDER BY t1.memory) memory_rank,
                    RANK() OVER(ORDER BY t1.upload_time DESC) upload_time_rank,
                    RANK() OVER(ORDER BY t1.score DESC) score_rank
                FROM
                    (SELECT
                        s.student_id student_id,
                        s.name name,
                        (CASE WHEN ISNULL(h.time) THEN 999999.999 ELSE h.time END) time,
                        (CASE WHEN ISNULL(h.memory) THEN 999999.999 ELSE h.memory END) memory,
                        h.upload_time upload_time,
                        h.score score,
                        h.file_name file_name
                    FROM AllHomework h JOIN StudentData s
                    ON s.student_id = h.student_id AND h.homework_number = '{homework_number}') t1) t2
            ORDER BY 1, 5;
            """

def hero_rank_sql():
    connection = sql_connect()
    sql_cursor = connection.cursor()
    sql_cursor.execute("SELECT DISTINCT h.homework_number FROM Homework h")
    all_homework = sql_cursor.fetchall()
    all_homework = [i[0] for i in all_homework]
    all_homework.sort(key = lambda x:int(x[2:]))

    sql = """
        # (最外層)======================= 給英雄榜的獎盃 =======================
            SELECT
                t4.rank_,
                t4.student_id,
                (CASE
                    WHEN rank_ = 1 THEN CONCAT(t4.name, '🏆')
                    ELSE t4.name
                END) name,
                t4.medals,
                t4.total_score,
                t4.upload_avg
            FROM
            # (t4層)======================= 計算 rank、生成獎牌字串、處理平均上傳次數的小數點 =======================
                (SELECT
                    RANK() OVER(ORDER BY t3.total_score DESC, x.upload_avg) rank_,
                    t3.student_id,
                    t3.name,
                    CONCAT(REPEAT("🥇", t3.gold_medal), REPEAT("🥈", t3.silver_medal), REPEAT("🥉", t3.bronze_medal)) medals,
                    t3.total_score,
                    (CASE
                        WHEN MOD(x.upload_avg, 1) != 0 THEN FORMAT(x.upload_avg, 1)
                        ELSE FORMAT(x.upload_avg, 0)
                    END) upload_avg
                FROM
                # (t3層)======================= 計算 GROUP 後每種獎牌的數量、計算加權分數 =======================
                    (SELECT
                        t2.student_id,
                        t2.name,
                        SUM(t2.gold_medal) gold_medal,
                        SUM(t2.silver_medal) silver_medal,
                        SUM(t2.bronze_medal) bronze_medal,
                        SUM(t2.gold_medal)*3 + SUM(t2.silver_medal)*2 + SUM(t2.bronze_medal) total_score
                    FROM
                    # (t2層)======================= 計算獎牌數量(還未 GROUP 起來，所以會有重複的人) =======================
                        (SELECT
                            t1.student_id,
                            t1.name,
                            (CASE
                                WHEN time_rank = 1 AND memory_rank = 1 THEN 2
                                WHEN time_rank = 1 OR memory_rank = 1 THEN 1
                                ELSE 0
                            END) gold_medal,
                            (CASE
                                WHEN time_rank = 2 AND memory_rank = 2 THEN 2
                                WHEN time_rank = 2 OR memory_rank = 2 THEN 1
                                ELSE 0
                            END) silver_medal,
                            (CASE
                                WHEN time_rank = 3 AND memory_rank = 3 THEN 2
                                WHEN time_rank = 3 OR memory_rank = 3 THEN 1
                                ELSE 0
                            END) bronze_medal
                        FROM
                        # (t1層)======================= 取得所有作業 Time 或 Memory 排名前三名的所有資料 =======================
                            (
            """
    for hwn in all_homework:
        sql += f"""
                                (SELECT
                                    *
                                FROM
                                # (最內層)======================= 取得第 n 次作業的資料、計算 Time 和 Memory Rank =======================
                                    (SELECT
                                        s.student_id student_id,
                                        s.name name,
                                        h.time time,
                                        h.memory memory,
                                        RANK() OVER(ORDER BY h.time) time_rank,
                                        RANK() OVER(ORDER BY h.memory) memory_rank
                                    FROM Homework h INNER JOIN StudentData s
                                    ON s.student_id = h.student_id AND h.homework_number = '{hwn}' AND h.score = 100) t
                                WHERE time_rank <= 3 OR memory_rank <= 3)
                """
        if hwn != all_homework[-1]: sql += "UNION"
    
    sql += """
                            ) t1
                        ) t2
                    GROUP BY t2.student_id, t2.name
                    ) t3
                LEFT JOIN
                    (SELECT
                        student_id,
                        AVG(h.upload_count) upload_avg
                    FROM Homework h
                    GROUP BY h.student_id) x
                ON x.student_id = t3.student_id
                ) t4
    """
    return sql

def get_homework_author(homework_number, student_id):
    return f"""
            SELECT
                s.name,
                h.random_id,
                h.file_name
            FROM Homework h JOIN StudentData s ON h.student_id = s.student_id
            WHERE h.homework_number = '{homework_number}' AND h.student_id = '{student_id}'
            """

def get_homework_reviewer(homework_number, author_id, student_id):
    return f"""
                SELECT
                    t3.review_time 時間,
                    t3.name 留言人,
                    t3.nickname 暱稱,
                    t3.content 留言內容,
                    t3.like_count 讚數,
                    t3.random_id 匿名,
                    t3.student_id 實名,
                    (CASE WHEN ISNULL(c.student_id) THEN 0 ELSE 1 END) islike,
                    ROW_NUMBER() OVER (ORDER BY t3.review_time) idx
                FROM
                    (SELECT
                        t2.review_time,
                        s2.name,
                        s2.nickname,
                        t2.content,
                        t2.like_count,
                        t2.random_id,
                        t2.student_id
                    FROM
                        (SELECT
                            t1.*,
                            h.random_id,
                            h.student_id
                        FROM
                            (SELECT
                                c.homework_number,
                                c.review_time,
                                c.reviewer_id,
                                c.content,
                                c.like_count
                            FROM Comment c
                            LEFT JOIN StudentData s1 ON c.author_id = s1.student_id
                            WHERE c.homework_number = '{homework_number}' AND c.author_id = '{author_id}') t1
                        LEFT JOIN Homework h ON t1.reviewer_id = h.student_id AND t1.homework_number = h.homework_number) t2
                    LEFT JOIN StudentData s2 ON t2.reviewer_id = s2.student_id) t3
                LEFT JOIN (SELECT * FROM CommentLike c1 WHERE c1.student_id = '{student_id}') c
                ON t3.student_id = c.reviewer_id AND t3.review_time = c.review_time
                ORDER BY 1;
                """

def homework_score(student_id):
    return f"""
            SELECT
                d.*,
                h.upload_count,
                h.score,
                FORMAT(SUM(h.score) OVER (ORDER BY h.score, d.homework_number) / COUNT(h.score) OVER (ORDER BY h.score, d.homework_number), 2) running_avg
            FROM Deadline d
            LEFT JOIN Homework h
            ON d.homework_number = h.homework_number
            WHERE h.student_id = '{student_id}';  
    """

def total_semester_grade(student_id):
    return f"""
            SELECT
                FORMAT(SUM(h.score)/COUNT(h.score), 2) hw,
                s.midterm_exam,
                s.final_exam
            FROM StudentData s
            LEFT JOIN Homework h
            ON s.student_id = h.student_id
            WHERE s.student_id = '{student_id}';
    """