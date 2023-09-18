def clearscreen():
    print('\033c')

def list_Input(inputset,menu = 0):
    numlist = []
    try:
        if len(inputset) <= 3:
            inputset = int(inputset)
            numlist.append(inputset)
            while True:
                if len(numlist) <= 99:
                    inputset = float(input(f'\tกรอกตัวเลขเพิ่มเติม (1-999) ตัวที่ : {len(numlist)+1} >>> '))
                    if inputset > 0 and inputset < 1000:
                        numlist.append(inputset)
                    else:
                        print(f'\n{"*"*50}\n')
                        print('เสร็จสิ้นการกรอกข้อมูล')
                        print(f'ชุดข้อมูลคือ (ขนาดชุดข้อมูล {len(numlist)}) : {numlist}')
                        break
                else:
                    print(f'\n{"*"*50}\n')
                    print('เสร็จสิ้นการกรอกข้อมูล')
                    print(f'ชุดข้อมูลคือ (ขนาดชุดข้อมูล {len(numlist)}) : {numlist}')
                    break
        else:
            numlist = map(float, inputset.replace(', ', ',').replace(',', ' ').split(" "))
            numlist = list(numlist)
            print(f'ชุดข้อมูลคือ (ขนาดชุดข้อมูล {len(numlist)}) : {numlist}')

        print(f'\n{"*"*50}\n')
        if menu == 0:
            print('ต้องการไปโหมดไหน')
            print('\t1. Min')
            print('\t2. Max')
            print('\t3. Median')
            print('\t4. Mean')
            print(f'\n{"*"*50}\n')
            menu = int(input('\t>>> '))
            print(f'\n{"*"*50}')

    except ValueError:
        print('พอข้อผิดพลาด กรุณาเช็คตัวเลขที่ท่านกรอกมา')

    finally:
        match menu:
            case 1:
                find_Max(numlist)
            case 2:
                find_Max(numlist)
            case 3:
                find_Mode(numlist)
            case 4:
                find_Mean(numlist)

def find_Max(numlist):
    numlist = numlist
    x = 0
    for i in numlist:
        if i > x:
            x = i
    print(f'\nค่าที่สูงที่สุด คือ {x}')
    print(f'\n{"*"*50}\n')

def find_Mode(numlist):
    numlist.sort()
    numlistpos = (len(numlist)) / 2 #ใช้หาตำแหน่ง
    mod = (len(numlist)) % 2 #เพื่่อเช็คว่าเป็นจำนวนเต็มมั้ย ถ้า0เป็นจำนวนเต็ม ถ้าเป็นค่าอื่นเป็นจำนวนเศษ
    if mod == 0 :#ในกรณีจำนวนเต็ม
        numlistpos = int(numlistpos)#แปลงเป็นintเพื่อใช้ระบุตำแหน่งในlist
        total = (numlist[numlistpos - 1] + numlist[numlistpos]) / 2#สูตรเมื่อจำนวนเป็นเลขคู่
    else :
        numlistpos = round(numlistpos)  #แปลงเป็นintเพื่อใช้ระบุตำแหน่งในlist โดยปัดเศษลง
        total = numlist[numlistpos - 1] #สูตรเมื่อจำนวนเป็นเลขคี่
    print(f'\nค่ามัธยฐาน คือ {total}')
    print(f'\n{"*"*50}\n')

def find_Mean(numlist):
    numlistlen = (len(numlist)) #นับสมาชิกเก็บไว้ในค่าn
    mean = 0
    for i in numlist :
        mean = mean + i #บวกค่าในลิตส์
    mean = mean / numlistlen #หาค่าเฉลี่ยโดยการหาร
    print(f'\nค่ามัชฌิมเลขคณิต คือ {mean}')
    print(f'\n{"*"*50}\n')

#!MAIN PROGRAM
clearscreen()
print(f'{"*"*50}\n')
num = input('กรอกตัวเลข (เป็นชุด หรือ ทีละตัว) >>> ')
print(f'\n{"*"*50}\n')
list_Input(num)


lislek = [1,3,7,6,9,5,8,2,1,9,4,4] #list รับอินพุท
n=(len(lislek))#นับสมาชิกเก็บไว้ในค่าn
list_num=[]
x=0
sum_num=0
for i in lislek : #ใช้Sum ค่าในlislek
    x=x+i#บวกค่าในลิตส์
x_bar=x/n#หาค่าเฉลี่ยโดยการหาร

for j in range(len(lislek)) : #อ่านค่าn
    lek_korn=lislek[j]-x_bar #เก็บสมาชิกลบX_barและเก็บไว้ในตัวแปร
    if lek_korn<0:#ถ้าเป็นลบให้คูณด้วย-1เพื่อแปลงเป็นบวก
        lek_korn=lek_korn*(-1)
    list_num.append(lek_korn)#Addเข้าlist_num

for k in list_num :#ใช้Sum ค่าในlist_num
    sum_num=sum_num+k#บวกค่าในลิตส์
sum_num=sum_num/n#หาค่าM.D.
print(round(sum_num,2))
