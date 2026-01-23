from matcher_class import ResumeMatcher

matcher = ResumeMatcher()
resume_list=['Developed scalable APIs using Python and AWS Lambda to support core platform features', 'Improved CI/CD pipelines', 'Used Jenkins to automate staging deployments', 'Reduced deployment time by 40%', 'Implemented authentication system', 'Integrated OAuth2 with company login', 'Enhanced login security and user experience']

keyword_list = ['Python', 'AWS', 'CI/CD', 'RESTful APIs', 'Backend development', 'Cloud infrastructure', 'Automation', 'AWS Lambda', 'Jenkins', 'GitHub Actions', 'OAuth2', 'JWT', 'Flask', 'Scripting', 'Bash', 'API design', 'DevOps', 'Infrastructure-as-code', 'Docker', 'Monitoring', 'Chart.js', 'Code reviews', 'Documentation', 'Agile', 'Full-stack', 'React', 'Netlify', 'Software engineering', 'Cloud-native', 'Authorization', 'Authentication', 'Deployment', 'Infrastructure scalability', 'Problem-solving', 'Open-source', 'Team collaboration', 'Security', 'Continuous delivery', 'Cross-functional teams', 'Scalable systems', 'Maintainable code']

matcher.load_keywords(keyword_list)
matcher.load_resume(resume_list)

matcher.match()


for i, fragment in enumerate(resume_list):
    resume_list[i] += matcher.scores_list[i]

print(resume_list)