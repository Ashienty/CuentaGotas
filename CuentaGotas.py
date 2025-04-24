from PySide6.QtWidgets import QApplication, QWidget, QPushButton,QMainWindow,QVBoxLayout, QHBoxLayout, QLabel,QLineEdit
from PySide6.QtCore import Qt,QThread
from PySide6.QtGui import QIcon,QIntValidator
import sys, time, winsound
app = QApplication(sys.argv)
##
app.setStyleSheet("""
    QWidget {
        background-color: #212121;
        color: #ffffff;
    }
    QPushButton {
        background-color: #2f2f2f;
        color: #ffffff;
        border: 1px solid #4d4d4d;
        padding: 5px;
    }
    QPushButton:hover {
        background-color: #676767;
    }
    QMainWindow::title {
        color: #ffffff;
        background-color: #222222;
        }              
""")
##Clase Ventana 
class CustomMainWindow(QMainWindow):
    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.dragPos = event.globalPosition().toPoint()

    def mouseMoveEvent(self, event):
        if event.buttons() == Qt.LeftButton:
            self.move(self.pos() + event.globalPosition().toPoint() - self.dragPos)
            self.dragPos = event.globalPosition().toPoint()
##Aplicacion de Clase Ventana 
window = CustomMainWindow()
window.setWindowTitle("Cuenta Gotas")
window.resize(160, 160) 
window.setWindowFlags(Qt.FramelessWindowHint)
centralWidget = QWidget()
window.setCentralWidget(centralWidget)
layout = QVBoxLayout(centralWidget)

##Barra de tareas
titleBar = QWidget()
titleBar.setFixedHeight(30)
titleBar.setStyleSheet("background-color: #333333;")
layout.setContentsMargins(0, 0, 0, 0)
layout.setSpacing(0)
layout.addWidget(titleBar)
layout.setAlignment(titleBar, Qt.AlignTop)
##Iconos de la Barra/abrir minimizar
minimise=QPushButton("-")
close=QPushButton("X")
close.setFixedWidth(30)
minimise.setFixedWidth(30)
symbol=QLabel()
icon=QIcon("Sonidos/Simbolo Opcional minimalista.png")
symbol.setPixmap(icon.pixmap(30,30))
titleBarLayout=QHBoxLayout(titleBar)
titleBarLayout.setContentsMargins(0,3,0,3)
titleBarLayout.setSpacing(5)
titleBarLayout.addWidget(symbol)
titleBarLayout.addWidget(minimise)
titleBarLayout.addWidget(close)
minimise.setStyleSheet(""" 
    QPushButton:hover {
        background-color: #2f2f2f;
    }
""")
close.setStyleSheet(""" 
    QPushButton:hover {
        background-color: #2f2f2f;
    }
""")
##Funcionalidad de los botones de la Barra/abrir minimizar
close.clicked.connect(window.close)
minimise.clicked.connect(window.showMinimized)
##Funciones del cuenta gotas
class cuentaGotas(QThread):
    def __init__(self, minutosIntervalo, horasIntervalo):
        super().__init__()
        self.minutosIntervalo = minutosIntervalo
        self.horasIntervalo = horasIntervalo
        self.runing =True
    def run(self):
        minutero=0
        vueltas=0
        total=0

        while self.runing:
            time.sleep(60)
            minutero+=1
            vueltas+=1
            total+=1
            print(total)
            if(vueltas/60) == self.horasIntervalo:
                vueltas=0
                minutero=0
                winsound.PlaySound("Sonidos/largo.wav", winsound.SND_FILENAME)
            elif minutero == self.minutosIntervalo:
                minutero=0
                winsound.PlaySound("Sonidos/corto.wav", winsound.SND_FILENAME)
    def stop(self):
        self.runing=False
#Inicia la instancia del HILO
cuentaHilo = None

##Botones de la funcion 
#Nuevo Contenedor
mainContent = QWidget()
mainLayout = QVBoxLayout(mainContent)
#Actividad
statusLabel=QLabel("●")
statusLabel.setStyleSheet("color:Red; font-size: 14px;")
mainLayout.addWidget(statusLabel)
#Botones e inputs  del nuevo contenedor
validador = QIntValidator(1, 59)
minutosInput = QLineEdit()
minutosInput.setPlaceholderText("Minutos")
minutosInput.setFixedWidth(150)
minutosInput.setValidator(validador)


horasInput =QLineEdit()
horasInput.setPlaceholderText("Horas")
horasInput.setFixedWidth(150)
horasInput.setValidator(validador)

inputLayout =QHBoxLayout()
mainLayout.addWidget(minutosInput)
mainLayout.addWidget(horasInput)

mainLayout.addLayout(inputLayout)
##
startButton = QPushButton("Inicio")
stopButton = QPushButton("Fin")
startButton.setFixedWidth(150)
stopButton.setFixedWidth(150)
mainLayout.addWidget(startButton)
mainLayout.addWidget(stopButton)
layout.addWidget(mainContent)

##Funciones de los botones e inputs 
def iniciarCuenta():
    global cuentaHilo
    statusLabel.setText("●")
    statusLabel.setStyleSheet("color:green; font-size: 14px;")
    if cuentaHilo and cuentaHilo.isRunning():
        return
    if not minutosInput.text() or not horasInput.text():
        minVal=10
        horasVal=1
    else:
        minVal = int(minutosInput.text())
        horasVal=int(horasInput.text())
    print(minVal)
    print(horasVal)
    cuentaHilo = cuentaGotas(minVal, horasVal)
    cuentaHilo.start()
def detenerCuenta():
    global cuentaHilo
    statusLabel.setText("●")
    statusLabel.setStyleSheet("color: red; font-size: 14px;")
    if cuentaHilo and cuentaHilo.isRunning():
        cuentaHilo.stop()
##Acciones de los botones
startButton.clicked.connect(iniciarCuenta)
stopButton.clicked.connect(detenerCuenta)
    


##
window.show()
sys.exit(app.exec())
