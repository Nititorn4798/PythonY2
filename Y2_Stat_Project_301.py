"""โปรแกรมคำนวณค่าสถิติ""" 
import math
import time
import os
import sys
import subprocess
import random
# pylint: disable=C0301
try:
    from prettytable import PrettyTable, SINGLE_BORDER
    print('\u001b[32m',"\n✔ Prettytable Module is installed.",'\u001b[0m')
except ImportError:
    print('\u001b[41m',"✖ You have not installed the 'Prettytable' module.")
    print("\u001b[0m ✖ You can install 'Prettytable' using the command \u001b[31m'\u001b[32mpython -m pip install -U prettytable\u001b[31m'","\u001b[0m")
    raise
from prettytable import PrettyTable
# pylint: disable=C0302
C_BLACK = '\u001b[30m'
C_RED = '\u001b[91m'
C_GREEN = '\u001b[92m'
C_YELLOW = '\u001b[93m'
C_BLUE = '\u001b[94m'
C_MAGENTA = '\u001b[95m'
C_CYAN = '\u001b[96m'
C_WHITE = '\u001b[97m'
C_RESET = '\u001b[0m'
C_BOLD = '\u001b[1m'
C_UNDERLINE = '\u001b[4m'

try: #!ส่วนการแก้ไขการแสดงผลสี โดยการแก้ไข ค่าใน register ให้ cmd รองรับ ansi color
    import ctypes
    if ctypes.windll.shell32.IsUserAnAdmin():
        CMD_CM = "reg add HKEY_CURRENT_USER\Console /v VirtualTerminalLevel /t REG_DWORD /d 1" # pylint: disable=W1401 # pyright: ignore[reportInvalidStringEscapeSequence]
        fixcolor = subprocess.Popen(CMD_CM, shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        if fixcolor.stdin is not None:
            fixcolor.stdin.write('Yes')
            fixcolor.stdin.flush()
            stdout, stderr = fixcolor.communicate()
            print("\u001b[32m","\n✔ Enabling ANSI Color support in the Windows console was successful.")
            print("\u001b[32m","\n✔ If colors are displayed abnormally, please restart the program to use ANSI colors.")
            if stderr:
                print("Error:")
                print(stderr)
            fixcolor.wait()
        else:
            print("\n\n✖ Enabling ANSI Color support in the Windows console was unsuccessful.")
except ImportError:
    pass

DELAY = 0

def clearscreen():
    """ฟังก์ชัน ล้างหน้าจอ terminal"""
    if DELAY > 0 :
        emoji = ['Made With ❤️  By CS65','🔥','😊','💀','👍','เกรด A สถิติ 🙏','✔️','🤔','🎃','😳','🥰','ความจริงมีเพียงหนึ่งเดียวเท่านั้น 🧐','พ่อสอนให้ที่ฮาวาย 😉','🤨']
        for i in range(1,DELAY+1):
            block_print = ((i / (DELAY)) * 100)
            for _ in range(int(block_print)) :
                print('▒',end='')
                time.sleep(0.001)
            print(f'{C_GREEN} {math.ceil(block_print)} % {emoji[random.randrange(0,len(emoji))]} {C_RESET}',end='\r')
            time.sleep(1)
    print('\033c',end='')

def resetcolor():
    """ฟังก์ชันรีเซ็ทค่าสี"""
    print('\u001b[0m',end='')

MYPATH = os.path.dirname(os.path.abspath(sys.argv[0]))
MYFILE = "NUM_SET.txt"
TXTMODE = "load"

CONFIGLANG = ''
ISDEBUG = False

textset = {"en": {
    "หาไม่เจอ": "Not Found,",
    "ไฟล์ถูกสร้างสำเร็จแล้ว": "file created successfully.",
    "พบแล้ว ใช้ไฟล์ที่มีอยู่": "Discovered, Utilize the existing file.",
    "การตั้งค่าภาษาปัจจุบันคือ": "Current language setting is",
    "! เปิดใช้งานการดีบั๊กค่าระหว่างคำนวณแล้ว": "! Enables debugging of values during calculation.",
    '! ตั้งค่าหน่วงเวลาล้างจอ สำเร็จแล้ว': '! The screen clearing delay setting has been successfully set.',
    "! ไม่สามารถเรียกการตั้งค่าการหน่วงเวลาได้": "! Unable to retrieve delay setting.",
    "ตั้งค่าหน่วงเวลาเป็น": "Set Delay to",
    "วินาที": "seconds.",
    "! พบข้อผิดพลาดในค่าที่ตั้งค่า จะเปลี่ยนตั้งค่าเป็นค่าตั้งต้น 0 0 เพื่อปิดการใช้งาน การเลือกโหมดตั้งต้น": "! An error was found in the setting value. Change the setting to the default '0 0' to disabled. 'Default mode'",
    "โหลดข้อมูลจาก": "Loading data from",
    "เสร็จสิ้น": "has been completed.",
    "ไม่พบข้อมูลในไฟล์ txt": "Data not found in the txt file.",
    "พิมพ์": "Type",
    "เพื่อจบการกรอกเลข": "To complete number entry",
    "กรอกตัวเลขเพิ่มเติม (1-999) ตัวที่ :": "Enter additional numbers (1-999) at number :",
    "กรุณากรอกตัวเลขเท่านั้น": "Please enter numbers only.",
    "เสร็จสิ้นการกรอกข้อมูล": "Data entry completed",
    "ชุดข้อมูลคือ (ขนาดชุดข้อมูล": "Data set is (data set size",
    "ค่าที่รับมา มีเกินจำนวนที่แนะนำ 100 ค่า (": "Received values exceed the recommended limit of 100 (",
    "ค่า": "values",
    "ต้องการตัดส่วนเกินออกหรือไม่": "Trim the excess values?",
    "รับค่าผ่านไฟล์ text สำเร็จ": "Successfully received values via text file",
    "ใช้ชุดข้อมูลเก่า สำเร็จ": "Used the latest data set successfully",
    "เลือกโหมดการคำนวณที่ต้องการ": "Select the desired calculation mode",
    "ไม่แจกแจงความถี่": "Not Frequency Distribution",
    "แจกแจงความถี่": "Frequency Distribution",
    "พบข้อผิดพลาด กรุณาตรวจสอบตัวเลขที่ท่านกรอกมา": "Error encountered. Please check the entered numbers.",
    "เลือกโหมดการคำนวณแบบไม่แจกแจง ที่ต้องการ": "Select the desired non-distributed calculation mode",
    "ค่าสูงสุด Max": "Maximum value",
    "ค่าต่่ำสุด Min": "Minimum value",
    "ค่ามัชฌิมเลขคณิต x̄ Mean": "Arithmetic mean",
    "ค่ามัธยฐาน Median": "Median",
    "ฐานนิยม Mode": "Mode",
    "ความเบี่ยงเบนเฉลี่ย Mean Deviation": "Average deviation",
    "ความเบี่ยงเบนมาตรฐาน Standard Deviation": "Standard deviation",
    "ความแปรปรวน S2, Variance": "Variance",
    "ค่าพิสัยของคะแนน Range": "Range of scores",
    "เรียกใช้ทุกการคำนวณ": "All calculations",
    "เกิดข้อผิดพลาดขณะโหลดไฟล์ (ValueError) กรุณาตรวจสอบค่า ในข้อมูลที่บรรทัด": "An error occurred while loading the file (ValueError). Please check the value in the line of data",
    "ว่าตัวสุดท้ายมีการเว้นไว้หรือไม่": "Whether the last value is omitted or not",
    "เกิดข้อผิดพลาดขณะโหลดไฟล์ (IndentationError) กรุณาตรวจสอบการเว้นวรรค ในข้อมูลที่บรรทัด": "An error occurred while loading the file (IndentationError). Please check the indentation in the line of data",
    "ค่าที่ต่่ำที่สุด คือ": "The minimum value is",
    "ค่าที่สูงที่สุด คือ": "The maximum value is",
    "ค่ามัธยฐาน คือ": "The median is",
    "ค่ามัชฌิมเลขคณิต คือ": "The arithmetic mean is",
    "ความเบี่ยงเบนเฉลี่ย คือ": "The average deviation is",
    "ความเบี่ยงเบนมาตรฐาน คือ": "The standard deviation is",
    "ความแปรปรวน คือ": "The variance is",
    "ค่าพิสัย คือ": "The range is",
    "คือ": "is",
    "ค่าฐานนิยมมี": "The mode value are",
    "ไม่มีค่าฐานนิยม": "No mode value",
    "ตารางแจกแจงความถี่": "Frequency Distribution Table",
    "อันตรภาคชั้น": "Class Intervals",
    "ขีดจำกัดล่าง": "Lower limit",
    "ขีดจำกัดบน": "Upper limit",
    "จุดกลางชั้น": "Middle point",
    "ความถี่": "Frequency",
    "ความถี่สะสม": "Cumulative frequency",
    "fx": "fx",
    "สัดส่วน": "Ratio",
    "ร้อยละ": "Percentage",
    "พิสัย": "Range",
    "ค่าพิสัยน้อยกว่า 5 ใช้รูปแบบการแจกแจงไม่ได้": "Range values less than 5 cannot use the distribution model.",
    "สามารถใช้ข้อมูลจำนวนชั้นได้มากสุด :": "Maximum number of classes that can be used:",
    "กรอกจำนวนชั้นที่ต้องการ >>>": "Enter the desired number of classes >>>",
    "ชั้นมีจำนวนมากกว่าความกว้างของอันตรภาคชั้น กรุณากรอกชั้นใหม่อีกครั้ง": "The number of classes exceeds the width of the class intervals. Please enter the number of classes again.",
    "อันตรภาคชั้นต้องอยู่ระหว่าง 3-15 ชั้น กรุณากรอกชั้นใหม่อีกครั้ง": "The number of classes must be between 3-15. Please enter the number of classes again.",
    "ความกว้างของอันตรภาคชั้น :": "Width of class interval:",
    "อัตราส่วนรวม   :": "Total Ratio   :",
    "เปอร์เซ็นต์รวม   :": "Total Percent :",
    "ค่าความเบี่ยงเบนควอไทล์ คือ": "The quantile deviation value is",
    "ความเบี่ยงเบนมาตรฐาน SD. คือ": "Standard deviation SD. is",
    "ความแปรปรวน S2 คือ": "The variance S2 is",
    "ค่าเฉลี่ย คือ": "The mean is",
    "ค่าฐานนิยม คือ": "The mode value is",
    "กรอกตัวเลข (เป็นชุด หรือ ทีละตัว) >>>": "Enter numbers (as sets or individually) >>>",
    "การโหลดข้อมูลจากไฟล์ txt ผิดพลาด ใช้งานการกรอกข้อมูลด้วยตนเอง": "Error loading data from txt file. Manual data entry is required.",
    "ต้องการรับข้อมูลผ่านไฟล์ txt หรือไม่": "Do you want to receive data via a txt file?",
    "เพื่อใช้งานโปรแกรมอีกครั้งโดยใช้ชุดข้อมูลล่าสุด": "To run the program again using the recent data set.",
    "ชุดข้อมูลล่าสุดคือ (ขนาดชุดข้อมูล": "The recent data set is (data set size",
    "ต้องการคำนวณอีกครั้งหรือไม่": "Do you want to calculate again?",
    "จบการทำงาน": "End of operation",
    "จัดทำโดย": "Program prepared by"
}}

def gettext(textcode, bypass = False):
    "ฟังก์ชันภาษา"
    if CONFIGLANG == 'en' or bypass:
        return textset['en'][textcode]
    return textcode

#!ฟังก์ชันโหลดการตั้งค่าภาษา และ สร้างไฟล์ txt ถ้าไม่พบ
DEFMODE = 0 #? ค่าตั้งต้น โหมดการทำงาน
DEFCALMODE = 0 #? ค่าตั้งต้น โหมดการคำนวณ (โหมดการทำงาน 1 ไม่แจกแจง 2 แจกแจง)
DEFNUMCLASS = 0 #? ค่าตั้งต้น จำนวนชั้น
CONFIGFILE = "settings_stat.txt"
while True:
    def createconfig(mode_file = 'x') :
        """ฟังก์ชันสร้างไฟล์การตั้งค่า หรือ รีเซ็ทการตั้งค่าหากไฟล์การตั้งค่าไม่ถูกต้อง"""
        with open(f'{MYPATH}/{CONFIGFILE}', f'{mode_file}', encoding="utf-8") as createconfig_x:
            print(f'{C_BLUE}{CONFIGFILE} {C_GREEN}{gettext("หาไม่เจอ", True)} {C_BLUE}{CONFIGFILE} {C_GREEN}{gettext("ไฟล์ถูกสร้างสำเร็จแล้ว", True)}{C_RESET}\n')
            createconfig_x.writelines('#  นี่คือไฟล์การตั้งค่า สามารถตั้งภาษาได้โดยการเปลี่ยนค่า = en หรือ = th | เปลี่ยน DEBUG = True เพื่อแสดงค่าระหว่างที่คำนวณ | Delay = (วิ) เพื่อตั้งหน่วงเวลาล้างหน้าจอในหน่วยวินาที | Default Mode = (1-2) (1-9,999 [เมื่อใช้โหมด 1 จะเป็นเลือกการคำนวณ, ในโหมด 2 จะเป็นจำนวนชั้น] ) เพื่อเลือกการทำงานโดยที่ไม่ต้องเลือกในโปรแกรม #\n')
            createconfig_x.writelines('languages [en,th] = please-setup\n')
            createconfig_x.writelines('DEBUG = False\n')
            createconfig_x.writelines('Delay [sec] = 1\n')
            createconfig_x.writelines('Default Mode = 0 0\n')
            createconfig_x.close()
    try:
        configs = open(f'{MYPATH}/{CONFIGFILE}', 'r+', encoding="utf-8")
        textconfig = configs.read()
        textconfig = textconfig.split("\n")
        if len(textconfig) < 6: #! รีเซ็ทการตั้งค่าหากบรรทัดไม่ครบ
            configs.close()
            createconfig('w')
            configs = open(f'{MYPATH}/{CONFIGFILE}', 'r+', encoding="utf-8")
        else:
            configs = open(f'{MYPATH}/{CONFIGFILE}', 'r+', encoding="utf-8")
        for line, content in enumerate(configs) :
            if line == 1 :
                tempconfig = content.replace('\n', '').replace(' = ', ' = ').split(" = ")
                CONFIGLANG = tempconfig[-1]
                while True:
                    if CONFIGLANG not in ['en', 'th']:
                        CONFIGLANG = input(f'{C_RED}\n✖ Language not found ({C_YELLOW}{CONFIGLANG}{C_RED}).\n✖ Please select language again [{C_YELLOW}en,th{C_RED}] >>> {C_GREEN}')
                        resetcolor()
                    else:
                        configsave = open(f'{MYPATH}/{CONFIGFILE}', 'r', encoding="utf-8")
                        configtemp = configsave.read()
                        configsave.close()
                        tempconfigtxt = configtemp.split('\n')
                        tempconfigtxt[1] = f'languages [en,th] = {CONFIGLANG}'
                        configsave = open(f'{MYPATH}/{CONFIGFILE}', 'w', encoding="utf-8")
                        for i_config in tempconfigtxt :
                            if i_config not in ['','\n'] :
                                configsave.writelines(f'{i_config}\n')
                        configsave.close()
                        break
            if line == 2 :
                tempconfig = content.replace('\n', '').replace(' = ', ' = ').split(" = ")
                if tempconfig[-1].upper() in ['TRUE'] :
                    ISDEBUG = True
                    print(f'\n{C_YELLOW}{gettext("! เปิดใช้งานการดีบั๊กค่าระหว่างคำนวณแล้ว")}{C_RESET}')
            if line == 3 :
                tempconfig = content.replace('\n', '').replace(' = ', ' = ').split(" = ")
                if tempconfig[-1].isnumeric() is True :
                    DELAY = int(tempconfig[-1])
                    print(f'\n{C_YELLOW}{gettext("! ตั้งค่าหน่วงเวลาล้างจอ สำเร็จแล้ว")} ({DELAY} {gettext("วินาที")}) {C_RESET}')
                else:
                    print(f'{C_RED}{gettext("! ไม่สามารถเรียกการตั้งค่าการหน่วงเวลาได้")}{C_YELLOW} {gettext("ตั้งค่าหน่วงเวลาเป็น")} 3 {gettext("วินาที")}')
                    DELAY = 3
            if line == 4 :
                tempconfig = content.replace('\n', '').replace(' = ', ' = ').split(" = ")
                tempconfig = tempconfig[-1].split(" ")
                def configeditor(defmode_x = '0'):
                    """ฟังก์ชันแก้ไขไฟล์ตั้งค่าเมื่อไฟล์ตั้งค่าไม่ถูกต้อง"""
                    print(f"{C_RED}{gettext('! พบข้อผิดพลาดในค่าที่ตั้งค่า จะเปลี่ยนตั้งค่าเป็นค่าตั้งต้น 0 0 เพื่อปิดการใช้งาน การเลือกโหมดตั้งต้น')}{C_RESET}")
                    configsave_x = open(f'{MYPATH}/{CONFIGFILE}', 'r', encoding="utf-8")
                    configtemp_x = configsave_x.read()
                    configsave_x.close()
                    tempconfigtxt_x = configtemp_x.split('\n')
                    tempconfigtxt_x[4] = f'Default Mode = {defmode_x} 0'
                    configsave_x = open(f'{MYPATH}/{CONFIGFILE}', 'w', encoding="utf-8")
                    for i_config_x in tempconfigtxt_x :
                        if i_config_x not in ['','\n'] :
                            configsave_x.writelines(f'{i_config_x}\n')
                    configsave_x.close()
                match len(tempconfig):
                    case 1 :
                        if tempconfig[0].isnumeric() is True :
                            if tempconfig[0] in ['0','1','2'] :
                                DEFMODE = int(tempconfig[0])
                        else:
                            configeditor()
                    case 2 :
                        if tempconfig[0].isnumeric() is True and tempconfig[1].isnumeric() is True:
                            if tempconfig[0] in ['0','1','2'] :
                                DEFMODE = int(tempconfig[0])
                                if DEFMODE == 1:
                                    if tempconfig[1] in ['0','1','2','3','4','5','6','7','8','9','999']:
                                        DEFCALMODE = int(tempconfig[1])
                                    else:
                                        configeditor('1')
                                if DEFMODE == 2:
                                    if 3 <= int(tempconfig[1]) <= 15:
                                        DEFNUMCLASS = int(tempconfig[1])
                            else:
                                configeditor()
                        else:
                            configeditor()
                    case _ :
                        configeditor()
                if ISDEBUG :
                    print(f'{C_YELLOW}\nDEFMODE : {DEFMODE} \nDEFCALMODE : {DEFCALMODE}{C_RESET}')
                    if DEFMODE == 2:
                        print(f'{C_YELLOW}DEFNUMCLASS : {DEFNUMCLASS}')
                configs.close()
                break
        print(f'\n{gettext("การตั้งค่าภาษาปัจจุบันคือ")} {C_BOLD}{C_YELLOW}{CONFIGLANG}{C_RESET}\n')
        break

    except FileNotFoundError:
        createconfig()

output_table = PrettyTable()
output_table.align = "r"
output_table.set_style(SINGLE_BORDER)

last_numlist = []
QUESTION = ''
def numlist_input(inputset, bypassinput = 0, defmode = 0, defcalmode = 0): #! bypassinput คือ การข้ามการรับข้อมูลด้วยการกรอก ถ้าหากรับผ่านไฟล์ text
    """ฟังก์ชัน รับชุดตัวเลข ที่มีการทำงานสองแบบ
    1. รับตัวเลข 1 ตัวก่อน
    2. รับตัวเลขมาทั้งชุด
        หลังจากรับข้อมูลเสร็จสิ้นจะให้เลือกการฟังก์ชันทำงานที่จะนำชุดตัวเลขไปคำนวณ"""
    numlist = []
    temp_last_numlist = []
    is_error = False
    try:
        if bypassinput == 0 :
            if len(inputset[0:10].replace(', ', ',').replace(',', ' ').split(" ")) == 1:
                inputset = float(inputset)
                if 0 < inputset < 1000:
                    numlist.append(inputset)
                print(f'{C_YELLOW}{gettext("พิมพ์")} {C_GREEN}0{C_YELLOW} {gettext("เพื่อจบการกรอกเลข")}{C_RESET}')
                while True:
                    if len(numlist) <= 99:
                        while True :
                            print(f'\t{C_RESET}{gettext("กรอกตัวเลขเพิ่มเติม (1-999) ตัวที่ :")} {C_BOLD}{C_BLUE}{len(numlist)+1}{C_RESET} >>> {C_GREEN}',end='')
                            inputset = input()
                            if inputset == '' or inputset.isnumeric() is False  :
                                print(f'{C_RED}✖ {gettext("กรุณากรอกตัวเลขเท่านั้น")}{C_RESET}')
                                print(f'{C_YELLOW}{gettext("พิมพ์")} {C_GREEN}0{C_YELLOW} {gettext("เพื่อจบการกรอกเลข")}{C_RESET}')
                            else:
                                inputset = float(inputset)
                                break
                        if 0 < inputset < 1000 :
                            numlist.append(inputset)
                        elif len(numlist) > 0:
                            print(f'\n{C_RESET}{"═"*100}\n')
                            print(f'{C_GREEN}✔ {gettext("เสร็จสิ้นการกรอกข้อมูล")}{C_RESET}')
                            print(f'{C_RESET}✔ {gettext("ชุดข้อมูลคือ (ขนาดชุดข้อมูล")} {C_BOLD}{C_GREEN}{len(numlist)}{C_RESET}) : {C_BLUE}{numlist}{C_RESET}\n')
                            break
                    else:
                        print(f'\n{"═"*100}\n')
                        print(f'{C_GREEN}✔ {gettext("เสร็จสิ้นการกรอกข้อมูล")}{C_RESET}')
                        print(f'{C_RESET}✔ {gettext("ชุดข้อมูลคือ (ขนาดชุดข้อมูล")} {C_BOLD}{C_GREEN}{len(numlist)}{C_RESET}) : {C_BLUE}{numlist}{C_RESET}\n')
                        break
            else:
                numlist = map(float, inputset.replace(', ', ',').replace(' ,', ',').replace(',', ' ').split(" "))
                numlist = list(numlist) #! ทำให้ Map เป็น List
                if len(numlist) > 100:
                    print(f'{C_RESET}{gettext("ค่าที่รับมา มีเกินจำนวนที่แนะนำ 100 ค่า (")}{C_BOLD}{C_RED}{len(numlist)} {gettext("ค่า")}{C_RESET}) {gettext("ต้องการตัดส่วนเกินออกหรือไม่")} [ Y / N ] ?')
                    quest = input(f'\t>>>{C_GREEN} ')
                    resetcolor()
                    if quest.upper() in ['Y']:
                        numlist = numlist[0:100] #! เอาแค่ 100 ตัว
                print(f'{C_RESET}{gettext("ชุดข้อมูลคือ (ขนาดชุดข้อมูล")} {C_BOLD}{C_GREEN}{len(numlist)}{C_RESET} {gettext("ค่า")}) : {C_BLUE}{numlist}{C_RESET}')
        else:
            numlist = inputset
            if QUESTION.upper() not in ['R'] :
                print(f'\n{"═"*100}\n')
                print(f'{C_GREEN}✔ {gettext("รับค่าผ่านไฟล์ text สำเร็จ")}{C_RESET}')
            else:
                print(f'\n{"═"*100}\n')
                print(f'{gettext("ใช้ชุดข้อมูลเก่า สำเร็จ")}')
            print(f'{C_RESET}{gettext("ชุดข้อมูลคือ (ขนาดชุดข้อมูล")} {C_BOLD}{C_GREEN}{len(numlist)}{C_RESET}) : {C_BLUE}{numlist}{C_RESET}\n')

        print(f'{"═"*100}\n')
        temp_last_numlist.extend(numlist)
        if defmode == 0:
            while True:
                print(f'{gettext("เลือกโหมดการคำนวณที่ต้องการ")}')
                print(f'\t1. {gettext("ไม่แจกแจงความถี่")}')
                print(f'\t2. {gettext("แจกแจงความถี่")}')
                print(f'\n{"═"*100}\n')
                print(f'\t>>>{C_GREEN} ',end='')
                defmode = input()
                if defmode == '' or defmode.isnumeric() is False  :
                    print(f'\n{C_RED}✖ {gettext("กรุณากรอกตัวเลขเท่านั้น")}{C_RESET}\n')
                else:
                    defmode = int(defmode)
                    break
            print(f'\n{C_RESET}{"═"*100}')

    except ValueError:
        print(f'{C_RED}✖ {gettext("พบข้อผิดพลาด กรุณาตรวจสอบตัวเลขที่ท่านกรอกมา")}{C_RESET}')
        is_error = True

    finally:
        if is_error is False:
            match defmode:
                case 1 :
                    while True:
                        print(f'\n{gettext("เลือกโหมดการคำนวณแบบไม่แจกแจง ที่ต้องการ")}')
                        print(f'\t1. {gettext("ค่าสูงสุด Max")}')
                        print(f'\t2. {gettext("ค่าต่่ำสุด Min")}')
                        print(f'\t3. {gettext("ค่ามัชฌิมเลขคณิต x̄ Mean")}')
                        print(f'\t4. {gettext("ค่ามัธยฐาน Median")}')
                        print(f'\t5. {gettext("ฐานนิยม Mode")}')
                        print(f'\t6. {gettext("ความเบี่ยงเบนเฉลี่ย Mean Deviation")}')
                        print(f'\t7. {gettext("ความเบี่ยงเบนมาตรฐาน Standard Deviation")}')
                        print(f'\t8. {gettext("ความแปรปรวน S2, Variance")}')
                        print(f'\t9. {gettext("ค่าพิสัยของคะแนน Range")}')
                        print(f'\t999. {gettext("เรียกใช้ทุกการคำนวณ")}')
                        print(f'\n{"═"*100}\n')
                        print(f'\t>>>{C_GREEN} ',end='')
                        if defcalmode == 0:
                            menu_x = input()
                            if menu_x == '' or menu_x.isnumeric() is False  :
                                print(f'\n{C_RED}✖ {gettext("กรุณากรอกตัวเลขเท่านั้น")}{C_RESET}')
                            else:
                                menu_x = int(menu_x)
                                break
                        else:
                            print(f'{defcalmode} {C_YELLOW}(Default Mode)')
                            menu_x = defcalmode
                            break
                    print(f'\n{C_RESET}{"═"*100}')
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
                        case 999 :
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
                            print(f'\n{C_RED}✖ {gettext("พบข้อผิดพลาด กรุณาตรวจสอบตัวเลขที่ท่านกรอกมา")}{C_RESET}')
                case 2 :
                    frequency_distribution(numlist,DEFNUMCLASS)
                case _ :
                    print(f'\n{C_RED}✖ {gettext("พบข้อผิดพลาด กรุณาตรวจสอบตัวเลขที่ท่านกรอกมา")}{C_RESET}')
        last_numlist.clear()
        last_numlist.extend(temp_last_numlist)

def loaddatatxt():
    """ฟังก์ชันโหลดข้อมูลจากไฟล์ txt"""
    try:
        if TXTMODE == "load":
            with open(f'{MYPATH}/{MYFILE}', 'x', encoding="utf-8") as numformtxt:
                print(f'\n{C_BLUE}{MYFILE} {C_GREEN}{gettext("หาไม่เจอ")} {MYFILE} {gettext("ไฟล์ถูกสร้างสำเร็จแล้ว")}{C_RESET}\n')
                numformtxt.writelines('# รูปแบบของข้อมูล "1 20 31 41" หรือ "1,2,3,4,5,60" หรือ "1, 2, 3, 41, 10" เริ่มกรอกข้อมูลที่บรรทัดที่ 3 เป็นต้นไป (รองรับมากกว่า 1 บรรทัด) (หากไม่ต้องการใช้ให้ทำให้บรรทัดที่ 3 ว่าง) #\n')
                numformtxt.writelines('# เริ่มกรอกบรรทัดถัดไป (ห้ามมีบรรทัดว่าง) #\n')
                numformtxt.close()
    except FileExistsError:
        print('')
        print(f'{C_BLUE}{MYFILE} {C_GREEN}{gettext("พบแล้ว ใช้ไฟล์ที่มีอยู่")}{C_RESET}\n')

    is_loaderror = False
    tempnumlist_str = ''
    numlist_txt = []
    numtxt = open(f'{MYPATH}/{MYFILE}', 'r+', encoding="utf-8")
    txtline = 1
    print(f'{C_GREEN}{gettext("โหลดข้อมูลจาก")} {C_BLUE}{MYFILE}{C_RESET}\n')
    try:
        for i in numtxt:
            if txtline > 2:
                numtxt_temp = i
                tempnumlist_str += numtxt_temp.replace('\n', ' ')
                if ISDEBUG is True :
                    print(f'  [{txtline}].\n{numtxt_temp}\n') #!DEBUG
            txtline += 1
        if not tempnumlist_str: #? ถ้า List ว่าง = False
            print(f'{C_YELLOW}{gettext("ไม่พบข้อมูลในไฟล์ txt")}{C_RESET}')
            is_loaderror = True #!ให้ไม่ขึ้น Loaddone
            print('\n')
            clearscreen()
            return 'empty'
        numlist_txt = map(float, tempnumlist_str.replace(', ', ',').replace(' ,', ',').replace(',', ' ').split(" "))
        numlist_txt = list(numlist_txt)
        if ISDEBUG is True :
            print(f'{C_YELLOW}{numlist_txt}{C_RESET}') #!DEBUG
        print(f'\n\t{C_BLUE}Load Done...{C_RESET}')
    except ValueError:
        is_loaderror = True
        print(f'\n{C_RED}✖ {gettext("เกิดข้อผิดพลาดขณะโหลดไฟล์ (ValueError) กรุณาตรวจสอบค่า ในข้อมูลที่บรรทัด")} {txtline-1} {gettext("ว่าตัวสุดท้ายมีการเว้นไว้หรือไม่")}{C_RESET}')
        print('\nError Detail : \n')
        return 'error'
    except IndentationError:
        is_loaderror = True
        print(f'\n{C_RED}✖ {gettext("เกิดข้อผิดพลาดขณะโหลดไฟล์ (IndentationError) กรุณาตรวจสอบการเว้นวรรค ในข้อมูลที่บรรทัด")} {txtline-1}{C_RESET}')
        print('\nError Detail : \n')
        return 'error'
    finally:
        if is_loaderror is False:
            print(f'\n{C_GREEN}✔ {gettext("โหลดข้อมูลจาก")} {C_BLUE}{MYFILE} {C_GREEN}{gettext("เสร็จสิ้น")}{C_RESET}\n')
    if is_loaderror is False:
        clearscreen()
        return numlist_txt

def find_min(numlist):
    """แสดงค่าน้อยที่สุดในช่วงข้อมูล"""
    min_num = numlist[0]
    numlistlen = len(numlist)
    for i in range(numlistlen):
        if numlist[i] < min_num:
            min_num = numlist[i]
    print(f'\n{gettext("ค่าที่ต่่ำที่สุด คือ")} {C_BOLD}{C_GREEN}{min_num:,.2f}{C_RESET}')
    output_table.add_column('Min',[min_num])

def find_max(numlist):
    """แสดงค่ามากที่สุดในช่วงข้อมูล"""
    max_num = 0
    for i in numlist:
        if i > max_num:
            max_num = i
    print(f'\n{gettext("ค่าที่สูงที่สุด คือ")} {C_BOLD}{C_GREEN}{max_num:,.2f}{C_RESET}')
    output_table.add_column('Max',[max_num])

def find_median(numlist):
    """มัธยฐาน (อังกฤษ: median) คือการวัดแนวโน้มสู่ส่วนกลางชนิดหนึ่ง 
    ที่ใช้อธิบายจำนวนหนึ่งจำนวนที่แบ่งข้อมูลตัวอย่าง หรือประชากร หรือการแจกแจงความน่าจะเป็น 
    ออกเป็นครึ่งส่วนบนกับครึ่งส่วนล่าง มัธยฐานของรายการข้อมูลขนาดจำกัด 
    สามารถหาได้โดยการเรียงลำดับข้อมูลจากน้อยไปมาก"""
    numlist.sort()
    numlistpos = (len(numlist)) / 2 #ใช้หาตำแหน่ง
    mod = len(numlist) % 2 #เพื่่อเช็คว่าเป็นจำนวนเต็ม ถ้า0เป็นจำนวนเต็ม ถ้าเป็นค่าอื่นเป็นจำนวนเศษ
    if mod == 0 : #ในกรณีจำนวนเต็ม
        numlistpos = int(numlistpos) #แปลงเป็นintเพื่อใช้ระบุตำแหน่งในlist
        total = (numlist[numlistpos - 1] + numlist[numlistpos]) / 2 #สูตรเมื่อจำนวนเป็นเลขคู่
    else :
        numlistpos = round(numlistpos) #แปลงเป็นintเพื่อใช้ระบุตำแหน่งในlist โดยปัดเศษลง
        total = numlist[numlistpos - 1] #สูตรเมื่อจำนวนเป็นเลขคี่
    print(f'\n{gettext("ค่ามัธยฐาน คือ")} {C_BOLD}{C_GREEN}{total:,.2f}{C_RESET}')
    output_table.add_column('Median',[f'{total:,.2f}'])

def find_mean(numlist):
    """ค่าเฉลี่ย x̄ (Average, Mean) หมายถึง 
    ค่าเฉลี่ยซึ่งเกิดจากข้อมูลของผลรวมทั้งหมดหารด้วยจำนวนรายการของข้อมูล"""
    numlistlen = len(numlist) #นับสมาชิกเก็บไว้ในค่า n
    mean = 0
    for i in numlist :
        mean = mean + i #บวกค่าในลิสต์
    mean = mean / numlistlen #หาค่าเฉลี่ยโดยการหาร
    print(f'\n{gettext("ค่ามัชฌิมเลขคณิต คือ")} {C_BOLD}{C_GREEN}{mean:,.2f}{C_RESET}')
    output_table.add_column('Mean',[f'{mean:,.2f}'])

def find_md(numlist):
    """ฟังก์ชัน ส่วนเบี่ยงเบนเฉลี่ย (Mean deviation : M.D.) เป็นค่าที่ใช้วัดการกระจายของข้อมูลรอบๆ 
    ค่าเฉลี่ย (Mean) โดยการหาค่าเฉลี่ยของผลรวมของผลต่างระหว่างคะแนนแต่ละตัวกับค่าเฉลี่ย 
    ถ้าส่วนเบี่ยงเบนเฉลี่ยมีค่ามากแสดงว่ามีการ กระจายมาก 
    ถ้าส่วนเบี่ยงเบนเฉลี่ยมีค่าน้อยแสดงว่ามีการกระจายน้อย"""
    lennumlist = len(numlist)
    list_num = []
    numtemp = 0
    sum_numlist = 0
    for i in numlist : #ใช้Sum ค่าใน numlist
        numtemp = numtemp + i
    x_bar = numtemp / lennumlist #หาค่าเฉลี่ยโดยการหาร

    for j in range(lennumlist) : #อ่านค่า n
        tempnum = numlist[j] - x_bar #เก็บสมาชิกลบ X_bar และเก็บไว้ในตัวแปร
        if tempnum < 0: #ถ้าเป็นลบให้คูณด้วย -1 เพื่อแปลงเป็นบวก
            tempnum = tempnum * (-1)
        list_num.append(tempnum) #Addเข้าlist_num

    for k in list_num : #ใช้ Sum ค่าในlist_num
        sum_numlist = sum_numlist + k #บวกค่าในลิสต์
    sum_numlist = sum_numlist / lennumlist #หาค่า M.D.
    md_value = round(sum_numlist,2)
    print(f'\n{gettext("ความเบี่ยงเบนเฉลี่ย คือ")} {C_BOLD}{C_GREEN}{md_value:,.2f}{C_RESET}')
    output_table.add_column('M.D.',[f'{md_value:,.2f}'])

def find_sd(numlist):
    """ส่วนเบี่ยงเบนมาตรฐาน (Standard deviation: SD) 
    เป็นค่าที่บอกถึงการกระจายของตัวเลขในกลุ่มข้อมูล"""
    lennumlist = len(numlist)
    list_num = []
    numtemp = 0
    sum_numlist = 0
    for i in numlist : #ใช้Sum ค่าใน numlist
        numtemp = numtemp + i #บวกค่าในลิสต์
    x_bar = numtemp / lennumlist #หาค่าเฉลี่ยโดยการหาร

    for j in range(lennumlist) : #อ่านค่าn
        tempnum = numlist[j] - x_bar #เก็บสมาชิกลบ X_bar และเก็บไว้ในตัวแปร
        tempnum = tempnum ** (2) #นำค่าหลังจากลบกับค่าเฉลี่ย
        list_num.append(tempnum) #Addเข้า list_num

    for k in list_num : #ใช้Sum ค่าในlist_num
        sum_numlist = sum_numlist + k #บวกค่าในลิสต์
    sum_numlist = math.sqrt(sum_numlist / (lennumlist-1))
    sd_value = round(sum_numlist,2)
    print(f'\n{gettext("ความเบี่ยงเบนมาตรฐาน คือ")} {C_BOLD}{C_GREEN}{sd_value:,.2f}{C_RESET}')
    output_table.add_column('S.D.',[f'{sd_value:,.2f}'])

def find_s_2(numlist):
    """ค่าความแปรปรวน (Variance) คือ ค่าของส่วนเบี่ยงเบนมาตรฐานยกกำลังสอง 
    ซึ่งความแปรปรวนสามารถวัดการกระจายของข้อมูลได้"""
    lennumlist = len(numlist)
    list_num = []
    numtemp = 0
    sum_numlist = 0
    for i in numlist : #ใช้Sum ค่าใน numlist
        numtemp = numtemp + i #บวกค่าในลิสต์
    x_bar = numtemp / lennumlist #หาค่าเฉลี่ยโดยการหาร

    for j in range(lennumlist) : #อ่านค่าn
        tempnum = numlist[j] - x_bar #เก็บสมาชิกลบX_barและเก็บไว้ในตัวแปร
        tempnum = tempnum ** (2) #นำค่าหลังจากลบกับค่าเฉลี่ย
        list_num.append(tempnum) #Addเข้าlist_num

    for k in list_num : #ใช้Sum ค่าใน list_num
        sum_numlist = sum_numlist + k #บวกค่าในลิตส์
    sum_numlist = sum_numlist / lennumlist
    s_2_value = round(sum_numlist,2)
    print(f'\n{gettext("ความแปรปรวน คือ")} {C_BOLD}{C_GREEN}{s_2_value:,.2f}{C_RESET}')
    output_table.add_column('S2',[f'{s_2_value:,.2f}'])

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
    print(f'\n{gettext("ค่าพิสัย คือ")} {C_BOLD}{C_GREEN}{range_value:,.2f}{C_RESET}')
    output_table.add_column('Range',[f'{range_value:,.2f}'])

def find_mode(numlist):
    """ค่าฐานนิยม ( Mode ) คือ ค่าของข้อมูลตัวที่เกิดขึ้นบ่อยที่สุด หรือตัวที่มีความถี่มากที่สุด 
    โดยปกติข้อมูล 1 ชุดจะมีฐานนิยมค่าเดียว แต่เป็นไปได้ที่ข้อมูลบางชุดอาจมีฐานนิยมมากกว่า 1 ค่า"""
    num_counter = {}
    num_members = []
    mode = ''
    for num_i in numlist:
        if num_i in num_counter: #ถ้าเลขที่อยู่ในlistซ้ำกับเลขในDictที่มีอยู่แล้วให้+1เพิ่มเป็นValue
            num_counter[num_i] += 1
        else: #ถ้าเลขยังไม่อยู่ในdictให้เซตเป็น1ไว้
            num_counter[num_i] = 1

    for (member,maxx) in num_counter.items() : #member,maxคือการเปรียบเทียบกับ.item()ที่มีค่าออกมาเป็นเซตๆ หรือ(member,max)=(x,y) เมื่อxและyเป็นค่าในnum_counter.items()
        if maxx == max(num_counter.values()): #หาค่าที่ซ้ำมากที่สุดของvalueทั้งหมดของdict และเทียบกับmaxxทุกๆตัว เพื่อหา member
            num_members.append(member) #เพื่อเพิ่มไว้ดูว่ามีฐานนิยมที่เป็นสมาชิกกี่ตัว และตัวไหนบ้างที่เป็น
    len_num_members = len(num_members)
    ishave_mode = True
    num_members.sort()
    for i in range(len_num_members):
        if len(num_members) == 1:
            mode = str(num_members[i])
        elif len(num_members) > 1 and len(num_members) < 3: #ถ้าสมาชิกของnumมากกว่า0และน้อยกว่า3ให้ปริ้นฐานนิยมออกมาได้(ฐานนิยมมีได้มากสุด2ตัว)
            mode = mode + ', '+ str(num_members[i])
        else : #แต่ถ้าสมาชิกของnumไม่อยู่ในเงื่อนไข
            ishave_mode = False

    if ishave_mode is True :
        mode = mode.replace(',','',1)
        print(f'\n{gettext("ค่าฐานนิยมมี")} {C_BOLD}{C_BLUE}{len_num_members} {gettext("ค่า")}{C_RESET} {gettext("คือ")} {C_BOLD}{C_GREEN}{mode}{C_RESET}')
        output_table.add_column('Mode',[mode])
    else :
        print(f'\n{C_BOLD}{C_GREEN}{gettext("ไม่มีค่าฐานนิยม")}{C_RESET}')
        output_table.add_column('Mode',[gettext("ไม่มีค่าฐานนิยม")])

def frequency_distribution(numlist,numclass = 0) :
    """ฟังก์ชันหา การแจกแจงความถี่ (Frequency Distribution)
    การแจกแจงความถี่เป็นการนำข้อมูลที่เป็นค่าของตัวแปรที่เราสนใจมาจัดเรียงตามลำดับความมากน้อย 
    และแบ่งเป็นช่วงเท่าๆกัน จำนวนข้อมูลในแต่ละช่วงคะแนน เรียกว่า ความถี่"""
    num_min = numlist[0]
    num_max = 0
    cumulative_frequency = 0
    class_frequency = {}
    lower_upper_class = {} #ขีดจำกัดล่างและขีดจำกัดบนในรูปแบบของ dict
    frequency_distribution_num_table = PrettyTable()
    frequency_distribution_num_table.align = "r"
    frequency_distribution_num_table.set_style(SINGLE_BORDER)
    frequency_distribution_num_table.field_names = [gettext("อันตรภาคชั้น"), gettext("ขีดจำกัดล่าง"), gettext("ขีดจำกัดบน"), gettext("จุดกลางชั้น"), gettext("ความถี่"), gettext("ความถี่สะสม"), gettext("fx"), gettext("สัดส่วน"), gettext("ร้อยละ")]

    for i in numlist:
        if i > num_max:
            num_max = i
    len_numlist_x = len(numlist)
    for i in range(len_numlist_x):
        if numlist[i] < num_min:
            num_min = numlist[i]

    print(f'\n{gettext("พิสัย")} : {C_BOLD}{C_GREEN}{(num_max - (num_min))}{C_RESET}')
    if (num_max - (num_min)) < 5 :
        print(f'{gettext("ค่าพิสัยน้อยกว่า 5 ใช้รูปแบบการแจกแจงไม่ได้")}')
        return 0
    max_class = ((num_max - (num_min)) + 1) / 2
    max_class = min(max_class, 15)
    while True :
        print(f'{gettext("สามารถใช้ข้อมูลจำนวนชั้นได้มากสุด :")} {C_BOLD}{C_RED}{math.floor(max_class)}{C_RESET}')
        while True :
            if numclass == 0 :
                num_class_interval = input(f'\t{gettext("กรอกจำนวนชั้นที่ต้องการ >>>")}{C_GREEN} ')
                if num_class_interval == '' or num_class_interval.isnumeric() is False  :
                    print(f'{C_RED}\n✖ {gettext("อันตรภาคชั้นต้องอยู่ระหว่าง 3-15 ชั้น กรุณากรอกชั้นใหม่อีกครั้ง")}\n{C_RESET}')
                else:
                    num_class_interval = int(num_class_interval)
                    break
            else:
                if 3 <= numclass <= 15:
                    num_class_interval = numclass
                    print(f'\t{gettext("กรอกจำนวนชั้นที่ต้องการ >>>")}{C_GREEN} {numclass} {C_YELLOW}(Default Mode)')
                    numclass = 0 #! ใช้ค่าตั้งต้นแค่รอบเดียว
                    break
        num_class_interval = int(num_class_interval)
        resetcolor()
        if num_class_interval > (num_max - (num_min) + 1) / 2 :
            print(f'{C_RED}\n✖ {gettext("ชั้นมีจำนวนมากกว่าความกว้างของอันตรภาคชั้น กรุณากรอกชั้นใหม่อีกครั้ง")}\n{C_RESET}')
        elif (num_class_interval < 3) or (num_class_interval > 15) :
            print(f'{C_RED}\n✖ {gettext("อันตรภาคชั้นต้องอยู่ระหว่าง 3-15 ชั้น กรุณากรอกชั้นใหม่อีกครั้ง")}\n{C_RESET}')
        else:
            break
    range_x = math.ceil(((num_max - (num_min)) + 1) / num_class_interval) # ความกว้างของอัตราภาคแบบจำนวนเต็มที่ต้อง+1เพื่อบวกจำนวนตัวมันเอง
    lower_class_limit = num_min #ขีดจำกัดล่างเริ่มต้นแถว1
    upper_class_limit = (num_min + range_x) - 1 #ขีดจำกัดบนเริ่มต้นแถว1
    lower_upper_class[lower_class_limit] = upper_class_limit
    for i in range(1,num_class_interval):
        lower_class_limit = upper_class_limit + 1 #ขีดจำกัดล่างตั้งแต่แถว2ขึ้นไป
        upper_class_limit = (lower_class_limit + range_x) - 1 #ขีดจำกัดบนตั้งแต่แถว2ขึ้นไป
        lower_upper_class[lower_class_limit] = upper_class_limit
    print(f'\n{gettext("ความกว้างของอันตรภาคชั้น :")} {C_BOLD}{C_GREEN}{range_x}{C_RESET}') #แสดงความกว้างของอันตรภาคชั้น

    table_martrix = []

    martrix_pointer_column = 0 #! Pointer เมทริกซ์ คอลัมน์
    martrix_pointer_row = 0 #! Pointer เมทริกซ์ แถว
    #แสดงค่าในตาราง (คอลัมน์ 0)
    for (k_lower_class,v_upper_class) in lower_upper_class.items() : #!k คือ key , v คือ value
        table_martrix.append(["",0,0,0,0,0,0,0,0])
        table_martrix[martrix_pointer_row][martrix_pointer_column] = f'{k_lower_class} - {v_upper_class}'
        martrix_pointer_row = martrix_pointer_row + 1

    #หาขีดจำกัดล่างและบน (คอลัมน์ 1 2)
    martrix_pointer_column = 1
    martrix_pointer_row = 0
    for (k_lower_class,v_upper_class) in lower_upper_class.items() :
        table_martrix[martrix_pointer_row][martrix_pointer_column] = f'{k_lower_class - 0.5}'
        table_martrix[martrix_pointer_row][martrix_pointer_column + 1] = f'{v_upper_class + 0.5}'
        martrix_pointer_row = martrix_pointer_row + 1

    #หาจุดกึ่งกลาง (คอลัมน์ 3)
    martrix_pointer_column = 3
    martrix_pointer_row = 0
    for (k_lower_class,v_upper_class) in lower_upper_class.items() :
        table_martrix[martrix_pointer_row][martrix_pointer_column] = f'{((k_lower_class - 0.5) + (v_upper_class + 0.5)) / 2}'
        martrix_pointer_row = martrix_pointer_row + 1

    #หาความถี่ (คอลัมน์ 4 5 6 7 8)
    martrix_pointer_column = 4
    martrix_pointer_row = 0
    for (k_lower_class,v_upper_class) in lower_upper_class.items() :
        class_frequency[k_lower_class] = 0
        len_numlist = len(numlist)
        for k in range(len_numlist):
            if (numlist[k] >= k_lower_class) and (numlist[k] <= v_upper_class) :
                class_frequency[k_lower_class] += 1
    for v_class_frequency in class_frequency.values() : #!v_class_frequency คือความถี่
        #? ค่าความถี่
        table_martrix[martrix_pointer_row][martrix_pointer_column] = f'{v_class_frequency}'
        #? ค่าความถี่สะสม
        cumulative_frequency = cumulative_frequency + v_class_frequency
        table_martrix[martrix_pointer_row][martrix_pointer_column + 1] = f'{cumulative_frequency}'
        #? หาสัดส่วน ร้อยละ
        table_martrix[martrix_pointer_row][martrix_pointer_column + 2] = f'{float(table_martrix[martrix_pointer_row][3]) * float(table_martrix[martrix_pointer_row][4])}'
        table_martrix[martrix_pointer_row][martrix_pointer_column + 3] = f'{v_class_frequency / sum(class_frequency.values()):.3f}'
        table_martrix[martrix_pointer_row][martrix_pointer_column + 4] = f'{(v_class_frequency / sum(class_frequency.values())) * 100:.3f}'
        martrix_pointer_row = martrix_pointer_row + 1

    if ISDEBUG is True :
        print(f'{C_YELLOW}')
        print(f'\tlower_upper_class {gettext("คือ")} \n\n{lower_upper_class}')
        print(f'\n\tclass_frequency {gettext("คือ")} \n\n{class_frequency}')
        print(f'\n\ttable_martrix {gettext("คือ")} \n')
        print(f'{C_GREEN} │ ',end='')
        for i, data in enumerate(table_martrix):
            for j, data in enumerate(data):
                if j % 2 == 0 :
                    print(f'{C_GREEN}{data}',end=' │ ')
                else :
                    print(f'{C_YELLOW}{data}',end=' │ ')
            if i < len(table_martrix) - 1 :
                print('\n │ ',end='')
            else:
                print('')
        print(f'{C_RESET}')

    #!ส่วนการแสดงตาราง
    len_num_martrix = len(table_martrix)
    for i in range(len_num_martrix):
        frequency_distribution_num_table.add_row([table_martrix[i][0], table_martrix[i][1], table_martrix[i][2],
                            table_martrix[i][3], table_martrix[i][4], table_martrix[i][5],
                            table_martrix[i][6], table_martrix[i][7], table_martrix[i][8]])
    print(f'\n{"═"*100}\n')
    print(f'\n\t{C_UNDERLINE}{C_CYAN}{gettext("ตารางแจกแจงความถี่")}{C_RESET}')
    print(f'\n{frequency_distribution_num_table}')
    sum_percent = 0
    for i in range(len_num_martrix) :
        sum_percent = sum_percent + float(table_martrix[i][8])
    sum_ratio = 0
    for i in range(len_num_martrix) :
        sum_ratio = sum_ratio + float(table_martrix[i][7])

    print(f'\n\tN : {C_BOLD}{C_GREEN}{len_numlist_x}{C_RESET} \n\t{gettext("อัตราส่วนรวม   :")} {C_BOLD}{C_GREEN}{round(sum_ratio):.2f}{C_RESET} \n\t{gettext("เปอร์เซ็นต์รวม   :")} {C_BOLD}{C_GREEN}{round(sum_percent):.3f}{C_RESET}')

    #?หาค่าสถิติ
    #!หาค่าความเบี่ยงเบนควอไทล์
    def find_r_quartile(r_input) :
        f_l = 0
        qr_r4n = (r_input / 4) * len_numlist_x
        quartile_pointer_row = 0
        for i in range(len_num_martrix) :
            if qr_r4n < float(table_martrix[i][5]) :
                quartile_pointer_row = i
                break

        f_x = float(table_martrix[quartile_pointer_row][4]) #Fx คือ ความถี่ในชั้นที่ควอร์ไทล์ตั้งอยู่
        if quartile_pointer_row - 1 >= 0 :
            f_l = float(table_martrix[quartile_pointer_row - 1][5]) #FL คือ ความถี่สะสมในชั้นก่อนหน้า
        else:
            f_l = 0.0 #FL คือ ความถี่สะสมในชั้นก่อนหน้า
        rn_4 = (r_input * len_numlist_x) / 4 #rN/4 คือตำแหน่งของควอร์ไทล์
        qr_i = range_x #I คือ ความกว้างของอันตรภาคชั้น
        qr_l = float(table_martrix[quartile_pointer_row][1]) #L คือ ขอบล่างที่ควอร์ไทล์นั้นๆตั้งอยู่

        q_r = qr_l + (((rn_4 - f_l) / f_x) * qr_i)

        if ISDEBUG is True :
            print(f'{C_YELLOW}')
            print(f'\tPointer row {gettext("คือ")} {quartile_pointer_row}')
            print(f'\tLo (qr_l) {gettext("คือ")} {qr_l}')
            print(f'\ti (qr_i) {gettext("คือ")} {qr_i}')
            print(f'\tN (len_numlist_x) {gettext("คือ")} {len_numlist_x}')
            print(f'\tX (r_input) {gettext("คือ")} {r_input}')
            print(f'\tF (f_l) {gettext("คือ")} {f_l}')
            print(f'\tf (f_x) {gettext("คือ")} {f_x}')
            print(f'\tQ{r_input} {gettext("คือ")} {q_r}')
            print(f'{C_RESET}')
        return q_r

    q_d = (find_r_quartile(3) - find_r_quartile(1)) / 2
    print(f'\n\t{gettext("ค่าความเบี่ยงเบนควอไทล์ คือ")} {C_BOLD}{C_BLUE}{q_d:,.3f}{C_RESET}')

    #!หาค่าเฉลี่ย
    n = len_numlist_x
    fx_1 = 0
    fx_2 = 0
    for row_i in range(len_num_martrix)  :
        fx_1 = fx_1 + math.pow(float(table_martrix[row_i][3]), 2) * float(table_martrix[row_i][4])
        fx_2 = fx_2 + float(table_martrix[row_i][3]) * float(table_martrix[row_i][4])
    sd_x = math.sqrt(((n * fx_1) - math.pow(fx_2, 2)) / (n * (n - 1)))
    s2_x = ((n * fx_1) - math.pow(fx_2, 2)) / (n * (n - 1))
    if ISDEBUG is True :
        print(f'{C_YELLOW}')
        print(f'\tN {gettext("คือ")} {n}')
        print(f'\tFX1 {gettext("คือ")} {fx_1}')
        print(f'\tFX2 {gettext("คือ")} {fx_2}')
        print(f'{C_RESET}')

    print(f'\n\t{gettext("ความเบี่ยงเบนมาตรฐาน SD. คือ")} {C_BOLD}{C_BLUE}{sd_x:,.3f}{C_RESET}')
    print(f'\n\t{gettext("ความแปรปรวน S2 คือ")} {C_BOLD}{C_BLUE}{s2_x:,.3f}{C_RESET}')
    x_bar = fx_2 / n
    print(f'\n\t{gettext("ค่าเฉลี่ย คือ")} {C_BOLD}{C_BLUE}{x_bar:,.3f}{C_RESET}')

    #!หาค่ามัธยฐาน
    def find_md_x() :
        n_2 = len_numlist_x / 2
        md_pointer_row = 0
        for i in range(len_num_martrix) :
            if n_2 < float(table_martrix[i][5]) :
                md_pointer_row = i
                break

        f_x = float(table_martrix[md_pointer_row][4])
        f_l = float(table_martrix[md_pointer_row - 1][5])
        md_i = range_x
        md_l = float(table_martrix[md_pointer_row - 1][2])
        if ISDEBUG is True :
            print(f'{C_YELLOW}')
            print(f'\tN {gettext("คือ")} {len_numlist_x}')
            print(f'\tN/2 {gettext("คือ")} {n_2}')
            print(f'\tPointer row {gettext("คือ")} {md_pointer_row}')
            print(f'\tL {gettext("คือ")} {md_l}')
            print(f'\tF (f_x) {gettext("คือ")} {f_x}')
            print(f'\tf (f_l) {gettext("คือ")} {f_l}')
            print(f'\ti {gettext("คือ")} {md_i}')
            print(f'{C_RESET}')

        md_x = md_l + (md_i * (n_2 - f_l)) / f_x
        return md_x

    print(f'\n\t{gettext("ค่ามัธยฐาน คือ")} {C_BOLD}{C_BLUE}{find_md_x():,.3f}{C_RESET}')

    #!หาค่าฐานนิยม
    def find_mode_x() :
        mo_pointer_row = 0
        f_max = 0
        i = range_x
        for i_row in range(len_num_martrix) :
            if int(table_martrix[i_row][4]) > f_max:
                f_max = int(table_martrix[i_row][4] )
                mo_pointer_row = i_row

        mo_l = float(table_martrix[mo_pointer_row][1])
        mo_d1 = 0
        mo_d2 = 0
        mo_d1 = float(table_martrix[mo_pointer_row][4]) - float(table_martrix[mo_pointer_row - 1][4])
        if mo_pointer_row + 1 < len_num_martrix :
            mo_d2 = float(table_martrix[mo_pointer_row][4]) - float(table_martrix[mo_pointer_row + 1][4])
        if ISDEBUG is True :
            print(f'{C_YELLOW}')
            print(f'\tD1 {gettext("คือ")} {mo_d1}')
            print(f'\tD2 {gettext("คือ")} {mo_d2}')
            print(f'\ti {gettext("คือ")} {i}')
            print(f'\tL {gettext("คือ")} {mo_l}')
            print(f'{C_RESET}')

        if (mo_d1 + mo_d2) == 0:
            return f'\n\t{C_BOLD}{C_GREEN}{gettext("ไม่มีค่าฐานนิยม")}{C_RESET}'

        mode_x = mo_l + ((mo_d1 / (mo_d1 + mo_d2)) * i)
        return f'\n\t{gettext("ค่าฐานนิยม คือ")} {C_BOLD}{C_BLUE}{mode_x:,.3f}{C_RESET}'

    print(f'{find_mode_x()}')

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
                    print(f'{C_RESET}{"═"*100}\n')
                    num = input(f'{C_RESET}{gettext("กรอกตัวเลข (เป็นชุด หรือ ทีละตัว) >>>")} {C_GREEN}')
                    print(f'{C_RESET}\n{"═"*100}\n')
                    numlist_input(num, defmode = DEFMODE, defcalmode = DEFCALMODE)
                case 'error':
                    print(f'{gettext("การโหลดข้อมูลจากไฟล์ txt ผิดพลาด ใช้งานการกรอกข้อมูลด้วยตนเอง")}\n')
                    print(f'{C_RESET}{"═"*100}\n')
                    num = input(f'{C_RESET}{gettext("กรอกตัวเลข (เป็นชุด หรือ ทีละตัว) >>>")} {C_GREEN}')
                    print(f'{C_RESET}\n{"═"*100}\n')
                    numlist_input(num, defmode = DEFMODE, defcalmode = DEFCALMODE)
                case _ :
                    if QUESTION == '' :
                        numlist_input(loadtemp, 1, DEFMODE, DEFCALMODE) #! loadtemp คือชุดข้อมูล ,1 คือ bypass input ,DEFMODE คือค่าโหมดตั้งต้น ,DEFCALMODE คือค่าโหมดตั้งต้นไม่แจกแจง
                    else:
                        while True:
                            print(f'\n{C_RESET}{gettext("ต้องการรับข้อมูลผ่านไฟล์ txt หรือไม่")} [ Y / N ] ?')
                            QUESTION = input(f'\t>>>{C_GREEN} ')
                            resetcolor()
                            if QUESTION not in [''] :
                                break
                        if QUESTION.upper() not in ['Y']:
                            print(f'\n{C_RESET}{"═"*100}\n')
                            num = input(f'{C_RESET}{gettext("กรอกตัวเลข (เป็นชุด หรือ ทีละตัว) >>>")} {C_GREEN}')
                            print(f'{C_RESET}\n{"═"*100}\n')
                            numlist_input(num)
                        else:
                            numlist_input(loadtemp, 1)
        else:
            numlist_input(last_numlist, 1)

    finally:
        print(f'\n{"═"*100}')
        if len(last_numlist) > 0 :
            print(f'\n{gettext("พิมพ์")} {C_GREEN}R{C_RESET} {gettext("เพื่อใช้งานโปรแกรมอีกครั้งโดยใช้ชุดข้อมูลล่าสุด")}')
            print(f'{C_RESET}{gettext("ชุดข้อมูลล่าสุดคือ (ขนาดชุดข้อมูล")} {C_BOLD}{C_GREEN}{len(last_numlist)}{C_RESET}) : {C_BLUE}{last_numlist}{C_RESET}')
            print(f'\n{C_RESET}{gettext("ต้องการคำนวณอีกครั้งหรือไม่")} [ Y / N / R ] ?')
        else:
            print(f'\n{C_RESET}{gettext("ต้องการคำนวณอีกครั้งหรือไม่")} [ Y / N ] ?')
        while True:
            QUESTION = input(f'\t>>>{C_GREEN} ')
            resetcolor()
            if QUESTION not in [''] :
                if QUESTION.upper() in ['SERECT', 'DEV']:
                    print(f'\nHi Dev!\nTry using python command. Here are some variables.\n[ {C_BLUE}CONFIGLANG ISDEBUG DELAY DEFMODE DEFCALMODE DEFNUMCLASS{C_RESET} ] Have fun!')
                    while True:
                        print(C_MAGENTA)
                        print('\t$ ',end='')
                        dev_cm = input()
                        try:
                            # pylint: disable-next=exec-used
                            exec(dev_cm)
                        except: # pylint: disable=W0702
                            print('Code Error ! ')
                            resetcolor()
                        if input('\nExit ? [Y / N] >> ').upper() in ['Y']:
                            resetcolor()
                            break
                    QUESTION = 'Y'
                break
        if QUESTION.upper() in ['R'] and len(last_numlist) > 0 :
            LOAD_LAST = True
            output_table.clear()
            DEFNUMCLASS = 0 #!เพื่อล้างค่าตั้งต้นที่รับมา
        elif QUESTION.upper() not in ['Y']:
            print(f'\n{C_RESET}{"═"*100}\n')
            print(f'{gettext("จบการทำงาน")}')
            print(f'\n{gettext("จัดทำโดย")}')
            print(f'\t{C_MAGENTA}65003120049 {C_GREEN}กิตติภพ มาสระ {C_MAGENTA}\n\t65003263018 {C_GREEN}ศุภวิชญ์ เวทยสาร {C_MAGENTA}\n\t65003263019 {C_GREEN}นิติธร นันทสินธ์{C_RESET}\n\n\t{C_BOLD}{C_YELLOW}CS65{C_RESET}')
            print(f'\n{"═"*100}\n')
            IS_RUN = False
        else:
            last_numlist.clear()
            LOAD_LAST = False
            output_table.clear()
            DEFNUMCLASS = 0 #!เพื่อล้างค่าตั้งต้นที่รับมา
            print('\n')
input()
