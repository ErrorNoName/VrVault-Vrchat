_A='auth_cookie'
import sys
from PyQt5.QtWidgets import QApplication,QWidget,QVBoxLayout,QLabel,QLineEdit,QListWidget,QPushButton,QFileDialog,QDialog,QProgressBar,QAction,QColorDialog,QFontDialog,QGraphicsView,QGraphicsScene
import os,json,requests
from PyQt5.QtGui import QPixmap,QIcon,QColor,QFont,QPainter
from PyQt5.QtCore import Qt,QPropertyAnimation,QRect
from PyQt5.QtWidgets import QInputDialog,QLabel
from PIL import Image
import datetime
from PyQt5.QtWidgets import QGraphicsBlurEffect
config_file='config.json'
class AvatarSelector(QWidget):
	def __init__(A):super().__init__();A.initUI()
	def initUI(A):A.setWindowTitle('Avatar Selector');A.setGeometry(100,100,800,600);A.setWindowIcon(QIcon('icon.ico'));A.layout=QVBoxLayout();A.setLayout(A.layout);A.credit_label=QLabel('Créé par Freakiv3 du groupe KawaiiSquad\nInventaire sans limite pour Vrchat');A.layout.addWidget(A.credit_label);A.search_entry=QLineEdit(A);A.search_entry.setPlaceholderText("Recherche d'un avatar...");A.layout.addWidget(A.search_entry);A.avatar_list=QListWidget(A);A.avatar_list.setStyleSheet('\n            QListWidget {\n                background-color: #333;\n                color: white;\n                font-size: 14px;\n            }\n            QListWidget::item:hover {\n                background-color: #555;\n            }\n        ');A.layout.addWidget(A.avatar_list);A.progress_bar=QProgressBar(A);A.layout.addWidget(A.progress_bar);A.img_panel=QLabel(A);A.img_panel.mousePressEvent=A.on_image_click;A.layout.addWidget(A.img_panel);A.folder_path='AvatarsPNG';A.update_avatar_list();A.search_entry.textChanged.connect(A.update_avatar_list);A.avatar_list.itemClicked.connect(lambda:A.preview_image(A.avatar_list.currentItem().text()));A.select_button=QPushButton('Sélectionner cet avatar',A);A.select_button.clicked.connect(lambda:A.select_avatar());A.layout.addWidget(A.select_button);A.customize_action=QAction('Personnaliser',A);A.customize_action.triggered.connect(A.customize_interface);A.addAction(A.customize_action);A.generate_profile_button=QPushButton("Générer Profil d'Avatar",A);A.generate_profile_button.clicked.connect(A.generate_avatar_profile);A.layout.addWidget(A.generate_profile_button)
	def keyPressEvent(A,event):
		D=event
		if D.key()==Qt.Key_Up:B=A.avatar_list.currentRow();C=max(B-10,0);A.avatar_list.setCurrentRow(C);A.preview_image(A.avatar_list.currentItem().text())
		elif D.key()==Qt.Key_Down:B=A.avatar_list.currentRow();C=min(B+10,A.avatar_list.count()-1);A.avatar_list.setCurrentRow(C);A.preview_image(A.avatar_list.currentItem().text())
	def update_avatar_list(A):
		D=A.search_entry.text().lower();A.avatar_list.clear();B=[A for A in os.listdir(A.folder_path)if A.endswith('.png')];G=len(B);C=[A for A in B if D in os.path.splitext(A)[0].lower()]
		for(E,F)in enumerate(C):A.avatar_list.addItem(os.path.splitext(F)[0]);A.progress_bar.setValue(int((E+1)/len(C)*100))
	def load_auth_cookie(C):
		if os.path.exists(config_file):
			with open(config_file,'r')as A:B=json.load(A);return B.get(_A,None)
		else:return
	def save_auth_cookie(B,auth_cookie):
		with open(config_file,'w')as A:json.dump({_A:auth_cookie},A)
	def get_auth_cookie(B):
		A=B.load_auth_cookie()
		if not A:
			A,C=QInputDialog.getText(B,'Auth Cookie Requise','Veuillez entrer votre auth_cookie:',QLineEdit.Password)
			if C and A:B.save_auth_cookie(A)
		return A
	def select_avatar(A):
		B=A.get_auth_cookie()
		if not B:print("Auth_cookie n'est pas valide ou n'a pas été fourni.");return
		C=A.avatar_list.currentItem().text();A.display_image(C);A.select_avatar_with_http_info(B,C)
	def select_avatar_with_http_info(H,auth_cookie,avatar_id):
		E='Status Code: ';D=avatar_id;C=auth_cookie;F=f"https://vrchat.com/api/1/avatars/{D}/select";G={'User-Agent':'VRCST/1.0 (VotreContactInfo)','Cookie':f"auth={C}",'Content-Type':'application/json'}
		try:
			A=requests.put(F,headers=G);print(f"Compte avec auth_cookie: {C}, Avatar ID: {D}");print(E+str(A.status_code));print('Response Headers: '+str(A.headers));print('Response Body: '+A.text)
			if A.status_code==200:print('Succès!');print("L'avatar a été sélectionné avec succès.")
			else:print('Échec!');print(f"Erreur lors de la sélection de l'avatar. Code d'état: {A.status_code}");print(A.text)
		except requests.exceptions.RequestException as B:print('Exception when calling AvatarsApi.SelectAvatarWithHttpInfo: '+str(B));print(E+str(B.response.status_code if B.response else'N/A'));print(B)
	def display_image(A,avatar_id):
		B=f"{A.folder_path}/{avatar_id}.png"
		if os.path.isfile(B):C=QPixmap(B);D=C.scaled(300,300,Qt.KeepAspectRatioByExpanding);A.img_panel.setPixmap(D)
	def preview_image(A,avatar_id):
		B=f"{A.folder_path}/{avatar_id}.png"
		if os.path.isfile(B):C=QPixmap(B);D=C.scaled(300,300,Qt.KeepAspectRatioByExpanding);A.img_panel.setPixmap(D);A.current_image_path=B
	def on_image_click(A,event):
		if A.current_image_path:A.zoomable_preview(A.current_image_path)
	def zoomable_preview(A,image_path):
		B=image_path
		if os.path.isfile(B):A.dialog=QDialog(A);A.dialog.setWindowTitle('Zoomed Image');C=QVBoxLayout(A.dialog);D=QLabel(A.dialog);E=QPixmap(B);D.setPixmap(E);C.addWidget(D);A.dialog.setLayout(C);A.dialog.exec_()
	def customize_interface(A):
		B=QColorDialog.getColor()
		if B.isValid():A.avatar_list.setStyleSheet(f"QListWidget {{ background-color: {B.name()}; }}")
		C,D=QFontDialog.getFont()
		if D:A.avatar_list.setFont(C);A.search_entry.setFont(C)
	def generate_avatar_profile(I):
		L='Arial';C=I.avatar_list.currentItem().text();M=f"ID: {C}\n";B=f"{I.folder_path}/{C}.png"
		if not os.path.isfile(B):return
		D=QPixmap(500,500);N=QPixmap(B).scaled(500,500,Qt.KeepAspectRatio);E=QGraphicsScene();E.addPixmap(N);J=QGraphicsBlurEffect();J.setBlurRadius(20);E.items()[0].setGraphicsEffect(J);K=QGraphicsView(E);K.setFixedSize(500,500);O=K.grab();A=QPainter();A.begin(D);A.drawPixmap(QRect(0,0,500,500),O);P=QPixmap(B).scaled(200,200,Qt.KeepAspectRatio);F=Image.open(B);Q=F.getcolors(F.size[0]*F.size[1]);R=sorted(Q,key=lambda x:x[0],reverse=True)[0][1];S=QColor(*R);A.setBrush(S);A.drawRoundedRect(150,50,200,200,10,10);A.drawPixmap(QRect(150,50,200,200),P);A.setPen(QColor('#ECEFF4'));G=QFont(L,12,QFont.Bold);A.setFont(G);A.drawText(50,300,M);A.setPen(QColor('#FFFFFF'));A.drawText(140,340,f"Date de creation: {datetime.datetime.now().strftime('%Y-%m-%d')}");A.setPen(QColor('#4C566A'));A.drawLine(0,450,500,450);A.setPen(QColor('#D8DEE9'));G=QFont(L,10,QFont.StyleItalic);A.setFont(G);A.drawText(50,470,'Créé par Freakiv3 du groupe KawaiiSquad\nwww.kawaiisquad.com');A.end();H='ImageShare'
		if not os.path.exists(H):os.makedirs(H)
		T=f"{H}/{C}_profile.png";D.save(T,'PNG');U=QApplication.clipboard();U.setPixmap(D)
if __name__=='__main__':app=QApplication(sys.argv);ex=AvatarSelector();ex.show();sys.exit(app.exec_())