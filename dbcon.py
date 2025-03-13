# 사전설치 : pip install pymysql
import pymysql

def connect_to_mysql(host, port, user, password, database):
    """
    PyMySQL을 사용하여 MariaDB 데이터베이스에 연결하는 함수입니다.

    Args:
        host (str): MariaDB 서버 호스트 주소.
        port (int): MariaDB 서버 포트 번호.
        user (str): MariaDB 사용자 이름.
        password (str): MariaDB 사용자 비밀번호.
        database (str): 연결할 데이터베이스 이름.

    Returns:
        pymysql.Connection: MySQL 연결 객체 (성공 시).
        None: 연결 실패 시.
    """
    try:
        conn = pymysql.connect(
            host=host,
            port=port,
            user=user,
            password=password,
            database=database,
            cursorclass=pymysql.cursors.DictCursor  # 딕셔너리 형태로 결과 받기 (선택 사항)
        )
        print(f"MySQL 데이터베이스 '{database}'에 성공적으로 연결되었습니다.")
        return conn
    except pymysql.MySQLError as e:
        print(f"MySQL 연결 오류: {e}")
        return None

# 사용 예시:
if __name__ == '__main__':
    # 데이터베이스 연결 정보 (실제 값으로 변경해야 합니다!)
    DB_HOST = "localhost"  # 또는 IP 주소
    DB_PORT = 3306
    DB_USER = "root"  # 사용자 이름
    DB_PASSWORD = "7777"  # 비밀번호
    DB_DATABASE = "test"  # 데이터베이스 이름

    # 데이터베이스 연결 시도
    conn = connect_to_mysql(DB_HOST, DB_PORT, DB_USER, DB_PASSWORD, DB_DATABASE)

    # 연결 성공 시, 연결 객체 활용 (예: 쿼리 실행)
    if conn:
        try:
            with conn.cursor() as cursor: # 커서를 with 문 안에서 생성 및 사용 (자동 close)
                # SQL 쿼리 실행 (예시)
                sql = "SELECT VERSION()"
                cursor.execute(sql)
                #print(list(cursor))
                result = cursor.fetchone()
                print(f"MariaDB 버전: {result}")  # 결과 출력

        except pymysql.MySQLError as e:
            print(f"데이터베이스 작업 오류: {e}")
        finally:
            # 연결 종료 (중요!) - with 문을 사용하여 커서를 닫으면 conn.close() 만 필요합니다.
            if conn:
                conn.close()
                print("MariaDB 연결이 종료되었습니다.")