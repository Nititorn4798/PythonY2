"""โปรแกรมคำนวณค่าสถิติ"""
import math

def clearscreen():
    """ฟังก์ชั่น ล้างหน้าจอ terminal"""
    print('\033c')
def resetcolor():
    """ฟังก์ชั่นรีเซ็ทค่าสี"""
    print('\u001b[0m',end='')

C_BLACK = '\u001b[30m'
C_RED = '\u001b[31m'
C_GREEN = '\u001b[32m'
C_YELLOW = '\u001b[33m'
C_BLUE = '\u001b[34m'
C_MAGENTA = '\u001b[35m'
C_CYAN = '\u001b[36m'
C_WHITE = '\u001b[37m'
C_RESET = '\u001b[0m'

def numlist_input(inputset,menu = 0):
    """ฟังก์ชั่น รับชุดตัวเลข ที่มีการทำงานสองแบบ
    1. รับตัวเลข 1 ตัวก่อน
    2. รับตัวเลขมาทั้งชุด
        หลังจากรับข้อมูลเสร็จสิ้นจะให้เลือกการฟังก์ชั่นทำงานที่จะนำชุดตัวเลขไปคำนวณ"""
    numlist = []
    is_error = False
    try:
        if len(inputset[0:10].replace(', ', ',').replace(',', ' ').split(" ")) == 1:
            inputset = float(inputset)
            numlist.append(inputset)
            print('พิมพ์ 0 เพื่อจบการกรอกเลข')
            while True:
                if len(numlist) <= 99:
                    inputset = float(input(f'\t{C_RESET}กรอกตัวเลขเพิ่มเติม (1-999) ตัวที่ : {C_BLUE}{len(numlist)+1}{C_RESET} >>> {C_GREEN}'))
                    if inputset > 0 and inputset < 1000:
                        numlist.append(inputset)
                    else:
                        print(f'\n{C_RESET}{"*"*50}\n')
                        print('เสร็จสิ้นการกรอกข้อมูล')
                        print(f'{C_RESET}ชุดข้อมูลคือ (ขนาดชุดข้อมูล {C_GREEN}{len(numlist)}{C_RESET}) : {C_BLUE}{numlist}{C_RESET}')
                        break
                else:
                    print(f'\n{"*"*50}\n')
                    print('เสร็จสิ้นการกรอกข้อมูล')
                    print(f'{C_RESET}ชุดข้อมูลคือ (ขนาดชุดข้อมูล {C_GREEN}{len(numlist)}{C_RESET}) : {C_BLUE}{numlist}{C_RESET}')
                    break
        else:
            numlist = map(float, inputset.replace(', ', ',').replace(',', ' ').split(" "))
            numlist = list(numlist) #! ทำให้ Map เป็น List
            if len(numlist) > 100:
                print(f'{C_RESET}ค่าที่รับมา มีเกินจำนวนที่แนะนำ 100 ค่า ({C_RED}{len(numlist)} ค่า{C_RESET}) ต้องการตัดส่วนเกินออกหรือไม่ [ Y / N ] ?')
                quest = input(f'\t>>>{C_GREEN} ')
                resetcolor()
                if quest.upper() in ['Y']:
                    numlist = numlist[0:100] #! เอาแค่ 100 ตัว
            print(f'{C_RESET}ชุดข้อมูลคือ (ขนาดชุดข้อมูล {C_GREEN}{len(numlist)}{C_RESET} ค่า) : {C_BLUE}{numlist}{C_RESET}')

        print(f'\n{"*"*50}\n')
        if menu == 0:
            print('เลือกโหมดการคำนวณที่ต้องการ')
            print('\t1. ค่าสูงสุด Max')
            print('\t2. ค่าต่่ำสุด Min')
            print('\t3. ค่ามัชฌิมเลขคณิต x̄ Mean')
            print('\t4. ค่ามัธยฐาน Median')
            print(f'\t{C_RED}5. ฐานนิยม{C_RESET}')
            print('\t6. ความเบี่ยงเบนเฉลี่ย Mean Deviation')
            print('\t7. ความเบี่ยงเบนมาตรฐาน Standard Deviation')
            print('\t8. ความแปรปรวน S2, Variance')
            print('\t9. ค่าพิสัยของคะแนน Range')
            print('\t999. ทุกการคำนวณ')
            print(f'\n{"*"*50}\n')
            menu = int(input(f'\t>>>{C_GREEN} '))
            print(f'\n{C_RESET}{"*"*50}')

    except ValueError:
        print(f'\n{C_RED}พบข้อผิดพลาด กรุณาเช็คตัวเลขที่ท่านกรอกมา{C_RESET}\n')
        is_error = True

    finally:
        if is_error is False:
            match menu:
                case 1:
                    find_max(numlist)
                case 2:
                    find_min(numlist)
                case 3:
                    find_mean(numlist)
                case 4:
                    find_median(numlist)
                case 5:
                    print(f'\n{C_MAGENTA}Soon{C_RESET}')
                case 6:
                    find_md(numlist)
                case 7:
                    find_sd(numlist)
                case 8:
                    find_s_2(numlist)
                case 9:
                    find_range(numlist)
                case 999:
                    find_max(numlist)
                    find_min(numlist)
                    find_mean(numlist)
                    find_median(numlist)
                    find_md(numlist)
                    find_sd(numlist)
                    find_s_2(numlist)
                    find_range(numlist)
                case _ :
                    print(f'\n{C_RED}พบข้อผิดพลาด กรุณาเช็คตัวเลขที่ท่านกรอกมา{C_RESET}\n')

def find_min(numlist):
    """แสดงค่าน้อยที่สุดในช่วงข้อมูล"""
    min_num = numlist[0]
    numlistlen = len(numlist)
    for i in range(numlistlen):
        if numlist[i] < min_num:
            min_num = numlist[i]
    print(f'\nค่าที่ต่่ำที่สุด คือ {C_GREEN}{min_num}{C_RESET}')
    print(f'\n{"*"*50}')

def find_max(numlist):
    """แสดงค่ามากที่สุดในช่วงข้อมูล"""
    max_num = 0
    for i in numlist:
        if i > max_num:
            max_num = i
    print(f'\nค่าที่สูงที่สุด คือ {C_GREEN}{max_num}{C_RESET}')
    print(f'\n{"*"*50}')

def find_median(numlist):
    """มัธยฐาน (อังกฤษ: median) คือการวัดแนวโน้มสู่ส่วนกลางชนิดหนึ่ง 
    ที่ใช้อธิบายจำนวนหนึ่งจำนวนที่แบ่งข้อมูลตัวอย่าง หรือประชากร หรือการแจกแจงความน่าจะเป็น 
    ออกเป็นครึ่งส่วนบนกับครึ่งส่วนล่าง มัธยฐานของรายการข้อมูลขนาดจำกัด 
    สามารถหาได้โดยการเรียงลำดับข้อมูลจากน้อยไปมาก"""
    numlist.sort()
    numlistpos = (len(numlist)) / 2 #ใช้หาตำแหน่ง
    mod = len(numlist) % 2 #เพื่่อเช็คว่าเป็นจำนวนเต็มมั้ย ถ้า0เป็นจำนวนเต็ม ถ้าเป็นค่าอื่นเป็นจำนวนเศษ
    if mod == 0 :#ในกรณีจำนวนเต็ม
        numlistpos = int(numlistpos)#แปลงเป็นintเพื่อใช้ระบุตำแหน่งในlist
        total = (numlist[numlistpos - 1] + numlist[numlistpos]) / 2#สูตรเมื่อจำนวนเป็นเลขคู่
    else :
        numlistpos = round(numlistpos)  #แปลงเป็นintเพื่อใช้ระบุตำแหน่งในlist โดยปัดเศษลง
        total = numlist[numlistpos - 1] #สูตรเมื่อจำนวนเป็นเลขคี่
    print(f'\nค่ามัธยฐาน คือ {C_GREEN}{total}{C_RESET}')
    print(f'\n{"*"*50}')

def find_mean(numlist):
    """ค่าเฉลี่ย (Average, Mean) หมายถึง 
    ค่าเฉลี่ยซึ่งเกิดจากข้อมูลของผลรวมทั้งหมดหารด้วยจำนวนรายการของข้อมูล"""
    numlistlen = len(numlist) #นับสมาชิกเก็บไว้ในค่าn
    mean = 0
    for i in numlist :
        mean = mean + i #บวกค่าในลิตส์
    mean = mean / numlistlen #หาค่าเฉลี่ยโดยการหาร
    print(f'\nค่ามัชฌิมเลขคณิต คือ {C_GREEN}{mean}{C_RESET}')
    print(f'\n{"*"*50}')

def find_md(numlist):
    """ฟังก์ชั่น ส่วนเบี่ยงเบนเฉลี่ย (Mean deviation : M.D.) เป็นค่าที่ใช้วัดการกระจายของข้อมูลรอบๆ 
    ค่าเฉลี่ย (Mean) โดยการหาค่าเฉลี่ยของผลรวมของผลต่างระหว่างคะแนนแต่ละตัวกับค่าเฉลี่ย 
    ถ้าส่วนเบี่ยงเบนเฉลี่ยมีค่ามากแสดงว่ามีการ กระจายมาก 
    ถ้าส่วนเบี่ยงเบนเฉลี่ยมีค่าน้อยแสดงว่ามีการกระจายน้อย"""
    lennumlist = len(numlist)
    list_num = []
    numtemp = 0
    sum_num = 0
    for i in numlist : #ใช้Sum ค่าใน numlist
        numtemp = numtemp + i#บวกค่าในลิตส์
    x_bar = numtemp / lennumlist#หาค่าเฉลี่ยโดยการหาร

    for j in range(lennumlist) : #อ่านค่าn
        tempnum = numlist[j] - x_bar #เก็บสมาชิกลบX_barและเก็บไว้ในตัวแปร
        if tempnum < 0:#ถ้าเป็นลบให้คูณด้วย-1เพื่อแปลงเป็นบวก
            tempnum = tempnum * (-1)
        list_num.append(tempnum)#Addเข้าlist_num

    for k in list_num :#ใช้Sum ค่าในlist_num
        sum_num = sum_num + k#บวกค่าในลิตส์
    sum_num = sum_num / lennumlist#หาค่าM.D.
    md_value = round(sum_num,2)
    print(f'\nความเบี่ยงเบนเฉลี่ย คือ {C_GREEN}{md_value}{C_RESET}')
    print(f'\n{"*"*50}')

def find_sd(numlist):
    """ส่วนเบี่ยงเบนมาตรฐาน (Standard deviation: SD) 
    เป็นค่าที่บอกถึงการกระจายของตัวเลขในกลุ่มข้อมูล"""
    lennumlist = len(numlist)
    list_num = []
    numtemp = 0
    sum_num = 0
    for i in numlist : #ใช้Sum ค่าใน numlist
        numtemp = numtemp + i#บวกค่าในลิตส์
    x_bar = numtemp / lennumlist#หาค่าเฉลี่ยโดยการหาร

    for j in range(lennumlist) : #อ่านค่าn
        tempnum = numlist[j] - x_bar #เก็บสมาชิกลบX_barและเก็บไว้ในตัวแปร
        tempnum = tempnum ** (2) #นำค่าหลังจากลบกับค่าาเฉลี่ย
        list_num.append(tempnum)#Addเข้าlist_num

    for k in list_num :#ใช้Sum ค่าในlist_num
        sum_num = sum_num + k#บวกค่าในลิตส์
    sum_num = math.sqrt(sum_num / lennumlist)
    sd_value = round(sum_num,2)
    print(f'\nความเบี่ยงเบนมาตรฐาน คือ {C_GREEN}{sd_value}{C_RESET}')
    print(f'\n{"*"*50}')

def find_s_2(numlist):
    """ค่าความแปรปรวน (Variance) คือ ค่าของส่วนเบี่ยงเบนมาตรฐานยกกำลังสอง 
    ซึ่งความแปรปรวนสามารถวัดการกระจายของข้อมูลได้"""
    lennumlist = len(numlist)
    list_num = []
    numtemp = 0
    sum_num = 0
    for i in numlist : #ใช้Sum ค่าใน numlist
        numtemp = numtemp + i#บวกค่าในลิตส์
    x_bar = numtemp / lennumlist#หาค่าเฉลี่ยโดยการหาร

    for j in range(lennumlist) : #อ่านค่าn
        tempnum = numlist[j] - x_bar #เก็บสมาชิกลบX_barและเก็บไว้ในตัวแปร
        tempnum = tempnum ** (2) #นำค่าหลังจากลบกับค่าาเฉลี่ย
        list_num.append(tempnum)#Addเข้าlist_num

    for k in list_num :#ใช้Sum ค่าในlist_num
        sum_num = sum_num + k#บวกค่าในลิตส์
    sum_num = sum_num / lennumlist
    s_2_value = round(sum_num,2)
    print(f'\nความแปรปรวน คือ {C_GREEN}{s_2_value}{C_RESET}')
    print(f'\n{"*"*50}')

def find_range(numlist):
    """พิสัย เป็นช่วงระหว่างค่าที่สูงที่สุดของชุดข้อมูลกับค่าที่ต่ำที่สุดของชุดข้อมูล 
    หาได้โดยการนำค่าที่สูงที่สุดลบด้วยค่าที่ต่ำที่สุด หากพิสัยมีค่าสูง 
    แสดงว่าข้อมูลชุดนั้นมีการกระจายตัวห่างกันมาก แต่หากพิสัยมีค่าน้อย แสดงว่าข้อมูลนั้นเกาะกลุ่มกัน"""
    max_num = 0
    min_num = numlist[0]
    numlistlen = len(numlist)

    for i in numlist:
        if i > max_num:
            max_num = i

    for i in range(numlistlen):
        if numlist[i] < min_num:
            min_num = numlist[i]

    range_value = max_num - min_num
    print(f'\nค่าพิสัยคือ {C_GREEN}{range_value}{C_RESET}')
    print(f'\n{"*"*50}')

#!MAIN PROGRAM
IS_RUN = True
clearscreen()
while IS_RUN:
    try:
        print(f'{C_RESET}{"*"*50}\n')
        num = input(f'{C_RESET}กรอกตัวเลข (เป็นชุด หรือ ทีละตัว) >>> {C_GREEN}')
        print(f'{C_RESET}\n{"*"*50}\n')
        numlist_input(num)
    finally:
        print(f'\n{C_RESET}ต้องการทำงานอีกครั้งหรือไม่ [ Y / N ] ?')
        q = input(f'\t>>>{C_GREEN} ')
        resetcolor()
        if q.upper() not in ['Y']:
            print(f'\n{C_RESET}{"*"*50}\n')
            print('จบการทำงาน')
            print(f'\n{"*"*50}\n')
            IS_RUN = False
        else:
            print('\n')
