from parser_class import Parser
from matcher_class_v3 import ResumeMatcher
from generator import yamlRenderer


Parser = Parser()
ResumeMatcher = ResumeMatcher()
Generator = yamlRenderer()

def main():

    def match_resume_to_job(resume = 'resume.yaml', job_desc = 'default_jkwl.txt'):
        Parser.load_resume(resume)
        Parser.load_keywords(job_desc)
        work_history_list, work_history_hash = Parser.turn_dict_to_list(Parser.get_section('work_history'))
        projects_list, projects_hash = Parser.turn_dict_to_list(Parser.get_section('projects'))
        internships_list, internships_hash = Parser.turn_dict_to_list(Parser.get_section('internships'))
        
        ResumeMatcher.load_keywords(Parser.keywords_list)

        ## FIX ISSUE: NO CHECK FOR EMPTY LISTS
        ## also: assert len(ResumeMatcher.per_sentence_append_data) == len(projects_list)

        ResumeMatcher.load_resume(work_history_list)
        ResumeMatcher.match()
        Parser.update_entries_with_list_hash('work_history', ResumeMatcher.per_sentence_append_data, work_history_hash) 

        ResumeMatcher.load_resume(projects_list)
        ResumeMatcher.match()
        Parser.update_entries_with_list_hash('projects', ResumeMatcher.per_sentence_append_data, projects_hash)

        ResumeMatcher.load_resume(internships_list)
        ResumeMatcher.match()
        Parser.update_entries_with_list_hash('internships', ResumeMatcher.per_sentence_append_data, internships_hash)


        Parser.save_resume('output_resume.yaml')  ## fix: make one reference of output yaml

    while True:
        print("Select an option:")
        print("1. Match default resume / job description")
        print("2. Match custom resume / job description")
        print("3. Render resume")
        print("4. Exit")
        choice = input("Enter your choice : ")

        if choice == "1":
            match_resume_to_job()
        elif choice == "2":
            resume = input("Enter the resume file name: ")
            job_desc = input("Enter the job description file name: ")
            match_resume_to_job(resume, job_desc)
        elif choice == "3":
            Parser.load_resume("output_resume.yaml")
            Generator.render(Parser.resume_dict)
        elif choice == "4":
            break


if __name__ == "__main__":
    main()
