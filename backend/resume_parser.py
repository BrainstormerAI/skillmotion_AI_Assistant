import fitz  # PyMuPDF
import pdfminer
from pdfminer.high_level import extract_text
from pdfminer.layout import LAParams
import re
import os

class ResumeParser:
    def __init__(self):
        self.supported_formats = ['.pdf']
    
    def extract_text_from_pdf(self, file_path):
        """Extract text from PDF using multiple methods for robustness"""
        try:
            # Method 1: Try PyMuPDF first (faster)
            return self._extract_with_fitz(file_path)
        except Exception as e:
            print(f"PyMuPDF failed: {e}")
            try:
                # Method 2: Fall back to pdfminer
                return self._extract_with_pdfminer(file_path)
            except Exception as e2:
                print(f"pdfminer failed: {e2}")
                raise Exception(f"Failed to extract text from PDF: {str(e2)}")
    
    def _extract_with_fitz(self, file_path):
        """Extract text using PyMuPDF/fitz"""
        doc = fitz.open(file_path)
        text = ""
        
        for page_num in range(doc.page_count):
            page = doc[page_num]
            text += page.get_text()
        
        doc.close()
        return self._clean_text(text)
    
    def _extract_with_pdfminer(self, file_path):
        """Extract text using pdfminer.six"""
        laparams = LAParams(
            line_margin=0.5,
            word_margin=0.1,
            char_margin=2.0,
            boxes_flow=0.5,
            all_texts=False
        )
        
        text = extract_text(file_path, laparams=laparams)
        return self._clean_text(text)
    
    def _clean_text(self, text):
        """Clean and normalize extracted text"""
        if not text:
            return ""
        
        # Remove excessive whitespace
        text = re.sub(r'\s+', ' ', text)
        
        # Remove special characters that might interfere with processing
        text = re.sub(r'[^\w\s@.,()-]', ' ', text)
        
        # Normalize line breaks
        text = text.replace('\n', ' ').replace('\r', ' ')
        
        # Remove multiple spaces
        text = re.sub(r' +', ' ', text)
        
        return text.strip()
    
    def extract_contact_info(self, text):
        """Extract contact information from resume text"""
        contact_info = {}
        
        # Email extraction
        email_pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
        emails = re.findall(email_pattern, text)
        if emails:
            contact_info['email'] = emails[0]
        
        # Phone number extraction
        phone_pattern = r'(\+?\d{1,3}[-.\s]?)?\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}'
        phones = re.findall(phone_pattern, text)
        if phones:
            contact_info['phone'] = ''.join(phones[0]) if isinstance(phones[0], tuple) else phones[0]
        
        # LinkedIn extraction
        linkedin_pattern = r'linkedin\.com/in/[\w-]+'
        linkedin = re.findall(linkedin_pattern, text, re.IGNORECASE)
        if linkedin:
            contact_info['linkedin'] = linkedin[0]
        
        return contact_info
    
    def extract_sections(self, text):
        """Extract common resume sections"""
        sections = {}
        
        # Common section headers
        section_patterns = {
            'experience': r'(work experience|professional experience|employment|experience)',
            'education': r'(education|academic background|qualifications)',
            'skills': r'(skills|technical skills|competencies|expertise)',
            'projects': r'(projects|personal projects|notable projects)',
            'certifications': r'(certifications|certificates|licenses)'
        }
        
        for section_name, pattern in section_patterns.items():
            # Find the section header
            matches = list(re.finditer(pattern, text, re.IGNORECASE))
            if matches:
                start_pos = matches[0].end()
                
                # Find the next section or end of text
                remaining_patterns = [p for name, p in section_patterns.items() if name != section_name]
                end_pos = len(text)
                
                for other_pattern in remaining_patterns:
                    other_matches = list(re.finditer(other_pattern, text[start_pos:], re.IGNORECASE))
                    if other_matches:
                        potential_end = start_pos + other_matches[0].start()
                        if potential_end < end_pos:
                            end_pos = potential_end
                
                sections[section_name] = text[start_pos:end_pos].strip()
        
        return sections
    
    def validate_file(self, file_path):
        """Validate if the file is a supported format and readable"""
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"File not found: {file_path}")
        
        file_ext = os.path.splitext(file_path)[1].lower()
        if file_ext not in self.supported_formats:
            raise ValueError(f"Unsupported file format: {file_ext}")
        
        # Check if file is readable
        try:
            with open(file_path, 'rb') as f:
                f.read(1024)  # Try to read first 1KB
        except Exception as e:
            raise Exception(f"File is not readable: {str(e)}")
        
        return True