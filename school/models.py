from datetime import datetime
from sqlalchemy import (
    Column, Integer, String, Date, DateTime, Text, Float, ForeignKey, Boolean
)
from sqlalchemy.orm import relationship
from .db import Base


class Student(Base):
    __tablename__ = 'students'

    
    
    student_id = Column('id', Integer, primary_key=True, nullable=False)
    first_name = Column('first_name', String(length=64), nullable=False)
    last_name = Column('last_name', String(length=64), nullable=False)
    birthdate = Column('birthdate', Date, nullable=False)
    gender = Column('gender', String(length=20), nullable=False)
    bio = Column('bio', Text)
    gpa = Column('gpa', Float, nullable=False)

    
    scores = relationship('Score', back_populates='student', cascade='all, delete-orphan')
    certificates = relationship('Certificate', back_populates='student', cascade='all, delete-orphan')

    created_at = Column('created_at', DateTime, default=datetime.utcnow)
    updated_at = Column('updated_at', DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def __str__(self):
        return f'Student(id={self.student_id}, name=\"{self.first_name} {self.last_name}\")'

    def __repr__(self):
        return f'Student(id={self.student_id}, name=\"{self.first_name} {self.last_name}\")'

    @property
    def full_name(self):
        return f'{self.first_name} {self.last_name}'


class Score(Base):
    __tablename__ = 'scores'

    score_id = Column('id', Integer, primary_key=True, nullable=False)
    subject = Column('subject', String(length=64), nullable=False)
    ball = Column('ball', Float, nullable=False)

    
    student_id = Column('student_id', Integer, ForeignKey('students.id', ondelete='CASCADE'), nullable=False)

    student = relationship('Student', back_populates='scores')

    def __str__(self):
        return f'Score(id={self.score_id}, name=\"{self.subject}\", ball={self.ball}, student={self.student_id})'

    def __repr__(self):
        return f'Score(id={self.score_id}, name=\"{self.subject}\", ball={self.ball}, student={self.student_id})'


class Certificate(Base):
    __tablename__ = 'certificates'

    id = Column('id', Integer, primary_key=True, nullable=False)
   
    student_id = Column('student_id', Integer, ForeignKey('students.id', ondelete='CASCADE'), nullable=False)
    title = Column('title', String(length=256), nullable=False)
    content = Column('content', Text, nullable=False)
    issued_at = Column('issued_at', DateTime, default=datetime.utcnow)
    certificate_code = Column('certificate_code', String(256), unique=True)
    is_verified = Column('is_verified', Boolean, default=False)

    student = relationship('Student', back_populates='certificates')

    def __str__(self):
        return f"Certificate(title={self.title}, code={self.certificate_code}, student_id={self.student_id})"

    def __repr__(self):
        return f"<Certificate id={self.id}, title='{self.title}', student_id={self.student_id}>"