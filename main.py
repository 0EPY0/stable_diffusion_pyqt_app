import sys
from PyQt6.QtWidgets import QApplication, QWidget, QLabel, QLineEdit, QPushButton, QVBoxLayout, QProgressDialog
from PyQt6.QtGui import QPixmap
from PIL import Image
import io
from PyQt6.QtCore import QThread, pyqtSignal, Qt
from generator_images import GenerateImage

class ImageGenerationThread(QThread):
    image_generated = pyqtSignal(object)

    def __init__(self, generator, prompt, negative_prompt):
        super().__init__()
        self.generator = generator
        self.prompt = prompt
        self.negative_prompt = negative_prompt

    def run(self):
        image = self.generator.generation(self.prompt, self.negative_prompt)
        self.image_generated.emit(image)


class ImageGenerationApp(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("StableDiffusion Image Generation")
        self.generator = GenerateImage()
        self.initUI()
        self.progress_dialog_lock = False
        self.progress = None

    def initUI(self):
        self.prompt_label = QLabel("Prompt:")
        self.prompt_input = QLineEdit()
        self.negative_prompt_label = QLabel("Negative Prompt:")
        self.negative_prompt_input = QLineEdit()
        self.generate_button = QPushButton("Generate")
        self.generate_button.clicked.connect(self.start_image_generation)
        self.result_label = QLabel("Generation Result:")
        self.image_label = QLabel()

        layout = QVBoxLayout()
        layout.addWidget(self.prompt_label)
        layout.addWidget(self.prompt_input)
        layout.addWidget(self.negative_prompt_label)
        layout.addWidget(self.negative_prompt_input)
        layout.addWidget(self.generate_button)
        layout.addWidget(self.result_label)
        layout.addWidget(self.image_label)
        self.setLayout(layout)
        
    def show_progress_dialog(self):
        if self.progress_dialog_lock:
            if not self.progress or not self.progress.isVisible():
                self.progress = QProgressDialog(self)
                self.progress.setCancelButton(None)
                self.progress.setWindowTitle("Attention")
                self.progress.setLabelText("Generating Image...")
                self.progress.setRange(0, 0)
                self.progress.setModal(True)
                self.progress.canceled.connect(self.progress_reopened)
                self.progress.show()
        else:
            self.progress.close()
            
    def progress_reopened(self):
        self.show_progress_dialog()
        
    def start_image_generation(self):
        prompt = self.prompt_input.text()
        negative_prompt = self.negative_prompt_input.text()
        
        self.progress_dialog_lock = True
        self.show_progress_dialog()

        self.thread = ImageGenerationThread(self.generator, prompt, negative_prompt)
        self.thread.image_generated.connect(self.display_generated_image)
        self.thread.finished.connect(self.unlock_process_dialog)
        self.thread.finished.connect(self.enable_window)
        
        self.disable_window()
        self.thread.start()
        
    def unlock_process_dialog(self):
        self.progress_dialog_lock = False
        self.show_progress_dialog()

    def disable_window(self):
        self.setEnabled(False)

    def enable_window(self):
        self.setEnabled(True)

    def convert_image_to_qpixmap(self, image):
        byte_array = io.BytesIO()
        with byte_array:
            image.save(byte_array, format='PNG')
            byte_array = byte_array.getvalue()
        pixmap = QPixmap()
        pixmap.loadFromData(byte_array)
        pixmap = pixmap.scaled(512, 512, aspectRatioMode=Qt.AspectRatioMode.KeepAspectRatio)
        return pixmap

    def display_generated_image(self, image):
        pil_image = Image.fromarray(image[0])
        pixmap = self.convert_image_to_qpixmap(pil_image)
        self.image_label.setPixmap(pixmap)
        

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = ImageGenerationApp()
    window.show()
    sys.exit(app.exec())
