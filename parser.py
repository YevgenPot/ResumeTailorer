import os
import yaml

def parse_resume(resumeText):

    filePath = os.path.dirname(os.path.abspath(__file__))
    path = os.path.join(filePath, "dataDir" , resumeText)    

    with open(path, 'r', encoding='utf-8') as file: ##  utf 8 encoding for reliable parsing and downstream text render

        resume_data = yaml.safe_load(file)


    return resume_data

def parse_job_description(jobText):


    filePath = os.path.dirname(os.path.abspath(__file__))
    path = os.path.join(filePath, "dataDir" , jobText)

    keywordList = []
    
    with open(path, 'r') as file:

        for line in file:
            if line.strip().startswith('///') or not line.strip():
                continue
            else:
                keywordList.append(line.strip())

    return keywordList