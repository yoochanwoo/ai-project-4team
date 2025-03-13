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

    def save_bmi_record(self,name):
        """과일을 데이터베이스에 저장"""
        try:
            if self.connection is None:
                print("데이터베이스 연결이 없습니다.")
                return False
                
            with self.connection.cursor() as cursor:
                query = """
                UPDATE fruits SET cnt = cnt +1  WHERE name = (%s)
                """
                cursor.execute(query, (name,))
            
            self.connection.commit()
            print("과일 정보가 성공적으로 저장되었습니다.")
            return True
        except Error as e:
            print(f"데이터 저장 중 오류 발생: {e}")
            return False

    def get_bmi_records(self):
        """최근 과일정보 기록을 가져옵니다"""
        try:
            if self.connection is None:
                print("데이터베이스 연결이 없습니다.")
                return []
                
            with self.connection.cursor() as cursor:
                query = """
                SELECT name,cnt,(cnt / (SELECT SUM(cnt) FROM fruits)) * 100 AS ratio
                FROM fruits
                """
                cursor.execute(query)
                records = cursor.fetchall()
            
            return records
        except Error as e:
            print(f"데이터 조회 중 오류 발생: {e}")
            return []

    def close(self):
        """데이터베이스 연결 종료"""
        if self.connection:
            self.connection.close()
            print("MariaDB 연결이 종료되었습니다.")