import sys
import os
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QApplication, QDialog, QFileDialog, QMessageBox
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt
from ela import convert_to_ela_image
from prediction import predict_result

class MainWindow(QDialog):
    def __init__(self):
        super(MainWindow, self).__init__()
        
        # Load UI file
        ui_path = os.path.join(os.path.dirname(__file__), "gui.ui")
        try:
            loadUi(ui_path, self)
        except Exception as e:
            QMessageBox.critical(None, "UI Error", f"Cannot load UI file: {str(e)}")
            sys.exit(1)
            
        self.Browse.clicked.connect(self.open_image)
        self.Test.clicked.connect(self.result)
        self.Quit.clicked.connect(self.close_main_window)
        self.fname = ""  # Initialize filename

    def open_image(self):
        try:
            self.fname, _ = QFileDialog.getOpenFileName(
                self, 
                "Open Image", 
                "", 
                "Image Files (*.png *.jpg *.jpeg *.xmp)"
            )
            
            if not self.fname:
                return
                
            # Display original image
            pixmap = QPixmap(self.fname)
            if pixmap.isNull():
                raise ValueError("Unsupported image format")
                
            self.ORIGINAL_IMAGE.setPixmap(
                pixmap.scaled(
                    self.ORIGINAL_IMAGE.width(), 
                    self.ORIGINAL_IMAGE.height(),
                    Qt.KeepAspectRatio,
                    Qt.SmoothTransformation
                )
            )
            
            # Generate and display ELA image
            convert_to_ela_image(self.fname, 90)
            ela_pixmap = QPixmap("ela_image.png")
            
            self.ELA_IMAGE.setPixmap(
                ela_pixmap.scaled(
                    self.ELA_IMAGE.width(),
                    self.ELA_IMAGE.height(),
                    Qt.KeepAspectRatio,
                    Qt.SmoothTransformation
                )
            )
            
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Cannot open image: {str(e)}")

    def result(self):
        try:
            if not self.fname:
                QMessageBox.warning(self, "Warning", "Please select an image first!")
                return
                
            prediction, confidence = predict_result(self.fname)
            self.Result.setText(f"Prediction: {prediction}\nConfidence: {confidence:.2f}%")
            
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Prediction failed: {str(e)}")

    def close_main_window(self):
        reply = QMessageBox.question(
            self,
            "Quit",
            "Are you sure you want to quit?",
            QMessageBox.Close | QMessageBox.Cancel,
            QMessageBox.Cancel
        )
        
        if reply == QMessageBox.Close:
            self.close()

def main():
    app = QApplication(sys.argv)
    
    try:
        main_window = MainWindow()
        main_window.show()
        sys.exit(app.exec_())
    except Exception as e:
        QMessageBox.critical(None, "Fatal Error", f"Application failed: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    main()