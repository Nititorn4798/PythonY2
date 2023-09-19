"""โปรแกรมคำนวณค่าสถิติ"""
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
C_REST = '\u001b[0m'

def numlist_input(inputset,menu = 0):
    """ฟังก์ชั่น รับชุดตัวเลข ที่มีการทำงานสองแบบ
    1. รับตัวเลข 1 ตัวก่อน
    2. รับตัวเลขมาทั้งชุด
        หลังจากรับข้อมูลเสร็จสิ้นจะให้เลือกการฟังก์ชั่นทำงานที่จะนำชุดตัวเลขไปคำนวณ"""
    numlist = []
    try:
        if ((len(inputset) <= 3) and inputset.isdigit()) or len(inputset.replace(', ', ',').replace(',', ' ').split(" ")) == 1:
            inputset = float(inputset)
            numlist.append(inputset)
            while True:
                if len(numlist) <= 99:
                    inputset = float(input(f'\t{C_REST}กรอกตัวเลขเพิ่มเติม (1-999) ตัวที่ : {C_BLUE}{len(numlist)+1}{C_REST} >>> {C_GREEN}'))
                    if inputset > 0 and inputset < 1000:
                        numlist.append(inputset)
                    else:
                        print(f'\n{C_REST}{"*"*50}\n')
                        print('เสร็จสิ้นการกรอกข้อมูล')
                        print(f'{C_REST}ชุดข้อมูลคือ (ขนาดชุดข้อมูล {C_GREEN}{len(numlist)}{C_REST}) : {C_BLUE}{numlist}{C_REST}')
                        break
                else:
                    print(f'\n{"*"*50}\n')
                    print('เสร็จสิ้นการกรอกข้อมูล')
                    print(f'{C_REST}ชุดข้อมูลคือ (ขนาดชุดข้อมูล {C_GREEN}{len(numlist)}{C_REST}) : {C_BLUE}{numlist}{C_REST}')
                    break
        else:
            numlist = map(float, inputset.replace(', ', ',').replace(',', ' ').split(" "))
            numlist = list(numlist) #! ทำให้ Map เป็น List
            print(f'{C_REST}ชุดข้อมูลคือ (ขนาดชุดข้อมูล {C_GREEN}{len(numlist)}{C_REST}) : {C_BLUE}{numlist}{C_REST}')

        print(f'\n{"*"*50}\n')
        if menu == 0:
            print('เลือกโหมดการคำนวณที่ต้องการ')
            print('\t1. Min')
            print('\t2. Max')
            print('\t3. Median')
            print('\t4. Mean')
            print(f'\n{"*"*50}\n')
            menu = int(input('\t>>> '))
            print(f'\n{"*"*50}')

    except ValueError:
        print(f'\n{C_RED}พบข้อผิดพลาด กรุณาเช็คตัวเลขที่ท่านกรอกมา{C_REST}\n')
        raise

    finally:
        match menu:
            case 1:
                find_min(numlist)
            case 2:
                find_max(numlist)
            case 3:
                find_median(numlist)
            case 4:
                find_mean(numlist)

def find_min(numlist):
    """แสดงค่าน้อยที่สุดในช่วงข้อมูล"""
    min_num = numlist[0]
    numlistlen = len(numlist)
    for i in range(numlistlen):
        if numlist[i] < min_num:
            min_num = numlist[i]
    print(f'\nค่าที่ต่่ำที่สุด คือ {C_GREEN}{min_num}{C_REST}')
    print(f'\n{"*"*50}\n')

def find_max(numlist):
    """แสดงค่ามากที่สุดในช่วงข้อมูล"""
    max_num = 0
    for i in numlist:
        if i > max_num:
            max_num = i
    print(f'\nค่าที่สูงที่สุด คือ {C_GREEN}{max_num}{C_REST}')
    print(f'\n{"*"*50}\n')

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
    print(f'\nค่ามัธยฐาน คือ {C_GREEN}{total}{C_REST}')
    print(f'\n{"*"*50}\n')

def find_mean(numlist):
    """ค่าเฉลี่ย (Average, Mean) หมายถึง 
    ค่าเฉลี่ยซึ่งเกิดจากข้อมูลของผลรวมทั้งหมดหารด้วยจำนวนรายการของข้อมูล"""
    numlistlen = len(numlist) #นับสมาชิกเก็บไว้ในค่าn
    mean = 0
    for i in numlist :
        mean = mean + i #บวกค่าในลิตส์
    mean = mean / numlistlen #หาค่าเฉลี่ยโดยการหาร
    print(f'\nค่ามัชฌิมเลขคณิต คือ {C_GREEN}{mean}{C_REST}')
    print(f'\n{"*"*50}\n')

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
    print(f'\nส่วนเบี่ยงเบนเฉลี่ย คือ {C_GREEN}{md_value}{C_REST}')

#!MAIN PROGRAM
IS_RUN = True
clearscreen()
while IS_RUN:
    try:
        print(f'{C_REST}{"*"*50}\n')
        num = input(f'{C_REST}กรอกตัวเลข (เป็นชุด หรือ ทีละตัว) >>> {C_GREEN}')
        print(f'{C_REST}\n{"*"*50}\n')
        numlist_input(num)
    finally:
        print(f'{C_REST}ต้องการทำงานอีกครั้งหรือไม่ [ Y / N ] ?')
        q = input(f'\t>>>{C_GREEN} ')
        resetcolor()
        if q.upper() not in ['Y']:
            print(f'\n{C_REST}{"*"*50}\n')
            print('จบการทำงาน')
            print(f'\n{"*"*50}\n')
            IS_RUN = False
        else:
            print('\n')
