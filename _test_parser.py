import time
#from parser import parse_resume, parse_job_description
from parser_class import ParserClass

'''
start=time.time()

resume = parse_resume('yourresume.yaml')

job_desc = parse_job_description('jobDkwl2.txt')

def test_resume():
    for i , v in resume.items():
        print('\n')
        print(i, v)

def test_job_desc():
    for item in job_desc:
        print(item)

def test_resume_navigation():
    for entry in resume.get("work_history").get("entries"):
        print(entry.get("summary"))
        for experience in entry.get("experiences"):
            print(experience.get("what"))
            print(experience.get("how"))
            print(experience.get("result"))

print( test_resume_navigation() )

end = time.time()
print(end - start)
'''



start = time.time()
parser = ParserClass()
parser.load_resume()
parser.load_keywords()

def test_print_update_print():

    for entry in parser.get_section('work_history.entries'):
        print(entry.get("summary"))
        for experience in entry.get("experiences"):
            print(experience.get("what"))
            print(experience.get("how"))
            print(experience.get("result"))

    copy = parser.get_section('work_history.entries')
    for entry in copy:
        entry['summary'] += ":test"
        for experience in entry.get("experiences"):
            experience['what'] += ":test"
            experience['how'] += ":test"
            experience['result'] += ":test"

    parser.update_section('work_history.entries', copy)


    for entry in parser.get_section('work_history.entries'):
        print(entry.get("summary"))
        for experience in entry.get("experiences"):
            print(experience.get("what"))
            print(experience.get("how"))
            print(experience.get("result"))
#####################################################
#test_print_update_print()

def test_navigation():
    for entry in parser.get_section('work_history.entries'):
        print(entry.get("summary"))
        for experience in entry.get("experiences"):
            print(experience.get("what"))
            print(experience.get("how"))
            print(experience.get("result"))
#####################################################
#test_navigation()

def test_keywords():
    print( parser.keywords_list)
#####################################################
#test_keywords()

def test_resume():
    print( parser.resume_dict)
############################################
#test_resume()

def test_resume_list():
    #print( parser.turn_dict_to_list(parser.resume_dict) )
    list, hash = parser.turn_dict_to_list(parser.get_section('work_history')) 
    print(list)
    #print( parser.turn_dict_to_list(parser.get_section('projects'))[0] )
############################################
#test_resume_list()

def test_list_and_update():
    list, hash = parser.turn_dict_to_list(parser.get_section('work_history'))
    for i, item in enumerate(list):
        list[i] = ":test"
    parser.update_entries_with_list_hash('work_history', list, hash)
    print( parser.get_section('work_history') )
#############################################
#test_list_and_update()

def test_save_resume():
    parser.resume_dict['contact_section']['name'] = "test"
    parser.save_resume('test_resume.yaml')
############################################
#test_save_resume()


end = time.time()
print(end - start)
