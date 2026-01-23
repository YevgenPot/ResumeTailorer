# Requirements Document

## Project Name
**YAML Resume Parser**

## Author
**Your Name**

## Purpose
This tool parses YAML-formatted resumes into Python dictionaries for downstream processing (e.g., keyword injection, formatting, job matching, etc).

---

## Background
Resumes are often misaligned with their true audience — **Recruiters**, not **Hiring Managers (HMs)**. Recruiters assist in the hiring process but typically lack deep industry knowledge.

**Keyword usage** is the primary metric recruiters use to evaluate resumes. A resume’s success is directly tied to the presence and frequency of relevant keywords.

This tool automates the keyword-matching process to streamline repeated job applications. Users are encouraged to create a **"kitchen sink" resume** — a detailed, diary-like document containing all personal and professional information. The app will then auto-tailor this into recruiter-optimized resumes based on specific job descriptions.

## Functional Requirements

- [ ] Load a resume YAML file from the filesystem
- [ ] Validate basic structure (e.g., required sections exist)
- [ ] Return a Python dictionary representing the resume
- [ ] Handle common parsing errors gracefully (e.g., missing file, malformed YAML)

---

## Non-Functional Requirements

- [ ] Parser should complete in under 250ms for standard resumes
- [ ] Designed to be human-readable/writable (YAML spec should be minimal)
- [ ] Code should be easily testable and modular
- [ ] Documentation (this site) should be auto-served with MkDocs


## Resume Formatting Rules

These rules govern how the final resume should be rendered for maximum compatibility with Applicant Tracking Systems (ATS) and recruiter expectations.

### General Formatting

- **Font**: Arial only
- **Colors**: Black and white only  
  - *Exception*: Contact details (phone, email, LinkedIn/portfolio) may use blue
- **Layout**: Single-column only
- **Line Spacing**: 1.5x
- **Length**: Multi-page resumes are acceptable
- **Photo**: Do **not** include a photo of yourself

### Contact Section

- **Alignment**: Center-aligned
- **Name**: First and Last name, **bold**, font size 14
- **Details**: Phone number, email, LinkedIn/portfolio, font size 12
- **Location/Citizenship**:
  - Include "US Citizen" or "Green Card Holder" if applicable
  - Format as part of City, State line (font size 12)

### Summary Section & Rules

The **Summary** section is **optional** and should only be included if **at least one** of the following conditions is met:

- **Industry Change**  
  The user is transitioning from one industry to another.  
  _Example_: "Transitioning from Education to UX Design."

- **Relocation**  
  The user needs to relocate or is planning to move for the job.  
  _Example_: "Relocating to Seattle in January; open to earlier start."

- **Sponsorship or Visa Status**  
  The user is on a visa or requires sponsorship. Include a brief, clear explanation of how the company can work with the user’s visa type.  
  _Example_: "Currently on OPT; eligible for H1B sponsorship in next cycle."

If **none** of these conditions are met, the Summary section **should be omitted** from the resume output.


## Education & Certificates

This section should follow a clean, minimal design and may be **relocated** to the bottom of the resume based on job relevance.

### Formatting Rules

- **Alignment**: Left-aligned
- **Font**: 10.5 pt
- **Header**: "Education & Certificates" should be **bolded**; all other text in this section should be regular weight
- **Layout**: Bullet points only
- **Length**: Maximum of 3 lines

### Content Rules

- Each entry should include:
  - Degree (e.g., B.A., M.S., PhD)
  - Field of study
  - Institution name

- **Graduation date rules**:
  - If graduated **more than 3 years ago** → write `Status: Graduated`
  - If graduated **within the last 3 years** → include the year of graduation

- **Certificates**:
  - Include relevant certifications only
  - Do **not** include dates unless the certificate is no longer active

### Placement Rule

If the job you're applying for **does not require a degree** or listing education would make you appear **overqualified**, move this section to the **bottom** of the resume instead of placing it near the top under the contact section.

---

## Out of Scope

- Keyword injection
- Resume formatting/styling
- Job matching

These are handled by separate components of the application.

---

## Terminology

### Keywords
**Keywords** are the individual skills, tools, qualifications, or traits that recruiters search for when matching resumes to roles.

### Job Title
A **Job Title** represents a standardized label for a set of qualifications Hiring Managers (HMs) are seeking. Recruiters and HMs associate each title with a core set of expected skills or **keywords**. 

Examples:

- **Barista**: POS, Customer Service, Basic Math, Multitasking  
- **Accountant**: Excel, GAAP, CPA  
- **IT Helpdesk**: Customer Service, Troubleshooting, MS Office, Windows, Zoom  
- **Project Manager**: PMP/CSM, Agile, Stakeholder Communication, Cross-Functional Teams  

### Job Description (JD)
A **Job Description** contains details about a role, such as: Job Title, Salary, Day-to-day duties, Legal/disclaimer text

Unlike a job title, the **keywords** found in specific sections do not have a regular structure, but are still just as relevant.

Sections to look out for include:

- Requirements  
- Qualifications  
- Must Have / Need to Have  
- What We Are Looking For  
- We Would Love To Meet You If  
- You Might Be a Great Fit If  


### Developmental Diary
After much model testing, the scope of the program is now this:
- Take a human wrote resume.yaml
- This will be split into respective separate sections

The program can then independantly, and with little coupling, do this:
- Recombine a set of sections into a rendered resume
- For each section, can be processed through a sentance transformer to find general relativity using an input list of keywords
