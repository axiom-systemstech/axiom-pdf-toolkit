import unittest
import os
from axiom_pdf.cli import AxiomPDF


class TestAxiomPDF(unittest.TestCase):
    def setUp(self):
        self.toolkit = AxiomPDF()
    
    def test_module_imports(self):
        """Test that all dependencies are available"""
        try:
            import PyPDF2
            import pypdf
            import pdf2image
            from PIL import Image
            self.assertTrue(True)
        except ImportError:
            self.assertTrue(False)
    
    def test_functions_exist(self):
        """Test that all methods exist"""
        self.assertTrue(hasattr(self.toolkit, 'merge'))
        self.assertTrue(hasattr(self.toolkit, 'split'))
        self.assertTrue(hasattr(self.toolkit, 'compress'))
        self.assertTrue(hasattr(self.toolkit, 'protect'))
        self.assertTrue(hasattr(self.toolkit, 'extract_text'))
        self.assertTrue(hasattr(self.toolkit, 'extract_images'))
        self.assertTrue(hasattr(self.toolkit, 'rotate'))


if __name__ == "__main__":
    unittest.main()
