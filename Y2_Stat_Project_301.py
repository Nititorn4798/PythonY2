"""โปรแกรมคำนวณค่าสถิติ"""
import math
import time
import os
import sys

try:
    from prettytable import PrettyTable
    print('\u001b[32m',"Prettytable Module is installed.",'\u001b[0m')
    time.sleep(0.3)
except ImportError:
    print('\u001b[31m',"ท่านยังไม่ได้ติดตั้งโมดูล prettytable")
    print(" ท่านสามารถติดตั้งโดยการใช้คำสั่ง '\u001b[32mpython -m pip install -U prettytable\u001b[31m'\u001b[0m")
    raise
from prettytable import PrettyTable

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

output_table = PrettyTable()
output_table.align = "r"

last_numlist = []
QUESTION = ''
def numlist_input(inputset,bypassinput = 0,menu = 0):
    """ฟังก์ชั่น รับชุดตัวเลข ที่มีการทำงานสองแบบ
    1. รับตัวเลข 1 ตัวก่อน
    2. รับตัวเลขมาทั้งชุด
        หลังจากรับข้อมูลเสร็จสิ้นจะให้เลือกการฟังก์ชั่นทำงานที่จะนำชุดตัวเลขไปคำนวณ"""
    numlist = []
    temp_last_numlist = []
    is_error = False
    try:
        if bypassinput == 0 :
            if len(inputset[0:10].replace(', ', ',').replace(',', ' ').split(" ")) == 1:
                inputset = float(inputset)
                numlist.append(inputset)
                print(f'{C_YELLOW}พิมพ์ {C_GREEN}0{C_YELLOW} เพื่อจบการกรอกเลข{C_RESET}')
                while True:
                    if len(numlist) <= 99:
                        while True :
                            print(f'\t{C_RESET}กรอกตัวเลขเพิ่มเติม (1-999) ตัวที่ : {C_BLUE}{len(numlist)+1}{C_RESET} >>> {C_GREEN}',end='')
                            inputset = input()
                            if inputset == '' or inputset.isnumeric() is False  :
                                print(f'{C_RED}กรุณากรอกตัวเลขเท่านั้น{C_RESET}')
                                print(f'{C_YELLOW}พิมพ์ {C_GREEN}0{C_YELLOW} เพื่อจบการกรอกเลข{C_RESET}')
                            else:
                                inputset = float(inputset)
                                break
                        if inputset > 0 and inputset < 1000 :
                            numlist.append(inputset)
                        else:
                            print(f'\n{C_RESET}{"*"*50}\n')
                            print(f'{C_GREEN}เสร็จสิ้นการกรอกข้อมูล{C_RESET}')
                            print(f'{C_RESET}ชุดข้อมูลคือ (ขนาดชุดข้อมูล {C_GREEN}{len(numlist)}{C_RESET}) : {C_BLUE}{numlist}{C_RESET}')
                            break
                    else:
                        print(f'\n{"*"*50}\n')
                        print(f'{C_GREEN}เสร็จสิ้นการกรอกข้อมูล{C_RESET}')
                        print(f'{C_RESET}ชุดข้อมูลคือ (ขนาดชุดข้อมูล {C_GREEN}{len(numlist)}{C_RESET}) : {C_BLUE}{numlist}{C_RESET}')
                        break
            else:
                numlist = map(float, inputset.replace(', ', ',').replace(' ,', ',').replace(',', ' ').split(" "))
                numlist = list(numlist) #! ทำให้ Map เป็น List
                if len(numlist) > 100:
                    print(f'{C_RESET}ค่าที่รับมา มีเกินจำนวนที่แนะนำ 100 ค่า ({C_RED}{len(numlist)} ค่า{C_RESET}) ต้องการตัดส่วนเกินออกหรือไม่ [ Y / N ] ?')
                    quest = input(f'\t>>>{C_GREEN} ')
                    resetcolor()
                    if quest.upper() in ['Y']:
                        numlist = numlist[0:100] #! เอาแค่ 100 ตัว
                print(f'{C_RESET}ชุดข้อมูลคือ (ขนาดชุดข้อมูล {C_GREEN}{len(numlist)}{C_RESET} ค่า) : {C_BLUE}{numlist}{C_RESET}')
        else:
            numlist = inputset
            if QUESTION.upper() not in ['R'] :
                print('รับค่าผ่านไฟล์ text สำเร็จ')
            else:
                print('ใช้ชุดข้อมูลเก่า สำเร็จ')
            print(f'{C_RESET}ชุดข้อมูลคือ (ขนาดชุดข้อมูล {C_GREEN}{len(numlist)}{C_RESET}) : {C_BLUE}{numlist}{C_RESET}')

        print(f'\n{"*"*50}\n')
        temp_last_numlist.extend(numlist)
        if menu == 0:
            while True:
                print('เลือกโหมดการคำนวณที่ต้องการ')
                print('\t1. ไม่แจกแจง')
                print('\t2. แจกแจง')
                print(f'\n{"*"*50}\n')
                print(f'\t>>>{C_GREEN} ',end='')
                menu = input()
                if menu == '' or menu.isnumeric() is False  :
                    print(f'{C_RED}กรุณากรอกตัวเลขเท่านั้น{C_RESET}')
                else:
                    menu = int(menu)
                    break
            print(f'\n{C_RESET}{"*"*50}')

    except ValueError:
        print(f'\n{C_RED}พบข้อผิดพลาด กรุณาเช็คตัวเลขที่ท่านกรอกมา{C_RESET}\n')
        is_error = True

    finally:
        if is_error is False:
            match menu:
                case 1:
                    while True:
                        print('\nเลือกโหมดการคำนวณแบบไม่แจกแจง ที่ต้องการ')
                        print('\t1. ค่าสูงสุด Max')
                        print('\t2. ค่าต่่ำสุด Min')
                        print('\t3. ค่ามัชฌิมเลขคณิต x̄ Mean')
                        print('\t4. ค่ามัธยฐาน Median')
                        print('\t5. ฐานนิยม Mode')
                        print('\t6. ความเบี่ยงเบนเฉลี่ย Mean Deviation')
                        print('\t7. ความเบี่ยงเบนมาตรฐาน Standard Deviation')
                        print('\t8. ความแปรปรวน S2, Variance')
                        print('\t9. ค่าพิสัยของคะแนน Range')
                        print('\t999. ทุกการคำนวณ')
                        print(f'\n{"*"*50}\n')
                        print(f'\t>>>{C_GREEN} ',end='')
                        menu_x = input()
                        if menu_x == '' or menu_x.isnumeric() is False  :
                            print(f'{C_RED}กรุณากรอกตัวเลขเท่านั้น{C_RESET}')
                        else:
                            menu_x = int(menu_x)
                            break
                    print(f'\n{C_RESET}{"*"*50}')
                    match menu_x:
                        case 1 :
                            find_max(numlist)
                        case 2 :
                            find_min(numlist)
                        case 3 :
                            find_mean(numlist)
                        case 4 :
                            find_median(numlist)
                        case 5 :
                            find_mode(numlist)
                        case 6 :
                            find_md(numlist)
                        case 7 :
                            find_sd(numlist)
                        case 8 :
                            find_s_2(numlist)
                        case 9 :
                            find_range(numlist)
                        case 999:
                            find_max(numlist)
                            find_min(numlist)
                            find_mean(numlist)
                            find_median(numlist)
                            find_mode(numlist)
                            find_md(numlist)
                            find_sd(numlist)
                            find_s_2(numlist)
                            find_range(numlist)
                            print(f'\n{output_table}')
                        case _ :
                            print(f'\n{C_RED}พบข้อผิดพลาด กรุณาเช็คตัวเลขที่ท่านกรอกมา{C_RESET}\n')
                case 2:
                    frequency_distribution(numlist)
                case _ :
                    print(f'\n{C_RED}พบข้อผิดพลาด กรุณาเช็คตัวเลขที่ท่านกรอกมา{C_RESET}\n')
        last_numlist.clear()
        last_numlist.extend(temp_last_numlist)

MYPATH = os.path.dirname(os.path.abspath(sys.argv[0]))
MYFILE = "NUM_SET.txt"
TXTFILENAMELEN = len(MYFILE)
TXTMODE = "load"

def loaddatatxt():
    """ฟังก์ชั่นโหลดข้อมูลจากไฟล์ txt"""
    try:
        if TXTMODE == "load":
            with open(f'{MYPATH}/{MYFILE}', 'x', encoding="utf-8") as numformtxt:
                print(f'{"*"*(35+TXTFILENAMELEN)}\n**    {C_GREEN}{MYFILE} Not Found สร้างไฟล์สำเร็จ{C_RESET}    **\n{"*"*(35+TXTFILENAMELEN)}\n')
                numformtxt.writelines('รูปแบบของข้อมูล "1 20 31 41" หรือ "1,2,3,4,5,60" หรือ "1, 2, 3, 41, 10" เริ่มกรอกข้อมูลที่บรรทัดด้านล่างเป็นต้นไป (รองรับมากกว่า 1 บรรทัด) (หากไม่ต้องการใช้ให้ทำให้บรรทัดถัดไปว่าง) \n')
                numformtxt.close()
    except FileExistsError:
        print('')
        print(f'{"*"*(27+TXTFILENAMELEN)}\n**    {C_GREEN}{MYFILE} Found ใช้ไฟล์เก่า{C_RESET}    **\n{"*"*(27+TXTFILENAMELEN)}\n')

    is_loaderror = False
    tempnumlist_str = ''
    numlist_txt = []
    numtxt = open(f'{MYPATH}/{MYFILE}', 'r+', encoding="utf-8")
    txtline = 1
    print(f'{"*"*(24+TXTFILENAMELEN)}\n**    {C_GREEN}โหลดข้อมูลจาก {MYFILE}{C_RESET}    **\n{"*"*(24+TXTFILENAMELEN)}\n')
    try:
        for i in numtxt:
            if txtline > 1:
                numtxt_temp = i
                tempnumlist_str += numtxt_temp.replace('\n', ' ')
                print(tempnumlist_str) #!DEBUG
            txtline += 1
        if not tempnumlist_str: #? ถ้า List ว่าง = False
            print('ไม่พบข้อมูลใน txt')
            is_loaderror = True #!ให้ไม่ขึ้น Loaddone
            for i in range(2,0,-1):
                print(f'Delay {i}s',end='.\n')
                time.sleep(1)
            clearscreen()
            return 'empty'
        numlist_txt = map(float, tempnumlist_str.replace(', ', ',').replace(' ,', ',').replace(',', ' ').split(" "))
        numlist_txt = list(numlist_txt)
        print(numlist_txt) #!DEBUG
        print(f'\n\t{C_BLUE}Load Done...{C_RESET}')
    except ValueError:
        is_loaderror = True
        print(f'\n{C_RED}เกิดข้อผิดพลาดขณะโหลดไฟล์ (ValueError) กรุณาตรวจสอบค่า ในข้อมูลที่บรรทัด {txtline-1} ว่าตัวสุดท้ายมีการเว้นไว้หรือไม่{C_RESET}')
        print('\nError Detail : \n')
        return 'error'
    except IndentationError:
        is_loaderror = True
        print(f'\n{C_RED}เกิดข้อผิดพลาดขณะโหลดไฟล์ (IndentationError) กรุณาตรวจสอบการเว้นวรรค ในข้อมูลที่บรรทัด {txtline-1}{C_RESET}')
        print('\nError Detail : \n')
        return 'error'
    finally:
        if is_loaderror is False:
            print(f'\n{"*"*(31+TXTFILENAMELEN)}\n**    {C_GREEN}โหลดข้อมูลจาก {MYFILE} เสร็จสิ้น{C_RESET}    **\n{"*"*(31+TXTFILENAMELEN)}\n')
    if is_loaderror is False:
        for i in range(1,0,-1):
            print(f'Delay {i}s',end='.\n')
            time.sleep(1)
        clearscreen()
        return numlist_txt

def find_min(numlist):
    """แสดงค่าน้อยที่สุดในช่วงข้อมูล"""
    min_num = numlist[0]
    numlistlen = len(numlist)
    for i in range(numlistlen):
        if numlist[i] < min_num:
            min_num = numlist[i]
    print(f'\nค่าที่ต่่ำที่สุด คือ {C_GREEN}{min_num}{C_RESET}')
    output_table.add_column('Min',[min_num])

def find_max(numlist):
    """แสดงค่ามากที่สุดในช่วงข้อมูล"""
    max_num = 0
    for i in numlist:
        if i > max_num:
            max_num = i
    print(f'\nค่าที่สูงที่สุด คือ {C_GREEN}{max_num}{C_RESET}')
    output_table.add_column('Max',[max_num])

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
    output_table.add_column('Median',[total])

def find_mean(numlist):
    """ค่าเฉลี่ย (Average, Mean) หมายถึง 
    ค่าเฉลี่ยซึ่งเกิดจากข้อมูลของผลรวมทั้งหมดหารด้วยจำนวนรายการของข้อมูล"""
    numlistlen = len(numlist) #นับสมาชิกเก็บไว้ในค่าn
    mean = 0
    for i in numlist :
        mean = mean + i #บวกค่าในลิตส์
    mean = mean / numlistlen #หาค่าเฉลี่ยโดยการหาร
    print(f'\nค่ามัชฌิมเลขคณิต คือ {C_GREEN}{mean}{C_RESET}')
    output_table.add_column('Mean',[mean])

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
    output_table.add_column('M.D.',[md_value])

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
    output_table.add_column('S.D.',[sd_value])

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
    output_table.add_column('S2',[s_2_value])

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
    output_table.add_column('Range',[range_value])

def find_mode(numlist):
    """ค่าฐานนิยม ( Mode ) คือ ค่าของข้อมูลตัวที่เกิดขึ้นบ่อยที่สุด หรือตัวที่มีความถี่มากที่สุด 
    โดยปกติข้อมูล 1 ชุดจะมีฐานนิยมค่าเดียว แต่เป็นไปได้ที่ข้อมูลบางชุดอาจมีฐานนิยมมากกว่า 1 ค่า"""
    num_counter = {
    }
    num_members = []
    mode = ''
    for num_i in numlist:
        if(num_i in num_counter):#ถ้าเลขที่อยู่ในlistซ้ำกับเลขในDictที่มีอยู๋แล้วให้+1เพิ่มเป็นValue
            num_counter[num_i] += 1
        else:#ถ้าเลขยังไม่อยู่ในdictให้เซตเป็น1ไว้
            num_counter[num_i] = 1

    for (member,maxx) in num_counter.items() :#samachick,maxคือการเปลี่ยเทียบกับ.item()ที่มีค่าออกมาเป็นเซตๆ หรือ(samachick,max)=(x,y) เมื่อxและyเป็นค่าในnaplek.items()
        if maxx == max(num_counter.values()):#หาค่าที่ซ้ำมากที่สุดของvalueทั้งหมดของdict และเทียบกับmaxxทุกๆตัว เพื่อหาsamachick
            num_members.append(member)#เพื่อเพิ่มไว้ดูว่ามีฐานนิยมที่เป็นสมาชิกกี่ตัว และตัวไหนบ้างที่เป็น
    len_num_members = len(num_members)
    ishave_mode = True
    num_members.sort()
    for i in range(len_num_members):
        if len(num_members) == 1:
            mode = str(num_members[i])
        elif len(num_members) > 1 and len(num_members) < 3:#ถ้าสมาชิกของnumมากกว่า0และน้อยกว่า3ให้ปริ้นฐานนิยมออกมาได้(ฐานนิยมมีได้มากสุด2ตัว)
            mode = mode + ', '+ str(num_members[i])
        else :#แต่ถ้าสมาชิกของnumไม่อยู่ในเงื่อนไข
            ishave_mode = False

    if ishave_mode is True :
        mode = mode.replace(',','',1)
        print(f'\nค่าฐานนิยมมี {C_BLUE}{len_num_members} ค่า{C_RESET} คือ {C_GREEN}{mode}{C_RESET}')
        output_table.add_column('Mode',[mode])
    else :
        print(f'\n{C_GREEN}ไม่มีค่าฐานนิยม{C_RESET}')
        output_table.add_column('Mode',['ไม่มีค่าฐานนิยม'])

def frequency_distribution(numlist) :
    """ฟังก์ชั่นหา การแจกแจงความถี่ (Frequency Distribution)
    การแจกแจงความถี่เป็นการนำข้อมูลที่เป็นค่าของตัวแปรที่เราสนใจมาจัดเรียงตามลำดับความมากน้อย 
    และแบ่งเป็นช่วงเท่าๆกัน จำนวนข้อมูลในแต่ละช่วงคะแนน เรียกว่า ความถี่"""
    num_min = numlist[0]
    num_max = 0
    f_mom_last = 0
    f_num={
    }
    low_upper_class = {
    }#ขีดจำกัดล่างและบนในรูปแบบของdict
    frequency_distribution_num_table = PrettyTable()
    frequency_distribution_num_table.align = "r"
    frequency_distribution_num_table.field_names = ["ช่วงคะแนน", "ขีดจำกัดล่าง", "ขีดจำกัดบน", "จุดกลางชั้น", "ความถี่", "ความถี่สะสม", "fx", "สัดส่วน", "ร้อยละ"]

    for i in numlist:
        if i > num_max:
            num_max = i
    len_numlist_x = len(numlist)
    for i in range(len_numlist_x):
        if numlist[i] < num_min:
            num_min = numlist[i]

    print(f'พิสัย : {C_GREEN}{(num_max - (num_min))}{C_RESET}')
    if (num_max - (num_min)) < 5 :
        print('ค่าพิสัยน้อยกว่า 5 ใช้รูปแบบการแจกแจงไม่ได้')
        return 0
    max_class = ((num_max - (num_min)) + 1) / 2
    max_class = min(max_class, 15)
    while True :
        print(f'สามารถใช้ข้อมูลจำนวนชั้นได้มากสุด : {C_RED}{max_class}{C_RESET}')
        num_class_interval = int(input(f'\tกรอกจำนวนชั้นที่ต้องการ >>>{C_GREEN} '))
        resetcolor()
        if (num_class_interval > (num_max - ((num_min)) + 1) / 2) :
            print(f'{C_RED}ชั้นมีจำนวนมากกว่าความกว้างของอันตรภาคชั้น กรุณากรอกชั้นใหม่อีกครั้ง{C_RESET}')
        elif (num_class_interval < 3) or (num_class_interval > 15) :
            print(f'{C_RED}อันตรภาคชั้นต้องอยู่ระหว่าง 3-15 ชั้น กรุณากรอกชั้นใหม่อีกครั้ง{C_RESET}')
        else:
            break
    range_x = math.ceil(((num_max - (num_min)) + 1) / num_class_interval)# ความกว้างของอัตราภาคแบบจำนวนเต็มที่ต้อง+1เพื่อบวกจำนวนตัวมันเอง
    lower_class_lim = num_min #ขีดจำกัดล่างเริ่มต้นแถว1
    upper_class_lim = (num_min + range_x) - 1#ขีดจำกัดบนเริ่มต้นแถว1
    low_upper_class[lower_class_lim] = upper_class_lim
    for i in range(1,num_class_interval):
        lower_class_lim = upper_class_lim + 1#ขีดจำกัดล่างตั้งแต่แถว2ขึ้นไป
        upper_class_lim = (lower_class_lim + range_x) - 1#ขีดจำกัดบนตั้งแต่แถว2ขึ้นไป
        low_upper_class[lower_class_lim] = upper_class_lim
    print(f'ความกว้างของอันตรภาค : {C_GREEN}{range_x}{C_RESET}')#แสดงความกว้างของอันตรภาคชั้น

    table_martrix = []

    matrx_ptr_column = 0 #! Pointer เมทริกซ์ คอลัมน์
    matrx_ptr_row = 0 #! Pointer เมทริกซ์ แถว
    #แสดงค่าในตาราง
    for (member,maxx) in low_upper_class.items() :#member,maxxคือการเปลี่ยเทียบกับ.item()ที่มีค่าออกมาเป็นเซตๆ หรือ(member,maxx)=(x,y) เมื่อxและyเป็นค่าในnum_taw.items()
        table_martrix.append(["",0,0,0,0,0,0,0,0])
        table_martrix[matrx_ptr_row][matrx_ptr_column] = f'{member} - {maxx}'
        matrx_ptr_row = matrx_ptr_row + 1

    #หาขีดจำกัดล่างและบน
    matrx_ptr_column = 1
    matrx_ptr_row = 0
    for (member,maxx) in low_upper_class.items() :#member,maxxคือการเปลี่ยเทียบกับ.item()ที่มีค่าออกมาเป็นเซตๆ หรือ(member,maxx)=(x,y) เมื่อxและyเป็นค่าในnum_taw.items()
        table_martrix[matrx_ptr_row][matrx_ptr_column] = f'{member - 0.5}'
        table_martrix[matrx_ptr_row][matrx_ptr_column + 1] = f'{maxx + 0.5}'
        matrx_ptr_row = matrx_ptr_row + 1

    #หาจุดกึ่งกลาง
    matrx_ptr_column = 3
    matrx_ptr_row = 0
    for (member,maxx) in low_upper_class.items() :#member,maxxคือการเปลี่ยเทียบกับ.item()ที่มีค่าออกมาเป็นเซตๆ หรือ(member,maxx)=(x,y) เมื่อxและyเป็นค่าในnum_taw.items()
        table_martrix[matrx_ptr_row][matrx_ptr_column] = f'{((member - 0.5) + (maxx + 0.5)) / 2}'
        matrx_ptr_row = matrx_ptr_row + 1

    #หาความถี่
    matrx_ptr_column = 4
    matrx_ptr_row = 0
    for (member,maxx) in low_upper_class.items() :#member,maxxคือการเปลี่ยเทียบกับ.item()ที่มีค่าออกมาเป็นเซตๆ หรือ(member,maxx)=(x,y) เมื่อxและyเป็นค่าในnum_taw.items()
        f_num[member] = 0
        len_numlist = len(numlist)
        for k in range(len_numlist):
            if (numlist[k] >= member) and (numlist[k] <= maxx) :
                f_num[member] += 1
    for (f_mem,f_mom) in f_num.items() : #!mem key ขอบล่าง แต่ชั้น fmon คือความถี่
        table_martrix[matrx_ptr_row][matrx_ptr_column] = f'{f_mom}'
        #?หาสัดส่วน ร้อยละ
        table_martrix[matrx_ptr_row][matrx_ptr_column + 2] = f'{float(table_martrix[matrx_ptr_row][3]) * float(table_martrix[matrx_ptr_row][4])}'
        table_martrix[matrx_ptr_row][matrx_ptr_column + 3] = f'{f_mom / sum(f_num.values()):.3f}'
        table_martrix[matrx_ptr_row][matrx_ptr_column + 4] = f'{(f_mom / sum(f_num.values())) * 100:.3f}'
        matrx_ptr_row = matrx_ptr_row + 1

    #ค่าความถี่สะสม
    matrx_ptr_column = 5
    matrx_ptr_row = 0
    for (f_mem,f_mom) in f_num.items() : #!f mem key f mom value
        f_mom_last = f_mom_last + f_mom
        table_martrix[matrx_ptr_row][matrx_ptr_column] = f'{f_mom_last}'
        matrx_ptr_row = matrx_ptr_row + 1

    #!ส่วนการแสดงตาราง
    len_num_martrix = len(table_martrix)
    for i in range(len_num_martrix):
        frequency_distribution_num_table.add_row([table_martrix[i][0], table_martrix[i][1], table_martrix[i][2],
                            table_martrix[i][3], table_martrix[i][4], table_martrix[i][5],
                            table_martrix[i][6], table_martrix[i][7], table_martrix[i][8]])
    print(f'\n\n{frequency_distribution_num_table}')
    sum_percent = 0
    for i in range(len_num_martrix) :
        sum_percent = sum_percent + float(table_martrix[i][8])
    sum_ratio = 0
    for i in range(len_num_martrix) :
        sum_ratio = sum_ratio + float(table_martrix[i][7])

    print(f'\n\tN : {C_GREEN}{len_numlist_x}{C_RESET} \n\tTotal Ratio   : {C_GREEN}{sum_ratio:.2f}{C_RESET} \n\tTotal Percent : {C_GREEN}{math.trunc(sum_percent):.3f}{C_RESET}')

#!MAIN PROGRAM
IS_RUN = True
LOAD_LAST = False
clearscreen()
while IS_RUN:
    try:
        if LOAD_LAST is False :
            loadtemp = loaddatatxt() #!เพื่อ Load เพียงครั้งเดียว
            match loadtemp :
                case 'empty':
                    print(f'{C_RESET}{"*"*50}\n')
                    num = input(f'{C_RESET}กรอกตัวเลข (เป็นชุด หรือ ทีละตัว) >>> {C_GREEN}')
                    print(f'{C_RESET}\n{"*"*50}\n')
                    numlist_input(num)
                case 'error':
                    print('การโหลดข้อมูลจากไฟล์ txt ผิดพลาด ใช้งานการกรอกข้อมูลด้วยมือ\n')
                    print(f'{C_RESET}{"*"*50}\n')
                    num = input(f'{C_RESET}กรอกตัวเลข (เป็นชุด หรือ ทีละตัว) >>> {C_GREEN}')
                    print(f'{C_RESET}\n{"*"*50}\n')
                    numlist_input(num)
                case _ :
                    if QUESTION == '' :
                        numlist_input(loadtemp,1) #! (loadtemp,X,Y) 1 คือ bypass input (!=0)
                    else:
                        print(f'\n{C_RESET}ต้องการรับข้อมูลผ่านไฟล์ txt หรือไม่ [ Y / N ] ?')
                        QUESTION = input(f'\t>>>{C_GREEN} ')
                        if QUESTION.upper() not in ['Y']:
                            print(f'{C_RESET}{"*"*50}\n')
                            num = input(f'{C_RESET}กรอกตัวเลข (เป็นชุด หรือ ทีละตัว) >>> {C_GREEN}')
                            print(f'{C_RESET}\n{"*"*50}\n')
                            numlist_input(num)
                        else:
                            numlist_input(loadtemp,1)
        else:
            numlist_input(last_numlist,1)

    finally:
        print(f'\n{"*"*50}')
        if len(last_numlist) > 0 :
            print(f'\nพิมพ์ {C_GREEN}R{C_RESET} เพื่อใช้งานโปรแกรมอีกครั้งโดยใช้ชุดข้อมูลล่าสุด')
            print(f'{C_RESET}ชุดข้อมูลล่าสุดคือ (ขนาดชุดข้อมูล {C_GREEN}{len(last_numlist)}{C_RESET}) : {C_BLUE}{last_numlist}{C_RESET}')
            print(f'\n{C_RESET}ต้องการทำงานอีกครั้งหรือไม่ [ Y / N / R ] ?')
        else:
            print(f'\n{C_RESET}ต้องการทำงานอีกครั้งหรือไม่ [ Y / N ] ?')
        QUESTION = input(f'\t>>>{C_GREEN} ')
        resetcolor()
        if QUESTION.upper() in ['R'] and len(last_numlist) > 0 :
            LOAD_LAST = True
            output_table.clear()
        elif QUESTION.upper() not in ['Y']:
            print(f'\n{C_RESET}{"*"*50}\n')
            print('จบการทำงาน')
            print(f'\n{"*"*50}\n')
            IS_RUN = False
        else:
            last_numlist.clear()
            LOAD_LAST = False
            output_table.clear()
            print('\n')
