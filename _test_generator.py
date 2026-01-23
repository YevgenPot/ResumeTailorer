import generator
import os
import yaml



resume_file = "yourresume.yaml"
path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "dataDir", resume_file)
with open(path, 'r', encoding='utf-8') as file: ##  utf 8 encoding for reliable parsing and downstream text render
    resume_dict = yaml.safe_load(file)
    ## attempt to catch no file error
    if not resume_dict: ## i have no idea if this will work
        raise ValueError(f"Resume file '{resume_file}' not found.") ## using  yaml.safe_load(file) will return an empty dict if missing
    

generator = generator.yamlRenderer()
generator.render(resume_dict)