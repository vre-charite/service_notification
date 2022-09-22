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

"""Add created_date to system_maintenance.

Revision ID: e6fcf3ec5303
Revises: 49fbb2de7523
Create Date: 2022-01-24 13:01:15.062858
"""
import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision = 'e6fcf3ec5303'
down_revision = '49fbb2de7523'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('system_maintenance', sa.Column('created_date', sa.DateTime(), nullable=True), schema='notifications')


def downgrade():
    op.drop_column('system_maintenance', 'created_date', schema='notifications')
