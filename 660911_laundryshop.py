import math
MYPATH = "/Dev/Coding/Python/Inclass/Homework/660911"
MYFILE = "DATA_laundryshop.txt"
fileNameLen = len(MYFILE)
mode = "create"

#? Try to create file if not exist Or Read File If exist
try:
    if mode == "create":
        with open(f'{MYPATH}/{MYFILE}', 'x', encoding="utf-8") as laundryshopData:
            print(f'\n{"*"*(42+fileNameLen)}\n**    {MYFILE} Not Found สร้างฐานใหม่ข้อมูลสำเร็จ    **\n{"*"*(42+fileNameLen)}\n')
            mode = "FirstCreate"
            print('Mode = FirstCreate')
            laundryshopData.seek(0,0) #!0: sets the reference point at the beginning of the file 1: sets the reference point at the current file position 2: sets the reference point at the end of the file 
            laundryshopData.writelines('USER PASS COIN POINT\n')
            laundryshopData.writelines('Admin 1234 99999 999999')
except FileExistsError:
    print('')
    print(f'\n{"*"*(31+fileNameLen)}\n**    {MYFILE} Found ใช้ฐานข้อมูลเก่า    **\n{"*"*(31+fileNameLen)}\n')
    mode = "oldDB"

#! Init
U = "user"
Pw = "password"
C = "coin"
P = "point"
R = "rowline"
isError = False
curUser = ""
curCoin = 0
curPoint = 0
ldsDataDict = {
}
gotpoint = 0
useCoin = 0
usePoint = 0
firstLoad = True
userlogin= ''
saveFile = False
oldUser = True
notUse = False



def loadData():
    laundryshopData = open(f'{MYPATH}/{MYFILE}', 'r+', encoding="utf-8")
    global ldsDataDict
    global isError
    global line
    line = 1
    print(f'\n{"*"*(24+fileNameLen)}\n**    โหลดข้อมูลจาก {MYFILE}    **\n{"*"*(24+fileNameLen)}\n')
    ldsDataDict.clear()
    try:
        for i in laundryshopData:
            if line > 1:
                ldsTempData = i
                tempList = (ldsTempData.replace('\n', '').split(" ")) #!เปลี่ยน \n เป็น ว่าง แล้วจึงแยกด้วย " " ได้ Type = List
                print(tempList) #!!!!DEBUG
                if tempList[0].upper() not in ldsDataDict:
                    print(f'Log : {tempList[0]} {tempList[1]} {tempList[2]} {tempList[3]}')
                    tempDict = {
                        tempList[0].upper() : {U:tempList[0], Pw:tempList[1], C:float(tempList[2]), P:float(tempList[3]), R:int(line)}
                    }
                    ldsDataDict.update(tempDict)
                    print(ldsDataDict)
                else:
                    print(f'\nเกิดข้อผิดพลาดขณะโหลดไฟล์ กรุณาตรวจสอบค่า ในฐานข้อมูลที่บรรทัด {line-1}(+1) ว่ามี Username ซ้ำหรือไม่')
                    isError = True
                    break
            line += 1
    except ValueError:
        isError = True
        print(f'\nเกิดข้อผิดพลาดขณะโหลดไฟล์ (ValueError) กรุณาตรวจสอบค่าของ Coin หรือ Point ในฐานข้อมูลที่บรรทัด {line-1}(+1)')
        print('\nError Detail : \n')
        raise
    except IndexError:
        isError = True
        print(f'\nเกิดข้อผิดพลาดขณะโหลดไฟล์ (IndexError) กรุณาตรวจสอบค่า ในฐานข้อมูลที่บรรทัด {line-1}(+1) ว่ามีการขาดหาย,มีบรรทัดว่าง หรือไม่')
        print('\nError Detail : \n')
        raise
        
    finally:
        if isError is False:
            print(f'\n{"*"*(31+fileNameLen)}\n**    โหลดข้อมูลจาก {MYFILE} เสร็จสิ้น    **\n{"*"*(31+fileNameLen)}\n')
            
def FitterInput(msg,mode):
    match mode:
        case "user":
            while True:
                temp = input(msg)
                if temp.upper() not in ldsDataDict:
                    if len(temp) < 4:
                        print('\tชื่อสั้นเกินไป...')
                    elif temp[0].isnumeric() == True:
                        print('\tชื่่อตัวแรกต้องไม่เป็นตัวเลข...')
                    else:
                        print('OK')
                        return temp
                else:
                    print('พบชื่อผู้ใช้ซ้ำ กรุณาใช้ชื่ออื่น')
        case "pass":
            while True:
                temp = input(msg)
                if len(temp) < 8:
                    print('\tรหัสสั้นเกินไป (8ตัวขึ้นไป)...\n')
                else:
                    print('OK')
                    return temp
        case _ :
            print('0o0 Error 0o0')
    
def memberRegister(regMode = ""):
    global line
    global oldUser
    tempList = []
    print(f'\n{"*"*50}')
    print('\nระบบสมัครสมาชิก')
    tempList.append(FitterInput('\tUser         : ',"user"))
    tempList.append(FitterInput('\tPassword     : ',"pass"))
    tempList.append(0) #!Coin
    tempList.append(0) #!Point
    tempDict = {
        tempList[0].upper() : {U:tempList[0], Pw:tempList[1], C:float(tempList[2]), P:float(tempList[3]), R:int(line)}
    }
    ldsDataDict.update(tempDict)
    line += 1
    oldUser = False
    return tempList[0].upper()
    # print(ldsDataDict)

def login():
    global userlogin
    while True:
        if userlogin in ["err",""]:
            print(f'\n{"*"*50}')
            print('\nโปรดเข้าสู่ระบบ')
            print('\tหากต้องการสมัครสมาชิก พิมพ์ r')
            usr = input('\n\tUser\t        >>> ')
            if usr.upper() == 'R':
                userlogin = memberRegister()
            elif usr.upper() in ldsDataDict:
                userlogin = usr.upper()
                print('OK')
                pwd = input('\tPassword\t>>> ')
                if pwd == ldsDataDict[userlogin]["password"]:
                    print('\nเข้าสู่ระบบสำเร็จ !')
                else:
                    print('รหัสผิด โปรดเข้าสู่ระบบอีกครั้ง !')
                    userlogin = "err"
            else:
                print('ไม่พบผู้ใช้กรุณาตรวจสอบใหม่อีกครั้ง')
                userlogin = "err"
        else:
            break

def topup():
    global curCoin
    print(f'\n{"*"*50}')
    print('\nระบบเติมเงิน')
    print(f'\n{"*"*50}')
    print('\nท่านต้องการเติมเงินเท่าไหร่ ')
    while True:
        topup = input('\n\t>>> ')
        if topup.isnumeric() == True and int(topup) > 1:
            topup = int(topup)
            curCoin += topup
            print(f'\n{"*"*50}')
            print(f'\nเติมเงินสำเร็จ {topup:,.2f} เหรียญ')
            print(f'เหรียญคงเหลือคือ {curCoin:,.2f}')
            print(f'แต้มคงเหลือคือ   {curPoint:,.2f}\n')
            break
        else:
            print('\nกรุณากรอกใหม่อีกครั้ง')

while not isError:
    #!Main
    loadData()
    print('\tยินดีต้อนรับสู่ร้านซักรีดเสื้อผ้าของเรา')
    if mode == "FirstCreate":
        print('ยินดีด้วยคุณคือลูกค้าคนแรก โปรดสมัครสมาชิกก่อนใช้งาน !')
        memberRegister()
        mode = "oldDB"
    if mode == "oldDB":
        # userlogin = "ADMIN" #!Bypass Login
        login()

        while True:
            price1 = 20
            price2 = 45
            totalprice = 0
            if firstLoad == True:
                curUser = ldsDataDict[userlogin]["user"]
                curCoin = float(ldsDataDict[userlogin]["coin"])
                curPoint = float(ldsDataDict[userlogin]["point"])
                firstLoad = False
            print(f'\n{"*"*50}\n')
            
            print(f'\n ยินดีต้อนรับคุณ {curUser}')
            print(f'\t เหรียญคงเหลือคือ {curCoin:,.2f}')
            print(f'\t แต้มคงเหลือคือ   {curPoint:,.2f}\n')

            if curCoin <= 0:
                print('ท่านไม่มีเหรียญคงเหลือในระบบ กำลังไประบบเติมเงิน...')
                topup()
            elif curCoin < price2:
                print('เหรียญคงเหลือในระบบของท่านเหลือน้อย ต้องการไปเติมเงินไหม? [Y / N]')
                q = input('\n\t>>> ')
                if q in ['Y','y']:
                    topup()
                    
            print('\nเลือกการทำงานที่ท่านต้องการ\n')
            print(f'\t 1.ซักแห้ง {price1} (บาท / ตัว) สามารถซักได้ {math.trunc((curCoin + curPoint) / price1):,.0f} ตัว')
            print(f'\t 2.ซักแห้งอบรีด {price2} (บาท / ตัว) สามารถซักได้ {math.trunc((curCoin + curPoint) / price2):,.0f} ตัว')
            print(f'\n{"*"*50}')
            ldsmode = input('\n\t >>>> ')
            if ldsmode not in ['1','2'] :
                print('\nกรุณาเลือกใหม่อีกครั้ง')
            else:
                break
        while True:
            print(f'\n{"*"*50}\n')
            print('กรอกจำนวนเสื้อผ้าที่ท่านต้องการจะใช้บริการ')
            print(f'\n{"*"*50}')
            piecelds = int(input('\n\t >>>> '))
            if piecelds < 1 :
                print('\nบริการตั้งแต่ 1 ชิ้นขึ้นไป')
            else:
                break
        match ldsmode:
            case '1':
                totalprice = piecelds * price1
                gotpoint = totalprice / 10

            case '2':
                totalprice = piecelds * price2
                gotpoint = totalprice / 10

        print(f'\n{"*"*50}\n')
        print('สรุป')
        match ldsmode:
            case '1':
                print(f'\tซักแห้ง {piecelds:,d} ตัว ตัวละ {price1:,d} บาท')
                print(f'\tทั้งหมดคิดเป็น {totalprice:,.2f} บาท')
            case '2':
                print(f'\tซักแห้ง อบรีด {piecelds:,d} ตัว ตัวละ {price2:,d} บาท')
                print(f'\tทั้งหมดคิดเป็น {totalprice:,.2f} บาท')

        while True:
            if totalprice > (curCoin + curPoint):
                print('\tจำนวนเหรียญและแต้มของท่านไม่พอ')
                print(f'\tขาดอีก {(totalprice-(curCoin + curPoint)):,.2f} เหรียญ')
                print('เหรียญคงเหลือในระบบของท่านไม่เพียงพอ ต้องการไปเติมเงินไหม? [Y / N]')
                q = input('\n\t>>> ')
                if q in ['Y','y']:
                    topup()
                else:
                    notUse = True
                    break
            else:
                notUse = False
                if totalprice - curPoint >= 0:
                    usePoint = curPoint
                    curPoint -= totalprice
                    totalprice -= usePoint
                    if curPoint < 0:
                        curPoint = 0
                    useCoin = totalprice
                    curCoin -= useCoin
                    curPoint += gotpoint
                    break
                else:
                    usePoint = totalprice
                    curPoint -= totalprice
                    totalprice -= usePoint
                    if curPoint < 0:
                        curPoint = 0
                    useCoin = totalprice
                    curCoin -= useCoin
                    curPoint += gotpoint
                    break

        if notUse == False:
            print(f'\nใช้เหรียญไป {useCoin:,.2f}')
            print(f'เหรียญคงเหลือคือ {curCoin:,.2f}')
            print(f'ใช้แต้มไป {usePoint:,.2f}')
            print(f'ได้แต้ม {gotpoint:,.2f}')
            print(f'แต้มคงเหลือคือ {curPoint:,.2f}')
            print(f'\n{"*"*50}\n')
        
        saveFile = True
        if saveFile == True:
            
            if oldUser is True: #! Update Data in file
                currowLine = ldsDataDict[userlogin]["rowline"] - 1
                laundryshopData = open(f'{MYPATH}/{MYFILE}', 'r+', encoding="utf-8")
                tempList = laundryshopData.readlines()
                # print(tempList)
                # print(tempList[currowLine])
                tempList[currowLine] = ldsDataDict[userlogin]["user"] + " " + ldsDataDict[userlogin]["password"] + " " + str(curCoin) + " " + str(curPoint)
                laundryshopData = open(f'{MYPATH}/{MYFILE}', 'w', encoding="utf-8")
                laundryshopData.writelines(tempList)
                laundryshopData.close()
            else:
                temp = ldsDataDict[userlogin]["user"] + " " + ldsDataDict[userlogin]["password"] + " " + str(curCoin) + " " + str(curPoint)
                # print(temp)
                laundryshopData = open(f'{MYPATH}/{MYFILE}', 'a', encoding="utf-8")
                laundryshopData.write("\n")
                laundryshopData.write(temp)
                laundryshopData.close()
            # print(ldsDataDict[userlogin]["user"] , ldsDataDict[userlogin]["password"] , ldsDataDict[userlogin]["coin"] , ldsDataDict[userlogin]["point"])
        
        print('ท่านต้องการทำงานอีกครั้งไหม [Y / N] ?')
        q = input('\t>>> ')
        if q not in ['Y','y']:
            print(f'\n{"*"*50}\n')
            print('จัดทำโดย นายนิติธร นันทสินธ์ 65003263019')
            print(f'\n{"*"*50}\n')
            break
        else:
            firstLoad = True #! ต้อง Save dict ลง text ก่อน
            print(f'\n\n{"*"*50}\n')
            
#ToDo : แก้ bug หลัง register user ใหม่ จะเป็นการ append 
