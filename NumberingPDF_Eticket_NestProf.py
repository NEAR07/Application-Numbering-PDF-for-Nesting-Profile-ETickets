from PyPDF2 import PdfReader, PdfWriter
from reportlab.pdfgen import canvas
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from io import BytesIO
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QPushButton, QLabel, QLineEdit, QVBoxLayout, QHBoxLayout, QFileDialog, QWidget, QGraphicsView, QGraphicsScene, QComboBox
)
from PyQt5.QtGui import QImage, QPixmap, QFont
from PyQt5.QtCore import Qt
import fitz
import os
import io

class PDFNumberingApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Numbering PDF Eticket Nesting Profile")
        self.setGeometry(100, 100, 1000, 600) # Window size for file reading

        # Init variables
        self.input_pdf_path = ""
        self.reader = None
        self.writer = PdfWriter()
        self.current_page = 0
        self.total_pages = 0
        self.page_data = {}
        self.paper_size = "A3" # Default paper size

        # Layout and widgets
        main_layout = QVBoxLayout()

        # Graphics view for displaying PDF
        self.pdf_view = QGraphicsView()
        self.pdf_scene = QGraphicsScene()
        self.pdf_view.setScene(self.pdf_scene)
        main_layout.addWidget(self.pdf_view)

        # User Interface
        # Information label
        self.label_info = QLabel("Upload a PDF file to start.")
        self.label_info.setFont(QFont("Arial", 10))
        main_layout.addWidget(self.label_info)

        # Choose paper size
        self.paper_size_label = QLabel("Select Paper Size: ")
        self.paper_size_label.setFont(QFont("Arial", 9))
        main_layout.addWidget(self.paper_size_label)

        self.paper_size_dropdown = QComboBox()
        self.paper_size_dropdown.setFont(QFont("Arial", 9))
        # self.paper_size_dropdown.addItems(["A3", "A4", "A5"]) #ada opsi 3
        self.paper_size_dropdown.addItems(["A3"]) #khusus A3
        self.paper_size_dropdown.setCurrentText("A3")
        self.paper_size_dropdown.currentTextChanged.connect(self.set_paper_size)  # Connect signal after the method definition
        main_layout.addWidget(self.paper_size_dropdown)

        # Input fields for block and sheet numbers
        form_layout = QVBoxLayout()

        self.block_label = QLabel("Block Number: ")
        self.block_label.setFont(QFont("Arial", 9))
        form_layout.addWidget(self.block_label)
        self.block_input = QLineEdit()
        self.block_input.setFont(QFont("Arial", 9))
        form_layout.addWidget(self.block_input)

        self.sheet_label = QLabel("Sheet Number: ")  # Corrected from block_label to sheet_label
        self.sheet_label.setFont(QFont("Arial", 9))
        form_layout.addWidget(self.sheet_label)
        self.sheet_input = QLineEdit()
        self.sheet_input.setFont(QFont("Arial", 9))
        form_layout.addWidget(self.sheet_input)

        main_layout.addLayout(form_layout)

        # Horiziontal layout for buttons
        button_layout = QHBoxLayout()

        self.upload_button = QPushButton("Upload PDF")
        self.upload_button.setFont(QFont("Arial", 9))
        self.upload_button.setFixedSize(120, 40)
        self.upload_button.setStyleSheet("""
            background-color: #4CAF50;
            color: white;
            border: none;
            border-radius: 5px;
            font-weight: bold;
        """) # Green background
        self.upload_button.clicked.connect(self.upload_pdf)
        button_layout.addWidget(self.upload_button)

        self.back_button = QPushButton("Previous Page")        
        self.back_button.setFont(QFont("Arial", 9))
        self.back_button.setFixedSize(135, 40)
        self.back_button.setStyleSheet("""
            background-color: #FFC107;
            color: white;
            border: none;
            border-radius: 5px;
            font-weight: bold;
        """) # Yellow background     
        self.back_button.clicked.connect(self.back_page)
        self.back_button.setEnabled(False)
        button_layout.addWidget(self.back_button)

        self.next_button = QPushButton("Next Page")        
        self.next_button.setFont(QFont("Arial", 9))
        self.next_button.setFixedSize(120, 40)
        self.next_button.setStyleSheet("""
            background-color: #2196F3;
            color: white;
            border: none;
            border-radius: 5px;
            font-weight: bold;
        """) # Blue background 
        self.next_button.clicked.connect(self.next_page)
        self.next_button.setEnabled(False)
        button_layout.addWidget(self.next_button)

        self.finish_button = QPushButton("Finish")        
        self.finish_button.setFont(QFont("Arial", 9))
        self.finish_button.setFixedSize(120, 40)
        self.finish_button.setStyleSheet("""
            background-color: #FF5722;
            color: white;
            border: none;
            border-radius: 5px;
            font-weight: bold;
        """) # Red background 
        self.finish_button.clicked.connect(self.finish)
        self.finish_button.setEnabled(False)
        button_layout.addWidget(self.finish_button)

        self.quit_button = QPushButton("Quit")        
        self.quit_button.setFont(QFont("Arial", 9))
        self.quit_button.setFixedSize(120, 40)
        self.quit_button.setStyleSheet("""
            background-color: #9E9E9E;
            color: white;
            border: none;
            border-radius: 5px;
            font-weight: bold;
        """) # Gray background 
        self.quit_button.clicked.connect(self.quit_program)
        button_layout.addWidget(self.quit_button)

        main_layout.addLayout(button_layout)

        # Central Widget
        central_widget = QWidget()
        central_widget.setLayout(main_layout)
        self.setCentralWidget(central_widget)

    def set_paper_size(self, size):
        """Set the paper size."""
        self.paper_size = size
        
    def upload_pdf(self):
        """Handle uploading and displaying the PDF."""
        self.reset_state()

        self.input_pdf_path, _ = QFileDialog.getOpenFileName(self, "Select PDF File", "", "PDF Files (*.pdf)")
        if self.input_pdf_path:
            self.reader = PdfReader(self.input_pdf_path)
            self.total_pages = len(self.reader.pages)
            self.label_info.setText(f"Loaded PDF with {self.total_pages} pages.")
            self.next_button.setEnabled(True)
            self.finish_button.setEnabled(True)

            # Display the first page
            self.display_pdf_page(0)

    def display_pdf_page(self, page_number):
        """Display the specified page in the QGraphicsView."""
        doc = fitz.open(self.input_pdf_path)
        page = doc[page_number]
        pix = page.get_pixmap()
        qt_image = QImage(pix.samples, pix.width, pix.height, pix.stride, QImage.Format_RGB888)
        pixmap = QPixmap.fromImage(qt_image)
        
        # Clear the scene before adding a new pixmap
        self.pdf_scene.clear()
        
        # Add the pixmap to the scene
        self.pdf_scene.addPixmap(pixmap)
        
        # Set alignment to center
        self.pdf_view.setAlignment(Qt.AlignCenter)

    def next_page(self):
        """Go to the next page."""
        self.save_current_page_data()  # Save current page data before switching
        if self.current_page < self.total_pages - 1:
            self.current_page += 1
            self.update_page_inputs()  # Load data for the next page
            self.display_pdf_page(self.current_page)

    def back_page(self):
        """Go to the previous page."""
        self.save_current_page_data()  # Save current page data before switching
        if self.current_page > 0:
            self.current_page -= 1
            self.update_page_inputs()  # Load data for the previous page
            self.display_pdf_page(self.current_page)

    def save_current_page_data(self):
        """Save block and sheet input for the current page."""
        block_number = self.block_input.text()
        sheet_number = self.sheet_input.text()
        # Save the data into the dictionary
        self.page_data[self.current_page] = {"block": block_number, "sheet": sheet_number}

    def update_page_inputs(self):
        """Update input fields based on saved data or use previous page's data."""
        if self.current_page in self.page_data:
            # If data exists for this page, load it
            self.block_input.setText(self.page_data[self.current_page].get("block", ""))
            self.sheet_input.setText(self.page_data[self.current_page].get("sheet", ""))
        else:
            # If no data exists for this page, use the previous page's data
            if self.current_page > 0 and (self.current_page - 1) in self.page_data:
                self.block_input.setText(self.page_data[self.current_page - 1].get("block", ""))
                self.sheet_input.setText(self.page_data[self.current_page - 1].get("sheet", ""))
            else:
                # If there's no previous data, clear the inputs
                self.block_input.clear()
                self.sheet_input.clear()

        # Update the label and button states
        self.label_info.setText(f"Editing page {self.current_page + 1} of {self.total_pages}")
        self.next_button.setEnabled(self.current_page < self.total_pages - 1)
        self.back_button.setEnabled(self.current_page > 0)

    def get_text_position(self):
        """Get text position based on paper size."""
        positions = {
            "A3" : (740, 18),
            # "A4" : (500, 40),
            # "A5" : (500, 40),
        }
        return positions.get(self.paper_size, (740, 18))

    def finish(self):
        """Process PDF and add block and sheet data with Verdana font."""
        font_path = r"C:\Windows\Fonts\verdana.ttf"  
        pdfmetrics.registerFont(TTFont("Verdana", font_path))  

        self.save_current_page_data()  # Save user input
        
        # Prompt user to select output path
        output_path, _ = QFileDialog.getSaveFileName(self, "Save PDF File", "", "PDF Files (*.pdf)")
        if not output_path:
            self.label_info.setText("Save operation canceled.")
            return  # Exit if the user cancels the save dialog

        # Ensure the file has .pdf extension
        if not output_path.endswith(".pdf"):
            output_path += ".pdf"
        
        temp_files = []  # To save temporary files
        doc = fitz.open(self.input_pdf_path)  # Open original PDF

        for i in range(self.total_pages):
            block = self.page_data.get(i, {}).get("block", "")
            sheet = self.page_data.get(i, {}).get("sheet", "")
            if block or sheet:  # Add text only if there is data
                # Page dimensions
                page = doc[i]
                rect = page.rect

                # Create temporary PDFs with ReportLab
                temp_pdf = BytesIO()
                c = canvas.Canvas(temp_pdf, pagesize=(rect.width, rect.height))
                c.setFont("Verdana", 6)  # Verdana font size

                # Text position
                x, y = self.get_text_position()
                c.drawString(x + 12.5, y + 10.2, f"{block}")  # Text to block
                c.drawString(x + 1, y - 0.4, f"{sheet}")   # Text to sheet

                c.save()
                temp_pdf.seek(0)
                temp_files.append(temp_pdf)

                # Merge original page and text
                temp_doc = fitz.open(stream=temp_pdf.read(), filetype="pdf")
                page.show_pdf_page(page.rect, temp_doc, 0)

        # Save new document
        doc.save(output_path)
        doc.close()

        # Clean up temporary files
        for temp_file in temp_files:
            temp_file.close()

        self.label_info.setText(f"Proses selesai. Perubahan disimpan ke {output_path}.")


    def quit_program(self):
        """Quit the applications."""
        self.close()

    def reset_state(self):
        """Reset the application state."""
        self.input_pdf_path = ""
        self.reader = None
        self.writer = PdfWriter()
        self.current_page = 0
        self.total_pages = 0
        self.page_data = {}

        # Clear the graphics scene
        if hasattr(self, 'pdf_scene'):
            self.pdf_scene.clear()

        # Reset UI elements
        if hasattr(self, 'label_info'):
            self.label_info.setText("Upload a PDF file to start.")
        if hasattr(self, 'block_input'):
            self.block_input.clear()
        if hasattr(self, 'sheet_input'):
            self.sheet_input.clear()
        if hasattr(self, 'next_button'):
            self.next_button.setEnabled(False)
        if hasattr(self, 'back_button'):
            self.back_button.setEnabled(False)
        if hasattr(self, 'finish_button'):
            self.finish_button.setEnabled(False)

# Run the application
if __name__ == "__main__":
    app = QApplication([])
    window = PDFNumberingApp()
    window.show()
    app.exec_()
