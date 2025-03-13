import pymysql
from pymysql import Error

class Database:
    def __init__(self):
        self.connection = None
        try:
            self.connection = pymysql.connect(
                host='192.168.0.97',
                database='test',  # test 데이터베이스 사용
                user='root',
                password='8948864a',  # mariadb 설치 당시의 패스워드, 실제 환경에서는 보안을 위해 환경변수 등을 사용
                charset='utf8mb4', 
                cursorclass=pymysql.cursors.DictCursor
            )
            print("MariaDB에 성공적으로 연결되었습니다.")
        except Error as e:
            print(f"MariaDB 연결 중 오류 발생: {e}")

    def save_bmi_record_cnt(self,name,age_name,gender_name):
        """최근 과일정보 기록을 가져옵니다"""
        try:
            if self.connection is None:
                print("데이터베이스 연결이 없습니다.")
                return []
                
            with self.connection.cursor() as cursor:
                query = """
                SELECT  count(*) as cnt
                FROM    fruits_records
                WHERE   fruit_cd = (%s)
                    and age_cd = (%s)
                    and gender_cd = (%s)
                """
                cursor.execute(query, (name,age_name,gender_name))
                cnt = cursor.fetchall()
            
            return cnt
        except Error as e:
            print(f"데이터 조회 중 오류 발생: {e}")
            return []
        
    def update_bmi_record(self,name,age_name,gender_name):
        """과일을 데이터베이스에 저장"""
        try:
            if self.connection is None:
                print("데이터베이스 연결이 없습니다.")
                return False
                
            with self.connection.cursor() as cursor:
                query = """
                UPDATE fruits_records SET cnt = cnt +1  WHERE fruit_cd = (%s) and age_cd = (%s) and gender_cd = (%s)
                """
                cursor.execute(query, (name,age_name,gender_name))
            
            self.connection.commit()
            print("과일 정보가 성공적으로 저장되었습니다.")
            return True
        except Error as e:
            print(f"데이터 저장 중 오류 발생: {e}")
            return False
        
    def insert_bmi_record(self,name,age_name,gender_name):
        """과일을 데이터베이스에 저장"""
        try:
            if self.connection is None:
                print("데이터베이스 연결이 없습니다.")
                return False
                
            with self.connection.cursor() as cursor:
                query = """
                INSERT INTO fruits_records(fruit_cd,age_cd,gender_cd,cnt)
                VALUES((%s),(%s),(%s),1)
                """
                cursor.execute(query, (name,age_name,gender_name))
            
            self.connection.commit()
            print("과일 정보가 성공적으로 저장되었습니다.")
            return True
        except Error as e:
            print(f"데이터 저장 중 오류 발생: {e}")
            return False
        
    def get_all_fruits(self):
        """과일별 합계"""
        try:
            if self.connection is None:
                print("데이터베이스 연결이 없습니다.")
                return []
                
            with self.connection.cursor() as cursor:
                query = """
                SELECT fruit_nm name,
                    SUM(cnt) cnt
                FROM fruits_records, fruits_code f
                WHERE fruit_cd=f.id
                GROUP BY fruit_cd
                """
                cursor.execute(query)
                records = cursor.fetchall()
            
            return records
        except Error as e:
            print(f"데이터 조회 중 오류 발생: {e}")
            return []
        
    def get_fruits_by_man(self):
        """남자 과일 합계"""
        try:
            if self.connection is None:
                print("데이터베이스 연결이 없습니다.")
                return []
                
            with self.connection.cursor() as cursor:
                query = """
                SELECT fruit_nm name,
                    SUM(cnt) cnt
                FROM fruits_records, fruits_code f, fruits_gender_code g
                WHERE fruit_cd=f.id AND gender_cd=g.id AND gender_cd=2
                GROUP BY fruit_cd, g.id
                """
                cursor.execute(query)
                records = cursor.fetchall()
            
            return records
        except Error as e:
            print(f"데이터 조회 중 오류 발생: {e}")
            return []
        
    def get_fruits_by_woman(self):
        """여자 과일 합계"""
        try:
            if self.connection is None:
                print("데이터베이스 연결이 없습니다.")
                return []
                
            with self.connection.cursor() as cursor:
                query = """
                SELECT fruit_nm name,
                    SUM(cnt) cnt
                FROM fruits_records, fruits_code f, fruits_gender_code g
                WHERE fruit_cd=f.id AND gender_cd=g.id AND gender_cd=1
                GROUP BY fruit_cd, g.id
                """
                cursor.execute(query)
                records = cursor.fetchall()
            
            return records
        except Error as e:
            print(f"데이터 조회 중 오류 발생: {e}")
            return []
        
    def get_fruits_by_one(self):
        """십대 과일 합계"""
        try:
            if self.connection is None:
                print("데이터베이스 연결이 없습니다.")
                return []
                
            with self.connection.cursor() as cursor:
                query = """
                SELECT  fruit_nm name,
                    SUM(cnt) cnt
                FROM fruits_records, fruits_code f, fruits_age_code a
                WHERE fruit_cd=f.id AND age_cd=a.id AND age_cd=1
                GROUP BY fruit_cd, age_cd
                """
                cursor.execute(query)
                records = cursor.fetchall()
            
            return records
        except Error as e:
            print(f"데이터 조회 중 오류 발생: {e}")
            return []
        
    def get_fruits_by_two(self):
        """이십대 과일 합계"""
        try:
            if self.connection is None:
                print("데이터베이스 연결이 없습니다.")
                return []
                
            with self.connection.cursor() as cursor:
                query = """
                SELECT  fruit_nm name,
                    SUM(cnt) cnt
                FROM fruits_records, fruits_code f, fruits_age_code a
                WHERE fruit_cd=f.id AND age_cd=a.id AND age_cd=2
                GROUP BY fruit_cd, age_cd
                """
                cursor.execute(query)
                records = cursor.fetchall()
            
            return records
        except Error as e:
            print(f"데이터 조회 중 오류 발생: {e}")
            return []
    
    def get_fruits_by_thr(self):
        """삼십대 과일 합계"""
        try:
            if self.connection is None:
                print("데이터베이스 연결이 없습니다.")
                return []
                
            with self.connection.cursor() as cursor:
                query = """
                SELECT  fruit_nm name,
                    SUM(cnt) cnt
                FROM fruits_records, fruits_code f, fruits_age_code a
                WHERE fruit_cd=f.id AND age_cd=a.id AND age_cd=3
                GROUP BY fruit_cd, age_cd
                """
                cursor.execute(query)
                records = cursor.fetchall()
            
            return records
        except Error as e:
            print(f"데이터 조회 중 오류 발생: {e}")
            return []
        
    def get_fruits(self):
        """최근 과일목록을 가져옵니다"""
        try:
            if self.connection is None:
                print("데이터베이스 연결이 없습니다.")
                return []
                
            with self.connection.cursor() as cursor:
                query = """
                SELECT id, fruit_nm as name
                FROM fruits_code
                order by id
                """
                cursor.execute(query)
                fruits = cursor.fetchall()
            
            return fruits
        except Error as e:
            print(f"데이터 조회 중 오류 발생: {e}")
            return []
        
    def get_ages(self):
        """최근 과일목록을 가져옵니다"""
        try:
            if self.connection is None:
                print("데이터베이스 연결이 없습니다.")
                return []
                
            with self.connection.cursor() as cursor:
                query = """
                SELECT id, age_nm as name
                FROM fruits_age_code
                order by id
                """
                cursor.execute(query)
                ages = cursor.fetchall()
            
            return ages
        except Error as e:
            print(f"데이터 조회 중 오류 발생: {e}")
            return []
        
    def get_genders(self):
        """최근 과일목록을 가져옵니다"""
        try:
            if self.connection is None:
                print("데이터베이스 연결이 없습니다.")
                return []
                
            with self.connection.cursor() as cursor:
                query = """
                SELECT id, gender_nm as name
                FROM fruits_gender_code
                order by id
                """
                cursor.execute(query)
                genders = cursor.fetchall()
            
            return genders
        except Error as e:
            print(f"데이터 조회 중 오류 발생: {e}")
            return []

    def close(self):
        """데이터베이스 연결 종료"""
        if self.connection:
            self.connection.close()
            print("MariaDB 연결이 종료되었습니다.")