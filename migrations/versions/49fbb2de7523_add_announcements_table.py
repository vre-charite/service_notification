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

"""Add announcements table.

Revision ID: 49fbb2de7523
Revises: acfc65939c91
Create Date: 2022-01-21 12:01:11.749704
"""
import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision = '49fbb2de7523'
down_revision = 'acfc65939c91'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        'announcement',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('project_code', sa.String(), nullable=True),
        sa.Column('content', sa.String(), nullable=True),
        sa.Column('version', sa.String(), nullable=True),
        sa.Column('publisher', sa.String(), nullable=True),
        sa.Column('date', sa.DateTime(), nullable=True),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('id'),
        sa.UniqueConstraint('project_code', 'version', name='project_code_version'),
        schema='announcements',
    )


def downgrade():
    op.drop_table('announcement', schema='announcements')
