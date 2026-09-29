import re
import spacy


# ==========================================
# LOAD SPACY NLP MODEL
# ==========================================

nlp = spacy.load("en_core_web_sm")


# ==========================================
# EMAIL EXTRACTION
# ==========================================

def extract_email(text):

    pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}\b'

    match = re.search(pattern, text)

    if match:
        return match.group().strip()

    return "Not found"


# ==========================================
# PHONE NUMBER EXTRACTION
# ==========================================

def extract_phone(text):

    patterns = [

        # Indian phone number with optional +91
        r'(?:\+91[\s-]?)?[6-9]\d{9}',

        # Phone numbers containing spaces/hyphens
        r'(?:\+91[\s-]?)?[6-9]\d{4}[\s-]\d{5}',

        # General international phone number
        r'\+\d{1,3}[\s-]?\d{7,12}'
    ]

    for pattern in patterns:

        match = re.search(pattern, text)

        if match:
            return match.group().strip()

    return "Not found"


# ==========================================
# NAME EXTRACTION
# ==========================================

def extract_name(text):

    # First try spaCy NER
    doc = nlp(text)

    for ent in doc.ents:

        if ent.label_ == "PERSON":

            name = ent.text.strip()

            if 1 < len(name.split()) <= 5:
                return name


    # Fallback: examine first few lines

    lines = [
        line.strip()
        for line in text.split("\n")
        if line.strip()
    ]

    for line in lines[:8]:

        if line.lower() in [
            "resume",
            "curriculum vitae",
            "cv",
            "profile",
            "personal information"
        ]:
            continue

        # Ignore email lines
        if "@" in line:
            continue

        # Ignore phone/address lines containing many digits
        if len(re.findall(r'\d', line)) >= 5:
            continue

        # Name-like line
        if re.fullmatch(
            r"[A-Za-z][A-Za-z .\'-]{2,60}",
            line
        ):

            if line.upper() not in [
                "EDUCATION",
                "EXPERIENCE",
                "SKILLS",
                "PROJECTS",
                "SUMMARY",
                "OBJECTIVE",
                "CONTACT",
                "PROFILE"
            ]:

                return line.strip()

    return "Not found"


# ==========================================
# SKILLS EXTRACTION
# ==========================================

def extract_skills(text):

    skills_list = [

        "Python",
        "Java",
        "C++",
        "C#",
        "JavaScript",
        "TypeScript",

        "HTML",
        "CSS",

        "React",
        "Angular",
        "Node.js",

        "SQL",
        "MySQL",
        "PostgreSQL",
        "MongoDB",

        "Machine Learning",
        "Deep Learning",
        "Artificial Intelligence",
        "Data Science",
        "Data Analysis",

        "NLP",
        "Natural Language Processing",

        "Flask",
        "Django",

        "Git",
        "GitHub",
        "Docker",

        "AWS",
        "Azure",

        "Excel",
        "Power BI",
        "Tableau",

        "MATLAB",
        "R",

        "Communication",
        "Leadership",
        "Teamwork"
    ]

    found_skills = []

    normalized_text = re.sub(
        r'\s+',
        ' ',
        text.lower()
    )

    for skill in skills_list:

        escaped_skill = re.escape(skill.lower())

        pattern = (
            r'(?<![a-z0-9])'
            + escaped_skill
            + r'(?![a-z0-9])'
        )

        if re.search(pattern, normalized_text):

            found_skills.append(skill)

    return found_skills


# ==========================================
# EDUCATION EXTRACTION
# ==========================================

def extract_education(text):

    education_keywords = [

        "b.tech",
        "btech",
        "b.e",
        "b.e.",
        "be ",

        "bachelor",

        "m.tech",
        "mtech",
        "m.e",
        "m.e.",

        "master",

        "b.sc",
        "bsc",

        "m.sc",
        "msc",

        "mba",

        "phd",
        "ph.d",

        "diploma",

        "computer engineering",
        "computer science",

        "chemical engineering",

        "mechanical engineering",

        "electrical engineering",

        "electronics engineering",

        "civil engineering"
    ]

    found_education = []

    for line in text.split("\n"):

        # Fix common OCR spacing:
        # Majorin -> Major in
        cleaned_line = re.sub(
            r'(?i)(major)(in)',
            r'\1 \2',
            line
        )

        cleaned_line = re.sub(
            r'\s+',
            ' ',
            cleaned_line
        ).strip()

        if not cleaned_line:
            continue

        for keyword in education_keywords:

            if keyword.lower() in cleaned_line.lower():

                if cleaned_line not in found_education:
                    found_education.append(cleaned_line)

                break

    return found_education


# ==========================================
# EXPERIENCE EXTRACTION
# ==========================================

def extract_experience(text):

    lines = [
        line.strip()
        for line in text.split("\n")
        if line.strip()
    ]

    found_experience = []

    experience_keywords = [

        "intern",
        "internship",

        "software developer",
        "software engineer",

        "developer",
        "engineer",

        "analyst",

        "manager",

        "worked as",

        "working as",

        "employment",

        "professional experience",

        "work experience"
    ]

    education_words = [

        "bachelor",
        "master",
        "b.tech",
        "btech",
        "b.e",
        "bsc",
        "b.sc",
        "m.tech",
        "mtech",
        "m.e",
        "mba",
        "phd",
        "diploma",
        "chemical engineering",
        "computer engineering",
        "computer science"
    ]

    for line in lines:

        lower_line = line.lower()

        # Do not classify education as experience
        if any(
            word in lower_line
            for word in education_words
        ):
            continue

        if any(
            keyword in lower_line
            for keyword in experience_keywords
        ):

            if line not in found_experience:
                found_experience.append(line)

        # Detect date ranges such as 2023-2024
        elif re.search(
            r'(19|20)\d{2}\s*[-–]\s*(19|20)\d{2}',
            lower_line
        ):

            if line not in found_experience:
                found_experience.append(line)

    return found_experience[:10]


# ==========================================
# MAIN RESUME PARSER
# ==========================================

def parse_resume(text):

    return {

        "name": extract_name(text),

        "email": extract_email(text),

        "phone": extract_phone(text),

        "skills": extract_skills(text),

        "education": extract_education(text),

        "experience": extract_experience(text)

    }
