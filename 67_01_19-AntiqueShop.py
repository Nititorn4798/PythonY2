"""ระบบจัดการร้านขายของเก่า V 0.1 (อยู่ระหว่างการพัฒนา)"""
import sqlite3
print('ระบบจัดการร้านขายของเก่า V 0.1 (อยู่ระหว่างการพัฒนา) Powered By SQLite3')

@staticmethod
def secure_input(text,mode='chk_float',strlen=0,chk_firstisalphabet=False):
    """ฟังก์ชันตรวจสอบการรับข้อมูล *Version 0.5*"""
    prefix = ''
    match mode:
        case 'chk_float':
            prefix = '(FLT) '
        case 'chk_int':
            prefix = '(Int) '
    def check_input_isnumber(value):
        if mode == 'chk_float':
            try:
                float(value)
                return True
            except (ValueError):
                return False
        elif mode in ['chk_lenstr','chk_lenstr_plus']:
            if strlen != 0 and len(to_return) < strlen:
                return False
            if chk_firstisalphabet and not to_return[0].isalpha():
                return False
            return True
        elif mode == 'chk_int' and value.isnumeric():
            return True
    to_return = input(f'{prefix}{text}')
    while True:
        if len(to_return) > 0 and check_input_isnumber(to_return):
            if mode == 'chk_float':
                return float(to_return)
            elif mode == 'chk_lenstr':
                return to_return
            elif mode == 'chk_lenstr_plus':
                to_return = to_return.replace("'", "").replace(";", "").replace("--", "").replace("=", "").replace("*", "").replace("?", "").replace("OR", "")
                return to_return
            elif mode == 'chk_int':
                return int(to_return)
        else:
            to_return = input(f'รับข้อมูลไม่สำเร็จลองใหม่อีกครั้ง!\n{prefix}{text}')

def cls():
    """ล้างหน้าจอ"""
    print('\033c', end='')

class Database:
    """ระบบเชื่อมต่อฐานข้อมูล"""
    try:
        conn = sqlite3.connect('antiqueshop_cs019.db')
    except:
        print('DB Connection Error.')
        raise

    def __init__(self):
        sql_create = """--sql
            CREATE TABLE IF NOT EXISTS UserDataCS019 (
                user_id INTEGER NOT NULL PRIMARY KEY,
                user_name text UNIQUE COLLATE NOCASE NOT NULL,
                user_password text,
                user_balance real,
                user_phone text,
                user_type text
            )
        """
        self.db_query(sql_create)
        sql_create = """--sql
            CREATE TABLE IF NOT EXISTS ItemsDataCS019 (
                item_id INTEGER NOT NULL PRIMARY KEY,
                item_name text,
                item_buyprice DECIMAL,
                item_status TEXT
            )
        """
        self.db_query(sql_create)
        sql_create = """--sql
            CREATE TABLE IF NOT EXISTS BuyDataCS019 (
                sell_id INTEGER NOT NULL PRIMARY KEY,
                sell_user_id INTEGER NOT NULL,
                sell_item_id INTEGER NOT NULL,
                sell_item_amount INTEGER NOT NULL,
                sell_total REAL NOT NULL,
                sell_datetime DATETIME,
                FOREIGN KEY (sell_user_id) REFERENCES UserDataCS019(user_id),
                FOREIGN KEY (sell_item_id) REFERENCES ItemsDataCS019(item_id)
            )
        """
        self.db_query(sql_create)

        cc = self.conn.execute("""select count(*) as A from UserDataCS019""").fetchone()
        if not cc[0]:
            print('Found New Database Insert DEMO Data!')
            cmd_insert_userdata = """insert into UserDataCS019 (user_id,user_name,user_password,user_balance,user_phone,user_type)"""
            cmd_insert_itemdata = """insert into ItemsDataCS019 (item_id,item_name,item_buyprice,item_status)"""
            cmd_insert_buydata = """insert into BuyDataCS019 (sell_id,sell_user_id,sell_item_id,sell_item_amount,sell_total,sell_datetime)"""
            demo_user = {
                1 : {
                    1 : "Nititorn4798",2 : "1234admin",3 : 65003263019,4 : "0987654321",5 : "T_ADMIN"
                },
                2 : {
                    1 : "user",2 : "1234",3 : 99987,4 : "0987654321",5 : "T_USER"
                },
                3 : {
                    1 : "admin",2 : "1234",3 : 99999,4 : "0667654321",5 : "T_ADMIN"
                }
            }
            demo_itemdata = {
                1 : {
                    1 : "พลาสติก PEP",2 : 9.8,3 : "ปกติ"
                },
                2 : {
                    1 : "พลาสติก GPS",2 : 99.98,3 : "งดรับ"
                }
            }
            demo_buydata = {
                1 : {
                    1 : 1,2 : 1,3 : 99,4: 9997,5 : "ตอนเที่ยงๆ"
                },
                2 : {
                    1 : 2,2 : 2,3 : 66,4: 9999,5 : "พรุ่งนี้ ตอนเที่ยงๆ"
                }
            }
            for i,j in demo_user.items():
                sql_insert = f"""--sql row {i}
                    {cmd_insert_userdata}
                    values (NULL,'{j[1]}','{j[2]}',{j[3]},'{j[4]}','{j[5]}');
                """
                print(sql_insert)
                self.db_query(sql_insert)
            for i,j in demo_itemdata.items():
                sql_insert = f"""--sql row {i}
                    {cmd_insert_itemdata}
                    values (NULL,'{j[1]}',{j[2]},'{j[3]}');
                """
                print(sql_insert)
                self.db_query(sql_insert)
            for i,j in demo_buydata.items():
                sql_insert = f"""--sql row {i}
                    {cmd_insert_buydata}
                    values (NULL,{j[1]},{j[2]},{j[3]},{j[4]},'{j[5]}');
                """
                print(sql_insert)
                self.db_query(sql_insert)

    def db_query(self,cmd,mode='insert',workmode='return'):
        """รันคำสั่ง"""
        try:
            temp = sqlite3.Cursor(self.conn) #!ไม่จำเป็นแค่ใส่ไว้กัน unbound
            match mode:
                case 'insert':
                    temp = self.conn.execute(cmd)
                case 'select':
                    temp = self.conn.execute(cmd)
            match workmode:
                case 'return':
                    return temp.fetchall()
                case 'print':
                    print(temp.fetchall())
        except:
            print("An error occurred while executing the command. Don't panic. We're fixing it.")
            raise
        finally:
            self.conn.commit()

    def db_select(self):
        """เลือกข้อมูล"""
        sql_select = """--sql
            select * from UserDataCS019
        """
        for row in self.conn.execute(sql_select):
            print(row)

    def db_close(self):
        """ปิดฐานข้อมูล"""
        self.conn.close()

db = Database()
# db.db_select()
# db.db_query("""--sql
#     SELECT * FROM BuyDataCS019
# 	INNER JOIN UserDataCS019
# 	ON BuyDataCS019.sell_user_id = UserDataCS019.user_id
#     WHERE user_id = 1
#     """,'select','print')

class AntiqueShop:
    """ร้านขายของเก่า"""
    current_menu = 'main'
    def __authenticator(self):
        """ระบบยืนยันตัวตน"""
        def register():
            while True:
                print('\nระบบสมัครสมาชิก')
                print('\nชื่อผู้ใช้ 4 ต้องการอักษรขึ้นไปและขึ้นต้นด้วยอักษรภาษาอังกฤษ. \nรหัสผ่านต้องการ 4ตัวอักษรขึ้นไป.\n')
                user = secure_input('\tUsername <<< ','chk_lenstr_plus',strlen=4,chk_firstisalphabet=True)
                pwd = secure_input('\tPassword <<< ','chk_lenstr_plus',strlen=4)
                phone_number = secure_input('\tเบอร์โทรศัพท์ <<< ','chk_lenstr')
                sql_insert = f"""--sql
                    insert into UserDataCS019 (user_id,user_name,user_password,user_balance,user_phone,user_type)
                    values (NULL,'{user}','{pwd}',{0},'{phone_number}','T_USER');
                """
                print(sql_insert)
                try:
                    db.db_query(sql_insert)
                    break
                except sqlite3.IntegrityError:
                    print(f'ชื่อผู้ใช้ [{user}] ไม่สามารถใช้ได้ หรือข้อมูลไม่ถูกต้อง! กรุณาลองใหม่อีกครั้ง')

        def login():
            """ล็อกอิน"""
            while True:
                print('กรุณากรอกข้อมูลเพื่อยืนยันตัวตน [พิมพ์ r เพื่อสมัครสมาชิก]\n')
                user = secure_input('\tUsername >>> ','chk_lenstr_plus')
                if user in ['r','R']:
                    register()
                else:
                    pwd = secure_input('\tPassword >>> ','chk_lenstr_plus')
                    cmd = f"""--sql
                        SELECT count(*) FROM UserDataCS019 WHERE user_name = '{user}' AND user_password = '{pwd}'
                    """
                    db.db_query(cmd,'select','print')
                    temp = db.db_query(cmd,'select','return')
                    if (temp is not None) and (temp[0][0] == 1):
                        self.user_name = user
                        cmd = f"""--sql
                            SELECT user_type FROM UserDataCS019 WHERE user_name = '{user}'
                        """
                        db.db_query(cmd,'select','print')
                        temp = db.db_query(cmd,'select','return')
                        if temp is not None:
                            self.user_role = temp[0][0]
                            break
                    else:
                        print('ชื่อผู้ใช้ หรือ รหัสผ่าน ไม่ถูกต้อง')
                        q = secure_input('เป็นผู้ใช้ใหม่หรือไม่? ต้องการสมัครสมาชิกไหม [Y/N] : ','chk_lenstr')
                        q = str(q)
                        if q.upper() in ['Y']:
                            register()
        login()

    def __init__(self):
        self.user_role = 'not_auth'
        self.user_name = ''
        try:
            self.__authenticator()
            # self.user_role = 'T_ADMIN' #!bypass
            self.main()
        except:
            print('เกิดข้อผิดพลาด')
            raise

    def main(self):
        """ระบบเลือกการแสดงผลตามสิทธิ"""
        while self.current_menu == 'main':
            cls()
            match self.user_role:
                case 'T_ADMIN':
                    self.__home_admin()
                case 'T_USER':
                    self.__home_user()
                case 'not_auth':
                    print('เซสชั่นไม่ถูกต้อง กรุณายืนยันตัวตนอีกครั้ง')
                    self.__authenticator()
            if self.current_menu != 'main':
                if secure_input('ต้องการดำเนินการต่อหรือไม่ ? [Y/N] >>> ','chk_lenstr') in ['n','N']:
                    print('\tจบการทำงาน')
                    print('\tจัดทำโดย นายนิติธร นันทสินธ์ 65003263019')
                    break
                else:
                    self.current_menu = 'main'

    def __home_user(self):
        """หน้าหลักของผู้ใช้"""
        self.current_menu = 'home_user'
        cls()
        print(f'{"*"*19}')
        print(f'\nยินดีต้อนรับคุณ {self.user_name}\n')
        print('เลือกการทำงานที่ต้องการ')
        print('-1. ขายของเก่า')
        print('-2. ถอนเงิน')
        print('9. ออกจากระบบ')
        q = secure_input('\t>>> ','chk_int')
        match q:
            case 1:
                cls()
                print('\n\tเข้าสู่การขายของเก่า')
            case 2:
                cls()
                print('\n\tเข้าสู่การถอนเงิน')
            case 9:
                cls()
                print('\n\tกำลังออกจากระบบ ขอบคุณที่ใช้บริการ')
                self.user_role = 'not_auth'
            case _:
                cls()
                print('\n\tไม่พบสิ่งที่คุณต้องการ')

    def __home_admin(self):
        """หน้าหลักของผู้ดูแลลร้าน"""
        self.current_menu = 'home_admin'
        cls()
        print(f'{"*"*19}')
        print(f'\nยินดีต้อนรับคุณ {self.user_name} ในฐานะผู้ดูแลร้าน\n')
        print('เลือกการทำงานที่ต้องการ')
        print('-1. เพิ่ม รายการรับซื้อ')
        print('-2. ลบ รายการรับซื้อ')
        print('-3. แก้ไข รายการรับซื้อ')
        print('4. ตรวจสอบ บันทึกรับซื้อ')
        print('5. ตรวจสอบ รายชื่อลูกค้า')
        print('6. ตรวจสอบ รายชื่อลูกค้าที่ยอดขายมากที่สุด')
        print('9. ออกจากระบบ')
        q = secure_input('\t>>> ','chk_int')
        match q:
            case 1:
                cls()
                print('\n\tเพิ่ม รายการรับซื้อ')
                item_name = secure_input('\tกรอกชื่อสินค้า   >>> ','chk_lenstr_plus')
                item_buyprice = secure_input('\tกรอกราคาสินค้า >>> ')
                sql_q = f"""--sql
                    INSERT INTO ItemsDataCS019 (item_id,item_name,item_buyprice,item_status)
                        VALUES (NULL,'{item_name}',{item_buyprice},'ปกติ');
                """
                try:
                    db.db_query(sql_q,'insert','return')
                except:
                    print('เกิดข้อผิดพลาดกรุณาลองใหม่อีกครั้ง')
                    raise
                else:
                    print(f'เพิ่มข้อมูลสินค้า {item_name} ในราคา {item_buyprice} บาท สำเร็จ!')
            case 2:
                cls()
                print('\n\tลบ รายการรับซื้อ')
            case 3:
                cls()
                print('\n\tแก้ไข รายการรับซื้อ')
            case 4:
                cls()
                print('\n\tเข้าสู่การตรวจสอบ บันทึกรับซื้อ')
                sql_q = """--sql
                    SELECT sell_id, sell_user_id, user_name, item_id , item_name, item_buyprice, sell_item_amount, sell_total FROM BuyDataCS019
                        INNER JOIN UserDataCS019
                        INNER JOIN ItemsDataCS019
                        ON UserDataCS019.user_id = BuyDataCS019.sell_user_id
                        AND ItemsDataCS019.item_id = BuyDataCS019.sell_item_id
                """
                db.db_query(sql_q,'select','print') #!DEBUG
                result = db.db_query(sql_q,'select','return')
                if result is not None:
                    for tuplex in result:
                        print(f"""
                                รหัสการรับซื้อ    : {tuplex[0]}
                                รหัสผู้ใช้ที่ขาย    : {tuplex[1]}
                                ผู้ใช้ที่ขาย       : {tuplex[2]}
                                รหัสสินค้า       : {tuplex[3]}
                                ชื่อสินค้า        : {tuplex[4]}
                                ราคาขาย (ชิ้น)  : {tuplex[5]} บาท
                                จำนวนที่รับ (ชิ้น) : {tuplex[6]} ชิ้น
                                จ่าย           : {tuplex[7]} บาท
                                คิดเป็นในปัจจุบัน  : {tuplex[5] * tuplex[6]} บาท
                        """)
            case 5:
                cls()
                print('\n\tเข้าสู่การตรวจสอบ รายชื่อลูกค้า')
                sql_q = """--sql
                    SELECT user_id, user_name, user_balance, user_phone
                        FROM UserDataCS019
                        WHERE user_type = 'T_USER'
                """
                db.db_query(sql_q,'select','print') #!DEBUG
                result = db.db_query(sql_q,'select','return')
                if result is not None:
                    for tuplex in result:
                        print(f"""
                                รหัสผู้ใช้         : {tuplex[0]}
                                ชื่อผู้ใช้          : {tuplex[1]}
                                จำนวนเงินคงเหลือ : {tuplex[2]} บาท
                                เบอร์โทรศัพท์     : {tuplex[3]}
                        """)
            case 6:
                cls()
                print('\n\tเข้าสู่การตรวจสอบ รายชื่อลูกค้า ยอดขายมากที่สด')
                sql_q = """--sql
                    SELECT user_id, user_name, user_balance, user_phone, sum(sell_total) as sum_sell_total
                        FROM UserDataCS019 INNER JOIN BuyDataCS019
                        ON UserDataCS019.user_id = BuyDataCS019.sell_user_id
                        WHERE user_type = 'T_USER'
                        GROUP BY user_id
                        ORDER BY sum_sell_total DESC
                """
                db.db_query(sql_q,'select','print') #!DEBUG
                result = db.db_query(sql_q,'select','return')
                if result is not None:
                    for idx, tuplex in enumerate(result):
                        print(f"""
                        อันดับที่ {idx+1}
                                รหัสผู้ใช้         : {tuplex[0]}
                                ชื่อผู้ใช้          : {tuplex[1]}
                                จำนวนเงินคงเหลือ : {tuplex[2]} บาท
                                เบอร์โทรศัพท์     : {tuplex[3]}
                                ยอดขายทั้งหมด    : {tuplex[4]}
                        """)
            case 9:
                cls()
                print('\n\tกำลังออกจากระบบ')
                self.user_role = 'not_auth'
            case _:
                cls()
                print('\n\tไม่พบสิ่งที่คุณต้องการ')

instance_z = AntiqueShop()
