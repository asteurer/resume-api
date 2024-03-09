from psycopg import sql, DatabaseError
from flask import jsonify
import logging

logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')

def get_return_val(cursor, 
                   return_column_name: str, 
                   table_name: str, 
                   key_column_name: str, 
                   key_column_variable: str) -> str:
                        result = cursor.fetchone()

                        if result:
                            return result[0]

                        else:
                            query = sql.SQL("SELECT {return_column} FROM {table} WHERE {key_column} = %s")\
                            .format(table=sql.Identifier(table_name),
                                    return_column=sql.Identifier(return_column_name),
                                    key_column=sql.Identifier(key_column_name),
                                    )

                            cursor.execute(query, (key_column_variable, ))
                            result = cursor.fetchone()
                        
                            if result:
                                 return result[0]
                            else:
                                 return None


def post_data(connection, contact, education, work_experience, skills, projects, certifications):
    with connection as conn:
        with conn.cursor() as cursor:
            try:
                if contact:
                    cursor.execute("""
                        INSERT INTO contact (
                            first_name, 
                            last_name,
                            location,
                            github_link, 
                            linkedin_link, 
                            professional_summary
                        ) VALUES (%s, %s, %s, %s, %s, %s)
                        ON CONFLICT (first_name, last_name) DO UPDATE SET
                        first_name = EXCLUDED.first_name,
                        last_name = EXCLUDED.last_name,
                        location = EXCLUDED.location,
                        github_link = EXCLUDED.github_link,
                        linkedin_link = EXCLUDED.linkedin_link,
                        professional_summary = EXCLUDED.professional_summary
                    """, (
                        contact.get('first_name'),
                        contact.get('last_name'),
                        contact.get('location'),
                        contact.get('github_link'),
                        contact.get('linkedin_link'),
                        contact.get('professional_summary'),
                    ))

                    conn.commit()

                if education: 
                    for degree in education:
                        cursor.execute("""
                            INSERT INTO education (
                                institution,
                                degree,
                                duration,
                                gpa
                            ) VALUES (%s, %s, %s, %s)
                            ON CONFLICT (institution, degree) DO NOTHING
                        """, (
                            degree.get('institution'),
                            degree.get('degree'),
                            degree.get('duration'),
                            degree.get('gpa')
                        ))
                    
                    conn.commit()
                    
                if work_experience:
                    for job in work_experience:
                        cursor.execute("""
                            INSERT INTO employer(
                                name,
                                location 
                            ) VALUES (%s, %s) ON CONFLICT (name, location) DO NOTHING RETURNING id 
                        """, (
                            job.get('employer'),
                            job.get('location')
                        ))
                        
                        employer_id = get_return_val(cursor, 'id', 'employer', 'name', job.get('employer'))

                        cursor.execute("""
                            INSERT INTO job (
                                employer_id,
                                duration,
                                title
                            ) VALUES (%s, %s, %s) ON CONFLICT (employer_id, title) DO UPDATE SET
                            duration = EXCLUDED.duration
                            RETURNING id
                        """, (
                            employer_id,
                            job.get('duration'), 
                            job.get('title')
                        ))

                        job_id = get_return_val(cursor, 'id', 'job', 'title', job.get('title'))

                        for description_entry in job.get('description', []):
                            cursor.execute("""
                                INSERT INTO work_experience (
                                    job_id,
                                    job_description
                                ) VALUES (%s, %s) ON CONFLICT (job_id, job_description) DO UPDATE SET
                                job_description = EXCLUDED.job_description
                            """, (
                                job_id,
                                description_entry
                            ))
                    
                    conn.commit()

                if skills:
                    cursor.execute("""
                        INSERT INTO skills (
                            languages,
                            technologies
                        ) VALUES (%s, %s) ON CONFLICT (languages, technologies) DO UPDATE SET
                        languages = EXCLUDED.languages,
                        technologies = EXCLUDED.technologies
                    """, (
                        skills.get('languages'),
                        skills.get('technologies')
                    ))

                    conn.commit()

                if projects:
                    for project in projects:
                        cursor.execute("""
                            INSERT INTO project (
                                name,
                                code_repository
                            ) VALUES (%s, %s) ON CONFLICT DO NOTHING RETURNING id
                        """, (
                            project.get('name'),
                            project.get('code_repository')
                        ))

                        project_id = get_return_val(cursor, 'id', 'project', 'name', project.get('name'))

                        for description_entry in project.get('description', []):
                            cursor.execute("""
                                INSERT INTO project_experience (
                                    project_id,
                                    project_description
                                ) VALUES (%s, %s) ON CONFLICT (project_id, project_description) DO UPDATE SET
                                project_description = EXCLUDED.project_description
                            """, (
                                project_id,
                                description_entry
                            ))

                    conn.commit()

                    if certifications:
                        for org in certifications:
                            cursor.execute("""
                                INSERT INTO certifying_org (
                                    name
                                ) VALUES (%s) ON CONFLICT (name) DO NOTHING RETURNING id
                            """, (
                                org.get('issuer'), 
                            ))

                            org_id = get_return_val(cursor, 'id', 'certifying_org', 'name', org.get('issuer'))

                            for certification in org.get('certifications', []):
                                cursor.execute("""
                                    INSERT INTO certification (
                                        org_id,
                                        name,
                                        expiration_date
                                    ) VALUES (%s, %s, %s) ON CONFLICT (org_id, name) DO UPDATE SET
                                    expiration_date = EXCLUDED.expiration_date
                                """, (
                                    org_id,
                                    certification.get('name'),
                                    certification.get('expiration_date')
                                ))

                        conn.commit()


            except DatabaseError as e:
                logging.error(f"DATABASE ERROR:\n{e}")
                conn.rollback()
            
            finally:
                cursor.close()
                conn.close()

    return jsonify({"success": True})
