from fastapi_sqlalchemy import db 
from sqlalchemy import Column, String, Date, DateTime, Integer, Column, UniqueConstraint
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime
from app.config import ConfigClass

Base = declarative_base()


class AnnouncementModel(Base):
    __tablename__ = 'announcement'
    id = Column(Integer, unique=True, primary_key=True)
    project_code = Column(String())
    content = Column(String())
    version = Column(String())
    publisher = Column(String())
    date = Column(DateTime(), default=datetime.utcnow)

    __table_args__ = (
        UniqueConstraint('project_code', 'version', name='project_code_version'),
        {"schema": ConfigClass.RDS_SCHEMA_DEFAULT},
    )

    def __init__(self, project_code, content, version, publisher):
        self.project_code = project_code
        self.content = content
        self.version = version
        self.publisher = publisher

    def to_dict(self):
        result = {}
        for field in ["id", "project_code", "content", "version", "date", "publisher"]:
            if field == "date":
                result[field] = str(getattr(self, field))
            else:
                result[field] = getattr(self, field)

        return result
