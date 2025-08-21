from PySide6.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QLabel,QLineEdit,QSizePolicy
from PySide6.QtCore import Qt,QObject, QTimer, Signal, QThread
from PySide6.QtGui import QIcon,QPixmap,QIntValidator
import sys, winsound, time

class CustomMainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Cuenta Gotas")
        self.resize(200, 125)
        self.setWindowFlags(Qt.WindowType.FramelessWindowHint| Qt.WindowType.WindowStaysOnTopHint)
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)

        #rgba(128, 41, 34, 0.8); el rojo que me gusta para el borde y rgba(34, 128, 34, 0.8) verde que me gusta
        self.estado=False
        self.minuto=0
        self.hora=0
        self.inputMinuto=10
        self.inputHora=1
        def estilo():
            estadoColor = "rgba(128, 41, 34, 0.8)" if not self.estado else "rgba(34, 128, 34, 0.8)"
            playColor= "rgba(34, 128, 34, 0.8)" if not self.estado else "rgba(128, 41, 34, 0.8)"
            self.setStyleSheet(f"""            
                QWidget {{
                    background-color: transparent;
                }}
                QLabel {{
                    font-weight: bold;
                }}
                QWidget#centralWidget , QWidget#title_bar {{
                    background-color: rgba(100, 100, 100, 90);
                    border-radius: 4px;
                    color: black;
                    font-family: Arial;
                    font-size: 14px;
                    border: 2px solid {estadoColor};
                }}
                QLabel#minimize_label:hover {{
                    background-color: rgba(211, 211, 211, 90);
                    color: black;
                }}
                QLabel#close_label:hover {{
                    background-color: rgba(255, 0, 0, 90);
                    color: white;
                }}
                QLineEdit {{
                    border: 2px solid rgba(0,0,0,90);
                    border-radius: 4px;
                    padding: 2px;
                }}
                QWidget#playBoton:hover {{
                    background: {playColor};
                    border-radius: 4px;
                }}
                QWidget#tiempoText {{
                    color:{estadoColor};
                    font-family: Arial;
                    font-size: 25px;
                }}
            """)
        estilo()
        # Widget central
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        central_widget.setObjectName("centralWidget")
        main_layout = QVBoxLayout(central_widget)
        main_layout.setContentsMargins(0, 0, 0, 0)        
        # Barra de título
        title_bar = QWidget()
        title_bar.setFixedHeight(30)
        title_bar.setObjectName("title_bar")
        title_layout = QHBoxLayout(title_bar)
        title_layout.setContentsMargins(5, 0, 5, 0)
        main_layout.addWidget(title_bar)
        main_layout.setAlignment(title_bar,Qt.AlignmentFlag.AlignTop)
        # Icono a la izquierda
        icon_label = QLabel()
        icon = QIcon("Sonidos/Simbolo Opcional minimalista.png")
        icon_label.setPixmap(icon.pixmap(20, 20))
        title_layout.addWidget(icon_label)
        title_text = QLabel("Cuenta Gotas")
        title_layout.addWidget(title_text)
        # Barra de botones cerrar minimizar
        class ClickableLabel(QLabel):
            def __init__(self, text, parent=None, callback=None):
                super().__init__(text, parent)
                self.callback = callback
                self.setFixedSize(20, 20)
                self.setAlignment(Qt.AlignmentFlag.AlignCenter)
            def mousePressEvent(self, event):
                if event.button() == Qt.MouseButton.LeftButton and self.callback:
                    self.callback()
        buttons_widget = QWidget()
        buttons_layout = QHBoxLayout(buttons_widget)
        buttons_layout.setContentsMargins(0, 0, 0, 0)
        buttons_layout.setSpacing(0)
        minimize_label = ClickableLabel("-", callback=self.showMinimized)
        close_label = ClickableLabel("X", callback=self.close)
        minimize_label.setObjectName("minimize_label")
        close_label.setObjectName("close_label")
        buttons_layout.addWidget(minimize_label)
        buttons_layout.addWidget(close_label)
        title_layout.addWidget(buttons_widget)
        title_layout.setAlignment(buttons_widget,Qt.AlignmentFlag.AlignRight)
        #Temporizador
        tiempo=QWidget(self)
        tiempo_layout=QVBoxLayout(tiempo)
        main_layout.addWidget(tiempo)
        self.tiempoText = QLabel(str(self.minuto))
        self.tiempoText.setObjectName("tiempoText")
        tiempo_layout.addWidget(self.tiempoText)
        tiempo_layout.setAlignment(self.tiempoText,Qt.AlignmentFlag.AlignCenter)
        # Inputs
        inputs = QWidget(self)
        inputs_layout = QVBoxLayout(inputs)
        main_layout.addWidget(inputs)
        self.minutos = QLineEdit()
        self.minutos.textChanged.connect(lambda text: setattr(self, 'inputMinuto', int(text) if text else 10))
        self.minutos.setPlaceholderText("10 Minutos por defecto")
        inputs_layout.addWidget(self.minutos)
        self.minutos.setValidator(QIntValidator(1, 30))
        self.horas = QLineEdit()
        self.horas.textChanged.connect(lambda text: setattr(self, 'inputHora', int(text) if text else 1))
        self.horas.setValidator(QIntValidator(1, 5))
        self.horas.setPlaceholderText("1 Hora por defecto")
        inputs_layout.addWidget(self.horas)
        self.setFocus()
        #Play pausa
        play = QWidget(self)
        play.setObjectName("play")
        play_layout =QVBoxLayout(play)
        main_layout.addWidget(play)
        playBoton=QLabel()
        playBoton.setObjectName("playBoton")
        playIcon=QPixmap("Sonidos/play.png").scaled(25, 25)
        playBoton.setPixmap(playIcon)
        play_layout.addWidget(playBoton)
        play_layout.setAlignment(Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignHCenter)
        playBoton.mousePressEvent = lambda event: cambiarIcono()
        #Boton play / pause
        def cambiarIcono():
            if playBoton.pixmap().toImage() == QPixmap("Sonidos/play.png").scaled(25, 25).toImage():
                playBoton.setPixmap(QPixmap("Sonidos/pause.png").scaled(25, 25))
                self.estado=True
                self.timer.start()
                estilo()
            else:
                playBoton.setPixmap(QPixmap("Sonidos/play.png").scaled(25, 25))
                self.estado=False
                self.timer.stop()
                estilo()
        #Espaciado
        main_layout.setSpacing(2)
        tiempo_layout.setContentsMargins(10, 0, 10, 10)
        tiempo_layout.setSpacing(0)
        inputs_layout.setContentsMargins(10, 0, 10, 10)
        inputs_layout.setSpacing(2)
        play_layout.setContentsMargins(0, 0, 0, 10)
        play_layout.setSpacing(0)
        #Temporizador y sonidos
        self.timer = QTimer()
        self.timer.setInterval(60000)
        self.timer.timeout.connect(self.tick)
    def tick(self):
        if self.estado:
            if self.minuto % self.inputMinuto == 0 and self.minuto!=0:
                winsound.PlaySound("Sonidos/corto.wav", winsound.SND_FILENAME | winsound.SND_ASYNC)
            else:
                if self.hora!=0 and self.hora%self.inputHora==0 and self.minuto==0:                
                    winsound.PlaySound("Sonidos/largo.wav", winsound.SND_FILENAME | winsound.SND_ASYNC)
            self.minuto += 1
            print(self.minuto)
            if self.minuto==60:
                self.minuto=0
                self.hora +=1
                if self.hora==99:
                    self.hora=0
            if self.minuto<10:
                self.tiempoText.setText(str(self.hora) + ":" +"0"+ str(self.minuto))
            else:
                self.tiempoText.setText(str(self.hora) + ":" + str(self.minuto))
    # Arrastrar ventana
    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            self.dragPos = event.globalPosition().toPoint()
            self.setFocus()
    def mouseMoveEvent(self, event):
        if event.buttons() == Qt.MouseButton.LeftButton:
            self.move(self.pos() + event.globalPosition().toPoint() - self.dragPos)
            self.dragPos = event.globalPosition().toPoint()
            self.setFocus()
# Aplicación
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = CustomMainWindow()
    window.show()
    sys.exit(app.exec())