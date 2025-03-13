import pymysql
from pymysql import Error

class Database:
    def __init__(self):
        self.connection = None
        try:
            self.connection = pymysql.connect(
                host='192.168.0.97',
                database='test',
                user='root',
                password='8948864a',
                charset='utf8mb4',
                cursorclass=pymysql.cursors.DictCursor
            )
            print("MariaDB에 성공적으로 연결되었습니다.")
        except pymysql.Error as e:
            print(f"MariaDB 연결 중 오류 발생: {e}")

    def get_fruit_data(self):
        """fruits 테이블에서 name과 cnt 데이터를 가져옵니다."""
        try:
            if self.connection is None:
                print("데이터베이스 연결이 없습니다.")
                return []
                
            with self.connection.cursor() as cursor:
                query = "SELECT name, cnt FROM fruits"
                cursor.execute(query)
                records = cursor.fetchall()
            
            return records
        except pymysql.Error as e:
            print(f"데이터 조회 중 오류 발생: {e}")
            return []

    def update_fruit_count(self, fruit_name):
        """선택한 과일의 cnt 값을 1 증가"""
        try:
            if self.connection is None:
                print("데이터베이스 연결이 없습니다.")
                return False

            with self.connection.cursor() as cursor:
                # 과일이 존재하는지 확인
                check_query = "SELECT cnt FROM fruits WHERE name = %s"
                cursor.execute(check_query, (fruit_name,))
                result = cursor.fetchone()

                if result:
                    # 과일이 존재하면 cnt 증가
                    update_query = "UPDATE fruits SET cnt = cnt + 1 WHERE name = %s"
                    cursor.execute(update_query, (fruit_name,))
                else:
                    # 과일이 존재하지 않으면 새로 추가
                    insert_query = "INSERT INTO fruits (name, cnt) VALUES (%s, 1)"
                    cursor.execute(insert_query, (fruit_name,))

            self.connection.commit()
            print(f"{fruit_name}의 개수가 업데이트되었습니다.")
            return True
        except pymysql.Error as e:
            print(f"데이터 업데이트 중 오류 발생: {e}")
            return False

    def close(self):
        """데이터베이스 연결 종료"""
        if self.connection:
            self.connection.close()
            print("MariaDB 연결이 종료되었습니다.")
