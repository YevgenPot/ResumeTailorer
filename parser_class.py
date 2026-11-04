import os
import yaml

class Parser:

    def __init__(self, resume_file='resume.yaml', job_file='jobDkwl.txt'):
        self.resume_file = resume_file
        self.job_file = job_file
        self.resume_dict = {}
        self.keywords_list = []

        

    def load_resume(self, resume_file_manual=None):
        """Load or reload the resume YAML file."""
        if resume_file_manual:
            self.resume_file = resume_file_manual
        if not self.resume_file:
            raise ValueError("No resume file specified")

        path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "dataDir", self.resume_file)
        with open(path, 'r', encoding='utf-8') as file: ##  utf 8 encoding for reliable parsing and downstream text render
            self.resume_dict = yaml.safe_load(file)
            ## attempt to catch no file error
            if not self.resume_dict: ## i have no idea if this will work
                raise ValueError(f"Resume file '{self.resume_file}' not found.") ## using  yaml.safe_load(file) will return an empty dict if missing

        return self.resume_dict ## should return the dict version of the yaml we already loaded, or the new entered yaml file
    
    def load_keywords(self, job_file_manual=None):
        """Load or reload the job description keywords."""
        if job_file_manual:
            self.job_file = job_file_manual
        if not self.job_file:
            raise ValueError("No job file specified")

        path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "dataDir", self.job_file)
        with open(path, 'r') as file:
            self.keywords_list = [line.strip() for line in file if line.strip()]

        return self.keywords_list
    
    def save_resume(self, new_filename):
        """Save the current resume_dict to a new YAML file."""
        
        if not new_filename:
            raise ValueError("A filename must be provided to save the resume.")
        
        # Ensure we save in the same directory structure
        path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "dataDir", new_filename)
        
        # Write the dictionary to a YAML file
        with open(path, 'w', encoding='utf-8') as file:
            yaml.dump(self.resume_dict,
                        file,
                        allow_unicode=True,
                        sort_keys=False,
                        default_flow_style=False,
                        width=float("inf")
                        )
            
        
        return path  # optional: return the path of the saved file

    def get_section(self, section_name):
        """Return a specific section from the resume."""
        
        keys = section_name.split('.')
        current_dict = self.resume_dict
        for key in keys:
            if key not in current_dict:
                raise KeyError(f"Section '{section_name}' not found in resume.")
            current_dict = current_dict[key]
        return current_dict
    
    def update_section(self, section_name, data):
        """Update a specific section of the resume."""
        keys = section_name.split('.')
        current_dict = self.resume_dict
        for key in keys[:-1]:
            if key not in current_dict:
                raise KeyError(f"Section '{section_name}' not found in resume.")
            current_dict = current_dict[key]
        current_dict[keys[-1]] = data

    def turn_dict_to_list(self, dictionary): ## used for work_hisotry, projects, and internships
        allowed_keys = "entries" ## all of the above have a "entries" key and only the above
        if allowed_keys not in dictionary.keys():
            raise ValueError(f"Invalid section name: {dictionary.keys()}")

        flat_list = []
        count_hash = [] # preserves the shape of the original dict
        for entry in dictionary.get("entries"):
            i=0
            flat_list.append(entry["summary"])
            i+=1
            for experience in entry.get("experiences"):
                flat_list.append( f"{experience.get('what')}")
                flat_list.append( f"{experience.get('how')}")
                flat_list.append( f"{experience.get('result')}")
                i+=3
            count_hash.append(i)   
        return flat_list, count_hash
    
    def update_entries_with_list_hash(self, section_name, flist, chash): ## used for work_hisotry, projects, and internships
        section = self.resume_dict.get(section_name)
        i=0
        for ind, count in enumerate(chash):
            section["entries"][ind]["summary"] += flist[i] ; i+=1 ## append the entry string
            
            for experience in section["entries"][ind]["experiences"]:
                experience["what"] += flist[i]; i+=1
                experience["how"] += flist[i]; i+=1
                experience["result"] += flist[i]; i+=1