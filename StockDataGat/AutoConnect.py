#-*- coding: utf-8 -*-

from pywinauto import application
import os, time

def AutoConnect():
    
    print('PLUS가 접속되어 있지 않아 로그인 시도.')
    os.system('taskkill /IM coStarter* /F /T')
    os.system('taskkill /IM CpStart* /F /T')
    os.system('taskkill /IM DibServer* /F /T')

    os.system('wmic process where "name like \'%coStarter%\'" call terminate')
    os.system('wmic process where "name like \'%CpStart%\'" call terminate')
    os.system('wmic process where "name like \'%DibServer%\'" call terminate')

    for i in range(5, 0, -1):
        print(f'접속시도 : {i}')
        time.sleep(1)

    app = application.Application()
    app.start('C:\CREON\STARTER\coStarter.exe /prj:cp '
        ' /id:tidlxod1 /pwd:rladn1! /pwdcert:dlrjtdms1! /autostart')

    for i in range(60, 0, -1):
        print(f'접속 완료 대기 {i}')
        time.sleep(1)