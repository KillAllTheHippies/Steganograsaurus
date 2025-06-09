from PyQt5.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QLabel,
    QPushButton, QTextEdit, QFileDialog, QComboBox, QMessageBox, QDockWidget
)
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt
from ..encoder import ImageEncoder
from ..image_utils import validate_image_format, calculate_max_capacity, get_image_preview

class ImagePreviewWidget(QLabel):
    def __init__(self, main_window, parent=None):
        super().__init__(parent)
        self.main_window = main_window
        self.setAcceptDrops(True)
        
    def dragEnterEvent(self, event):
        if event.mimeData().hasUrls():
            urls = event.mimeData().urls()
            if len(urls) == 1:
                file_path = urls[0].toLocalFile()
                if any(file_path.lower().endswith(ext) for ext in ['.png', '.bmp', '.tiff']):
                    event.acceptProposedAction()
                    self.setProperty("dragging", "true")
                    self.style().polish(self)

    def dragLeaveEvent(self, event):
        self.setProperty("dragging", "false")
        self.style().polish(self)

    def dropEvent(self, event):
        self.setProperty("dragging", "false")
        self.style().polish(self)
        
        try:
            if event.mimeData().hasUrls():
                file_path = event.mimeData().urls()[0].toLocalFile()
                if not file_path:
                    return
                    
                # Verify file exists and is readable
                import os
                if not os.path.exists(file_path) or not os.access(file_path, os.R_OK):
                    QMessageBox.warning(self.main_window, "Error", "Cannot read the selected file")
                    return
                    
                self.main_window.select_image(file_path)
        except Exception as e:
            QMessageBox.critical(self.main_window, "Error", f"Failed to load image: {str(e)}")


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Image Steganography")
        self.setMinimumSize(800, 600)
        
        # Initialize encoder
        self.encoder = ImageEncoder()
        
        # Create main widgets
        self.init_ui()
        
        # Apply custom QSS stylesheet
        self.setStyleSheet("""
            QMainWindow {
                background-color: #2E2E2E; /* Dark gray background */
            }

            QDockWidget {
                background-color: #3C3C3C; /* Slightly lighter gray for dock widgets */
                color: #FFFFFF; /* White text */
            }

            QDockWidget::title {
                background-color: #555555; /* Darker gray for title bar */
                padding: 5px;
                border: 1px solid #2E2E2E;
            }

            QLabel {
                color: #E0E0E0; /* Light gray text for labels */
                font-size: 14px;
            }

            QPushButton {
                background-color: #5E5E5E; /* Medium gray for buttons */
                color: #FFFFFF;
                border: 1px solid #777777;
                padding: 8px 16px;
                font-size: 14px;
                border-radius: 4px;
            }

            QPushButton:hover {
                background-color: #6E6E6E; /* Lighter gray on hover */
            }

            QPushButton:pressed {
                background-color: #4E4E4E; /* Darker gray when pressed */
            }

            QComboBox {
                background-color: #4E4E4E;
                color: #FFFFFF;
                border: 1px solid #777777;
                padding: 5px;
                font-size: 14px;
                border-radius: 4px;
                selection-background-color: #6E6E6E;
            }

            QComboBox::drop-down {
                border: none;
            }

            QComboBox QAbstractItemView { /* Styling for the dropdown list items */
                background-color: #4E4E4E;
                color: #FFFFFF;
                selection-background-color: #6E6E6E;
                border: 1px solid #777777;
            }

            QTextEdit {
                background-color: #3C3C3C;
                color: #E0E0E0;
                border: 1px solid #555555;
                padding: 5px;
                font-size: 14px;
                border-radius: 4px;
            }

            QStatusBar {
                color: #E0E0E0;
            }

            QStatusBar::item {
                border: none; /* Remove borders between status bar items */
            }

            /* Styling for the ImagePreviewWidget specifically */
            ImagePreviewWidget {
                border: 2px dashed #555555; /* Darker dashed border for preview */
                min-height: 200px;
            }

            ImagePreviewWidget[dragging="true"] {
                border: 2px dashed #007ACC; /* Blue border when dragging */
                background-color: #3A3A3A;
            }
        """)
        
    def init_ui(self):
        """Initialize the user interface"""

        # Image selection label and button (will remain in central widget for now)
        self.image_label = QLabel("No image selected")
        self.image_label.setAlignment(Qt.AlignCenter)

        select_image_btn = QPushButton("Select Image")
        select_image_btn.clicked.connect(self.select_image)

        # Image Preview Dock
        self.image_preview = ImagePreviewWidget(self)
        self.image_preview.setAlignment(Qt.AlignCenter)
        # The setStyleSheet call for image_preview is removed, will be handled by global QSS
        image_preview_dock = QDockWidget("Image Preview", self)
        image_preview_dock.setWidget(self.image_preview)
        self.addDockWidget(Qt.TopDockWidgetArea, image_preview_dock)

        # Text Input Dock
        self.text_input = QTextEdit()
        self.text_input.setPlaceholderText("Enter message to encode...")
        self.text_input.setAcceptDrops(False)
        text_input_dock = QDockWidget("Message", self)
        text_input_dock.setWidget(self.text_input)
        self.addDockWidget(Qt.BottomDockWidgetArea, text_input_dock)

        # Encoding Options Dock
        self.method_combo = QComboBox()
        self.method_combo.addItems([
            "LSB Encoding",
            "Alpha Channel Encoding",
            "Direct Alpha Encoding",
            "Combined Encoding"
        ])
        
        options_container_widget = QWidget()
        options_layout = QHBoxLayout(options_container_widget)
        options_layout.addWidget(QLabel("Encoding Method:"))
        options_layout.addWidget(self.method_combo)
        
        encoding_options_dock = QDockWidget("Encoding Options", self)
        encoding_options_dock.setWidget(options_container_widget)
        self.addDockWidget(Qt.LeftDockWidgetArea, encoding_options_dock)

        # Buttons (will remain in central widget for now)
        encode_btn = QPushButton("Encode")
        encode_btn.clicked.connect(self.encode_message)
        
        decode_btn = QPushButton("Decode")
        decode_btn.clicked.connect(self.decode_message)
        
        # Status bar
        self.status_bar = self.statusBar()
        
        # Central Widget setup
        main_widget = QWidget()
        main_layout = QVBoxLayout(main_widget)
        main_layout.addWidget(self.image_label)
        main_layout.addWidget(select_image_btn)
        main_layout.addWidget(encode_btn)
        main_layout.addWidget(decode_btn)
        
        self.setCentralWidget(main_widget)

        # Connect signals for dynamic updates
        self.method_combo.currentIndexChanged.connect(self.update_status_bar_capacity)
        
    def update_status_bar_capacity(self):
        """Updates the status bar with the max message capacity for the current image and method."""
        if hasattr(self.encoder, 'image_path') and self.encoder.image_path and self.encoder.image:
            try:
                method = self.method_combo.currentText().lower().split()[0]
                capacity = calculate_max_capacity(self.encoder.image_path, method)
                self.status_bar.showMessage(f"Max message capacity: {capacity} characters")
            except Exception as e:
                # Handle cases where capacity calculation might fail or image not fully loaded
                self.status_bar.showMessage(f"Could not calculate capacity: {e}")
        elif hasattr(self.encoder, 'image') and self.encoder.image:
            # If image is loaded but no path (e.g. if image was passed as object, not path)
            # This case might need more robust handling in calculate_max_capacity if it only takes path
            self.status_bar.showMessage("Capacity unknown (image loaded without path).")
        else:
            self.status_bar.showMessage("No image loaded or method selected.")


    def select_image(self, file_path=None):
        """Handle image selection"""
        if not file_path:
            file_path, _ = QFileDialog.getOpenFileName(
                self, "Select Image", "", "Images (*.png *.bmp *.tiff)"
            )
        
        if file_path:
            valid, error = validate_image_format(file_path)
            if not valid:
                QMessageBox.warning(self, "Invalid Image", error)
                return
                
            self.encoder.load_image(file_path)
            self.image_label.setText(file_path)
            
            # Update preview
            preview = get_image_preview(file_path)
            from PIL.ImageQt import ImageQt
            from PyQt5.QtGui import QImage
            qimage = QImage(preview.tobytes(), preview.size[0], preview.size[1], QImage.Format_RGBA8888)
            self.image_preview.setPixmap(QPixmap.fromImage(qimage))
            
            # Update status
            self.encoder.image_path = file_path # Store image path in encoder instance
            self.update_status_bar_capacity()
            
    def encode_message(self):
        """Handle message encoding"""
        if not self.encoder.image:
            QMessageBox.warning(self, "Error", "No image selected")
            return
            
        message = self.text_input.toPlainText()
        if not message:
            QMessageBox.warning(self, "Error", "No message to encode")
            return
            
        try:
            method = self.method_combo.currentText().lower().split()[0]
            if method == 'lsb':
                self.encoder.encode_lsb(message)
            elif method == 'alpha':
                self.encoder.encode_alpha(message)
            elif method == 'direct':
                self.encoder.encode_direct_alpha(message)
            else:  # combined
                self.encoder.encode_combined(message)
                
            # Save encoded image
            file_path, _ = QFileDialog.getSaveFileName(
                self, "Save Encoded Image", "", "PNG Image (*.png)"
            )
            if file_path:
                self.encoder.save_image(file_path)
                QMessageBox.information(self, "Success", "Message encoded successfully")
                
        except Exception as e:
            QMessageBox.critical(self, "Error", str(e))
            
    def decode_message(self):
        """Handle message decoding"""
        if not self.encoder.image:
            QMessageBox.warning(self, "Error", "No image selected")
            return
            
        try:
            method = self.method_combo.currentText().lower().split()[0]
            if method == 'lsb':
                message = self.encoder.decode_lsb()
            elif method == 'alpha':
                message = self.encoder.decode_alpha()
            else:  # direct
                message = self.encoder.decode_direct_alpha()
                
            self.text_input.setPlainText(message)
            QMessageBox.information(self, "Decoded Message", message)
            
        except Exception as e:
            QMessageBox.critical(self, "Error", str(e))