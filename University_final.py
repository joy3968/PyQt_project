import sys, pymysql
from PyQt5.QtWidgets import *
from PyQt5.QtGui import QStandardItemModel
from PyQt5.QtCore import Qt, QDate
from PyQt5.QtCore import *



#가장 초기 화면 클래스 구성(큰 틀)
class MyApp(QDialog):

    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        tabs = QTabWidget()
        tabs.addTab(SubjectTab(), '학과 등록')    #나중에 만들거임
        tabs.addTab(StudentTab(), '학생 등록')
        tabs.addTab(LessonTab(), '과목 등록')
        tabs.addTab(TraineeTab(), '수강 신청')

        buttonbox = QDialogButtonBox(QDialogButtonBox.Ok)
        buttonbox.accepted.connect(self.accept)                   #버튼을 누르면 승인을 하는 이벤트

        vbox = QVBoxLayout()         #vbox레이아웃 생성
        vbox.addWidget(tabs)         #vbox에 tabs 위잿을 담음
        vbox.addWidget(buttonbox)    #vbox에 buttonbox 위잿을 담음

        self.setLayout(vbox)

        self.setWindowTitle('미래 대학교 수강 관리')      #제목 설정
        self.setGeometry(0, 0, 1200, 600)
        self.center()                                 #화면이 중앙으로 오게 설정하는 함수를 불러옴
        self.show()


    #화면을 중앙으로 불러오는 함수 만들기
    def center(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

# 학과 등록(탭) 클래스 만들기
class SubjectTab(QWidget):
    def __init__(self):
        super().__init__()
        self.dbConnect()        #db연결하는 메서드 자동실행
        self.initUI()
        self.subjectlist(self)    #위치추적(나중에 켤꺼임)



    #db 연결하는 메서드
    def dbConnect(self):
        try:
            self.conn = pymysql.connect(
                host = "127.0.0.1",
                user = "manager",
                password = "manager",
                db = "universitydb",
                port = 3306,
                charset = "utf8"
                )
        except:
            print("문제가 있네요!")
            exit(1)

        print("연결 성공!")

        self.uni_cur = self.conn.cursor()


    def initUI(self):


        self.lbl_subject_register = QLabel('학과 등록', self) #학과 등록 라벨 생성
        self.lbl_subject_register.move(30, 25)               #라벨 위치설정

        #일련번호 라벨
        self.lbl_s_num = QLabel('일련 번호 :', self)
        self.lbl_s_num.move(50,55)
        self.edit_s_num = QLineEdit(self)
        self.edit_s_num.move(120, 50)
        self.edit_s_num.setDisabled(True)
        # self.edit_s_num.setReadOnly(True)

        #학과 번호 라벨
        self.lbl_subjerct_num = QLabel('학과 번호 :', self)
        self.lbl_subjerct_num.move(50, 85)
        self.edit_subject_num = QLineEdit(self)
        self.edit_subject_num.move(120, 80)

        #학과명 라벨
        self.lbl_subject_name = QLabel('학  과  명 :', self)
        self.lbl_subject_name.move(50, 115)
        self.edit_subject_name = QLineEdit(self)
        self.edit_subject_name.move(120 ,110)

        #등록 버튼
        self.btn_subject_insert = QPushButton("등 록", self)
        self.btn_subject_insert.move(50, 150)
        self.btn_subject_insert.clicked.connect(self.subject_insert)    #클릭하면 subject_insert 메서드 실행

        #수정 버튼
        self.btn_subject_update = QPushButton("수 정", self)
        self.btn_subject_update.move(130, 150)
        self.btn_subject_update.clicked.connect(self.subject_edit)      #클릭하면 subject_edit 메서드 실행

        #삭제 버튼
        self.btn_subject_delete = QPushButton("삭 제", self)
        self.btn_subject_delete.move(210, 150)
        self.btn_subject_delete.clicked.connect(self.subject_delete)        #클릭하면 subject_edlete 메서드 실행

        #초기화 버튼
        self.btn_subject_init = QPushButton("초기화", self)
        self.btn_subject_init.move(130, 180)
        self.btn_subject_init.clicked.connect(self.subject_init)        #클릭하면 subject_init 메서드 실행

        #업데이트와 삭제 버튼은 초기에 비활성화 시켜놓음
        self.btn_subject_update.setDisabled(True)
        self.btn_subject_delete.setDisabled(True)

        #학과 목록 라벨
        self.lbl_subject_num = QLabel('학과 목록', self)
        self.lbl_subject_num.move(350, 25)


            #트리뷰(학과 목록 둘러 쌀 트리뷰)
        self.list = QTreeView(self)
        self.list.setRootIsDecorated(False)
        self.list.setAlternatingRowColors(True)
        self.list.resize(500, 450)                #사이즈 설정
        self.list.move(350, 50)

            #학과 목록 리스트 헤더
        self.item_list = QStandardItemModel(0, 3, self)
        self.item_list.setHeaderData(0, Qt.Horizontal, "일련 번호")
        self.item_list.setHeaderData(1, Qt.Horizontal, "학과 번호")
        self.item_list.setHeaderData(2, Qt.Horizontal, "학 과 명")

        # self.item_list.set
            #학과 목록 테이블 클릭 이벤트 연결
        self.list.clicked.connect(self.item_select)         # 위치추적(나중에 연결)

            #학과 목록 리스트를 트리뷰 리스트에 추가
        self.list.setModel(self.item_list)



    #학과 등록 메서드
    def subject_insert(self):
        # 학과번호 수정창이나 학과명 수정 창에 아무것도 없다면
        if((self.edit_subject_num.text() != "") and (self.edit_subject_name.text() != "")):
            try:
                #sql에 입력할 명령어
                self.subject_insert_sql = "insert into subject(s_num, s_name) values('{}', '{}')"\
                                            .format(self.edit_subject_num.text(), self.edit_subject_name.text())
                print(self.subject_insert_sql)    #파이썬 화면에 명령어를 보여줌

                self.uni_cur.execute(self.subject_insert_sql)    #명령어를 커서를 이용하여 실행
                self.conn.commit()

            except:
                #형식을 잘못 입력하였을 경우 메세지 출력(메세지 박스를 통해)
                QMessageBox.information(self, "삽입 오류", "올바른 형식으로 입력하세요.",
                                        QMessageBox.Yes, QMessageBox.Yes)
                return

        self.subject_init()
        self.subjectlist(self)


    #학과 수정 메서드
    def subject_edit(self):
        # 학과번호 수정창이나 학과명 수정 창에 아무것도 없다면
        if ((self.edit_subject_num.text() != "") and (self.edit_subject_name.text() != "")):
            try:
                #sql에 입력할 명령어
                self.subject_update_sql = "update subject set s_num = '{}', s_name = '{}' where s_no = '{}'" \
                                            .format(self.edit_subject_num.text(), self.edit_subject_name.text(), self.edit_s_num.text())

                print(self.subject_update_sql)                #파이썬 화면에 명령어를 보여줌
                self.uni_cur.execute(self.subject_update_sql)  #커서를 통해 명령어 실행
                self.conn.commit()

            #오류가 났을 시에 실행
            except:
                QMessageBox.information(self, "삽입 오류", "올바른 형식으로 입력하세요.",
                                        QMessageBox.Yes, QMessageBox.Yes)
                self.subject_init()
                return


        else:
            QMessageBox.information(self, "입력 오류", "빈칸 없이 입력하세요.",
                                    QMessageBox.Yes, QMessageBox.Yes)
            self.subject_init()

            return

        QMessageBox.information(self, "수정 성공", "수정되었습니다.",
                                QMessageBox.Yes, QMessageBox.Yes)

        self.subject_init()
        self.subjectlist(self)


    #학과 삭제 메서드
    def subject_delete(self):
        #에딧창에 학과번호 텍스트가 있다면
        if (self.edit_s_num.text() != ""):
            try:
                #삭제를 누를 경우 확인 메세지 실행
                agree = QMessageBox.question(self, "삭제 확인", "정말로 삭제 하시겠습니까?",
                                             QMessageBox.Yes|QMessageBox.No, QMessageBox.No)
                if agree == QMessageBox.Yes:
                    #삭제 명령어
                    self.delete_sql = "delete from subject where s_no = '{}'".format(self.edit_s_num.text())
                    print(self.delete_sql) #파이썬 화면에 명령어 보여줌

                    self.uni_cur.execute(self.delete_sql)
                    self.conn.commit()

                    ## 오류 의심
                    self.subject_init()
                    self.subjectlist(self)

                    QMessageBox.information(self, "삭제 성공", "삭제 되었습니다.",
                                            QMessageBox.Yes, QMessageBox.Yes)

            except:
                QMessageBox.information(self, "삭제 오류", "잘못 선택된 학과입니다.",
                                        QMessageBox.Yes, QMessageBox.Yes)
                return

        else:
            QMessageBox.information(self, "삭제 오류", "학과 번호가 없습니다.",
                                    QMessageBox.Yes, QMessageBox.Yes)
            return



    #학과 테이블 목록 클릭 이벤트
    def item_select(self):

        #학과 테이블에서 오른쪽 보이는 학과 정보를 클릭했을 때 실행
        self.edit_s_num.setText(str(str(self.item_list.index(self.list.currentIndex().row(), 0).data())))
        self.edit_subject_num.setText(self.item_list.index(self.list.currentIndex().row(), 1).data())
        self.edit_subject_name.setText(str(self.item_list.index(self.list.currentIndex().row(), 2).data()))

        #오른쪽 학과 정보 클릭 했을시 -> 수정, 삭제버튼 활성화, 삽입버튼 비활성화
        self.btn_subject_delete.setDisabled(False)
        self.btn_subject_update.setDisabled(False)
        self.btn_subject_insert.setDisabled(True)


    # 학과 목록 등록 후 전체 목록 보여주기
    def subjectlist(self, QShowEvent):
        # sql에서 정보 가져오기 위한 셀렉트 명령어
        self.subject_totallist = "select * from subject"
        self.uni_cur.execute(self.subject_totallist)      #커서를 통해 불러온 정보(학과 정보)읽어옴
        self.conn.commit()

        rs = self.uni_cur.fetchall()     #행을 모두 뽑아냄

        self.item_list.removeRow(len(rs))


        #불러온 정보를 화면에 보여주기 위함
        for i in range(len(rs)):
            self.item_list.removeRow(i)
            self.item_list.insertRow(i)
            self.item_list.setData(self.item_list.index(i, 0), rs[i][0])
            self.item_list.setData(self.item_list.index(i, 1), rs[i][1])
            self.item_list.setData(self.item_list.index(i, 2), rs[i][2])

        #오류 의심(들여쓰기)
        self.edit_s_num.clear()
        self.edit_subject_num.clear()
        self.edit_subject_name.clear()
        # print('학과 등록 탭')


    # 학과 목록 클릭 이벤트
    def subject_select(self):
        self.edit_s_num.setText(str(self.item_list.index(self.list.currentIndex().row(), 0).data()))
        self.edit_subject_num.setText(str(self.item_list.index(self.list.currentIndex().row(), 1).data()))
        self.edit_subject_name.setText(str(self.item_list.index(self.list.currentIndex().row(), 2).data()))

        #학과 목록을 클릭하면 수정,삭제 버튼 비활성화
        self.btn_subject_update.setDisabled(True)
        self.btn_subject_delete.setDisabled(True)

    # 학과 등록 화면 초기화
    def subject_init(self):
        self.edit_s_num.clear()
        self.edit_subject_num.clear()
        self.edit_subject_name.clear()

        self.btn_subject_insert.setDisabled(False)
        self.btn_subject_update.setDisabled(True)
        self.btn_subject_delete.setDisabled(True)


# 학생 정보 등록 탭
class StudentTab(QWidget):
    def __init__(self):
        super().__init__()
        self.dbConnect()
        self.initUI()
        self.enterEvent(self)     #수정했음

    #db 연결
    def dbConnect(self):
        try:
            self.conn = pymysql.connect(
                host = "127.0.0.1",
                user = "manager",
                password = "manager",
                db = "universitydb",
                port = 3306,
                charset = "utf8"
                )
        except:
            print("문제가 있네요!")
            exit(1)

        print("연결 성공")

        self.uni_cur = self.conn.cursor()

    # 초기화면
    def initUI(self):

        self.lbl_student_register = QLabel('학생 등록', self)
        self.lbl_student_register.move(30, 25)

        self.btn_subjectName_load = QPushButton("학과명 로드", self)
        self.btn_subjectName_load.move(90, 20)
        self.btn_subjectName_load.clicked.connect(self.subjectName_load)

        self.lbl_sd_no = QLabel('일련번호 :', self)
        self.lbl_sd_no.move(30, 55)
        self.edit_sd_no = QLineEdit(self)
        self.edit_sd_no.move(90, 50)
        self.edit_sd_no.setDisabled(True)

        self.lbl_s_num = QLabel('학과명 : ', self)
        self.lbl_s_num.move(30, 85)

        # 학과 등록에서 등록된 학과명 불러오기(주의 : self를 사용하지 않는다.)
        self.subjectNamelist = []
        self.subjectNamecombo = QComboBox(self)
        self.subjectNamecombo.move(90, 80)
        self.subjectNamecombo.resize(85,20)
        self.subjectNamecombo.activated[str].connect(self.onActivated)

        self.subjectName = QLabel('학과명을 선택하세요', self)
        self.subjectName.move(190, 85)

        #학번을 보여줍니다.
        self.lbl_sd_num = QLabel('학 번 : ', self)
        self.lbl_sd_num.move(30, 115)
        self.edit_sd_num = QLineEdit(self)
        self.edit_sd_num.move(90, 110)
        self.edit_sd_num.setDisabled(True)

        #이름
        self.lbl_sd_name = QLabel('이 름 : ', self)
        self.lbl_sd_name.move(30, 145)
        self.edit_sd_name = QLineEdit(self)
        self.edit_sd_name.move(90, 140)

        #아이디
        self.lbl_sd_id = QLabel('아이디 : ', self)
        self.lbl_sd_id.move(30, 175)
        self.edit_sd_id = QLineEdit(self)
        self.edit_sd_id.move(90,170)

        #아이디 체크
        self.btn_id_check = QPushButton("아이디 체크", self)
        self.btn_id_check.move(245, 168)
        self.btn_id_check.clicked.connect(self.id_check)

        #비밀번호
        self.lbl_sd_passwd = QLabel('비밀번호 : ', self)
        self.lbl_sd_passwd.move(30, 205)
        self.edit_sd_passwd = QLineEdit(self)
        self.edit_sd_passwd.setEchoMode(QLineEdit.Password)     #에코모드를 통해 보안강화! -> 비밀번호 숨김
        self.edit_sd_passwd.move(90, 200)

        #비밀번호는 12자 이하로 받는다는 라벨 표시
        self.lbl_sd_pw = QLabel('12 자 이하', self)
        self.lbl_sd_pw.move(245, 205)

        #생년월일
        self.lbl_sd_birthday = QLabel('생년월일 : ', self)
        self.lbl_sd_birthday.move(30, 235)
        self.date_sd_birthday = QDateEdit(self)
        self.date_sd_birthday.setDate(QDate.currentDate())       #우선 현재 날짜로 표시(초기값)
        self.date_sd_birthday.move(90, 230)

        #연락처
        self.lbl_sd_phone = QLabel('연락처 : ',self)
        self.lbl_sd_phone.move(30, 265)
        self.edit_sd_phone = QLineEdit(self)
        self.edit_sd_phone.move(90, 260)

        #주소
        self.lbl_sd_address = QLabel('주 소 : ', self)
        self.lbl_sd_address.move(30, 295)
        self.edit_sd_address = QLineEdit(self)
        self.edit_sd_address.move(90, 290)

        #이메일
        self.lbl_sd_email = QLabel('이메일 : ', self)
        self.lbl_sd_email.move(30, 325)
        self.edit_sd_email = QLineEdit(self)
        self.edit_sd_email.move(90, 320)

        #등록 버튼
        self.btn_student_insert = QPushButton("등 록", self)
        self.btn_student_insert.move(30, 360)
        self.btn_student_insert.clicked.connect(self.student_insert)

        #수정 버튼
        self.btn_student_update = QPushButton("수 정", self)
        self.btn_student_update.move(110, 360)
        self.btn_student_update.clicked.connect(self.student_edit)

        #삭제 버튼
        self.btn_student_delete = QPushButton("삭 제", self)
        self.btn_student_delete.move(190, 360)
        self.btn_student_delete.clicked.connect(self.student_delete)

        #초기화 버튼
        self.btn_student_init = QPushButton("초기화", self)
        self.btn_student_init.move(110, 390)
        self.btn_student_init.clicked.connect(self.student_init)

        #버튼 비활성화 시킴
        self.btn_student_insert.setDisabled(True)
        self.btn_student_update.setDisabled(True)
        self.btn_student_delete.setDisabled(True)

        #학생 목록 라벨
        self.lbl_student = QLabel('학생 목록', self)
        self.lbl_student.move(350, 25)

        #트리뷰
        self.studentlist = QTreeView(self)
        self.studentlist.setRootIsDecorated(False)
        self.studentlist.setAlternatingRowColors(True)
        self.studentlist.resize(800, 450)
        self.studentlist.move(350, 50)

        #학생 목록 리스트 헤더
        self.student_item_list = QStandardItemModel(0, 11, self)
        self.student_item_list.setHeaderData(0, Qt.Horizontal, "일련 번호")
        self.student_item_list.setHeaderData(1, Qt.Horizontal, "학번")
        self.student_item_list.setHeaderData(2, Qt.Horizontal, "이름")
        self.student_item_list.setHeaderData(3, Qt.Horizontal, "아이디")
        self.student_item_list.setHeaderData(4, Qt.Horizontal, "비밀번호")
        self.student_item_list.setHeaderData(5, Qt.Horizontal, "학과번호")
        self.student_item_list.setHeaderData(6, Qt.Horizontal, "생년월일")
        self.student_item_list.setHeaderData(7, Qt.Horizontal, "핸드폰번호")
        self.student_item_list.setHeaderData(8, Qt.Horizontal, "주소")
        self.student_item_list.setHeaderData(9, Qt.Horizontal, "이메일")
        self.student_item_list.setHeaderData(10, Qt.Horizontal, "등록일")

        #학생 목록 테이블 클릭 이벤트 연결
        self.studentlist.clicked.connect(self.item_select)

        #학생 목록 리스트를 트리뷰 리스트에 추가
        self.studentlist.setModel(self.student_item_list)

    #학과 테이블에서 학과명 불러오기
    def subjectName_load(self):
        subjectNamelist = self.subject_nameList()
        self.subjectNamecombo.clear()

        for i in range(len(subjectNamelist)):
            s_name = subjectNamelist[i]
            self.subjectNamecombo.addItem(s_name[0])

            self.btn_subjectName_load.setDisabled(True)
            self.btn_student_insert.setDisabled(False)

    #학생 등록
    def student_insert(self):
        if ((self.edit_sd_num.text() != "") and (self.edit_sd_name.text() != "") and (self.edit_sd_id.text() != "") and (self.edit_sd_passwd.text() != "")
            and (self.edit_sd_phone.text() != "") and (self.edit_sd_address.text() != "") and (self.edit_sd_email.text() != "")):

            try:
                print('하하')
                self.subject_list = "select s_num from subject where s_name = '{}'".format(self.subjectName.text())
                print(self.subject_list)
                self.uni_cur.execute(self.subject_list)
                self.conn.commit()
                s_num = self.uni_cur.fetchone()      #학과 이름을 통해 학과 일련번호(s_num)을 읽어와서 s_num에 할당한다.

                # (학번, 이름, 아이디, 비밀번호, 학과번호, 생년월일, 핸드폰 번호, 주소, 이메일)
                self.student_insert_sql = "insert into student(sd_num, sd_name, sd_id, sd_passwd, s_num, sd_birthday, sd_phone, sd_address, sd_email) values('{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}')"\
                 .format(self.edit_sd_num.text(), self.edit_sd_name.text(), self.edit_sd_id.text(), self.edit_sd_passwd.text(), s_num[0], self.date_sd_birthday.text(), self.edit_sd_phone.text(), self.edit_sd_address.text(), self.edit_sd_email.text())

                print(self.student_insert_sql)   #명령어를 파이썬에 보여준다.
                self.uni_cur.execute(self.student_insert_sql)
                self.conn.commit()
            except:
                QMessageBox.information(self, "삽입 오류", "올바른 형식으로 입력하세요.",
                                        QMessageBox.Yes, QMessageBox.Yes)
                return

        else:
            QMessageBox.information(self, "입력 오류", "빈칸 없이 입력하세요.",
                                    QMessageBox.Yes, QMessageBox.Yes)
            return

        self.student_init()
        # self.studentlist(self)              #없앴음(변경)
        self.enterEvent(self)  #수정했음(변경)

    #학생 정보 수정
    def student_edit(self):
        if ((self.edit_sd_passwd.text() != "") and (self.edit_sd_phone.text() != "") and (self.edit_sd_address.text() != "") and (self.edit_sd_email.text() != "")):
            try:

                self.edit_date = self.date_sd_birthday.text()
                self.student_update_sql = "update student set sd_passwd = '{}', sd_birthday = '{}' ,sd_phone = '{}', sd_address = '{}', sd_email = '{}' where sd_no = '{}'"\
                                            .format(self.edit_sd_passwd.text(),self.edit_date , self.edit_sd_phone.text(), self.edit_sd_address.text(), self.edit_sd_email.text(), self.edit_sd_no.text())
                print(self.student_update_sql)   #명령어를 파이썬에 보여줌
                self.uni_cur.execute(self.student_update_sql)
                self.conn.commit()

            except:
                QMessageBox.information(self, "삽입 오류", "올바른 형식으로 입력하세요.",
                                        QMessageBox.Yes, QMessageBox.Yes)
                self.student_init()
                return

        else:
            QMessageBox.information(self, "입력 오류", "빈칸 없이 입력하세요.",
                                    QMessageBox.Yes, QMessageBox.Yes)
            self.student_init()
            return

        QMessageBox.information(self, "수정 성공", "수정되었습니다.",
                                QMessageBox.Yes, QMessageBox.Yes)

        self.student_init()
        # self.studentlist(self)            #없앴음 (변경)
        self.enterEvent(self)

    #학생 정보 삭제
    def student_delete(self):
        if (self.edit_sd_no.text() != ""):
            try:
                agree = QMessageBox.question(self, "삭제 확인", "정말로 삭제 하시겠습니까?",
                                             QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
                if agree == QMessageBox.Yes:
                    self.student_delete_sql = "delete from student where sd_no = '{}'".format(self.edit_sd_no.text())
                    print(self.student_delete_sql) #명령어를 파이썬에 보여줌
                    self.uni_cur.execute(self.student_delete_sql) #커서를 통해 명령어 실행
                    self.conn.commit()

                    self.student_init()
                    self.enterEvent(self)  #없앴음 변경 ->studentlist -> enterevent
                else:
                    # QMessageBox.information(self, "취소 메시지", "취소되었습니다.",
                    #                         QMessageBox.Yes, QMessageBox.Yes)
                    return

            except:
                QMessageBox.information(self, "삭제 오류", "해당 학생의 수강신청을 취소한 후 삭제해 주세요.",
                                        QMessageBox.Yes, QMessageBox.Yes)
                return

        else:
            QMessageBox.information(self, "삭제 오류", "회원 번호가 없습니다.",
                                    QMessageBox.Yes, QMessageBox.Yes)
            return

        QMessageBox.information(self, "삭제 성공", "삭제되었습니다.",
                                QMessageBox.Yes, QMessageBox.Yes)

    #학생 목록 테이블 클릭 이벤트
    def item_select(self):
        self.edit_sd_no.setText(str(self.student_item_list.index(self.studentlist.currentIndex().row(), 0).data()))
        self.edit_sd_num.setText(str(self.student_item_list.index(self.studentlist.currentIndex().row(), 1).data()))
        self.edit_sd_name.setText(str(self.student_item_list.index(self.studentlist.currentIndex().row(), 2).data()))
        self.edit_sd_id.setText(str(self.student_item_list.index(self.studentlist.currentIndex().row(), 3).data()))
        self.edit_sd_id.setDisabled(True)      #학생 id버튼 비활성화
        self.edit_sd_passwd.setText(str(self.student_item_list.index(self.studentlist.currentIndex().row(), 4).data()))


        date = self.student_item_list.index(self.studentlist.currentIndex().row(), 6).data()
        q_date = QDate.fromString(date, "yyyy-MM-dd")
        self.date_sd_birthday.setDate(q_date)
        # self.date_sd_birthday.setDate(QDate.currentDate())

        self.edit_sd_phone.setText(str(self.student_item_list.index(self.studentlist.currentIndex().row(), 7).data()))
        self.edit_sd_address.setText(str(self.student_item_list.index(self.studentlist.currentIndex().row(), 8).data()))
        self.edit_sd_email.setText(str(self.student_item_list.index(self.studentlist.currentIndex().row(), 9).data()))

        self.edit_sd_name.setDisabled(True)   #학생 이름 비활성화
        self.btn_id_check.setDisabled(True)   #id체크 버튼 비활성화
        self.btn_subjectName_load.setDisabled(True) #학과이름 로드 비활성화
        self.btn_student_update.setDisabled(False)   #학생 업데이트 활성화
        self.btn_student_delete.setDisabled(False)   #학생 삭제 활성화
        self.btn_student_insert.setDisabled(True)    #학생 삽입 비활성화


    # 학생 목록 등록 후 전체 목록 보여주기
    def studentlist(self, QShowEvent):                      #수정했음.
        self.student_totallist = "select * from student"    #학생 정보를 보여주기 위한 명령어
        self.uni_cur.execute(self.student_totallist)
        self.conn.commit()
        rs = self.uni_cur.fetchall()

        self.student_item_list.removeRow(len(rs))

        for i in range(len(rs)):
            self.student_item_list.removeRow(i)
            self.student_item_list.insertRow(i)
            self.student_item_list.setData(self.student_item_list.index(i, 0), rs[i][0])
            self.student_item_list.setData(self.student_item_list.index(i, 1), rs[i][1])
            self.student_item_list.setData(self.student_item_list.index(i, 2), rs[i][2])
            self.student_item_list.setData(self.student_item_list.index(i, 3), rs[i][3])
            self.student_item_list.setData(self.student_item_list.index(i, 4), rs[i][4])
            self.student_item_list.setData(self.student_item_list.index(i, 5), rs[i][5])
            self.student_item_list.setData(self.student_item_list.index(i, 6), rs[i][6])
            self.student_item_list.setData(self.student_item_list.index(i, 7), rs[i][7])
            self.student_item_list.setData(self.student_item_list.index(i, 8), rs[i][8])
            self.student_item_list.setData(self.student_item_list.index(i, 9), rs[i][9])
            self.student_item_list.setData(self.student_item_list.index(i, 10), rs[i][10])

    #학생 목록 테이블에 마우스가 들어오면 발생하는 이벤트 : 학생 목록 다시 보여주기
    def enterEvent(self, QShowEvent):
        self.student_list = "select * from student"
        self.uni_cur.execute(self.student_list)
        self.conn.commit()
        rs = self.uni_cur.fetchall()    #결과는 튜플이다.

        self.student_item_list.removeRow(len(rs))

        for i in range(len(rs)):
            self.student_item_list.removeRow(i)
            self.student_item_list.insertRow(i)
            self.student_item_list.setData(self.student_item_list.index(i, 0), rs[i][0])
            self.student_item_list.setData(self.student_item_list.index(i, 1), rs[i][1])
            self.student_item_list.setData(self.student_item_list.index(i, 2), rs[i][2])
            self.student_item_list.setData(self.student_item_list.index(i, 3), rs[i][3])
            self.student_item_list.setData(self.student_item_list.index(i, 4), rs[i][4])
            self.student_item_list.setData(self.student_item_list.index(i, 5), rs[i][5])
            self.student_item_list.setData(self.student_item_list.index(i, 6), rs[i][6])
            self.student_item_list.setData(self.student_item_list.index(i, 7), rs[i][7])
            self.student_item_list.setData(self.student_item_list.index(i, 8), rs[i][8])
            self.student_item_list.setData(self.student_item_list.index(i, 9), rs[i][9])
            self.student_item_list.setData(self.student_item_list.index(i, 10), str(rs[i][10])) # 날짜를 문자열로 변경

    # 초기화 버튼 이벤트 핸들러
    def student_init(self):
        self.edit_sd_no.clear()
        self.subjectName.setText('학과명을 선택하세요')
        self.edit_sd_num.clear()
        self.edit_sd_name.clear()
        self.edit_sd_name.setDisabled(False)   #학생이름 활성화
        self.edit_sd_id.clear()
        self.edit_sd_id.setDisabled(False)
        self.edit_sd_passwd.clear()
        self.date_sd_birthday.setDate(QDate.currentDate())
        self.edit_sd_phone.clear()
        self.edit_sd_address.clear()
        self.edit_sd_email.clear()

        self.btn_id_check.setDisabled(False) #아이디 체크버튼 활성화
        self.btn_subjectName_load.setDisabled(False) #학과명 로드 활성화
        self.btn_student_insert.setDisabled(False)   #학생 등록 활성화
        self.btn_student_update.setDisabled(True)    #학생 업데이트 버튼 비활성화
        self.btn_student_delete.setDisabled(True)    #학생 삭제 버튼 비활성화

    # 아이디 체크 이벤트 핸들러
    def id_check(self):
        if (self.edit_sd_id.text() != ""):
            try:
                self.id_checksql = "select sd_id from student where sd_id = '{}'".format(self.edit_sd_id.text())
                print(self.id_checksql)   #명령어를 파이썬에 보여줌
                self.uni_cur.execute(self.id_checksql)
                rs = self.uni_cur.fetchone()
                print(rs)

                if (rs == None):
                    # self.edit_sd_id.setDisabled(True)                    #비활성화 기능 없앴음. (수정)
                    QMessageBox.information(self, "아이디 체크 성공", "사용할 수 있는 아이디 입니다.",
                                            QMessageBox.Yes, QMessageBox.Yes)
                else:
                    self.edit_sd_id.clear()
                    QMessageBox.information(self, "아이디 체크 성공", "사용할 수 없는 아이디 입니다.",
                                            QMessageBox.Yes, QMessageBox.Yes)

            except:
                QMessageBox.information(self, "아이디 체크 오류", "아이디를 잘못 입력하였습니다.",
                                        QMessageBox.Yes, QMessageBox.Yes)
                return

        else:
            QMessageBox.information(self, "아이디 체크 오류", "아이디를 입력하세요.",
                                    QMessageBox.Yes, QMessageBox.Yes)
            return


    # 학과명 선택 이벤트 핸들러
    def onActivated(self, text):
        self.subjectName.setText(text)
        self.sd_num_create(self.subjectName.text())

    # 학번 생성
    def sd_num_create(self, s_name):
        #학번 생성(연도 2자리 + 학과 2자리 + 일련번호 - 예로 06010001)
        self.subject_num = "select s_num from subject where s_name = '{}'".format(self.subjectName.text())
        self.uni_cur.execute(self.subject_num)
        self.conn.commit()
        s_num = self.uni_cur.fetchone() #결과가 튜플이므로 s_num[0]으로 값을 선택함

        self.student_sd_no = "select max(sd_no) from student"
        self.uni_cur.execute(self.student_sd_no)
        self.conn.commit()
        sd_no = self.uni_cur.fetchone()
        sd_no = list(sd_no)
        print(sd_no)

        # 연도의 뒤 두자리
        now = QDate.currentDate()
        year = now.toString('yy')

        #최초 등록 학생의 학번 일련번호 생성
        if (sd_no[0] == None):
            sd_no[0] = 1

            sd_num = str(year) + str(s_num[0]) + str(sd_no[0]).zfill(4) # 학번 일련번호 4자리중 빈공간을 0으로 채움
            self.edit_sd_num.setText(sd_num)

        else:
            sd_num = str(year) + str(s_num[0]) + str(sd_no[0]+1).zfill(4)  # 학번 일련번호 4자리중 빈공간을 0으로 채움
            self.edit_sd_num.setText(sd_num)


    #학과명을 불러오는 이벤트 핸들러
    def subject_nameList(self):
        self.subject_namesql = "select s_name from subject order by s_no"
        self.uni_cur.execute(self.subject_namesql)
        self.conn.commit()
        rs = self.uni_cur.fetchall()

        subject_name = []
        subject_name = rs
        return subject_name




# 과목 등록(탭) 클래스 만들기
class LessonTab(QWidget):
    def __init__(self):
        super().__init__()
        self.dbConnect()
        self.initUI()
        self.lessonlist(self)

    #DB 연결하기
    def dbConnect(self):
        try:
            self.conn = pymysql.connect(
                host = "127.0.0.1",
                user = "manager",
                password = "manager",
                db = "universitydb",
                port = 3306,
                charset = "utf8"
                )

        except:
            print("문제가 있네요!")
            exit(1)

        print("연결 성공")

        self.uni_cur = self.conn.cursor()


    def initUI(self):
        self.lbl_lesson_register = QLabel('과목 등록', self)
        self.lbl_lesson_register.move(30, 25)


        #과목 일련번호
        self.lbl_lesson_no = QLabel('일련 번호 :', self)
        self.lbl_lesson_no.move(50, 55)
        self.edit_lesson_no = QLineEdit(self)
        self.edit_lesson_no.move(120, 50)
        self.edit_lesson_no.setDisabled(True)
        # self.edit_lesson_no.setReadOnly(True)   #바꿨음(선택 못하는 걸로)

        #과목 번호
        self.lbl_lesson_num = QLabel('과목 번호 :', self)
        self.lbl_lesson_num.move(50, 85)            #y값 +40
        self.edit_lesson_num = QLineEdit(self)
        self.edit_lesson_num.move(120, 80)


        # 과목 명
        self.lbl_lesson_name = QLabel('과목 명 :', self)
        self.lbl_lesson_name.move(50, 115)  # y값 +30
        self.edit_lesson_name = QLineEdit(self)
        self.edit_lesson_name.move(120, 110)

        # 등록 버튼
        self.btn_lesson_insert = QPushButton("등 록", self)
        self.btn_lesson_insert.move(50, 150)
        self.btn_lesson_insert.clicked.connect(self.lesson_insert)

        #수정 버튼
        self.btn_lesson_update = QPushButton("수 정", self)
        self.btn_lesson_update.move(130, 150)
        self.btn_lesson_update.clicked.connect(self.lesson_edit)

        #삭제 버튼
        self.btn_lesson_delete = QPushButton("삭 제", self)
        self.btn_lesson_delete.move(210, 150)
        self.btn_lesson_delete.clicked.connect(self.lesson_delete)

        # 초기화 버튼
        self.btn_lesson_init = QPushButton("초기화", self)
        self.btn_lesson_init.move(130, 180)
        self.btn_lesson_init.clicked.connect(self.lesson_init)

        #수정버튼과 삭제버튼은 초기에 비활성화 시켜놓음
        self.btn_lesson_update.setDisabled(True)
        self.btn_lesson_delete.setDisabled(True)


        #학과 목록 라벨
        self.lbl_lesson_num = QLabel('과목 목록', self)
        self.lbl_lesson_num.move(350, 25)

        # 트리뷰(과목 목록 둘러 쌀 트리뷰)
        self.list = QTreeView(self)
        self.list.setRootIsDecorated(False)
        self.list.setAlternatingRowColors(True)
        self.list.resize(380, 450)  # 사이즈 설정
        self.list.move(350, 50)

        # 과목 목록 리스트 헤더
        self.item_list = QStandardItemModel(0, 3, self)
        self.item_list.setHeaderData(0, Qt.Horizontal, "일련 번호")
        self.item_list.setHeaderData(1, Qt.Horizontal, "과목 번호")
        self.item_list.setHeaderData(2, Qt.Horizontal, "과목명")

        #과목 테이블 클릭 이벤트 연결
        self.list.clicked.connect(self.item_select)         # 위치추적(나중에 연결)

        #학과 목록 리스트를 트리뷰 리스트에 추가
        self.list.setModel(self.item_list)

    # 과목 등록 메서드
    def lesson_insert(self):
        # 과목 수정이나 학과명 수정 창에 아무것도 없다면
        if ((self.edit_lesson_num.text() != "") and (self.edit_lesson_name.text() != "")):
            try:
                # sql에 입력할 명령어
                self.lesson_insert_sql = "insert into lesson(l_num, l_name) values('{}', '{}')" \
                    .format(self.edit_lesson_num.text(), self.edit_lesson_name.text())
                print(self.lesson_insert_sql)  # 파이썬 화면에 명령어를 보여줌

                self.uni_cur.execute(self.lesson_insert_sql)  # 명령어를 커서를 이용하여 실행
                self.conn.commit()

            except:
                #형식을 잘못 입력하였을 경우 메세지 출력(메세지 박스를 통해)
                QMessageBox.information(self, "삽입 오류", "올바른 형식으로 입력하세요.",
                                        QMessageBox.Yes, QMessageBox.Yes)
                return

        self.lesson_init()
        self.lessonlist(self)

    # 과목 수정 메서드
    def lesson_edit(self):
        # 과목번호 수정창이나 과목명 수정 창에 아무것도 없다면
        if ((self.edit_lesson_num.text() != "") and (self.edit_lesson_name.text() != "")):
            try:
                # sql에 입력할 명령어
                self.lesson_update_sql = "update lesson set l_num = '{}', l_name = '{}' where l_no = '{}'" \
                    .format(self.edit_lesson_num.text(), self.edit_lesson_name.text(), self.edit_lesson_no.text())

                print(self.lesson_update_sql)  # 파이썬 화면에 명령어를 보여줌
                self.uni_cur.execute(self.lesson_update_sql)  # 커서를 통해 명령어 실행
                self.conn.commit()

            except:
                QMessageBox.information(self, "삽입 오류", "올바른 형식으로 입력하세요.",
                                        QMessageBox.Yes, QMessageBox.Yes)
                self.subject_init()
                return

        else:
            QMessageBox.information(self, "입력 오류", "빈칸 없이 입력하세요.",
                                    QMessageBox.Yes, QMessageBox.Yes)
            self.lesson_init()

            return

        QMessageBox.information(self, "수정 성공", "수정되었습니다.",
                                QMessageBox.Yes, QMessageBox.Yes)

        self.lesson_init()
        self.lessonlist(self)

    # 과목 삭제 메서드
    def lesson_delete(self):
        # 에딧창에 과목번호 텍스트가 있다면
        if (self.edit_lesson_num.text() != ""):
            try:
                # 삭제를 누를 경우 확인 메세지 실행
                agree = QMessageBox.question(self, "삭제 확인", "정말로 삭제 하시겠습니까?",
                                             QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
                if agree == QMessageBox.Yes:
                    # 삭제 명령어
                    self.delete_sql = "delete from lesson where l_no = '{}'".format(self.edit_lesson_no.text())
                    print(self.delete_sql)  # 파이썬 화면에 명령어 보여줌

                    self.uni_cur.execute(self.delete_sql)
                    self.conn.commit()

                    ## 오류 의심
                    self.lesson_init()
                    self.lessonlist(self)

                    QMessageBox.information(self, "삭제 성공", "삭제 되었습니다.",
                                            QMessageBox.Yes, QMessageBox.Yes)

            except:
                QMessageBox.information(self, "삭제 오류", "잘못 선택된 과목입니다.",
                                        QMessageBox.Yes, QMessageBox.Yes)
                return

        else:
            QMessageBox.information(self, "삭제 오류", "과목 번호가 없습니다.",
                                    QMessageBox.Yes, QMessageBox.Yes)
            return

    # 과목 테이블 목록 클릭 이벤트
    def item_select(self):

        # 과목 테이블에서 오른쪽 보이는 과목 정보를 클릭했을 때 실행
        self.edit_lesson_no.setText(str(str(self.item_list.index(self.list.currentIndex().row(), 0).data())))
        self.edit_lesson_num.setText(self.item_list.index(self.list.currentIndex().row(), 1).data())
        self.edit_lesson_name.setText(str(self.item_list.index(self.list.currentIndex().row(), 2).data()))

        # 오른쪽 학과 정보 클릭 했을시 -> 수정, 삭제버튼 활성화, 삽입버튼 비활성화
        self.btn_lesson_delete.setDisabled(False)   #삭제 활성화
        self.btn_lesson_update.setDisabled(False)   #수정 활성화
        self.btn_lesson_insert.setDisabled(True)    #입력 비활성화


    # 과목 목록 등록 후 전체 목록 보여주기
    def lessonlist(self, QShowEvent):
        # sql에서 정보 가져오기 위한 셀렉트 명령어
        self.lesson_totallist = "select * from lesson"
        self.uni_cur.execute(self.lesson_totallist)      #커서를 통해 불러온 정보(과목 정보)읽어옴
        self.conn.commit()

        rs = self.uni_cur.fetchall()     #행을 모두 뽑아냄

        self.item_list.removeRow(len(rs))

        #불러온 정보를 화면에 보여주기 위함
        for i in range(len(rs)):
            self.item_list.removeRow(i)
            self.item_list.insertRow(i)
            self.item_list.setData(self.item_list.index(i, 0), rs[i][0])
            self.item_list.setData(self.item_list.index(i, 1), rs[i][1])
            self.item_list.setData(self.item_list.index(i, 2), rs[i][2])

        #오류 의심(들여쓰기)
        self.edit_lesson_no.clear()
        self.edit_lesson_num.clear()
        self.edit_lesson_name.clear()

    # 과목 목록 클릭 이벤트
    def lesson_select(self):
        self.edit_lesson_no.setText(str(self.item_list.index(self.list.currentIndex().row(), 0).data()))
        self.edit_lesson_num.setText(str(self.item_list.index(self.list.currentIndex().row(), 1).data()))
        self.edit_lesson_name.setText(str(self.item_list.index(self.list.currentIndex().row(), 2).data()))

        # 과목 목록을 클릭하면 수정,삭제 버튼 비활성화
        self.btn_lesson_update.setDisabled(True)
        self.btn_lesson_delete.setDisabled(True)

    # 학과 등록 화면 초기화
    def lesson_init(self):
        self.edit_lesson_no.clear()
        self.edit_lesson_num.clear()
        self.edit_lesson_name.clear()

        self.btn_lesson_insert.setDisabled(False)   # 과목삽입 활성화
        self.btn_lesson_update.setDisabled(True)    # 과목수정 비활성화
        self.btn_lesson_delete.setDisabled(True)    # 과목삭제 비활성화



    # 수강 신청(탭) 클래스 만들기
class TraineeTab(QWidget):
    def __init__(self):
        super().__init__()
        self.dbConnect()
        self.initUI()
        #시작하자마자 트리뷰 보여줌
        self.traineeList(self)
        #시작 하자마자 전공 콤보박스 선택하게 해놓음
        # self.section_select1()


    # db 연결하는 메서드
    def dbConnect(self):
        try:
            self.conn = pymysql.connect(
                host="127.0.0.1",
                user="manager",
                password="manager",
                db="universitydb",
                port=3306,
                charset="utf8"
            )
        except:
            print("문제가 있네요!")
            exit(1)

        print("연결 성공!")

        self.uni_cur = self.conn.cursor()

    #초기 화면
    def initUI(self):

        self.lbl_trainee_register = QLabel('수강 신청', self)  # 학과 등록 라벨 생성
        self.lbl_trainee_register.move(30, 25)  # 라벨 위치설정

        # 학번검색
        self.lbl_trainee_search = QLabel('학번 검색 :', self)
        self.lbl_trainee_search.move(470, 25)
        self.edit_trainee_search = QLineEdit(self)
        self.edit_trainee_search.move(540, 22)

        # 검색버튼
        self.btn_search = QPushButton("검색", self)
        self.btn_search.move(694,21)
        self.edit_trainee_search.text()
        self.btn_search.clicked.connect(self.onChanged)


        # 일련번호 라벨
        self.lbl_t_no = QLabel('일련 번호 :', self)
        self.lbl_t_no.move(50, 55)
        self.edit_t_no = QLineEdit(self)
        self.edit_t_no.move(120, 50)
        self.edit_t_no.setDisabled(True)


        # 학번 라벨(참조)
        self.lbl_sd_num = QLabel('학 번 :', self)
        self.lbl_sd_num.move(50, 85)
        self.edit_sd_num = QLineEdit(self)
        self.edit_sd_num.move(120, 80)

        #학번 체크
        self.btn_sd_num_check = QPushButton("학번 체크", self)
        self.btn_sd_num_check.move(275, 78)
        self.btn_sd_num_check.clicked.connect(self.sd_num_check)


        #학과 명 라벨
        self.lbl_subject_name = QLabel('학과 명 :', self)
        self.lbl_subject_name.move(50, 115)
        self.edit_subject_name = QLineEdit(self)
        self.edit_subject_name.move(120 ,110)
        self.edit_subject_name.setReadOnly(True)

        #과목 번호 라벨(참조)
        self.lbl_l_num = QLabel('과목 번호 :', self)
        self.lbl_l_num.move(50, 145)
        self.edit_l_num = QLineEdit(self)
        self.edit_l_num.setReadOnly(True)
        self.edit_l_num.move(120 ,140)

        #과목 구분 라벨
        self.lbl_t_section = QLabel('과목 구분 :', self)
        self.lbl_t_section.move(50, 175)
        self.edit_t_section = QLineEdit(self)
        self.edit_t_section.setReadOnly(True)
        self.edit_t_section.move(120 ,170)


        #전공, 교양을 선택할 라디오박스
        self.rbtn1 = QRadioButton('전공', self)
        self.rbtn1.move(50, 200)
        # self.rbtn1.setChecked(True)
        self.rbtn1.clicked.connect(self.section_select1)


        self.rbtn2 = QRadioButton(self)
        self.rbtn2.move(50, 225)
        self.rbtn2.setText('교양')
        self.rbtn2.clicked.connect(self.section_select2)

        #과목 선택할 콤보박스
        self.cb = QComboBox(self)
        lessonNameList = self.lesson_nameList()
        self.cb.clear()

        for i in range(len(lessonNameList)):
            l_name = lessonNameList[i]
            self.cb.addItem(l_name[0])


        self.cb.resize(100,20)
        self.cb.move(130, 210)

        # 콤보박스 옆 비어있을 때의 라벨
        # self.text_lbl = QLabel('비어있습니다', self)
        # self.text_lbl.move(245, 214)

        self.cb.activated[str].connect(self.onActivated)

        #신청 버튼
        self.btn_trainee_insert = QPushButton("신 청", self)
        self.btn_trainee_insert.move(50, 250)
        self.btn_trainee_insert.clicked.connect(self.trainee_insert)    #클릭하면 subject_insert 메서드 실행

        #수정 버튼
        self.btn_trainee_update = QPushButton("수 정", self)
        self.btn_trainee_update.move(130, 250)
        self.btn_trainee_update.clicked.connect(self.trainee_edit)      #클릭하면 subject_edit 메서드 실행

        #삭제 버튼
        self.btn_trainee_delete = QPushButton("취 소", self)
        self.btn_trainee_delete.move(210, 250)
        self.btn_trainee_delete.clicked.connect(self.trainee_delete)        #클릭하면 subject_edlete 메서드 실행

        #초기화 버튼
        self.btn_trainee_init = QPushButton("초기화", self)
        self.btn_trainee_init.move(130, 280)
        self.btn_trainee_init.clicked.connect(self.trainee_init)        #클릭하면 subject_init 메서드 실행
        self.btn_trainee_init.clicked.connect(self.abc)

        #업데이트와 취소 버튼은 초기에 비활성화 시켜놓음
        self.btn_trainee_update.setDisabled(True)
        self.btn_trainee_delete.setDisabled(True)

        #수강신청 목록 라벨
        self.lbl_trainee_list = QLabel('수강신청 목록', self)
        self.lbl_trainee_list.move(990, 25)

        # # 과목 목록 보여 줄 트리뷰(수강 신청 하기 위해서)
        # self.lesson_list = QTreeView(self)
        # self.lesson_list.setRootIsDecorated(False)
        # self.lesson_list.setAlternatingRowColors(True)
        # self.lesson_list.resize(200,450)
        # self.lesson_list.move(400, 50)

        # 트리뷰(수강신청 목록 둘러 쌀 트리뷰)
        self.list = QTreeView(self)
        self.list.setRootIsDecorated(False)
        self.list.setAlternatingRowColors(True)
        self.list.resize(700, 450)  # 사이즈 설정
        self.list.move(400, 50)

        #수강신청 목록 리스트 헤더
        self.item_list = QStandardItemModel(0, 6, self)             #총 6개
        self.item_list.setHeaderData(0, Qt.Horizontal, "일련 번호")
        self.item_list.setHeaderData(1, Qt.Horizontal, "학번")
        self.item_list.setHeaderData(2, Qt.Horizontal, "과목 명")
        self.item_list.setHeaderData(3, Qt.Horizontal, "과목 번호")
        self.item_list.setHeaderData(4, Qt.Horizontal, "과목 구분")
        self.item_list.setHeaderData(5, Qt.Horizontal, "신청일")



        #학과 목록 테이블 클릭 이벤트 연결
        self.list.clicked.connect(self.item_select)         # 위치추적(나중에 연결)

        #학과 목록 리스트를 트리뷰 리스트에 추가
        self.list.setModel(self.item_list)

    # 수강 신청
    def trainee_insert(self):
        if ((self.edit_sd_num.text() != "") and (self.edit_l_num.text() != "") and (self.edit_t_section.text() != "")):
            # if self.edit_sd_num.text()

            self.overlap_sql = "select l_num from trainee where sd_num = '{}'".format(self.edit_sd_num.text())
            print(self.overlap_sql)  # 명령어를 파이썬에 보여줌
            self.uni_cur.execute(self.overlap_sql)
            ov = self.uni_cur.fetchall()
            self.conn.commit()
            print(ov)
            self.lesson_list = []
            for i in range(len(ov)):
                self.lesson_list.append(ov[i][0])

            if self.edit_l_num.text() not in self.lesson_list:

                try:
                    #sql에 입력할 명령어
                    self.trainee_insert_sql = "insert into trainee(sd_num, l_num, t_section) values('{}', '{}', '{}')"\
                                                .format(self.edit_sd_num.text(), self.edit_l_num.text(), self.edit_t_section.text())
                    print(self.trainee_insert_sql)    #파이썬 화면에 명령어를 보여줌

                    self.uni_cur.execute(self.trainee_insert_sql)    #명령어를 커서를 이용하여 실행
                    self.conn.commit()

                    QMessageBox.information(self, "등록 완료", "수강신청 완료",
                                            QMessageBox.Yes, QMessageBox.Yes)


                except:
                    QMessageBox.information(self, "삽입 오류", "올바른 형식으로 입력하세요.",
                                            QMessageBox.Yes, QMessageBox.Yes)
                    return

            else:
                QMessageBox.information(self, "신청 오류", "이미 수강 신청 목록에 존재합니다.",
                                        QMessageBox.Yes, QMessageBox.Yes)
                # self.trainee_init()

                self.edit_l_num.clear()
                self.edit_t_section.clear()

                return

        else:
            QMessageBox.information(self, "입력 오류", "빈칸 없이 입력하세요.",
                                    QMessageBox.Yes, QMessageBox.Yes)
            return

        self.trainee_init()       #입력창 초기화
        self.traineeList(self)    #트리뷰 보여주기


    # 수강신청 수정
    def trainee_edit(self):

        if ((self.edit_sd_num.text() != "") and (self.edit_l_num.text() != "") and (self.edit_t_section.text() != "")):
            self.overlap_sql = "select l_num from trainee where sd_num = '{}'".format(self.edit_sd_num.text())
            print(self.overlap_sql)  # 명령어를 파이썬에 보여줌
            self.uni_cur.execute(self.overlap_sql)
            ov = self.uni_cur.fetchall()
            self.conn.commit()
            print(ov)
            self.lesson_list = []
            for i in range(len(ov)):
                self.lesson_list.append(ov[i][0])

            if self.edit_l_num.text() not in self.lesson_list:

                try:
                    self.trainee_update_sql = "update trainee set sd_num = '{}', l_num = '{}', t_section = '{}' where t_no = '{}'"\
                                                .format(self.edit_sd_num.text(), self.edit_l_num.text(), self.edit_t_section.text(), self.edit_t_no.text())
                    print(self.trainee_update_sql)   #명령어를 파이썬에 보여줌
                    self.uni_cur.execute(self.trainee_update_sql)
                    self.conn.commit()

                except:
                    QMessageBox.information(self, "삽입 오류", "올바른 형식으로 입력하세요.",
                                            QMessageBox.Yes, QMessageBox.Yes)
                    self.trainee_init()
                    return

            else:
                QMessageBox.information(self, "신청 오류", "이미 수강 신청 목록에 존재합니다.",
                                        QMessageBox.Yes, QMessageBox.Yes)
                return

        else:
            QMessageBox.information(self, "입력 오류", "빈칸 없이 입력하세요.",
                                    QMessageBox.Yes, QMessageBox.Yes)
            self.trainee_init()
            return

            QMessageBox.information(self, "수정 성공", "수정되었습니다.",
                                    QMessageBox.Yes, QMessageBox.Yes)

        self.trainee_init()
        self.traineeList(self)


    #학생 정보 삭제
    def trainee_delete(self):
        if (self.edit_t_no.text() != ""):
            try:
                agree = QMessageBox.question(self, "삭제 확인", "정말로 삭제 하시겠습니까?",
                                             QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
                if agree == QMessageBox.Yes:
                    self.trainee_delete_sql = "delete from trainee where t_no = '{}'".format(self.edit_t_no.text())
                    print(self.trainee_delete_sql) #명령어를 파이썬에 보여줌
                    self.uni_cur.execute(self.trainee_delete_sql) #커서를 통해 명령어 실행
                    self.conn.commit()

                    self.trainee_init()
                    self.traineeList(self)
                    QMessageBox.information(self, "삭제 성공", "수강을 취소하였습니다.",
                                            QMessageBox.Yes, QMessageBox.Yes)

            except:
                QMessageBox.information(self, "삭제 오류", "잘못 선택된 강의입니다.",
                                        QMessageBox.Yes, QMessageBox.Yes)
                return

        else:
            QMessageBox.information(self, "삭제 오류", "수강신청 내역이 없습니다.",
                                    QMessageBox.Yes, QMessageBox.Yes)
            return


    # 수강신청 목록 테이블 클릭 이벤트

    def item_select(self):
        self.edit_t_no.setText(str(self.item_list.index(self.list.currentIndex().row(), 0).data()))

        self.edit_sd_num.setText(str(self.item_list.index(self.list.currentIndex().row(), 1).data()))

        # 학번에 맞는 학과 뽑아내서 학과 입력란에 삽입
        self.s_num = str(self.item_list.index(self.list.currentIndex().row(), 1).data())[2:4]  # 학번의 3,4번째 문자열만 가져와서 학과 번호를 뽑아옴 - 슬라이스 사용

        self.subject_name_sql = "select s_name from subject where s_num = '{}'".format(self.s_num)  # 학과 번호를 이용해 학과 이름을 뽑아옴
        self.uni_cur.execute(self.subject_name_sql)
        self.conn.commit()
        self.subject_name = self.uni_cur.fetchone()[0]  # 학번을 통해 과를 뽑아냄.
        self.edit_subject_name.setText(self.subject_name)

        self.edit_l_num.setText(str(self.item_list.index(self.list.currentIndex().row(), 3).data()))
        # self.edit_sd_id.setDisabled(True)  # 학생 id버튼 비활성화
        self.edit_t_section.setText(str(self.item_list.index(self.list.currentIndex().row(), 4).data()))
        # self.date_sd_birthday.setDate(QDate.currentDate())

        if self.edit_t_section.text() == "전공":
            self.section_select1()
            # self.edit_l_num.setText()
            self.rbtn1.setChecked(True)
        else:
            self.section_select2()
            self.rbtn2.setChecked(True)


        self.edit_sd_num.setDisabled(True)  # 학생 이름 비활성화
        self.edit_subject_name.setDisabled(True)
        # self.btn_id_check.setDisabled(True)  # id체크 버튼 비활성화
        # self.btn_subjectName_load.setDisabled(True)  # 학과이름 로드 비활성화
        self.btn_trainee_update.setDisabled(False)  # 학생 업데이트 활성화
        self.btn_trainee_delete.setDisabled(False)  # 학생 삭제 활성화
        self.btn_trainee_insert.setDisabled(True)  # 학생 삽입 비활성화

    # 학번 체크 이벤트 핸들러
    def sd_num_check(self):
        if (self.edit_sd_num.text() != ""):             #학번 입력창에 번호가 있다면(없지 않다면)
            try:
                self.sd_num_checksql = "select sd_num from student where sd_num = '{}'".format(self.edit_sd_num.text())
                print(self.sd_num_checksql)  # 명령어를 파이썬에 보여줌
                self.uni_cur.execute(self.sd_num_checksql)
                self.conn.commit()
                rs = self.uni_cur.fetchone()[0]
                print(rs)

                if (rs != None):
                    self.sd_name_sql = "select sd_name from student where sd_num = '{}'".format(self.edit_sd_num.text())
                    print(self.sd_name_sql)
                    self.uni_cur.execute(self.sd_name_sql)
                    self.conn.commit()
                    self.sd_name = self.uni_cur.fetchone()[0]


                    agree = QMessageBox.information(self, "학번 체크 성공", "{} 학생이 맞습니까?".format(self.sd_name),
                                            QMessageBox.Yes|QMessageBox.No, QMessageBox.Yes)

                    if agree == QMessageBox.Yes:

                        self.edit_sd_num.setDisabled(True)                    #비활성화 기능 없앴음. (수정)
                        print('학과번호 :', rs[2:4])


                        self.s_num = rs[2:4]  # 학번의 3,4번째 문자열만 가져와서 학과 번호를 뽑아옴 - 슬라이스 사용
                        self.subject_name_sql = "select s_name from subject where s_num = '{}'".format(self.s_num) #학과 번호를 이용해 학과 이름을 뽑아옴
                        print(self.subject_name_sql)
                        self.uni_cur.execute(self.subject_name_sql)
                        self.conn.commit()

                        self.subject_name = self.uni_cur.fetchone()[0]  # 학번을 통해 과를 뽑아냄.
                        self.edit_subject_name.setText(self.subject_name) # 뽑아온 학과를 자동으로 학과명 입력란에 삽입


                        QMessageBox.information(self, "학번 체크 성공", "선택되었습니다.",
                                                QMessageBox.Yes, QMessageBox.Yes)

                        # self.subject_name_extract(rs)
                        # #학번 체크 성공시 자동으로 학과명 입력
                        self.s_num = rs[2:4]                  #학번의 3,4번째 문자열만 가져옴 - 슬라이스 사용
                        self.subject_name_sql = "select s_name from subject where s_num = '{}'".format(self.s_num)
                        print(self.subject_name_sql)
                        self.uni_cur.execute(self.subject_name_sql)
                        self.conn.commit()
                        #
                        # subject_name = self.uni_cur.fetchone()[0]  # 학번을 통해 과를 뽑아냄.
                        # #
                        # #
                        # # return subject_name
                    else:
                        QMessageBox.information(self, "취소 메세지", "취소 되었습니다.",
                                                QMessageBox.Yes, QMessageBox.Yes)
                        self.edit_sd_num.clear()
                        return

                else:
                    self.edit_sd_id.clear()
                    QMessageBox.information(self, "학번 체크 오류", "사용할 수 없는 학번 입니다.",
                                            QMessageBox.Yes, QMessageBox.Yes)

            except:
                QMessageBox.information(self, "학번 체크 오류", "등록되지 않은 학생입니다.",
                                        QMessageBox.Yes, QMessageBox.Yes)
                return


    # def lesson_Load(self):
    #     lessonNameList = self.lesson_nameList()
    #     self.subjectNamecombo.clear()
    #
    #     for i in range(len(lessonNameList)):
    #         l_name = lessonNameList[i]
    #         self.cb.addItem(l_name[0])

    # 전공 구분에 맞는 과목명을 불러오는 메서드
    def lesson_section(self, number):

        self.lesson_namesql = "select l_name from lesson where l_num like '%{}' order by l_no".format(number)
        self.uni_cur.execute(self.lesson_namesql)
        self.conn.commit()
        lt = self.uni_cur.fetchall()

        lesson_s = lt
        return lesson_s

    # 과목명을 불러오는 메서드
    def lesson_nameList(self):
        self.lesson_namesql = "select l_name from lesson order by l_no"
        self.uni_cur.execute(self.lesson_namesql)
        self.conn.commit()
        ls = self.uni_cur.fetchall()

        lesson_name = ls
        return lesson_name

    # 콤보박스 선택시 이벤트 -> 과목번호를 자동으로 넣어줌
    def onActivated(self, text):
        self.l_num_sql = "select l_num from lesson where l_name = '{}'".format(text)
        print(self.l_num_sql)
        self.uni_cur.execute(self.l_num_sql)
        self.conn.commit()
        l_num = self.uni_cur.fetchone()[0]
        # print(l_num)
        self.edit_l_num.setText(l_num)

    def section_select1(self):
        self.rbtn1.setChecked(True)
        self.edit_t_section.setText('전공')
        # self.cb = QComboBox(self)
        lessonSectionList = self.lesson_section('1')
        self.cb.clear()

        for i in range(len(lessonSectionList)):
            l_section = lessonSectionList[i]
            self.cb.addItem(l_section[0])
        self.edit_l_num.clear()

        print(lessonSectionList[0][0])
        self.first_l_num = "select l_num from lesson where l_name = '{}'".format(lessonSectionList[0][0])
        self.uni_cur.execute(self.first_l_num)
        fln = self.uni_cur.fetchone()[0]


        self.conn.commit()
        self.edit_l_num.setText(fln)


    def section_select2(self):
        self.edit_t_section.setText('교양')
        # self.cb = QComboBox(self)
        lessonSectionList = self.lesson_section('2')
        self.cb.clear()
        # print(lessonSectionList)

        for i in range(len(lessonSectionList)):
            l_section = lessonSectionList[i]
            self.cb.addItem(l_section[0])

        self.edit_l_num.clear()
        if len(lessonSectionList) != 0:

            print(lessonSectionList[0][0])
            self.first_l_num = "select l_num from lesson where l_name = '{}'".format(lessonSectionList[0][0])
            self.uni_cur.execute(self.first_l_num)
            fln = self.uni_cur.fetchone()[0]

            self.conn.commit()
            self.edit_l_num.setText(fln)
        else:
            # self.text_lbl.setText('하하.')
            # self.text_lbl = QLabel('비어있습니다', self)
            # self.text_lbl.move(245, 214)
            # self.cb.addItem('비어있습니다.')
            return
    # 입력창 초기화
    def trainee_init(self):
        self.edit_t_no.clear()
        self.edit_sd_num.clear()
        self.edit_subject_name.clear()
        self.edit_l_num.clear()
        self.edit_t_section.clear()


        self.btn_trainee_insert.setDisabled(False)
        self.btn_trainee_update.setDisabled(True)
        self.btn_trainee_delete.setDisabled(True)

        # self.rbtn1.setChecked(True)
        # self.rbtn2.setChecked(False)

    def abc(self):
        self.rbtn1.setChecked(True)
        # self.rbtn1.setChecked(False)

    def traineeList(self, QShowEvent):
        # sql에서 정보 가져오기 위한 셀렉트 명령어
        self.trainee_totallist = "select * from trainee"
        self.uni_cur.execute(self.trainee_totallist)      #커서를 통해 불러온 정보(학과 정보)읽어옴
        self.conn.commit()

        ti = self.uni_cur.fetchall()     #행을 모두 뽑아냄

        self.item_list.removeRow(len(ti))
        # print(ti[0][4])
        print(ti)


        #과목 번호 통해서 과목명 불러오기


        #불러온 정보를 화면에 보여주기 위함
        for i in range(len(ti)):

            self.item_list.removeRow(i)
            self.item_list.insertRow(i)
            self.item_list.setData(self.item_list.index(i, 0), ti[i][0])
            self.item_list.setData(self.item_list.index(i, 1), ti[i][1])

            self.lesson_name = "select l_name from lesson where l_num = '{}'".format(ti[i][2])
            self.uni_cur.execute(self.lesson_name)
            self.conn.commit()
            self.lesson_name = self.uni_cur.fetchone()[0]

            self.item_list.setData(self.item_list.index(i, 2), self.lesson_name)
            self.item_list.setData(self.item_list.index(i, 3), ti[i][2])
            self.item_list.setData(self.item_list.index(i, 4), ti[i][3])
            self.item_list.setData(self.item_list.index(i, 5), str(ti[i][4]))


        #오류 의심(들여쓰기)
        self.edit_t_no.clear()
        self.edit_sd_num.clear()
        self.edit_subject_name.clear()
        self.edit_l_num.clear()
        self.edit_t_section.clear()
        # print('학과 등록 탭')

    # # 학번을 통해 학과명을 뽑아냄
    # def subject_name_extract(self, sd_num):
    #     print(self.sd_num,1221)



    #초기화 버튼
    def trainee_init(self):
        self.edit_t_no.clear()
        # self.subjectName.setText('학과명을 선택하세요')
        self.edit_sd_num.clear()
        self.edit_subject_name.clear()
        self.edit_sd_num.setDisabled(False)  # 학생이름 활성화
        self.edit_l_num.clear()
        self.edit_subject_name.setDisabled(False)
        self.edit_t_section.clear()

        # self.date_sd_birthday.setDate(QDate.currentDate())
        # self.edit_sd_phone.clear()
        # self.edit_sd_address.clear()
        # self.edit_sd_email.clear()

        # self.btn_id_check.setDisabled(False)  # 아이디 체크버튼 활성화
        # self.btn_subjectName_load.setDisabled(False)  # 학과명 로드 활성화
        self.btn_trainee_insert.setDisabled(False)
        self.btn_trainee_update.setDisabled(True)  # 학생 업데이트 버튼 비활성화
        self.btn_trainee_delete.setDisabled(True)  # 학생 삭제 버튼 비활성화

    def onChanged(self):
        # sql에서 정보 가져오기 위한 셀렉트 명령어
        self.trainee_totallist = "select * from trainee where sd_num like '{}%'".format(self.edit_trainee_search.text())
        print(self.trainee_totallist)
        self.uni_cur.execute(self.trainee_totallist)  # 커서를 통해 불러온 정보(학과 정보)읽어옴
        self.conn.commit()

        ti = self.uni_cur.fetchall()        # 행을 모두 뽑아냄
        self.item_list.removeRow(len(ti))
        # for i in range(len(ti)):
        # self.item_list.removeRow(i)
        # print(ti[0][4])
        ti = list(ti)
        # print(ti)
        # print(len(ti))
        # self.item_list.removeRow
        # for j in range(len(ti)):
        #     self.item_list.removeRow(j)

        # print(self.item_list.index(1,1).text())
        # self.item_list.index(0, 0), row[0][0]
        # print(self.itme_list.removeRow(len(1)))


        # print(self.item_list.removeRow(len(ti)))

        # 과목 번호 통해서 과목명 불러오기
        if len(ti) != 0:
            # 불러온 정보를 화면에 보여주기 위함
            while self.item_list.removeRow(len(ti)):
                self.item_list.removeRow(len(ti))

            for i in range(len(ti)):
                self.item_list.removeRow(i)
                self.item_list.insertRow(i)
                self.item_list.setData(self.item_list.index(i, 0), ti[i][0])
                self.item_list.setData(self.item_list.index(i, 1), ti[i][1])

                self.lesson_name = "select l_name from lesson where l_num = '{}'".format(ti[i][2])
                self.uni_cur.execute(self.lesson_name)
                self.conn.commit()
                self.lesson_name = self.uni_cur.fetchone()[0]

                self.item_list.setData(self.item_list.index(i, 2), self.lesson_name)
                self.item_list.setData(self.item_list.index(i, 3), ti[i][2])
                self.item_list.setData(self.item_list.index(i, 4), ti[i][3])
                self.item_list.setData(self.item_list.index(i, 5), str(ti[i][4]))


            # QMessageBox.information(self, "검색 메세지", "검색 완료",
            #                         QMessageBox.Yes, QMessageBox.Yes)
            self.edit_trainee_search.clear()

        else:
            QMessageBox.information(self, "검색 에러 메세지", "검색 정보가 없습니다.",
                                    QMessageBox.Yes, QMessageBox.Yes)
            self.edit_trainee_search.clear()





if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MyApp()
    sys.exit(app.exec_())