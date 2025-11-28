from datetime import datetime
from sqlalchemy import or_, not_, and_
from .models import Student, Score , Certificate
from .db import get_db


def create_student(first_name: str, last_name: str, birthdate: datetime, bio: str | None = None):
    student = Student(
        first_name=first_name,
        last_name=last_name,
        birthdate=birthdate,
        bio=bio
    )
    
    with get_db() as session:
        session.add(student)
        session.commit()

def get_students() -> list[Student]:
    with get_db() as session:
        students = session.query(Student).all()
    
    return students

def get_one_student(student_id: int) -> Student | None:
    with get_db() as session:
        student = session.query(Student).get(student_id)
    
    return student

def search_students_by_first_name(first_name: str) -> list[Student]:
    with get_db() as session:
        students = session.query(Student).filter(Student.first_name==first_name).all()
    
    return students

def search_students_by_name(name: str) -> list[Student]:
    with get_db() as session:
        students = session.query(Student).filter(
            or_(Student.first_name.like(f'%{name}%'), Student.last_name.like(f'%{name}%'))
        ).all()
    
    return students

def update_student(
    student_id: int | None = None,
    first_name: str | None = None, 
    last_name: str | None = None, 
    birthdate: datetime | None = None, 
    bio: str | None = None
):
    student = get_one_student(student_id)

    if student:
        with get_db() as session:
            student.first_name = first_name if first_name else student.first_name
            student.last_name = last_name if last_name else student.last_name
            student.birthdate = birthdate if birthdate else student.birthdate
            student.bio = bio if bio else student.bio

            session.add(student)
            session.commit()

def delete_student(student_id: int):
    student = get_one_student(student_id)

    if student:
        with get_db() as session:
            session.delete(student)
            session.commit()

def filter_students_by_gender(gender: str) -> list[Student]:
    with get_db() as session:
        
        result = session.query(Student).filter_by(gender=gender).all()

    return result

def filter_students_by_gpa(min_gpa: float, max_gpa: float) -> list[Student]:
    with get_db() as session:
        
        result = session.query(Student).filter(Student.gpa.between(min_gpa, max_gpa)).all()

    return result

def get_sorted_students_by_gpa(by: str = 'asc') -> list[Student]:
    with get_db() as session:
        if by == 'asc':
            result = session.query(Student).order_by(Student.gpa.asc())
        else:
            result = session.query(Student).order_by(Student.gpa.desc())
            
    return result

def add_score(student_id: int, subject: str, ball: float):
    with get_db() as session:
        student: Student = session.query(Student).get(student_id)
        student.scores.append(Score(subject=subject, ball=ball))
        session.commit()

def get_scores(student_id: int) -> list[Score]:
    with get_db() as session:
        student: Student = session.query(Student).get(student_id)
        return student.scores
    
def get_student_with_scores():
    with get_db() as session:
        students: list[Student] = session.query(Student).all()

        result = []
        for student in students:
            result.append({
                'student': student.full_name,
                'total_scores': len(student.scores)
            })
    
    return result
    
def create_certificate(student_id, title, content, issued_at=None, certificate_code=None, is_verified=False):
    with get_db() as session:
        session.commit()
        
def get_all_certificates() -> list[Certificate]:
    with get_db() as session:
        certificates = session.query(Certificate).all()
    return certificates

def get_unverified_certificates() -> list[Certificate]:
    with get_db() as session:
        certificates = session.query(Certificate).filter(Certificate.is_verified == False).all()
    return certificates

def get_certificates_by_student(student_id: int) -> list[Certificate]:
    with get_db() as session:
        certificates = session.query(Certificate).filter(Certificate.student_id == student_id).all()
    return certificates

def get_certificate_by_code(certificate_code: str) -> Certificate | None:
    with get_db() as session:
        certificate = session.query(Certificate).filter(Certificate.certificate_code == certificate_code).first()
    return certificate

def get_last_five_certificates() -> list[Certificate]:
    with get_db() as session:
        certificates = session.query(Certificate).order_by(Certificate.issued_at.desc()).all()
    return certificates[:5]    
