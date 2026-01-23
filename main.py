from parser_class import ParserClass
from matcher_class import ResumeMatcher
from generator import yamlRenderer


ParserClass = ParserClass()
ResumeMatcher = ResumeMatcher()
Generator = yamlRenderer()

def main():

    def match_resume_to_job(resume = None, job_desc = None):
        ParserClass.load_resume(resume)
        ParserClass.load_keywords(job_desc)
        work_history_list, work_history_hash = ParserClass.turn_dict_to_list(ParserClass.get_section('work_history'))
        projects_list, projects_hash = ParserClass.turn_dict_to_list(ParserClass.get_section('projects'))
        internships_list, internships_hash = ParserClass.turn_dict_to_list(ParserClass.get_section('internships'))
        
        ResumeMatcher.load_keywords(ParserClass.keywords_list)

        ## FIX ISSUE: NO CHECK FOR EMPTY LISTS

        ResumeMatcher.load_resume(work_history_list)
        ResumeMatcher.match()
        ParserClass.update_entries_with_list_hash('work_history', ResumeMatcher.scores_list, work_history_hash) 

        ResumeMatcher.load_resume(projects_list)
        ResumeMatcher.match()
        ParserClass.update_entries_with_list_hash('projects', ResumeMatcher.scores_list, projects_hash)

        ResumeMatcher.load_resume(internships_list)
        ResumeMatcher.match()
        ParserClass.update_entries_with_list_hash('internships', ResumeMatcher.scores_list, internships_hash)


        ParserClass.save_resume('test_resume.yaml')

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
            ParserClass.load_resume("test_resume.yaml")
            Generator.render(ParserClass.resume_dict)
        elif choice == "4":
            break


if __name__ == "__main__":
    main()
