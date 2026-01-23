'''
using jinja2 vs reportlab
'''

from jinja2 import Template
import os
import webbrowser
from datetime import datetime

resume_html = (
    """
<html>
    <head>
        <style>
            body {
                font-family: Arial, Helvetica, sans-serif;
                font-size: 14px; 
                line-height: 1.5;
                margin: 0px; 
                color: #333;
            }
            .contact_name {
                font-weight: bold;
                font-size: 19px; 
                text-align: center;
            }
            .contact_section {
                font-size: 16px; 
                text-align: center;
            }
            .section_title {
                font-weight: bold;
            }
            .entry_list {
                list-style-type: none; 
                padding: 0;
                margin: 0;
            }

            .entry_item {
                display: flex;
                justify-content: space-between; 
                margin-bottom: 6px;
                margin-left: 30px;
            }

            .entry_item_italic {
                font-style: italic;
                display: flex;
                justify-content: space-between; 
                margin-bottom: 6px;
                margin-left: 3px;
            } 

            .entry_left {
                text-align: left;
            }

            .entry_right {
                text-align: right;
            }

            .sentence_list {
                list-style-type: disc; 
                padding: 0;
                margin: 0;
            }

            .sentence_item {
                margin-bottom: 6px;
                margin-left: 40px;
                text-align: left;
            }


        </style>
    </head>
    <body>
    <div class="contact_section">
        <div class="contact_name">
        <p>{{resume.contact_section.name}}</p>
        </div>

        <p>{{resume.contact_section.contact.phone}} |
          {{resume.contact_section.contact.email}} |
          {{resume.contact_section.contact.linkedin}} |
          {{resume.contact_section.contact.portfolio}}
        </p>
        <p>
          {{resume.contact_section.location.city}}, {{resume.contact_section.location.state}}, {{resume.contact_section.location.immigration_status}}
        </p>
    </div>

    <div class="summary">
        {% if resume.summary.include %}
            <p class="section_title">Summary</p>
            <p>{{resume.summary.reason}}: {{resume.summary.text}}</p>
        {% endif %}
    </div>

    <div class="education_certificates">
        <p class="section_title">Education and Certificates</p>
        {% for item in resume.education_certificates.entries %}
        {% if item.type == "education" %}
            <ul class="entry_list">
            <li class="entry_item">
            <span class="entry_left">{{item.degree}} in {{item.major}} at {{item.institution}}</span>
            {% if resume.current_year - (item.graduation_date | int) < 3 %}
                <span class="entry_right">{{item.graduation_date}}</span> 
            {% else %}
                <span class="entry_right">Graduated</span> 
            {% endif %}
            </li>
            </ul>
        {% elif item.type == "certificate" %}
            <ul class="entry_list">
            <li class="entry_item">
            <span class="entry_left">{{item.name}}</span>
            <span class="entry_right">Active</span> 
            </li>
            </ul>
        {% endif %}
        {% endfor %}
    </div>

    {% if resume.work_history.include %}
    <div class="work_history">
        <p class="section_title">Work History</p>
        {% for item in resume.work_history.entries %}
            <ul class="entry_list">
            <li class="entry_item_italic">
            <span class="entry_left">{{item.title}} at {{item.company}}, {{item.location}}</span>
            <span class="entry_right">{{item.date.start}} to {{item.date.end}}</span>
            </li>
            </ul>
            {% if item.summary %}
                <ul class="sentence_list">
                <li class="sentence_item">{{item.summary}}</li>
            {% for experience in item.experiences %}
                {% if experience.full %}
                    <li class="sentence_item">{{experience.full}}</li>
                {% endif %}
            {% endfor %}
                </ul>
            {% endif %}
        {% endfor %}
    </div>
    {% endif %}

    {% if resume.internships.include %}
    <div class="internships">
        <p class="section_title">Internships</p>
        {% for item in resume.internships.entries %}
            <ul class="entry_list">
            <li class="entry_item_italic">
            <span class="entry_left">{{item.title}} at {{item.company}}, {{item.location}}</span>
            <span class="entry_right">{{item.date.start}} to {{item.date.end}}</span>
            </li>
            </ul>
            {% if item.summary %}
                <ul class="sentence_list">
                <li class="sentence_item">{{item.summary}}</li>
            {% for experience in item.experiences %}
                {% if experience.full %}
                    <li class="sentence_item">{{experience.full}}</li>
                {% endif %}
            {% endfor %}
                </ul>
            {% endif %}
        {% endfor %}
    </div>
    {% endif %}

    {% if resume.projects.include %}
    <div class="projects">
        <p class="section_title">Projects</p>
        {% for item in resume.projects.entries %}
            <ul class="entry_list">
            <li class="entry_item_italic">
            <span class="entry_left">{{item.title}} for {{item.company}}</span>
            </li>
            </ul>
            {% if item.summary %}
                <ul class="sentence_list">
                <li class="sentence_item">{{item.summary}}</li>
            {% for experience in item.experiences %}
                {% if experience.full %}
                    <li class="sentence_item">{{experience.full}}</li>
                {% endif %}
            {% endfor %}
                </ul>
            {% endif %}
        {% endfor %}
    </div>
    {% endif %}

    </body>
</html>

    """
)


class yamlRenderer():
    def __init__(self):
        self.html_template = Template(resume_html)

    def render(self, yaml_file):
        yaml_file['current_year']  = datetime.now().year
        resume_render = self.html_template.render(resume=yaml_file)

        filePath = os.path.dirname(os.path.abspath(__file__))
        path = os.path.join(filePath, "dataDir" , "output.html")

        with open(path, "w", encoding="utf-8") as f:
            f.write(resume_render)

        webbrowser.open(path)
        pass

    