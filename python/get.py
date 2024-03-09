from flask import jsonify
import logging

logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')

def get_data(connection):
    result = {}
    try:
        with connection as conn:
            with conn.cursor() as cursor:

                # CONTACT
                cursor.execute("SELECT * FROM contact")
                contact_records = cursor.fetchall()
                first_name, last_name, location, github, linkedin, summary = contact_records[0]
                result["contact"] = {"firstName": first_name,
                                        "lastName": last_name,
                                        "location": location,
                                        "githubLink": github,
                                        "linkedinLink": linkedin,
                                        "professionalSummary": summary}
                
                # EDUCATION
                cursor.execute("SELECT * FROM education")
                education_records = cursor.fetchall()
                result["education"] = []
                for institution, degree, duration, gpa in education_records:
                    result["education"].append({"institution": institution,
                                                "degree": degree,
                                                "duration": duration,
                                                "gpa": gpa})
                    
                # WORK EXPERIENCE
                cursor.execute("""
                    SELECT 
                        job.id AS job_id,
                        employer.name AS employer,
                        employer.location,
                        job.title,
                        job.duration,
                        work_experience.job_description
                    FROM work_experience
                    LEFT JOIN job ON job.id = work_experience.job_id
                    LEFT JOIN employer ON employer.id = job.employer_id
                """)

                work_experience_records = cursor.fetchall()
                result["work_experience"] = []
                temp = {}

                for job_id, employer, location, title, duration, job_description in work_experience_records:
                    if job_id in temp:
                        temp[job_id]["job_description"].append(job_description)
                    else:
                        temp[job_id] = {"employer": employer, 
                                        "location": location, 
                                        "title": title, 
                                        "duration": duration,
                                        "job_description": [job_description]}

                for data in temp.values():
                    result["work_experience"].append({"employer": data["employer"], 
                                                      "location": data["location"], 
                                                      "title": data["title"], 
                                                      "duration": data["duration"], 
                                                      "jobDescription": data["job_description"]})
                    
                # SKILLS
                cursor.execute("SELECT * FROM skills")
                languages, technologies =  cursor.fetchall()[0]
                result["skills"] = {"languages": languages, "technologies": technologies}

                # PROJECTS
                cursor.execute("""
                    SELECT 
                        project.id,
                        project.name,
                        project.code_repository,
                        project_experience.project_description
                    FROM project_experience
                    LEFT JOIN project ON project.id = project_experience.project_id
                """)

                project_records = cursor.fetchall()
                result["projects"] = []
                temp = {}

                for project_id, name, code_repository, project_description in project_records:
                    if project_id in temp:
                        temp[project_id]["project_description"].append(project_description)
                    else:
                        temp[project_id] = {"name": name, 
                                    "code_repository": code_repository, 
                                    "project_description": [project_description]}

                for data in temp.values():
                    result["projects"].append({"name": data["name"], 
                                              "codeRepository": data["code_repository"], 
                                              "projectDescription": ["project_description"]})

                # CERTIFICATIONS
                    cursor.execute("""
                        SELECT
                            certifying_org.name,
                            certification.name,
                            certification.expiration_date
                        FROM certification
                        LEFT JOIN certifying_org on certifying_org.id = certification.org_id
                            
                    """)

                    cert_records = cursor.fetchall()
                    result["certifications"] = []
                    temp = {}

                    for issuer, cert_name, exp_date in cert_records:
                        cert_entry = {"name": cert_name, "expirationDate": exp_date}
                        if issuer in temp:
                            temp[issuer].append(cert_entry)
                        else:
                            temp[issuer] = [cert_entry]

                    for key, value in temp.items():
                        result["certifications"].append({"issuer": key, "certifications": value})
                    

                return jsonify(result)
            
    except Exception as e:
        logging.error(f"ERROR FETCHING DATA:\n{e}")
        return jsonify([]), 500