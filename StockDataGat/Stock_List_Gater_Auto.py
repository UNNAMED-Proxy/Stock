# pip install pywinauto
# pip install pymysql

import win32com.client
import AutoConnect
import DataBase_Create_Info

def login_Check():
    print('로그인여부 Check')
    try:
        # 연결 여부 체크
        objCpCybos = win32com.client.Dispatch("CpUtil.CpCybos")
        bConnect = objCpCybos.IsConnect
        print('로그인이 되어있습니다.')
    except:
        if (bConnect == 0):
            print('로그인이 안되어있습니다.')
            AutoConnect.AutoConnect()

def Stock_List():
    # 종목코드 리스트 구하기
    objCpCodeMgr = win32com.client.Dispatch("CpUtil.CpCodeMgr")

    for i in range(1, 3):
        """
        1 : 거래소(코스피)
        2 : 코스닥
        """
        codeList = objCpCodeMgr.GetStockListByMarket(i)

        for j, code in enumerate(codeList):
            name = objCpCodeMgr.CodeToName(code)
            secondCode = objCpCodeMgr.GetStockSectionKind(code)

            DataBase_Create_Info.dbInsert_Stock_Info(i, secondCode, name, code)

if __name__ == "__main__":
    DataBase_Create_Info.create_stock_database()
    login_Check()
    Stock_List()