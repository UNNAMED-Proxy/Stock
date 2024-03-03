import pymysql

def dbConnect1():
    # MariaDB 연결 정보 설정
    host = 'localhost'
    user = user_name
    password = user_password

    conn = None
    try:
        # MariaDB 연결
        conn = pymysql.connect(
            host=host,
            user=user,
            password=password,
            charset='utf8mb4',
            cursorclass=pymysql.cursors.DictCursor
        )
        print("MariaDB에 연결되었습니다.")

    except pymysql.Error as err:
        print("Error : ", err)

    return conn

def dbConnect2():
    # MariaDB 연결 정보 설정
    host = 'localhost'
    user = user_name
    password = user_password
    database = 'Stock'
    tablename = 'StockList'

    conn = None
    try:
        # MariaDB 연결
        conn = pymysql.connect(
            host=host,
            user=user,
            password=password,
            database=database,
            charset='utf8mb4',
            cursorclass=pymysql.cursors.DictCursor
        )
        print("MariaDB에 연결되었습니다.")

    except pymysql.Error as err:
        print("Error : ", err)

    return conn

def create_stock_database():
    database = 'Stock'
    tablenames = ['StockList', 'FindStock', 'StockTradelog']

    """
    StockList : 주식기본정보
    FindStock : 감시주식
    StockTrageLog : 주식 거래 일지
    """

    conn = dbConnect1()

    try:
        with conn.cursor() as cursor:
            # 데이터베이스 존재 여부 확인
            cursor.execute("SHOW DATABASES LIKE '{}'".format(database))
            result = cursor.fetchone()
            if not result:
                print("데이터베이스 '{}' 이(가) 없어 신규 생성합니다.".format(database))
                cursor.execute("CREATE DATABASE {} CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci".format(database))
                print("데이터베이스 '{}' 신규 생성완료".format(database))
            else:
                print("데이터베이스 '{}' 이(가) 이미 존재합니다.".format(database))

            # 데이터베이스 선택
            cursor.execute("USE {}".format(database))
            for tablename in tablenames:
                # 테이블 존재 여부 확인
                cursor.execute("SHOW TABLES LIKE '{}'".format(tablename))
                result = cursor.fetchone()

                if tablename == 'StockList':
                    if not result:
                        # StockList 테이블 생성
                        print("테이블 '{}' 이(가) 없어 신규 생성합니다.".format(tablename))
                        cursor.execute(f"""
                            CREATE TABLE {tablename} (
                                StockType INT,
                                StockSecondType INT,
                                StockName NVARCHAR(100),
                                StockSymbol NVARCHAR(100)
                            ) CHARACTER SET=utf8mb4 COLLATE=utf8mb4_unicode_ci
                        """)
                        print("테이블 '{}' 신규 생성완료".format(tablename))
                    else:
                        print("테이블 '{}' 이(가) 이미 존재합니다.".format(tablename))

                elif tablename == 'FindStock':
                    if not result:
                        print("테이블 '{}' 이(가) 없어 신규 생성합니다.".format(tablename))
                        cursor.execute(f"""
                            CREATE TABLE {tablename} (
                                StockSymbol     NVARCHAR(100),
                                StockFindDate   DATETIME,
                                LastOpenDate    NCHAR(8),
                                Vol             BIGINT,
                                open            BIGINT,
                                High            BIGINT,
                                Low             BIGINT,
                                Close           BIGINT,
                                IsSale          NCHAR(1),
                                IsBuy           NCHAR(1)
                            ) CHARACTER SET=utf8mb4 COLLATE=utf8mb4_unicode_ci
                        """)
                        print("테이블 '{}' 신규 생성완료".format(tablename))
                    else:
                        print("테이블 '{}' 이(가) 이미 존재합니다.".format(tablename))

                elif tablename == 'StockTradelog':
                    if not result:
                        print("테이블 '{}' 이(가) 없어 신규 생성합니다.".format(tablename))
                        cursor.execute(f"""
                            CREATE TABLE {tablename} (
                                StockSymbol     NVARCHAR(100)   NOT NULL,
                                Qty             INT             NOT NULL,
                                BuyPrice        BIGINT          NOT NULL,
                                BuyDateTime     DATETIME        NOT NULL,
                                SalePrice       BIGINT              NULL,
                                SaleDateTime    DATETIME            NULL,
                                BalancePrice    BIGINT              NULL,
                                AccBalance      BIGINT              NULL
                            ) CHARACTER SET=utf8mb4 COLLATE=utf8mb4_unicode_ci
                        """)
                        print("테이블 '{}' 신규 생성완료".format(tablename))
                    else:
                        print("테이블 '{}' 이(가) 이미 존재합니다.".format(tablename))                        

    except pymysql.Error as err:
        print("Error : ", err)

    finally:
        # 커넥션 종료
        if conn:
            conn.close()
            print("MariaDB conn 종료")

def dbInsert_Stock_Info(StockType, StockSecondType, StockName, StockSymbol):
    conn = dbConnect2()
    print(StockType, StockSecondType, StockName, StockSymbol)
    try:
        with conn.cursor() as cursor:
            sql_select = "SELECT * FROM StockList WHERE StockSymbol = %s"
            cursor.execute(sql_select, (StockSymbol))
            result = cursor.fetchone()

            if result:
                print(f"StockList 테이블에 StockSymbol '{StockSymbol}' 이(가) 이미 존재합니다.")
            else:
                sql_insert = 'INSERT INTO StockList (StockType, StockSecondType, StockName, StockSymbol) VALUES (%s, %s, %s, %s)'
                cursor.execute(sql_insert, (StockType, StockSecondType, StockName, StockSymbol))
        conn.commit()
    except pymysql.Error as err:
        print("Error : ", err)            

    finally:
        if conn:
            conn.close()
            print('Insert 작업 완료하여 MariaDb Conn 종료')
