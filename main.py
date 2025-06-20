# جميع الحقوق محفوظة للمربمج العراقي محمد
import sqlite3 as sql
from flet import Page, RoundedRectangleBorder, FontWeight,MainAxisAlignment, ThemeMode, FilledButton, CrossAxisAlignment, Text, Image, TextField, ElevatedButton, TextButton, Row, Ref, Colors, app, Icons, Column, ProgressRing, IconButton, ListTile, ListView, TextAlign, AppBar, PopupMenuButton, PopupMenuItem, Checkbox
import uuid  # لإنشاء id فريد
from datetime import datetime
import time, random, string, base64

def encrypt(data):
    return base64.b32encode(data.encode('utf-8')).decode()

def decrypt(data):
    return base64.b32decode(data.encode('utf-8')).decode()

def create_table():
    connect = sql.connect('data.db',
                          check_same_thread=False)
    cursor = connect.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS users(username TEXT, 
                   password TEXT, 
                   date TEXT)''')
    connect.commit()
    cursor.close()
    connect.close()

def splash(page:Page):
    page.clean()
    page.theme_mode = ThemeMode.DARK
    page.window.width = 370
    page.window.height = 630
    page.horizontal_alignment = CrossAxisAlignment.CENTER
    page.vertical_alignment = MainAxisAlignment.CENTER
    page.add(Text('...جاري التحميل',
                  color=Colors.BLUE,
                  size=18,
                  weight=FontWeight.BOLD),
                 Text(''),
                 ProgressRing(width=50,
                 height=50,
                 color=Colors.BLUE))
    page.update()
    time.sleep(1)

# الانتقال إلى صفحة إنشاء الحساب مع إظهار شاشة التحميل
def navigate_to_create_account(page: Page):
    splash(page)
    page.clean()
    create_an_account(page)

# الانتقال إلى صفحة تسجيل الدخول مع إظهار شاشة التحميل
def navigate_to_login(page: Page):
    page.appbar = None
    splash(page)
    page.clean()
    main(page)

def navigate_to_add_data(page:Page,username):
    splash(page)
    page.clean()
    add_data(page,username)

def navigate_to_generate_password(page:Page):
    splash(page)
    page.clean()
    generate_password(page)

def navigate_to_app(page: Page,username):
    splash(page)
    page.clean()
    myapp(page,username)

def navigate_to_my_data(page: Page,username):
    splash(page)
    page.clean()
    my_account(page,username)

def navigate_to_about_us(page: Page, username):
    splash(page)
    page.clean()
    about_us(page, username)

def navigate_to_contact(page: Page):
    splash(page)
    page.clean()
    contact_with_me(page)

def check_range_accounts():
    connect = sql.connect('data.db',check_same_thread=False)
    cursor = connect.cursor()
    try:
        account_range = cursor.execute('SELECT * FROM users').fetchall()
        if len(account_range) > 0:
            cursor.close()
            connect.close()
            return True
        else:
            cursor.close()
            connect.close()
            return False
    except:
        cursor.close()
        connect.close()
        return False

def collect_data(username):
    connect = sql.connect('data.db',
                          check_same_thread=False)
    cursor = connect.cursor()
    data = cursor.execute('SELECT * FROM '+username).fetchall()
    cursor.close()
    connect.close()
    return data

def delete_data(uid,username):
    connect = sql.connect('data.db',
    check_same_thread=False)
    cursor = connect.cursor()
    cursor.execute(f'DELETE FROM {username} where id="{uid}"')
    connect.commit()
    cursor.close()
    connect.close()

def contact_with_me(page: Page):
    page.title = "Contact Me"
    page.vertical_alignment = MainAxisAlignment.CENTER
    page.horizontal_alignment = CrossAxisAlignment.CENTER
    page.window.width = 370
    page.window.height = 630
    page.theme_mode = ThemeMode.DARK
    # Create the UI elements
    title = Text("Contact Me", size=30, weight=FontWeight.W_500, color=Colors.BLUE)
    telegram_button = ElevatedButton(
        text="Telegram",
        on_click=lambda _: page.launch_url("https://t.me/lw_w7"),
        icon=Icons.TELEGRAM,
        color=Colors.BLUE,
        icon_color=Colors.BLUE
    )
    youtube_button = ElevatedButton(
        text="YouTube",
        on_click=lambda _: page.launch_url("https://www.youtube.com/@lw_w3"),
        icon=Icons.VIDEO_LIBRARY,
        color=Colors.BLUE,
        icon_color=Colors.BLUE
    )
    instagram_button = ElevatedButton(
        text="Instagram",
        on_click=lambda _: page.launch_url("https://www.instagram.com/lw__w6"),
        icon=Icons.CAMERA_ALT,
        color=Colors.BLUE,
        icon_color=Colors.BLUE
    )
    telegram_channel_button = ElevatedButton(
        text="Telegram Channel",
        on_click=lambda _: page.launch_url("https://t.me/LWTF1"),
        icon=Icons.CHAT_BUBBLE_OUTLINE,
        color=Colors.BLUE,
        icon_color=Colors.BLUE
    )
    # Add elements to the page
    page.add(
        title,
        Column(
            [
                telegram_button,
                youtube_button,
                instagram_button,
                telegram_channel_button,
            ],
            spacing=20,
            alignment=MainAxisAlignment.CENTER,
        ),
    )

def my_account(page:Page, username):
    page.theme_mode = ThemeMode.DARK
    page.window.width = 370
    page.window.height = 630
    page.window.top = 0
    page.window.left = 0
    page.window.min_width = 370
    page.vertical_alignment = MainAxisAlignment.CENTER
    page.horizontal_alignment = CrossAxisAlignment.CENTER
    page.scroll = True
    old_password_ref = Ref[Text]()
    new_password_ref = Ref[Text]()
    re_new_password_ref = Ref[Text]()
    message_ref = Ref[Text]()

    def update_password(username):
        connect = sql.connect('data.db',
                            check_same_thread=False)
        cur = connect.cursor()
        old_password = cur.execute(f'SELECT password FROM users WHERE username="{username}"').fetchone()[0]
        if re_new_password_ref.current.value != new_password_ref.current.value:
            cur.close()
            connect.close()
            message_ref.current.value = 'كلمة المرور التي ادخلتها غير متطابقة'
            message_ref.current.color = Colors.RED

        elif old_password == old_password_ref.current.value:
            cur.execute(f'UPDATE users SET password=? WHERE username=?',(new_password_ref.current.value,username))
            connect.commit()
            cur.close()
            connect.close()
            message_ref.current.value = 'تم تحديث كلمة المرور بنجاح'
            message_ref.current.color = Colors.GREEN
        else:
            cur.close()
            connect.close()
            message_ref.current.value = 'كلمة المرور التي ادخلتها غير صحيحة'
            message_ref.current.color = Colors.RED
        page.update()
    connect = sql.connect('data.db',
                          check_same_thread=False)
    cursor = connect.cursor()
    data = cursor.execute(f'SELECT * FROM {username}').fetchall()
    ud = cursor.execute('SELECT * FROM users WHERE username="{0}"'.format(username)).fetchone()
    
    the_list = ListView(expand=True,
                        padding=20,
                        spacing=10,
                        width=370)
    til = ListTile(width=370,
        title=Text('معلوماتك في ابرنامج',
                   color=Colors.AMBER,
                   size=20,
                   text_align=TextAlign.CENTER,
                   width=100),
        subtitle=Column(controls=[
                Row(controls=[
                    Text(len(data), text_align=TextAlign.RIGHT,
                   width=100,
                   size=16),
                    Text(' :عدد حساباتك', text_align=TextAlign.RIGHT,
                   width=100,
                   size=16)
                ]),
                Row(controls=[
                    Text(ud[0], text_align=TextAlign.RIGHT,
                   width=100,
                   size=16),
                    Text(' :يوزرك', text_align=TextAlign.RIGHT,
                    width=100,
                    size=16)
                ]),
                Row(controls=[
                    Text(ud[2], text_align=TextAlign.RIGHT,
                    width=100,
                    size=16),
                    Text(' :تاريخ تسجيلك', text_align=TextAlign.RIGHT,
                    width=100,
                    size=16)
                ])
            ],
            alignment=MainAxisAlignment.END)
        )
    the_list.controls.append(til)
    old_password = TextField(label='كلمة السر الحالية',
                         width=326,
                         ref=old_password_ref)
    passwords = Row(controls=[
        TextField(label='كلمة المرور الجديدة',
                  width=162,
                  ref=new_password_ref),
        TextField(label='اعد كتابة كلمة المرور',
                  width=162,
                  ref=re_new_password_ref)
    ],
    width=326)
    save_new_data = FilledButton('حفظ كلمة السر الجديدة',
                                 icon=Icons.SAVE,
                                 on_click=lambda e:update_password(ud[0]))
    message = Text('',
                    ref=message_ref)
    page.add(the_list,
             old_password,
             passwords,
             message,
             save_new_data)
    page.update()

def about_us(page:Page, username):
    page.theme_mode = ThemeMode.DARK
    page.window.width = 370
    page.window.height = 630
    page.window.top = 0
    page.window.left = 0
    page.window.min_width = 250
    page.vertical_alignment = MainAxisAlignment.CENTER
    page.horizontal_alignment = CrossAxisAlignment.CENTER
    view = ListView(expand=True,
                    padding=20,
                    spacing=20,
                    width=370)
    til = ListTile(title=Text('من نحن',
                              size=20,
                              text_align=TextAlign.CENTER,
                              width=370,
                              color=Colors.AMBER),
                    subtitle=Column(controls=[
                            Text(f'''تعرّف على تطبيق Scwe - أداة بسيطة لإدارة كلمات المرور!

مرحبًا {username}،

أنا محمد، مؤسس تطبيق Scwe، وأريد أشاركك بأداة بسيطة وسهلة تساعدك في تنظيم كلمات المرور الخاصة بك. في عالم مليء بالحسابات والمنصات المختلفة، تذكر كل كلمة مرور قد يكون أمرًا مزعجًا ومعقدًا.

تطبيق Scwe صممناه علشان نوفر لك طريقة سهلة لتخزين كلمات المرور الخاصة بك في مكان واحد. مع Scwe، راح تقدر:

- تنظيم كلمات المرور: حفظ كل كلمات المرور الخاصة بك في مكان واحد، علشان ما تضطر تتذكرها كلها.
- إنشاء كلمات مرور قوية: التطبيق يقدر يساعدك في إنشاء كلمات مرور آمنة وفريدة لكل حساب.
- الوصول السريع: تقدر توصل لكلمات المرور الخاصة بك بسرعة وسهولة من خلال التطبيق.

هدفنا في Scwe هو تبسيط إدارة كلمات المرور وجعلها أقل تعقيدًا. سواء كنت شخصًا عاديًا أو محترفًا، التطبيق راح يساعدك تنسّق حياتك الرقمية بسهولة.

إذا كان عندك أي أسئلة أو تحتاج مساعدة، ما تتردد تواصل معنا عن طريق الذهاب الى صفحة تواصل معي وتواصل معي

شكرًا لوقتك، ونتمنى تشوف فائدة في Scwe!

مع أطيب التحيات،  
محمد  
مؤسس Scwe''',
                            size=16,
                            color=Colors.WHITE,
                            text_align=TextAlign.RIGHT,
                            rtl=True)
                        ])
                    ,
                    bgcolor='#134f68',
                    shape=RoundedRectangleBorder(20))
    view.controls.append(til)
    page.add(view)
    page.update()

def generate_password(page: Page):
    page.title = "إنشاء كلمة مرور - Scwe"
    page.window.width = 370
    page.window.height = 630
    page.vertical_alignment = MainAxisAlignment.CENTER
    page.horizontal_alignment = CrossAxisAlignment.CENTER
    page.bgcolor = "#121212"  # خلفية داكنة
    page.padding = 50
    # عناصر الواجهة
    title = Text("إنشاء كلمة مرور قوية",
    size=24,
    color="#FFFFFF")  # نص أبيض
    length_input = TextField(
        label="طول كلمة المرور",
        value="12",
        width=300,
        text_align=TextAlign.RIGHT,
        color="#FFFFFF",  # نص أبيض
        bgcolor="#333333",  # خلفية داكنة
    )
    uppercase_check = Checkbox(label="أحرف كبيرة (A-Z)",
    value=True,
    fill_color="#BB86FC")  # لون أرجواني
    lowercase_check = Checkbox(label="أحرف صغيرة (a-z)",
    value=True,
    fill_color="#BB86FC")
    numbers_check = Checkbox(label="أرقام (0-9)",
    value=True,
    fill_color="#BB86FC")
    symbols_check = Checkbox(label="رموز خاصة (!@#$%^&*)",
    value=True,
    fill_color="#BB86FC")
    result = Text(color="#FFFFFF",
                           weight="bold",
                           selectable=True,
                           text_align=TextAlign.CENTER,
                           width=370)  # نص أبيض

    def generate_password(e):
        length = int(length_input.value)
        uppercase = uppercase_check.value
        lowercase = lowercase_check.value
        numbers = numbers_check.value
        symbols = symbols_check.value
        chars = ""
        if uppercase:
            chars += string.ascii_uppercase
        if lowercase:
            chars += string.ascii_lowercase
        if numbers:
            chars += string.digits
        if symbols:
            chars += "!@#$%^&*()_+[]{}|;:,.<>?"
        if not chars:
            result.value = "الرجاء اختيار خيار واحد على الأقل!"
            page.update()
            return
        password = ''.join(random.choice(chars) for _ in range(length))
        result.value = f"{password}"
        page.update()
    generate_button = ElevatedButton(
        "إنشاء كلمة مرور",
        on_click=generate_password,
        bgcolor="#BB86FC",  # لون أرجواني
        color="#000000",  # نص أسود
    )

    # إضافة العناصر إلى الصفحة
    page.add(
        Column(
            [
                title,
                length_input,
                uppercase_check,
                lowercase_check,
                numbers_check,
                symbols_check,
                generate_button,
                result
            ],
            alignment=MainAxisAlignment.CENTER,
            spacing=20,
        )
    )

def myapp(page: Page,username):
    page.theme_mode = ThemeMode.DARK
    page.window.width = 370
    page.window.height = 630
    page.window.top = 0
    page.window.left = 0
    page.window.min_width = 250
    page.vertical_alignment = MainAxisAlignment.CENTER
    page.horizontal_alignment = CrossAxisAlignment.CENTER
    page.scroll = True
    page.appbar=AppBar(title=Text('برنامج ادارة الحسابات',
                                  color=Colors.WHITE),
                                  shadow_color=Colors.BLUE_ACCENT,
                       center_title=True,
                       bgcolor='#134f68',
                       actions=[
                           PopupMenuButton(items=[
                               PopupMenuItem('الصفحة الرئيسية', on_click=lambda e:navigate_to_app(page,username)),
                               PopupMenuItem('أضافة بيانات جديدة',on_click=lambda e:navigate_to_add_data(page,username)),
                               PopupMenuItem('حسابي',on_click=lambda e:navigate_to_my_data(page,username)),
                               PopupMenuItem('تواصل معي',on_click=lambda e:navigate_to_contact(page)),
                               PopupMenuItem('انشاء كلمة سر قوية',on_click=lambda e:navigate_to_generate_password(page)),
                               PopupMenuItem('من نحن', on_click=lambda e:navigate_to_about_us(page, username)),
                               PopupMenuItem('تسجيل الخروج',on_click=lambda e:navigate_to_login(page))
                           ],
                           icon_color=Colors.BLACK)
                       ]
    )
    # القائمة لعرض العناصر
    passwords = ListView(expand=True, spacing=10, padding=20)
    # البيانات في شكل JSON مع إضافة id فريد
    json = collect_data(username)
    # دالة لحذف عنصر من القائمة
    def delete_item(item_id):
        # إزالة العنصر من القائمة بناءً على id
        passwords.controls = [tile for tile in passwords.controls if tile.key != item_id]
        delete_data(item_id,username)
        page.update()  # تحديث الصفحة
    # إضافة عناصر JSON إلى 
    for data in json:
        tile = ListTile(
            bgcolor='#134f68',
            shape=RoundedRectangleBorder(radius=20),
            key=data[0],  # استخدام id كـ key للعنصر
            title=Text(decrypt(data[1]), text_align=TextAlign.RIGHT),  # العنوان من اليمين
            subtitle=Column(
                controls=[
                    Row(controls=[Text(f'يوزر: '),
                                  Text(f'{decrypt(data[2])}',
                                       selectable=True)]),
                    Row(controls=[Text(f'الأيميل: '),
                                  Text(f'{decrypt(data[3])}',
                                       selectable=True)]),
                    Row(controls=[Text(f'الرمز: '),
                                  Text(f'{decrypt(data[4])}',
                                       selectable=True)]),
                    Row(controls=[Text(f'الرقم: '),
                                  Text(f'{decrypt(data[5])}',
                                       selectable=True)]),
                    Row(controls=[Text(f'الموقع: '),
                                  Text(f'{decrypt(data[6])}',
                                       selectable=True)])
                ],
                spacing=5,  # المسافة بين الأسطر
                rtl=True
            ),
            trailing=IconButton(
                icon=Icons.DELETE,
                on_click=lambda e, item_id=data[0]: delete_item(item_id),  # ربط زر الحذف بالدالة
            ),
        )
        passwords.controls.append(tile)
    page.add(passwords)
    page.update()

def add_data(page: Page,account_name):
    page.theme_mode = ThemeMode.DARK
    page.window.width = 370
    page.window.height = 630
    page.window.top = 0
    page.window.left = 0
    page.window.min_width = 250
    page.vertical_alignment = MainAxisAlignment.CENTER
    page.horizontal_alignment = CrossAxisAlignment.CENTER
    name_ref = Ref[Text]()
    username_ref = Ref[Text]()
    mail_ref = Ref[Text]()
    password_ref = Ref[Text]()
    phone_ref = Ref[Text]()
    url_ref = Ref[Text]()
    message_ref = Ref[Text]()
    def add_data():
        connect = sql.connect('data.db',
                              check_same_thread=False)
        cursor = connect.cursor()
        if len(cursor.execute(f'SELECT * FROM {account_name}').fetchall()) < 20:
            cursor.execute(f'INSERT INTO {account_name} VALUES(?,?,?,?,?,?,?)',(str(uuid.uuid4()),
                    encrypt(name_ref.current.value),
                    encrypt(username_ref.current.value),
                    encrypt(mail_ref.current.value),
                    encrypt(password_ref.current.value),
                    encrypt(phone_ref.current.value),
                    encrypt(url_ref.current.value)))
            connect.commit()
            cursor.close()
            name_ref.current.value = ''
            username_ref.current.value = ''
            mail_ref.current.value = ''
            password_ref.current.value = ''
            phone_ref.current.value = ''
            url_ref.current.value = ''
            message_ref.current.value = 'تم اضافة المعلومات بنجاح'
        else:
            message_ref.current.value = 'عفوا ولكنك بلغت الحد الأقصى لحفط الحسابات وهو 20 حساب لحفظ حسابات اكثر  يمكنك شراء النسخة المدفوعة من التطبيق'
            message_ref.current.color = Colors.RED
            contact_telegram.visible = True
            save_data.visible = False
            

        page.update()
    title = Text('اضف معلومات الأن',
                font_family='Sakkal Majalla',
                size=35,
                color=Colors.BLUE_300,
                tooltip='سبحان الله وبحمده سبحان الله العظيم')
    name = TextField(label='اسم الحساب',
                         ref=name_ref)
    username = TextField(label='اسم المستخدم',
                         ref=username_ref)
    mail = TextField(label='الأيميل',
                     ref=mail_ref)
    password = TextField(label='كلمة المرور',
                         ref=password_ref)
    phone = TextField(label='رقم الهاتف',
                      ref=phone_ref)
    site = TextField(label='الموقع',
                     ref=url_ref)
    save_data = FilledButton('حفظ المعلومات',
                             icon=Icons.SAVE,
                             bgcolor=Colors.AMBER,
                             color=Colors.BLACK,
                             on_click=lambda e:add_data())
    message = Text('',
                   color=Colors.GREEN,
                   ref=message_ref,
                   text_align=TextAlign.CENTER,
                   rtl=True)
    
    contact_telegram = ElevatedButton('تواصل معي تليكرام',
                                  visible=False,
                                  color=Colors.BLACK,
                                  bgcolor=Colors.AMBER,
                                  on_click= lambda e: page.launch_url('https://t.me/lw_w7'),
                                  icon=Icons.TELEGRAM,
                                  icon_color=Colors.BLACK)
    page.add(title,
             Text(' '),
             name,
             username,
             mail,
             password,
             phone,
             site,
             message,
             save_data,
             contact_telegram)
    page.update()

# صفحة تسجيل الدخول
def main(page: Page):
    page.theme_mode = ThemeMode.DARK
    page.window.width = 370
    page.window.height = 630
    page.window.top = 0
    page.window.left = 0
    page.window.min_width = 250
    page.vertical_alignment = MainAxisAlignment.CENTER
    page.horizontal_alignment = CrossAxisAlignment.CENTER
    username_ref = Ref[TextField]()
    password_ref = Ref[TextField]()
    error_message_ref = Ref[Text]()
    def check(data):
        try:
            connect = sql.connect('data.db',check_same_thread=False)
            cursor = connect.cursor()
            username,password = data
            data2 = cursor.execute(f'SELECT * FROM users WHERE username="{username}"').fetchone()
            if password == data2[1]:
                error_message_ref.current.value = 'تم تسجيل الدخول'
                error_message_ref.current.color = Colors.GREEN
                page.update()
                navigate_to_app(page,username)
        except TypeError as e:
            error_message_ref.current.value = 'اسم المستخدم او كلمة المرور غير صحيح'
            error_message_ref.current.color = Colors.RED
            page.update()
        except sql.OperationalError as e:
            error_message_ref.current.value = 'اسم المستخدم او كلمة المرور غير صحيح'
            error_message_ref.current.color = Colors.RED
            page.update()
            create_table()
    title = Text('لوحة تسجيل الدخول',
                 color=Colors.BLUE_ACCENT,
                 size=35,
                 text_align='Center',
                 font_family='Sakkal Majalla',
                 width=330,
                 height=50,
                 rtl=True,
                 tooltip='تم برمجة هذه التطبيق لأدارة كلمات مبرورك بسهولة. من قبل المبرمج محمد العراقي')
    logo = Image(src=f'src/assets/logo.png',
                 width=100,
                 height=150)
    Username = TextField(label='اسم المستخدم',
                         width=250,
                         tooltip='اسم المستخدم الذي استخدمته لأنشاء حسابك',
                         icon=Icons.PEOPLE,
                         ref=username_ref)
    Password = TextField(label='كلمة المرور',
                         width=250,
                         password=True,
                         tooltip='كلمة مرور حسابك',
                         icon=Icons.PASSWORD,
                         can_reveal_password=True,
                         ref=password_ref)
    Login = ElevatedButton('تسجيل الدخول',
                           icon=Icons.LOGIN,
                           bgcolor=Colors.AMBER,
                           color=Colors.BLACK,
                           icon_color=Colors.BLACK,
                           width=150,
                           height=30,
                           on_click=lambda e:check((username_ref.current.value,password_ref.current.value)))
    Create = TextButton('انشاء حساب',
                        icon=Icons.ACCOUNT_BOX,
                        on_click=lambda e: navigate_to_create_account(page))
    error_message = Text('',ref=error_message_ref)
    page.add(title,
             Text(''),
             logo,
             Username,
             Password,
             error_message,
             Login,
             Create)
    page.update()

# صفحة انشاء حساب
def create_an_account(page: Page):
    page.theme_mode = ThemeMode.DARK
    page.window.width = 370
    page.window.height = 630
    page.window.top = 0
    page.window.left = 0
    page.window.min_width = 250
    page.vertical_alignment = MainAxisAlignment.CENTER
    page.horizontal_alignment = CrossAxisAlignment.CENTER
    error_message_ref = Ref[Text]()
    username_ref = Ref[Text]()
    password_ref = Ref[Text]()
    repassword_ref = Ref[Text]()
    title = Text('انشئ حسابك الأن',
                font_family='Sakkal Majalla',
                size=35,
                color=Colors.BLUE_300,
                tooltip='سبحان الله وبحمده سبحان الله العظيم')
    logo = Image('src/assets/add.png',
                 width=100,
                 height=100)
    username = TextField(label='اسم المستخدم',
                tooltip='اسم المستخدم الخاص فيك',
                icon=Icons.PEOPLE,
                width=300,
                ref=username_ref)
    password = TextField(label='كلمة السر',
                tooltip='اسم المستخدم الخاص فيك',
                password=True,
                can_reveal_password=True,
                width=160,
                ref=password_ref)
    repassword = TextField(label='اعادة كتابة كلمة السر',tooltip='اسم المستخدم الخاص فيك',
                password=True,
                can_reveal_password=True,
                width=160,
                ref=repassword_ref)
    row = Row(width=370,
              height=100,
              scroll='always',wrap=False)
    row.controls.append(password)
    row.controls.append(repassword)
    error_message = Text(color=Colors.RED,
                         size=14,
                         ref=error_message_ref,rtl=True,
                         text_align=TextAlign.CENTER)
    
    def new_account(username,password):
        try:
            connect = sql.connect('data.db',check_same_thread=False)
            cursor = connect.cursor()
            cursor.execute(f'CREATE TABLE {username}(id TEXT, account TEXT, username, mail TEXT,password TEXT,phone TEXT, url TEXT)')
            connect.commit()
            cursor.execute('CREATE TABLE IF NOT EXISTS users(username TEXT, password TEXT, date TEXT)')
            date = f'{datetime.now().year}/{datetime.now().month}/{datetime.now().day}'
            cursor.execute('INSERT INTO users VALUES(?,?,?)',(username,password,date))
            connect.commit()
            cursor.close()
            connect.close()
            navigate_to_login(page)
            return ['تم انشاء حسابك بنجاح',Colors.GREEN]
        except sql.OperationalError:
            return ['عفواً ولكن هذه الحساب محجوز',Colors.RED_ACCENT]

    def on_create_click(e):
        username = username_ref.current.value
        password = password_ref.current.value
        repassword = repassword_ref.current.value
        invalid_chars = " !@#$%^&*()+=[]{}|\\:;\"'<>,.?/"
        if check_range_accounts():
            error_message_ref.current.value = 'عفواً ولكنك تملك حساب سابقاً في التطبيق من اجل الحصول على حسابات اكثر اشترك في المميز'
            error_message_ref.current.color = Colors.RED
            contact_telegram.visible=True
            create.visible=False
        elif any(char in invalid_chars for char in username):
            error_message_ref.current.color = Colors.RED
            error_message_ref.current.value = (
                "خطأ: لا يمكن استخدام المسافات أو الرموز الخاصة التالية في اسم المستخدم:\n"
                "! @ # $ % ^ & * ( ) + = [ ] { } | \\ : ; \" ' < > , . ? /"
            )
        elif password != repassword:
            error_message_ref.current.value = 'كلمة المرور غير متطابقة الرجاء اعادة المحاولة '
        elif username == '' or username.isspace() or len(username) < 4:
            error_message_ref.current.color = Colors.RED
            error_message_ref.current.value = 'اسم المستخدم الذي ادخلته غير صحيح جرب مع اسم اخر'
        elif len(password) < 7:
            error_message_ref.current.color = Colors.RED
            error_message_ref.current.value = 'كلمة المرور التي ادخلتها قصيرة جدا اقل عدد مطلوب 8 حروف'
        else:
            da = new_account(username=username,password=password)
            error_message_ref.current.color = da[1]
            error_message_ref.current.value = da[0]
        page.update()
    create = ElevatedButton('انشاء الحساب',
                            color=Colors.BLACK,
                            bgcolor=Colors.AMBER,
                            icon=Icons.CREATE,
                            icon_color=Colors.BLACK,
                            width=150,
                            height=30,
                            on_click=on_create_click)
    have = TextButton('لدي حساب الفعل',
                      on_click=lambda e:navigate_to_login(page))
    contact_telegram = ElevatedButton('تواصل تليكرام',
                                  visible=False,
                                  color=Colors.BLACK,
                                  bgcolor=Colors.AMBER,
                                  on_click= lambda e: page.launch_url('https://t.me/lw_w7'),
                                  icon=Icons.TELEGRAM,
                                  icon_color=Colors.BLACK)
    page.add(title,
             logo,
             username,
             row,
             error_message,
             contact_telegram,
             create,
             have)
    page.update()

# تشغيل التطبيق
app(target=main)