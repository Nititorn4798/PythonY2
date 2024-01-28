"""ระบบจัดการร้านขายของเก่า V 1 """
import sqlite3
from datetime import datetime
print('ระบบจัดการร้านขายของเก่า V 1.0 Powered By SQLite3')

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

        cc = [0]
        try:
            cc = self.conn.execute("""select count(*) as A from UserDataCS019""").fetchone()
        except sqlite3.DatabaseError:
            print('โครงสร้างฐานข้อมูลเกิดข้อผิดพลาด (malformed) ลองลบไฟล์ฐานข้อมูลแล้วใช้งานโปรแกรมใหม่อีกครั้ง')
        if not cc[0]:
            print('\nFound New Database Insert DEMO Data!\n')
            cmd_insert_userdata = """INSERT INTO UserDataCS019 (user_id,user_name,user_password,user_balance,user_phone,user_type)"""
            cmd_insert_itemdata = """INSERT INTO ItemsDataCS019 (item_id,item_name,item_buyprice,item_status)"""
            cmd_insert_buydata = """INSERT INTO BuyDataCS019 (sell_id,sell_user_id,sell_item_id,sell_item_amount,sell_total,sell_datetime)"""
            demo_user = {
                1 : {
                    1 : "Nititorn4798",2 : "1234admin",3 : -65003263019,4 : "0906501999",5 : "T_ADMIN"
                },
                2 : {
                    1 : "user",2 : "1234",3 : 1599,4 : "0999999998",5 : "T_USER"
                },
                3 : {
                    1 : "admin",2 : "1234",3 : 5657,4 : "0667654321",5 : "T_ADMIN"
                },
                4 : {
                    1 : "dong",2 : "1234",3 : 4952,4 : "0236545691",5 : "T_USER"
                }
            }
            demo_itemdata = {
                1 : {
                    1 : "กระป๋องกาแฟ / นม / สังกะสี",2 : 2.0,3 : "ปกติ"
                },
                2 : {
                    1 : "กระป๋องน้ำอัดลม + อลูมิเนียม",2 : 25.00,3 : "ปกติ"
                },
                3 : {
                    1 : "พลาสติกใส / ขวดน้ำดื่ม",2 : 5.0,3 : "ปกติ"
                },
                4 : {
                    1 : "พลาสติกสี รวม",2 : 3.0,3 : "งดรับ"
                }
            }
            demo_buydata = {
                1 : {
                    1 : 2,2 : 1,3 : 10,4: 30,5 : "18-01-2024 19:06:50"
                },
                2 : {
                    1 : 4,2 : 3,3 : 20,4: 60,5 : "19-01-2024 19:06:50"
                }
            }
            for i,j in demo_user.items():
                sql_insert = f"""--sql row {i}
                    {cmd_insert_userdata}
                    VALUES (NULL,'{j[1]}','{j[2]}',{j[3]},'{j[4]}','{j[5]}');
                """
                self.db_query(sql_insert)
            for i,j in demo_itemdata.items():
                sql_insert = f"""--sql row {i}
                    {cmd_insert_itemdata}
                    VALUES (NULL,'{j[1]}',{j[2]},'{j[3]}');
                """
                self.db_query(sql_insert)
            for i,j in demo_buydata.items():
                sql_insert = f"""--sql row {i}
                    {cmd_insert_buydata}
                    VALUES (NULL,{j[1]},{j[2]},{j[3]},{j[4]},'{j[5]}');
                """
                self.db_query(sql_insert)

    def db_query(self,cmd,mode='insert',workmode='return'):
        """รันคำสั่ง"""
        try:
            temp = sqlite3.Cursor(self.conn) #!ไม่จำเป็นแค่ใส่ไว้กัน unbound
            match mode:
                case 'insert' | 'select' | 'update':
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

class AntiqueShop:
    """ร้านขายของเก่า"""
    current_menu = 'main'
    def __authenticator(self):
        """ระบบยืนยันตัวตน"""
        def register():
            cls()
            while True:
                print('ระบบสมัครสมาชิก')
                print('\nชื่อผู้ใช้ 4 ต้องการอักษรขึ้นไปและขึ้นต้นด้วยอักษรภาษาอังกฤษ. \nรหัสผ่านต้องการ 4ตัวอักษรขึ้นไป.\nพิมพ์ "cancel" เพื่อยกเลิก')
                user = secure_input('\tUsername <<< ','chk_lenstr_plus',strlen=4,chk_firstisalphabet=True)
                if user in ['c','cancel']:
                    cls()
                    return 'cancel'
                pwd = secure_input('\tPassword <<< ','chk_lenstr_plus',strlen=4)
                phone_number = secure_input('\tเบอร์โทรศัพท์ <<< ','chk_lenstr')
                sql_insert = f"""--sql
                    insert into UserDataCS019 (user_id,user_name,user_password,user_balance,user_phone,user_type)
                    values (NULL,'{user}','{pwd}',{0},'{phone_number}','T_USER');
                """
                try:
                    db.db_query(sql_insert)
                    cls()
                    break
                except sqlite3.IntegrityError:
                    print(f'ชื่อผู้ใช้ [{user}] ไม่สามารถใช้ได้ หรือข้อมูลไม่ถูกต้อง! กรุณาลองใหม่อีกครั้ง')

        def login():
            """ล็อกอิน"""
            while True:
                print('กรุณากรอกข้อมูลเพื่อยืนยันตัวตน [พิมพ์ r เพื่อสมัครสมาชิก] [พิมพ์ cancel เพื่อยกเลิก]\n')
                user = secure_input('\tUsername >>> ','chk_lenstr_plus')
                if user in ['r','R']:
                    register()
                elif user in ['c','cancel']:
                    cls()
                    return 'cancel'
                else:
                    pwd = secure_input('\tPassword >>> ','chk_lenstr_plus')
                    cmd = f"""--sql
                        SELECT count(*) FROM UserDataCS019 WHERE user_name = '{user}' AND user_password = '{pwd}'
                    """
                    temp = db.db_query(cmd,'select','return')
                    if (temp is not None) and (temp[0][0] == 1):
                        self.user_name = user
                        cmd = f"""--sql
                            SELECT user_type FROM UserDataCS019 WHERE user_name = '{user}'
                        """
                        temp = db.db_query(cmd,'select','return')
                        if temp is not None:
                            self.user_role = temp[0][0]
                            break
                    else:
                        print('\nชื่อผู้ใช้ หรือ รหัสผ่าน ไม่ถูกต้อง\n')
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
            self.main()
        except:
            print('เกิดข้อผิดพลาด')
            raise

    def main(self):
        """ระบบเลือกการแสดงผลตามสิทธิ"""
        while self.current_menu == 'main':
            cls()
            now = datetime.now()
            dt_string_b = now.strftime("%d/%m/%Y")
            print(f'วันที่  : {dt_string_b}')
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
                    print('\n\tจบการทำงาน')
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
        print('\t1. ขายของเก่า')
        print('\t2. ถอนเงิน')
        print('\t9. ออกจากระบบ')
        q = secure_input('\t>>> ','chk_int')
        match q:
            case 1:
                cls()
                print('\n\tเข้าสู่การขายของเก่า')
                sql_q = """--sql
                    SELECT * FROM ItemsDataCS019
                        WHERE ItemsDataCS019.item_status <> 'ยกเลิก' AND ItemsDataCS019.item_status <> 'งดรับ'
                """
                result = db.db_query(sql_q,'select','return')
                if result is not None:
                    for tuplex in result:
                        print(f"""
                                รหัสสินค้า : [ {tuplex[0]} ] ชื่อสินค้า : [ {tuplex[1]} ]
                                ราคาขาย (ต่อกิโล) : [ {tuplex[2]:,} บาท ]
                        """)

                item_id = secure_input('\tกรอกรหัสสินค้าที่จะขาย   >>> ','chk_lenstr_plus')
                sql_q = f"""--sql
                    SELECT * FROM ItemsDataCS019
                        WHERE ItemsDataCS019.item_id = {item_id} AND ItemsDataCS019.item_status <> 'ยกเลิก' AND ItemsDataCS019.item_status <> 'งดรับ'
                """
                result = db.db_query(sql_q,'select','return')
                item_name = ''
                item_id_get = 0
                item_price_get = 0
                if result is not None:
                    for tuplex in result:
                        item_id_get = tuplex[0]
                        item_name = tuplex[1]
                        item_price_get = tuplex[2]
                        print(f"""
                                รหัสสินค้า : [ {tuplex[0]} ] ชื่อสินค้า : [ {tuplex[1]} ]
                                ราคาขาย (ต่อกิโล) : [ {tuplex[2]:,} บาท ]
                        """)

                sql_q = f"""--sql
                    SELECT user_id FROM UserDataCS019
                        WHERE UserDataCS019.user_name = '{self.user_name}'
                """
                result = db.db_query(sql_q,'select','return')
                user_id_get = 0
                if result is not None:
                    for tuplex in result:
                        user_id_get = tuplex[0]

                item_amount = secure_input('\tกรอกน้ำหนักสินค้าที่ขาย (กก.) >>> ','chk_int')

                if not (item_name == '' or item_id_get == 0):
                    if (secure_input(f"\tท่านยืนยันที่จะขายสินค้าดังกล่าวหรือไม่ [Y/N] ({item_amount} กก.) >>> ",mode='chk_lenstr')) in ['Y','y']:
                        cal_sell_total = item_amount * item_price_get
                        cal_sell_total = float(cal_sell_total)
                        if cal_sell_total <= 0:
                            print('ข้อมูลธุรกรรมไม่ถูกต้องกรุณาลองใหม่อีกครั้ง')
                        else:
                            sql_q = f"""--sql
                                INSERT INTO BuyDataCS019 (sell_id,sell_user_id,sell_item_id,sell_item_amount,sell_total,sell_datetime)
                                    VALUES (NULL,{user_id_get},{item_id},{item_amount},{cal_sell_total},strftime('%d-%m-%Y %H:%M:%S', 'now', 'localtime'))
                            """
                            try:
                                db.db_query(sql_q,'update','return')
                            except:
                                print('เกิดข้อผิดพลาดกรุณาลองใหม่อีกครั้ง')
                                raise
                            else:
                                sql_q = f"""--sql
                                    UPDATE UserDataCS019
                                        SET user_balance = (user_balance + {cal_sell_total})
                                        WHERE user_id = {user_id_get}
                                """
                                try:
                                    db.db_query(sql_q,'update','return')
                                except:
                                    print('เกิดข้อผิดพลาดกรุณาลองใหม่อีกครั้ง')
                                    raise
                                else:
                                    cls()
                                    print(f'ขายสินค้า [ {item_name} ] รหัส [ {item_id_get} ] สำเร็จ! ได้เงินจำนวน +{cal_sell_total:,} บาท!\n')
                    else:
                        print('\nยกเลิกการขายสินค้าแล้ว\n')
                else:
                    print(f"ไม่พบสินค้าที่ท่านต้องการขาย (ID: {item_id}) หรือสินค้านั้นถูกลบไปแล้ว\n")
            case 2:
                cls()
                print('\n\tเข้าสู่การถอนเงิน')
                sql_q = f"""--sql
                    SELECT user_name, user_balance FROM UserDataCS019
                        WHERE user_name = '{self.user_name}'
                """
                result = db.db_query(sql_q,'select','return')
                __current_user_balance = 0
                if result is not None:
                    for tuplex in result:
                        __current_user_balance = tuplex[1]
                        print(f"""
                                ชื่อผู้ใช้          : {tuplex[0]}
                                จำนวนเงินคงเหลือ : {__current_user_balance:,}
                        """)
                    if __current_user_balance > 0:
                        __to_withdraw = float(secure_input('\tกรอกจำนวนเงินที่ท่านต้องการถอน >>> '))
                        if __to_withdraw > __current_user_balance:
                            print(f'จำนวนเงินคงเหลือของท่านไม่เพียงพอ ขาดอีก {(__to_withdraw - __current_user_balance):,.3f} บาท')
                        else:
                            __current_user_balance = __current_user_balance - __to_withdraw
                            print(f'\tถอนเงินสำเร็จ\n\tจำนวนเงินคงเหลือของท่าน คือ {__current_user_balance:,} บาท\n')
                            sql_q = f"""--sql
                                UPDATE UserDataCS019
                                    SET user_balance = {__current_user_balance}
                                    WHERE user_name = '{self.user_name}'
                            """
                            try:
                                db.db_query(sql_q,'update','return')
                            except:
                                print('เกิดข้อผิดพลาดกรุณาลองใหม่อีกครั้ง')
                                raise
                    else:
                        print('จำนวนเงินคงเหลือของท่านไม่เพียงพอ')
            case 9:
                cls()
                print('\n\tกำลังออกจากระบบ ขอบคุณที่ใช้บริการ')
                self.user_role = 'not_auth'
            case _:
                cls()
                print('\n\tไม่พบสิ่งที่คุณต้องการ')

    def __home_admin(self):
        """หน้าหลักของผู้ดูแลร้าน"""
        self.current_menu = 'home_admin'
        cls()
        print(f'{"*"*19}')
        print(f'\nยินดีต้อนรับคุณ {self.user_name} ในฐานะผู้ดูแลร้าน\n')
        print('เลือกการทำงานที่ต้องการ')
        print('\t1. เพิ่ม รายการรับซื้อ')
        print('\t2. ลบ รายการรับซื้อ')
        print('\t3. แก้ไข รายการรับซื้อ')
        print('\t4. ตรวจสอบ รายการรับซื้อ')
        print('\t5. ตรวจสอบ บันทึกรับซื้อ')
        print('\t6. ตรวจสอบ รายชื่อลูกค้า')
        print('\t7. ตรวจสอบ รายชื่อลูกค้าที่ยอดขายมากที่สุด')
        print('\t8. ตรวจสอบ รายชื่อผู้ใช้งานทั้งหมด')
        print('\t9. ออกจากระบบ')
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
                    print(f'เพิ่มข้อมูลสินค้า {item_name} ในราคา {item_buyprice:,} บาท สำเร็จ!\n')
            case 2:
                cls()
                print('\n\tลบ รายการรับซื้อ')
                sql_q = """--sql
                    SELECT * FROM ItemsDataCS019 WHERE ItemsDataCS019.item_status <> 'ยกเลิก'
                """
                result = db.db_query(sql_q,'select','return')
                if result is not None:
                    for tuplex in result:
                        print(f"""
                                รหัสสินค้า          : {tuplex[0]}
                                ชื่อสินค้า           : {tuplex[1]}
                                ราคาขาย (ต่อกิโล)  : {tuplex[2]:,} บาท
                                สถานะ            : {tuplex[3]}
                        """)

                item_id = secure_input('\tกรอกรหัสสินค้าที่จะลบ   >>> ','chk_lenstr_plus')
                sql_q = f"""--sql
                    SELECT * FROM ItemsDataCS019
                        WHERE ItemsDataCS019.item_id = {item_id} AND ItemsDataCS019.item_status <> 'ยกเลิก'
                """
                result = db.db_query(sql_q,'select','return')
                item_name = ''
                item_id_get = 0
                if result is not None:
                    for tuplex in result:
                        item_id_get = tuplex[0]
                        item_name = tuplex[1]
                        print(f"""
                                รหัสสินค้า          : {tuplex[0]}
                                ชื่อสินค้า           : {tuplex[1]}
                                ราคาขาย (ต่อกิโล)  : {tuplex[2]:,} บาท
                                สถานะ            : {tuplex[3]}
                        """)
                if not (item_name == '' or item_id_get == 0):
                    if (secure_input("\tท่านยืนยันที่จะลบสินค้าดังกล่าวหรือไม่ [Y/N] >>> ",mode='chk_lenstr')) in ['Y','y']:
                        sql_q = f"""--sql
                            UPDATE ItemsDataCS019
                                SET item_status = 'ยกเลิก'
                                WHERE item_id = {item_id}
                        """
                        try:
                            db.db_query(sql_q,'update','return')
                        except:
                            print('เกิดข้อผิดพลาดกรุณาลองใหม่อีกครั้ง')
                            raise
                        else:
                            cls()
                            print(f'ลบข้อมูลสินค้า {item_name} รหัส {item_id_get} สำเร็จ!\n')
                    else:
                        print('\nยกเลิกการลบสินค้าแล้ว\n')
                else:
                    print(f"ไม่พบสินค้าที่ท่านต้องการลบ (ID: {item_id}) หรือสินค้านั้นถูกลบไปแล้ว\n")
            case 3:
                cls()
                print('\n\tแก้ไข รายการรับซื้อ')
                sql_q = """--sql
                    SELECT * FROM ItemsDataCS019
                """
                result = db.db_query(sql_q,'select','return')
                if result is not None:
                    for tuplex in result:
                        print(f"""
                                รหัสสินค้า          : {tuplex[0]}
                                ชื่อสินค้า           : {tuplex[1]}
                                ราคาขาย (ต่อกิโล)  : {tuplex[2]:,} บาท
                                สถานะ            : {tuplex[3]}
                        """)

                item_id = secure_input('\tกรอกรหัสสินค้าที่จะแก้ไข   >>> ','chk_lenstr_plus')
                sql_q = f"""--sql
                    SELECT * FROM ItemsDataCS019
                        WHERE ItemsDataCS019.item_id = {item_id}
                """
                result = db.db_query(sql_q,'select','return')
                item_name = ''
                item_id_get = 0
                if result is not None:
                    for tuplex in result:
                        item_id_get = tuplex[0]
                        item_name = tuplex[1]
                        print(f"""
                                รหัสสินค้า          : {tuplex[0]}
                                ชื่อสินค้า           : {tuplex[1]}
                                ราคาขาย (ต่อกิโล)  : {tuplex[2]:,} บาท
                                สถานะ            : {tuplex[3]}
                        """)
                if not (item_name == '' or item_id_get == 0):
                    print("กรอกรายละเอียดที่ต้องการแก้ไข")
                    print("หากไม่ต้องการแก้ไขให้กรอก - ไว้ แล้วกด Enter")
                    print("หากไม่ต้องการแก้ไขราคาขาย ให้กรอก -1 ไว้ แล้วกด Enter")
                    edit_name = secure_input('\tชื่อสินค้า   >>> ','chk_lenstr_plus')
                    edit_price = secure_input('\tราคาขาย (ต่อกิโล)   >>> ','chk_float')
                    print("สถานะสินค้ามี -> 'ปกติ','งดขาย','ยกเลิก', '-' ")
                    while True:
                        edit_status = secure_input('\tสถานะ   >>> ','chk_lenstr_plus')
                        if edit_status in ['ปกติ','งดขาย','ยกเลิก','-']:
                            break
                        else:
                            print("กรุณากรอก 'ปกติ','งดขาย','ยกเลิก', '-' ")
                    if edit_name in ['-']:
                        edit_name = 'NULL'
                    else:
                        edit_name = f"'{edit_name}'"
                    if edit_price == -1:
                        edit_price = 'NULL'
                    if edit_status in ['-']:
                        edit_status = 'NULL'
                    else:
                        edit_status = f"'{edit_status}'"
                    if (secure_input("\tท่านยืนยันที่แก้ไขข้อมูลสินค้าดังกล่าวหรือไม่ [Y/N] >>> ",mode='chk_lenstr')) in ['Y','y']:
                        sql_q = f"""--sql
                            UPDATE ItemsDataCS019
                                SET item_name = IFNULL({edit_name}, item_name),
                                    item_buyprice = IFNULL({edit_price}, item_buyprice),
                                    item_status = IFNULL({edit_status}, item_status)
                                WHERE item_id = {item_id}
                        """
                        try:
                            db.db_query(sql_q,'update','return')
                        except:
                            print('เกิดข้อผิดพลาดกรุณาลองใหม่อีกครั้ง')
                            raise
                        else:
                            # cls()
                            print(f'แก้ไขข้อมูลสินค้า รหัส {item_id_get} สำเร็จ!\n')
                    else:
                        print('\nยกเลิกการลบสินค้าแล้ว\n')
                else:
                    print(f"ไม่พบสินค้าที่ท่านต้องการลบ (ID: {item_id}) หรือสินค้านั้นถูกลบไปแล้ว\n")
            case 4:
                cls()
                print('\n\tแก้ไข รายการรับซื้อ')
                sql_q = """--sql
                    SELECT * FROM ItemsDataCS019
                """
                result = db.db_query(sql_q,'select','return')
                if result is not None:
                    for tuplex in result:
                        print(f"""
                                รหัสสินค้า          : {tuplex[0]}
                                ชื่อสินค้า           : {tuplex[1]}
                                ราคาขาย (ต่อกิโล)  : {tuplex[2]:,} บาท
                                สถานะ            : {tuplex[3]}
                        """)
            case 5:
                cls()
                print('\n\tเข้าสู่การตรวจสอบ บันทึกรับซื้อ')
                sql_q = """--sql
                    SELECT sell_id, sell_user_id, user_name, item_id , item_name, item_buyprice, sell_item_amount, sell_total FROM BuyDataCS019
                        INNER JOIN UserDataCS019
                        INNER JOIN ItemsDataCS019
                        ON UserDataCS019.user_id = BuyDataCS019.sell_user_id
                        AND ItemsDataCS019.item_id = BuyDataCS019.sell_item_id
                """
                result = db.db_query(sql_q,'select','return')
                if result is not None:
                    for tuplex in result:
                        print(f"""
                                รหัสการรับซื้อ       : {tuplex[0]}
                                รหัสผู้ใช้ที่ขาย       : {tuplex[1]}
                                ผู้ใช้ที่ขาย          : {tuplex[2]}
                                รหัสสินค้า          : {tuplex[3]}
                                ชื่อสินค้า           : {tuplex[4]}
                                ราคาขาย (ต่อกิโล)  : {tuplex[5]:,} บาท
                                จำนวนที่รับ (กิโล)   : {tuplex[6]} กก.
                                จ่าย              : {tuplex[7]:,} บาท
                                คิดเป็นในปัจจุบัน     : {tuplex[5] * tuplex[6]} บาท
                        """)
            case 6:
                cls()
                print('\n\tเข้าสู่การตรวจสอบ รายชื่อลูกค้า')
                sql_q = """--sql
                    SELECT user_id, user_name, user_balance, user_phone
                        FROM UserDataCS019
                        WHERE user_type = 'T_USER'
                """
                result = db.db_query(sql_q,'select','return')
                if result is not None:
                    for tuplex in result:
                        print(f"""
                                รหัสผู้ใช้         : {tuplex[0]}
                                ชื่อผู้ใช้          : {tuplex[1]}
                                จำนวนเงินคงเหลือ : {tuplex[2]:,} บาท
                                เบอร์โทรศัพท์     : {tuplex[3]}
                        """)
            case 7:
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
                result = db.db_query(sql_q,'select','return')
                if result is not None:
                    for idx, tuplex in enumerate(result):
                        print(f"""
                        อันดับที่ {idx+1}
                                รหัสผู้ใช้         : {tuplex[0]}
                                ชื่อผู้ใช้          : {tuplex[1]}
                                จำนวนเงินคงเหลือ : {tuplex[2]:,} บาท
                                เบอร์โทรศัพท์     : {tuplex[3]}
                                ยอดขายทั้งหมด    : {tuplex[4]}
                        """)
            case 8:
                cls()
                print('\n\tเข้าสู่การตรวจสอบ รายชื่อผู้ใช้งานทั้งหมด')
                sql_q = """--sql
                    SELECT user_id, user_name, user_balance, user_phone
                        FROM UserDataCS019
                """
                result = db.db_query(sql_q,'select','return')
                if result is not None:
                    for tuplex in result:
                        print(f"""
                                รหัสผู้ใช้         : {tuplex[0]}
                                ชื่อผู้ใช้          : {tuplex[1]}
                                จำนวนเงินคงเหลือ : {tuplex[2]:,} บาท
                                เบอร์โทรศัพท์     : {tuplex[3]}
                        """)
            case 9:
                cls()
                print('\n\tกำลังออกจากระบบ')
                self.user_role = 'not_auth'
            case _:
                cls()
                print('\n\tไม่พบสิ่งที่คุณต้องการ')

instance_z = AntiqueShop()
db.db_close()
