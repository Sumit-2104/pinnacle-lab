import re
import json
import csv
import pdfplumber
import docx
import spacy
from pathlib import Path
from tkinter import *
from tkinter import filedialog, messagebox, ttk
from spacy.matcher import Matcher

# Load spaCy NLP model
nlp = spacy.load("en_core_web_sm")
matcher = Matcher(nlp.vocab)

# Skills database (expand as needed)
SKILLS_DB = [
    "Python", "Java", "Machine Learning", "SQL", "React", 
    "AWS", "Docker", "Flask", "Git", "JavaScript",
    "TensorFlow", "PyTorch", "Data Analysis", "C++", "HTML/CSS"
]

class ResumeParser:
    def __init__(self, file_path):
        self.file_path = file_path
        self.text = self.extract_text()
        self.doc = nlp(self.text)
        self.data = {
            "name": None,
            "email": None,
            "phone": None,
            "skills": [],
            "education": [],
            "experience": []
        }
    
    def extract_text(self):
        """Extract text from PDF or DOCX"""
        if self.file_path.endswith(".pdf"):
            with pdfplumber.open(self.file_path) as pdf:
                return "\n".join([page.extract_text() for page in pdf.pages])
        elif self.file_path.endswith(".docx"):
            doc = docx.Document(self.file_path)
            return "\n".join([para.text for para in doc.paragraphs])
        else:
            raise ValueError("Unsupported file format")
    
    def extract_name(self):
        """Extract name using pattern matching"""
        name_pattern = [{"POS": "PROPN"}, {"POS": "PROPN"}]
        matcher.add("NAME", [name_pattern])
        matches = matcher(self.doc)
        
        for match_id, start, end in matches:
            span = self.doc[start:end]
            self.data["name"] = span.text
            break
        
        if not self.data["name"]:
            self.data["name"] = self.text.split('\n')[0].strip()
    
    def extract_email(self):
        email = re.findall(r"[a-z0-9\.\-+_]+@[a-z0-9\.\-+_]+\.[a-z]+", self.text, re.IGNORECASE)
        if email:
            self.data["email"] = email[0]
    
    def extract_phone(self):
        phone = re.findall(r"[\+\(]?[1-9][0-9 .\-\(\)]{8,}[0-9]", self.text)
        if phone:
            self.data["phone"] = phone[0]
    
    def extract_skills(self):
        skills = []
        for token in self.doc:
            if token.text in SKILLS_DB:
                skills.append(token.text)
        for chunk in self.doc.noun_chunks:
            if chunk.text in SKILLS_DB:
                skills.append(chunk.text)
        self.data["skills"] = list(set(skills))
    
    def extract_education(self):
        edu_keywords = ["B.Sc", "B.Tech", "M.Sc", "Ph.D", "University", "College"]
        sentences = [sent.text.strip() for sent in self.doc.sents]
        edu = []
        for sentence in sentences:
            for word in edu_keywords:
                if word.lower() in sentence.lower():
                    edu.append(sentence)
        self.data["education"] = edu
    
    def extract_experience(self):
        exp_keywords = ["Experience", "Work History", "Internship", "Job"]
        sentences = [sent.text.strip() for sent in self.doc.sents]
        exp = []
        for sentence in sentences:
            for word in exp_keywords:
                if word.lower() in sentence.lower():
                    exp.append(sentence)
        self.data["experience"] = exp
    
    def parse(self):
        self.extract_name()
        self.extract_email()
        self.extract_phone()
        self.extract_skills()
        self.extract_education()
        self.extract_experience()
        return self.data

class ResumeParserApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Resume Parser AI")
        self.root.geometry("800x600")
        
        # Styling
        self.style = ttk.Style()
        self.style.configure('TButton', font=('Helvetica', 10))
        self.style.configure('TLabel', font=('Helvetica', 11))
        
        # Main Frame
        self.main_frame = ttk.Frame(root, padding="20")
        self.main_frame.pack(fill=BOTH, expand=True)
        
        # Header
        ttk.Label(self.main_frame, text="Resume Parser AI", font=('Helvetica', 16, 'bold')).pack(pady=10)
        
        # Upload Section
        self.upload_frame = ttk.LabelFrame(self.main_frame, text="Upload Resume", padding=10)
        self.upload_frame.pack(fill=X, pady=10)
        
        self.btn_browse = ttk.Button(self.upload_frame, text="Browse", command=self.browse_file)
        self.btn_browse.pack(side=LEFT, padx=5)
        
        self.btn_parse = ttk.Button(self.upload_frame, text="Parse Resume", command=self.parse_resume, state=DISABLED)
        self.btn_parse.pack(side=LEFT, padx=5)
        
        self.file_path = StringVar()
        ttk.Label(self.upload_frame, textvariable=self.file_path).pack(side=LEFT, padx=5)
        
        # Results Section
        self.results_frame = ttk.LabelFrame(self.main_frame, text="Extracted Information", padding=10)
        self.results_frame.pack(fill=BOTH, expand=True, pady=10)
        
        self.text_results = Text(self.results_frame, wrap=WORD, font=('Helvetica', 10))
        self.scrollbar = ttk.Scrollbar(self.results_frame, orient=VERTICAL, command=self.text_results.yview)
        self.text_results.configure(yscrollcommand=self.scrollbar.set)
        
        self.scrollbar.pack(side=RIGHT, fill=Y)
        self.text_results.pack(fill=BOTH, expand=True)
        
        # Export Section
        self.export_frame = ttk.Frame(self.main_frame)
        self.export_frame.pack(fill=X, pady=10)
        
        self.btn_export_json = ttk.Button(self.export_frame, text="Export to JSON", command=lambda: self.export_data('json'))
        self.btn_export_json.pack(side=LEFT, padx=5)
        
        self.btn_export_csv = ttk.Button(self.export_frame, text="Export to CSV", command=lambda: self.export_data('csv'))
        self.btn_export_csv.pack(side=LEFT, padx=5)
        
        # Initialize
        self.parsed_data = None
    
    def browse_file(self):
        filetypes = [("Resume Files", "*.pdf *.docx")]
        filename = filedialog.askopenfilename(title="Select Resume", filetypes=filetypes)
        if filename:
            self.file_path.set(filename)
            self.btn_parse['state'] = NORMAL
    
    def parse_resume(self):
        try:
            parser = ResumeParser(self.file_path.get())
            self.parsed_data = parser.parse()
            
            # Display results
            self.text_results.delete(1.0, END)
            for key, value in self.parsed_data.items():
                self.text_results.insert(END, f"{key.upper()}:\n")
                if isinstance(value, list):
                    for item in value:
                        self.text_results.insert(END, f"  • {item}\n")
                else:
                    self.text_results.insert(END, f"  {value}\n")
                self.text_results.insert(END, "\n")
            
            messagebox.showinfo("Success", "Resume parsed successfully!")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to parse resume:\n{str(e)}")
    
    def export_data(self, format_type):
        if not self.parsed_data:
            messagebox.showwarning("Warning", "No data to export. Please parse a resume first.")
            return
        
        filetypes = [("JSON Files", "*.json")] if format_type == 'json' else [("CSV Files", "*.csv")]
        filename = filedialog.asksaveasfilename(
            title=f"Export as {format_type.upper()}",
            defaultextension=f".{format_type}",
            filetypes=filetypes
        )
        
        if not filename:
            return
        
        try:
            if format_type == 'json':
                with open(filename, 'w') as f:
                    json.dump(self.parsed_data, f, indent=4)
            else:
                # Flatten data for CSV
                csv_data = []
                for key, value in self.parsed_data.items():
                    if isinstance(value, list):
                        csv_data.append([key, "; ".join(value)])
                    else:
                        csv_data.append([key, value])
                
                with open(filename, 'w', newline='') as f:
                    writer = csv.writer(f)
                    writer.writerow(["Field", "Value"])
                    writer.writerows(csv_data)
            
            messagebox.showinfo("Success", f"Data exported successfully to {filename}")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to export data:\n{str(e)}")

if __name__ == "__main__":
    root = Tk()
    app = ResumeParserApp(root)
    root.mainloop()