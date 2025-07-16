# 📝 Resume Parser AI (Internship Project @ Pinnacle Labs)

This project is a Python-based Resume Parser designed to automatically extract key information from resumes in **PDF** or **DOCX** formats using Natural Language Processing techniques. Built during my internship at **Pinnacle Labs Pvt Ltd**, it’s a practical application of NLP, regex, and document parsing, with a modular design for easy customization and extension.

---

## 🚀 Features

- ✅ Extracts **Name**, **Email**, and **Phone Number**
- ✅ Identifies **Skills** from a predefined database
- ✅ Detects **Education** and **Experience** sections
- ✅ Supports `.pdf` and `.docx` resume formats
- ✅ CLI-driven interface for quick usage
- ✅ Written with modular, beginner-friendly Python code

---

## 🧰 Tech Stack

| Tool            | Purpose                               |
|----------------|----------------------------------------|
| `pdfplumber`    | Extracts text from PDF files           |
| `python-docx`   | Reads content from DOCX documents      |
| `spaCy`         | NLP processing (tokenization, POS, NER)|
| `regex (re)`    | Pattern matching for email/phone       |
| `pathlib`       | Validates file paths and extensions    |

---

## 📦 Installation

Before running the script, make sure these dependencies are installed:

```bash
pip install pdfplumber python-docx spacy
python -m spacy download en_core_web_sm
