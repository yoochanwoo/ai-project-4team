import pymysql
from pymysql import Error

class Database:
    def __init__(self):
        self.connection = None
        try:
            self.connection = pymysql.connect(
                host='localhost',
                database='test',  # test 데이터베이스 사용
                user='root',
                password='7777',  # mariadb 설치 당시의 패스워드, 실제 환경에서는 보안을 위해 환경변수 등을 사용
                # 내 비밀번호는 7777
                charset='utf8mb4',
                cursorclass=pymysql.cursors.DictCursor
            )
            print("MariaDB에 성공적으로 연결되었습니다.")
        except Error as e:
            print(f"MariaDB 연결 중 오류 발생: {e}")

    def save_bmi_record(self, weight, height, bmi, category):
        """BMI 기록을 데이터베이스에 저장"""
        try:
            if self.connection is None:
                print("데이터베이스 연결이 없습니다.")
                return False
                
            with self.connection.cursor() as cursor:
                query = """
                INSERT INTO bmi_records (weight, height, bmi, category)
                VALUES (%s, %s, %s, %s)
                """
                cursor.execute(query, (weight, height, bmi, category))
            
            self.connection.commit()
            print("BMI 기록이 성공적으로 저장되었습니다.")
            return True
        except Error as e:
            print(f"데이터 저장 중 오류 발생: {e}")
            return False

    def get_bmi_records(self, limit=10):
        """최근 BMI 기록을 가져옵니다"""
        try:
            if self.connection is None:
                print("데이터베이스 연결이 없습니다.")
                return []
                
            with self.connection.cursor() as cursor:
                query = """
                SELECT * FROM bmi_records
                ORDER BY created_at DESC
                LIMIT %s
                """
                cursor.execute(query, (limit,))
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