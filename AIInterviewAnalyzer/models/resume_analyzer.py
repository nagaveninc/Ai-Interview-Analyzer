import os
import pdfplumber
from docx import Document


class ResumeAnalyzer:

    def __init__(self):

        self.skills = [
            "python",
            "java",
            "c",
            "c++",
            "html",
            "css",
            "javascript",
            "flask",
            "mysql",
            "sql",
            "mongodb",
            "react",
            "node",
            "django",
            "machine learning",
            "artificial intelligence",
            "deep learning",
            "data science",
            "git",
            "github",
            "aws",
            "azure",
            "cloud"
        ]


    def extract_text(self, filepath):

        text = ""

        extension = os.path.splitext(filepath)[1].lower()

        if extension == ".pdf":

            with pdfplumber.open(filepath) as pdf:

                for page in pdf.pages:

                    page_text = page.extract_text()

                    if page_text:
                        text += page_text + "\n"

        elif extension == ".docx":

            doc = Document(filepath)

            for para in doc.paragraphs:

                text += para.text + "\n"

        return text


    def analyze(self, filepath):

        text = self.extract_text(filepath).lower()

        found_skills = []

        for skill in self.skills:

            if skill in text:

                found_skills.append(skill.title())

        ats_score = min(100, len(found_skills) * 5)

        suggestions = []

        if "github" not in text:
            suggestions.append("Add your GitHub profile.")

        if "projects" not in text:
            suggestions.append("Include more academic or personal projects.")

        if "internship" not in text:
            suggestions.append("Mention internships if available.")

        if len(found_skills) < 10:
            suggestions.append("Add more technical skills.")

        return {

            "skills": found_skills,

            "ats_score": ats_score,

            "suggestions": suggestions,

            "text": text
        }