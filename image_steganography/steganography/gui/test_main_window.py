import unittest
from unittest.mock import patch, MagicMock
import os
import sys

# Ensure the application path is in sys.path to import MainWindow and other components
# This assumes the test file is in image_steganography/steganography/gui/
# and the root of the 'image_steganography' module is three levels up from there.
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../..')))

from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QPushButton, QDockWidget
from PyQt5.QtTest import QTest
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap

from image_steganography.steganography.gui.main_window import MainWindow, ImagePreviewWidget
from image_steganography.steganography.encoder import ImageEncoder # For mocking

# It's good practice to have one QApplication instance for all tests
app = QApplication.instance()
if app is None:
    app = QApplication(sys.argv)

class TestMainWindowInteractions(unittest.TestCase):
    dummy_image_path = os.path.join(os.path.dirname(__file__), "dummy_test_image.png")

    @classmethod
    def setUpClass(cls):
        # Create a dummy image for testing image loading
        try:
            from PIL import Image
            # Check if Pillow is available and create the image
            if Image.__file__: # A simple check if Image is not a mock or something unexpected
                img = Image.new('RGBA', (60, 30), color = (255, 0, 0, 255)) # RGBA for PNG
                img.save(cls.dummy_image_path, "PNG")
            else:
                raise ImportError("Pillow's Image module seems unusual.")
        except ImportError:
            print(f"Pillow not found or failed to create image, creating empty file for {cls.dummy_image_path}. Image tests might be skipped or fail.")
            # Create an empty file if Pillow is not there, so os.path.exists works, but tests should skip.
            with open(cls.dummy_image_path, 'wb') as f: # wb for binary context if some code expects read bytes
                pass
        except Exception as e:
            print(f"Failed to create dummy image: {e}. Image tests might be skipped or fail.")
            with open(cls.dummy_image_path, 'wb') as f:
                pass


    @classmethod
    def tearDownClass(cls):
        # Clean up the dummy image
        if os.path.exists(cls.dummy_image_path):
            try:
                os.remove(cls.dummy_image_path)
            except OSError as e:
                print(f"Error removing dummy image: {e}")

    def setUp(self):
        """Set up for each test."""
        self.window = MainWindow()
        # It's important to set object names in MainWindow for robust testing
        # e.g., self.image_preview_dock.setObjectName("imagePreviewDock")
        # For now, we find them by searching for QDockWidget type and checking titles or contained widgets.

        self.window.show() # Window must be shown for some QTest events and widget properties
        QApplication.processEvents() # Ensure window is processed

        # Find dock widgets. A more robust way is self.window.findChild(QDockWidget, "objectName")
        all_dock_widgets = self.window.findChildren(QDockWidget)
        self.image_preview_dock = None
        self.message_dock = None
        self.options_dock = None

        for dock in all_dock_widgets:
            if dock.windowTitle() == "Image Preview": # Assuming titles are set
                self.image_preview_dock = dock
            elif dock.windowTitle() == "Message":
                self.message_dock = dock
            elif dock.windowTitle() == "Encoding Options":
                self.options_dock = dock

        # Fallback if titles didn't match (e.g. changed by stylesheet or other reasons)
        # This relies on the specific widget being the direct child of the QDockWidget's content area
        # or the QDockWidget itself if setWidget was used directly with these.
        if not self.image_preview_dock and hasattr(self.window, 'image_preview'):
            # image_preview is the widget set on the dock. Its parent should be the dock.
            if isinstance(self.window.image_preview.parentWidget(), QDockWidget):
                 self.image_preview_dock = self.window.image_preview.parentWidget()

        if not self.message_dock and hasattr(self.window, 'text_input'):
            if isinstance(self.window.text_input.parentWidget(), QDockWidget):
                 self.message_dock = self.window.text_input.parentWidget()

        if not self.options_dock and hasattr(self.window, 'method_combo'):
            # method_combo is inside a QWidget container, which is then set on the dock.
            # So, parent of method_combo is QWidget, parent of QWidget is QDockWidget.
            container_widget = self.window.method_combo.parentWidget()
            if container_widget and isinstance(container_widget.parentWidget(), QDockWidget):
                self.options_dock = container_widget.parentWidget()


    def tearDown(self):
        """Clean up after each test."""
        self.window.close()
        QApplication.processEvents() # Process close events
        del self.window


    def test_docks_exist(self):
        """Test that the dock widgets were found."""
        self.assertIsNotNone(self.image_preview_dock, "Image Preview dock could not be identified.")
        self.assertIsNotNone(self.message_dock, "Message dock could not be identified.")
        self.assertIsNotNone(self.options_dock, "Encoding Options dock could not be identified.")

    def test_dock_widget_float_and_dock(self):
        """Test floating and docking a dock widget."""
        if not self.image_preview_dock:
            self.skipTest("Image Preview dock not identified for test.")

        self.window.addDockWidget(Qt.TopDockWidgetArea, self.image_preview_dock) # Ensure it's docked first
        self.image_preview_dock.setVisible(True) # Ensure visible
        QApplication.processEvents()

        self.image_preview_dock.setFloating(True)
        self.assertTrue(self.image_preview_dock.isFloating())
        QApplication.processEvents()

        self.image_preview_dock.setFloating(False)
        self.assertFalse(self.image_preview_dock.isFloating())
        QApplication.processEvents()
        self.assertIn(self.window.dockWidgetArea(self.image_preview_dock),
                      [Qt.TopDockWidgetArea, Qt.BottomDockWidgetArea, Qt.LeftDockWidgetArea, Qt.RightDockWidgetArea, Qt.AllDockWidgetAreas])


    def test_dock_widget_move_area(self):
        """Test moving a dock widget to a different area."""
        if not self.message_dock:
            self.skipTest("Message dock not identified for test.")

        self.message_dock.setFloating(False) # Ensure it's not floating
        self.message_dock.setVisible(True)
        QApplication.processEvents()

        original_area = self.window.dockWidgetArea(self.message_dock)
        if original_area == Qt.NoDockWidgetArea: # If it was floating or not yet placed
            self.window.addDockWidget(Qt.BottomDockWidgetArea, self.message_dock)
            original_area = Qt.BottomDockWidgetArea
            QApplication.processEvents()

        target_area = Qt.RightDockWidgetArea
        if original_area == target_area:
            target_area = Qt.LeftDockWidgetArea

        self.window.addDockWidget(target_area, self.message_dock)
        QApplication.processEvents()
        self.assertEqual(self.window.dockWidgetArea(self.message_dock), target_area)


    @patch('image_steganography.steganography.gui.main_window.QFileDialog.getOpenFileName')
    def test_image_selection_updates_ui(self, mock_get_open_file_name):
        """Test UI updates on image selection."""
        if not os.path.exists(self.dummy_image_path) or os.path.getsize(self.dummy_image_path) == 0:
            self.skipTest(f"Dummy image {self.dummy_image_path} not available or empty. Pillow might be missing or failed.")

        mock_get_open_file_name.return_value = (self.dummy_image_path, "Images (*.png *.bmp *.tiff)")

        select_button = self.window.findChild(QPushButton, "selectImageBtn") # Assuming objectName is set
        if not select_button: # Fallback to text search if objectName not set
            for btn in self.window.findChildren(QPushButton):
                if "Select Image" in btn.text():
                    select_button = btn
                    break

        self.assertIsNotNone(select_button, "Select Image button not found.")
        if not select_button: return

        QTest.mouseClick(select_button, Qt.LeftButton)
        QApplication.processEvents()

        self.assertEqual(self.window.image_label.text(), self.dummy_image_path)
        self.assertIsNotNone(self.window.image_preview.pixmap(), "Pixmap should be set.")
        self.assertFalse(self.window.image_preview.pixmap().isNull(), "Pixmap should not be null.")

        self.assertTrue("capacity" in self.window.status_bar.currentMessage().lower(),
                        f"Status bar message '{self.window.status_bar.currentMessage()}' does not contain 'capacity'.")

        initial_message = self.window.status_bar.currentMessage()
        self.window.method_combo.setCurrentIndex(1)
        QApplication.processEvents()
        self.assertNotEqual(self.window.status_bar.currentMessage(), initial_message, "Status bar message should change with encoding method.")
        self.assertTrue("capacity" in self.window.status_bar.currentMessage().lower())


    @patch.object(MainWindow, 'encode_message') # We are testing decode, so encode is not primary here, but let's use a more specific mock for decode
    @patch.object(ImageEncoder, 'decode_lsb', return_value="Test decoded message LSB")
    @patch.object(ImageEncoder, 'decode_alpha', return_value="Test decoded message Alpha")
    @patch.object(ImageEncoder, 'decode_direct_alpha', return_value="Test decoded message Direct Alpha")
    @patch('image_steganography.steganography.gui.main_window.QMessageBox.information') # Mock the success dialog
    def test_decode_updates_text_input(self, mock_qmessagebox, mock_decode_direct, mock_decode_alpha, mock_decode_lsb, mock_encode_call_not_used_here):
        """Test that decoding updates the text input area and shows a dialog."""
        if not os.path.exists(self.dummy_image_path) or os.path.getsize(self.dummy_image_path) == 0:
            self.skipTest(f"Dummy image {self.dummy_image_path} not available. Decode test relies on image being 'loaded'.")

        # Simulate that an image is loaded by setting the encoder's image path and a mock image object
        self.window.encoder.image_path = self.dummy_image_path
        self.window.encoder.image = MagicMock(spec_set=["mode", "size", "getpixel", "putpixel", "copy", "save"]) # Mock a PIL image
        self.window.encoder.image.mode = 'RGBA'
        self.window.encoder.image.size = (100,100)


        decode_button = None
        for btn in self.window.findChildren(QPushButton):
            if "Decode" in btn.text():
                decode_button = btn
                break
        self.assertIsNotNone(decode_button, "Decode button not found.")
        if not decode_button: return

        test_cases = [
            ("LSB Encoding", mock_decode_lsb, "Test decoded message LSB"),
            ("Alpha Channel Encoding", mock_decode_alpha, "Test decoded message Alpha"),
            ("Direct Alpha Encoding", mock_decode_direct, "Test decoded message Direct Alpha"),
        ]

        for i, (method_name, mock_decoder, expected_text) in enumerate(test_cases):
            self.window.method_combo.setCurrentText(method_name)
            QApplication.processEvents()

            # Reset text input for each case
            self.window.text_input.clear()
            QApplication.processEvents()

            QTest.mouseClick(decode_button, Qt.LeftButton)
            QApplication.processEvents()

            self.assertEqual(self.window.text_input.toPlainText(), expected_text, f"Failed for {method_name}")
            # QMessageBox.information should be called with (parent, title, message_text)
            # We check that the message_text is what we expect
            mock_qmessagebox.assert_called_with(self.window, "Decoded Message", expected_text)
            mock_decoder.assert_called_once()
            mock_decoder.reset_mock() # Reset for the next iteration
            mock_qmessagebox.reset_mock()


if __name__ == '__main__':
    # This allows running the tests directly from this file, e.g. for debugging.
    # Ensure QApplication is created before tests.
    if QApplication.instance() is None:
        local_app = QApplication(sys.argv)

    # For running in headless environments like CI, Xvfb might be needed.
    # Example: xvfb-run python -m unittest test_main_window.py
    unittest.main(argv=[sys.argv[0]] + sys.argv[1:], exit=False)
