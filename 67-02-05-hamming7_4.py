"""65003263019
    * มีการนำโค้ดจากโปรแกรมเก่าที่เคยเขียนไว้มาใช้งาน (secure_input)
    * โปรแกรมอาจมีความซับซ้อนโดยไม่จำเป็น
    * การแสดงผลอาจผิดพลาดหาก Termimal ไม่รองรับ ANSI escape code

"""
import random

def secure_input(text,mode='chk_float',strlen=0,chk_firstisalphabet=False):
    """ฟังก์ชันตรวจสอบการรับข้อมูล *Version 0.7* (*แก้ให้จำนวนตัว==strlenเท่านั้น + แก้ไขให้เข้ากันกับโปรแกรม)"""
    prefix = ''
    match mode:
        case 'chk_float':
            prefix = '(FLT) '
        case 'chk_int':
            prefix = '(Int) '
        case 'chk_lenstr':
            prefix = f'(Str. {strlen}) '
    def check_input_isnumber(value):
        if mode == 'chk_float':
            try:
                float(value)
                return True
            except (ValueError):
                return False
        elif mode in ['chk_q']:
            if len(value) == strlen:
                return True
        elif mode in ['chk_lenstr','chk_lenstr_plus']:
            if (strlen != 0) and (len(value) == strlen) and value.isnumeric():
                disallow = False
                for i in value:
                    if i not in ['0','1']:
                        disallow = True
                if disallow:
                    return False
                return True
            if chk_firstisalphabet and not to_return[0].isalpha():
                return False
            return False
        elif mode == 'chk_int' and value.isnumeric():
            return True
    to_return = input(f'{prefix}{text}')
    while True:
        if len(to_return) > 0 and check_input_isnumber(to_return):
            if mode == 'chk_float':
                return float(to_return)
            elif mode in ['chk_lenstr','chk_q']:
                return to_return
            elif mode == 'chk_lenstr_plus':
                to_return = to_return.replace("'", "").replace(";", "").replace("--", "").replace("=", "").replace("*", "").replace("?", "").replace("OR", "")
                return to_return
            elif mode == 'chk_int':
                print('\n')
                return int(to_return)
        else:
            to_return = input(f'\nError encountered. Please check the entered Data.\n\n{prefix}{text}')

class HammingReaderCS019:
    """hammimg reader and checker"""

    def __init__(self,b: list) -> list :
        self.list_binary = b
        self.list_p1 = []
        self.list_p2 = []
        self.list_p4 = []

    def get_list_p1(self):
        """ค่า p1"""
        # print('P1 Parity')
        self.list_p1 = []
        for i,j in enumerate(self.list_binary[-1::-1], start=1):
            if i % 2 not in [0]:
                self.list_p1.append(j)
        return self.list_p1

    def get_list_p2(self):
        """ค่า p2"""
        # print('P2 Parity')
        for i,j in enumerate(self.list_binary[-2::-1], start=2):
            if i not in [4,5]:
                self.list_p2.append(j)
        return self.list_p2

    def get_list_p4(self):
        """ค่า p4"""
        self.list_p4 = []
        for i,j in enumerate(self.list_binary[-4::-1], start=4):
            if i <= 7:
                self.list_p4.append(j)
        return self.list_p4

def xor_me(list_data_b) -> int:
    """just xor"""
    res = int(list_data_b[1])
    for i in list_data_b[2::]:
        res ^= int(i)
    return res

def hamming_generator_cs019(b:str,mode='print'):
    """hammimg generator"""
    b_int = str(b) #!4
    list_binary = [str(x) for x in str(b_int)]
    if len(list_binary) != 4:
        print('In This Program, Data Bit Must be 4 bit.')
        return 0

    final_list = [None,None,None,None,None,None,None]
    for i, j in enumerate(list_binary[::-1],start=3):
        if i in [3]:
            final_list[-i] = j
        elif i in [4,5,6]:
            final_list[-(i+1)] = j

    cs019 = HammingReaderCS019(final_list)
    final_list[-1] = str(xor_me(cs019.get_list_p1()))
    final_list[-2] = str(xor_me(cs019.get_list_p2()))
    final_list[-4] = str(xor_me(cs019.get_list_p4()))
    if mode == 'print':
        print(f"""
                Calculate

                    Input Data Bit : {' '.join(list_binary)}
                    Hammimg Code   : {' '.join(final_list)}
                """)
    elif mode == 'return':
        return final_list

underline_ansi = '\033[4m'
end_ansi = '\033[0m'

def hamming_checker_cs019(b:str,mode='print'):
    """check hamming"""
    def get_hamming_code(list_b:list):
        """get hamming code in list"""
        ham_list = []
        for i, j in enumerate(list_b[::-1],start=1):
            if i in [1,2,4]:
                # print(i,j)
                ham_list.append(j)
        ham_list.reverse()
        return ham_list

    b_int = str(b) #!7
    list_binary = [str(x) for x in str(b_int)]
    if len(list_binary) == 0:
        return []

    ham_cal = []
    cs019 = HammingReaderCS019(list_binary)
    ham_cal.append(str(xor_me(cs019.get_list_p4())))
    ham_cal.append(str(xor_me(cs019.get_list_p2())))
    ham_cal.append(str(xor_me(cs019.get_list_p1())))

    ham_get = get_hamming_code(list_binary)
    list_binary_clone = []
    if ham_cal == ham_get:
        text_result = 'Error bit Not Found !'
        if mode == 'print':
            print(f"""
                    Code Input           : {' '.join(list_binary)}

                    Parity bit Calculate : {' '.join(ham_cal)}
                                                ==
                    Parity bit Get       : {' '.join(ham_get)}

                    {text_result}
                    """)
        elif mode == 'return':
            return ["Error bit Not Found !",list_binary]
    else:
        if mode == 'print':
            print('\nCorrecting Binary...\n')
        b_to_dec = 0
        error_index_cal = [None, None, None]
        error_index_cal[0] = int(ham_cal[0]) ^ int(ham_get[0])
        error_index_cal[1] = int(ham_cal[1]) ^ int(ham_get[1])
        error_index_cal[2] = int(ham_cal[2]) ^ int(ham_get[2])
        for i, j in enumerate(error_index_cal[::-1],start=0):
            b_to_dec += (2**i) * j
        if mode == 'print':
            print('Error At Position DEC ',error_index_cal[0],error_index_cal[1],error_index_cal[2], ' >>> ',b_to_dec)
        list_binary_clone.extend(list_binary)
        list_binary_clone[-b_to_dec] = underline_ansi + str(int(not(int(list_binary_clone[-b_to_dec])))) + end_ansi #! Hard

        if mode == 'print':
            print(f"""
                    Code Input           : {' '.join(list_binary)}

                    Parity bit Calculate : {' '.join(ham_cal)}
                                                != {b_to_dec}
                    Parity bit Get       : {' '.join(ham_get)}

                    Data Error Detected !
                    Code Corrected       : {' '.join(list_binary_clone)}
                    """)
        elif mode == 'return':
            return [f"Data Error Detected at bit {b_to_dec} (R) !",list_binary_clone]

try:
    MENU4 = '\n\nTip : The "Automate" menu will test data from 0000 - 1111 and will randomly modify 1 bit of the code. and let the algorithm find and correct it.'
    while True:
        match (secure_input(f'\nHamming(7,4) Calculator\n\nMode \t1. Basic \n\t2. Normal \n\t3. Automate {MENU4}\n\n\t>>> ',mode='chk_q',strlen=1)):
            case '1':
                underline_ansi = ''
                end_ansi = ''
                print(hamming_generator_cs019(secure_input('Data 4 bit >>> ',mode='chk_lenstr',strlen=4),mode='return'))
                print(hamming_checker_cs019(secure_input('Code 7 bit >>> ',mode='chk_lenstr',strlen=7),mode='return'))
                underline_ansi = '\033[4m'
                end_ansi = '\033[0m'
            case '2':
                hamming_generator_cs019(secure_input('Data 4 bit >>> ',mode='chk_lenstr',strlen=4))
                hamming_checker_cs019(secure_input('Code 7 bit >>> ',mode='chk_lenstr',strlen=7))
            case '3':
                print('\nBrute Force Data 0000-1111 & Check')
                for ii in range(2):
                    for jj in range(2):
                        for kk in range(2):
                            for mm in range(2):
                                data_gen = (str(ii) + str(jj) + str(kk) + str(mm))
                                temp = hamming_generator_cs019(data_gen,mode='return')
                                print(f'\nData :  {"".join(data_gen[0:3:])}__{"".join(data_gen[3])}_ \nCode :  {"".join(temp)}')
                                temp_b = hamming_checker_cs019("".join(temp),mode='return')
                                print(f'\tCheck Status : {temp_b[0]} Result : {"".join(temp_b[1])}')
                                rand_list = [0,1,2,3,4,5,6]
                                while rand_list:
                                    r_idx = random.choice(rand_list)
                                    temp[r_idx] = str(int(not(int(temp[r_idx])))) #! r_idx ต้องมีค่าเท่ากัน บัคเพราะ random สองรอบ :(
                                    temp_b = hamming_checker_cs019("".join(temp),mode='return')
                                    print(f'\tRandom 1 bit Error : {"".join(temp)} Check Status : {temp_b[0]} Result : {"".join(temp_b[1])}')
                                    temp[r_idx] = str(int(not(int(temp[r_idx])))) #! reset
                                    rand_list.remove(r_idx)
            case '4':
                underline_ansi = ''
                end_ansi = ''
                print('\nCongratulations, problem solved. :)',underline_ansi,end_ansi)
            case _ :
                print('The selected menu is not available.')
        if (secure_input('\n\tCalculate Again [Y / n] >>> ',mode='chk_q', strlen=1)) in ['n','N']:
            break
        else:
            MENU4 = '\n\t4. Disable Underline (if display abnormally)'
except:
    print('something went wrong. try again.')
    raise
finally:
    print('\n\nNititorn Nantasin 65003263019\n\n')
