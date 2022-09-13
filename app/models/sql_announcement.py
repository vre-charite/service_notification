# Copyright 2022 Indoc Research
# 
# Licensed under the EUPL, Version 1.2 or – as soon they
# will be approved by the European Commission - subsequent
# versions of the EUPL (the "Licence");
# You may not use this work except in compliance with the
# Licence.
# You may obtain a copy of the Licence at:
# 
# https://joinup.ec.europa.eu/collection/eupl/eupl-text-eupl-12
# 
# Unless required by applicable law or agreed to in
# writing, software distributed under the Licence is
# distributed on an "AS IS" basis,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either
# express or implied.
# See the Licence for the specific language governing
# permissions and limitations under the Licence.
# 

from datetime import datetime

from sqlalchemy import Column
from sqlalchemy import DateTime
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy import UniqueConstraint
from sqlalchemy.ext.declarative import declarative_base

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
        {'schema': ConfigClass.ANNOUNCEMENTS_SCHEMA},
    )

    def __init__(self, project_code, content, version, publisher):
        self.project_code = project_code
        self.content = content
        self.version = version
        self.publisher = publisher

    def to_dict(self):
        result = {}
        for field in ['id', 'project_code', 'content', 'version', 'date', 'publisher']:
            if field == 'date':
                result[field] = str(getattr(self, field))
            else:
                result[field] = getattr(self, field)

        return result
